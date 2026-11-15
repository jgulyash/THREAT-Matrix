#!/usr/bin/env python3
"""Consumer smoke test: every shipped document validates against its schema.

This gate proves the published contract works end to end for a consumer
who has only the files in this repository. It validates, with JSON Schema
2020-12 and a format checker:

  1. docs/data/framework.json            against docs/data/framework.schema.json
  2. docs/data/scoring-overlay.json      against docs/data/scoring-overlay.schema.json
  3. every examples/worked-cases/*.json  against docs/data/case-record.schema.json
     (the score-free case record, the default)
  4. every examples/experimental-scoring/worked-cases/*.json against the
     scored-record definition in scoring-overlay.schema.json
  5. both templates: examples/*template*.json (score-free) and
     examples/experimental-scoring/*template*.json (scored)

Beyond schema validity it checks the joins a consumer relies on: every
indicator_id in a record exists in the framework; a score-free record's
framework_version matches the framework; a scored record's type_band
equals the overlay's authored band for that indicator; and
conditioned_priority never ranks below type_band (escalate-only).

It then runs the reference consumer (examples/python_consumer.py) twice:
without the overlay, where no score may appear in its output, and with
--with-experimental-scores, where the overlay's notice must be printed
before any score. Finally it runs negative controls, so a validator that
has stopped rejecting bad input fails this gate instead of passing it.

Nothing is fetched from the network. Schema references resolve only
inside the local schema file; a remote $ref is an error.

Exit codes: 0 every document is valid and every check passed; 1 one or
more documents are invalid or a check failed; 2 a required file could not
be read or the jsonschema package is not installed.

Usage: python3 scripts/lint/consumer-smoke.py [--root REPO_ROOT]
Requires: jsonschema 4.18 or later (pip install jsonschema)
"""
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

NAME = "consumer-smoke"
BAND_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}
SCORE_WORDS = ("type_band", "type_weight", "type_band_floor", "conditioned_priority")


class InputError(Exception):
    """A required file could not be read or is not the expected shape."""


def load_json(path: Path, label: str):
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise InputError(f"{label} not found at {path}")
    except UnicodeDecodeError:
        raise InputError(f"{label} at {path} is not valid UTF-8")
    except json.JSONDecodeError as exc:
        raise InputError(f"{label} at {path} is not valid JSON ({exc.msg}, line {exc.lineno})")
    except RecursionError:
        raise InputError(f"{label} at {path} is nested too deeply to parse")
    except OSError as exc:
        raise InputError(f"{label} could not be read at {path} ({exc.__class__.__name__})")


def make_validator(schema, label: str):
    """Build a format-checking validator that can never reach the network."""
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
    from referencing import Registry

    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise InputError(f"{label} is not a valid JSON Schema ({exc.message[:120]})")
    return Draft202012Validator(
        schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
        registry=Registry(),  # empty: only in-document references resolve
    )


def schema_errors(validator, document) -> list[str]:
    try:
        errors = sorted(validator.iter_errors(document), key=lambda e: [str(p) for p in e.absolute_path])
    except Exception as exc:  # for example an unresolvable (remote) $ref
        return [f"validation could not run ({exc.__class__.__name__}: {str(exc)[:120]})"]
    out = []
    for error in errors:
        location = "/".join(str(part) for part in error.absolute_path) or "(root)"
        out.append(f"{location}: {error.message[:140]}")
    return out


def find_scored_record_def(overlay_schema: dict) -> str:
    """Name of the scored-record definition in scoring-overlay.schema.json."""
    defs = overlay_schema.get("$defs")
    if not isinstance(defs, dict):
        raise InputError("scoring-overlay.schema.json has no $defs")
    for name in ("scored_case_record", "scored_record", "conditioned_assessment"):
        if name in defs:
            return name
    for name, node in defs.items():
        props = node.get("properties") if isinstance(node, dict) else None
        if isinstance(props, dict) and "conditioned_priority" in props and "type_band" in props:
            return name
    raise InputError("scoring-overlay.schema.json defines no scored-record object")


def indicator_ids(framework: dict) -> set[str]:
    out: set[str] = set()
    matrices = framework.get("matrices") if isinstance(framework, dict) else None
    for matrix in (matrices or {}).values() if isinstance(matrices, dict) else []:
        if not isinstance(matrix, dict):
            continue
        for tactic in matrix.get("tactics") or []:
            if not isinstance(tactic, dict):
                continue
            for ind in tactic.get("indicators") or []:
                if isinstance(ind, dict) and isinstance(ind.get("id"), str) \
                        and ind.get("lifecycle_state") != "reserved":
                    out.add(ind["id"])
    return out


def case_record_join_errors(record, framework: dict, ind_ids: set[str]) -> list[str]:
    """Joins for a score-free case record (assumes it is schema-valid)."""
    errors = []
    if record.get("framework_version") != framework.get("version"):
        errors.append(
            f"framework_version {record.get('framework_version')!r} does not match "
            f"the framework version {framework.get('version')!r}"
        )
    for index, observation in enumerate(record.get("observations") or []):
        ind_id = observation.get("indicator_id") if isinstance(observation, dict) else None
        if ind_id not in ind_ids:
            errors.append(f"observations/{index}: indicator_id {ind_id!r} does not exist in the framework")
    return errors


def scored_record_join_errors(record, overlay: dict, ind_ids: set[str]) -> list[str]:
    """Joins for a scored record (assumes it is schema-valid)."""
    errors = []
    ind_id = record.get("indicator_id")
    scores = overlay.get("indicator_scores") if isinstance(overlay.get("indicator_scores"), dict) else {}
    entry = scores.get(ind_id)
    if ind_id not in ind_ids:
        errors.append(f"indicator_id {ind_id!r} does not exist in the framework")
    if not isinstance(entry, dict):
        errors.append(f"indicator_id {ind_id!r} has no entry in the overlay's indicator_scores")
    elif record.get("type_band") != entry.get("type_band"):
        errors.append(
            f"type_band {record.get('type_band')!r} does not equal the overlay's authored "
            f"type_band {entry.get('type_band')!r} for {ind_id}"
        )
    band, priority = record.get("type_band"), record.get("conditioned_priority")
    if band in BAND_RANK and priority in BAND_RANK and BAND_RANK[priority] < BAND_RANK[band]:
        errors.append(f"conditioned_priority {priority!r} ranks below type_band {band!r} (escalate-only)")
    return errors


def run_consumer(consumer: Path, extra: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(consumer), *extra],
        capture_output=True, text=True, encoding="utf-8", errors="backslashreplace",
    )
    return result.returncode, result.stdout + result.stderr


def run(root: Path) -> int:
    try:
        import jsonschema  # noqa: F401
        import referencing  # noqa: F401
    except ImportError:
        print(
            f"error: {NAME}: the jsonschema package (4.18 or later) is required: pip install jsonschema",
            file=sys.stderr,
        )
        return 2

    data = root / "docs" / "data"
    examples = root / "examples"
    scored_dir = examples / "experimental-scoring"
    consumer = examples / "python_consumer.py"

    framework = load_json(data / "framework.json", "framework.json")
    overlay = load_json(data / "scoring-overlay.json", "scoring-overlay.json")
    framework_schema = load_json(data / "framework.schema.json", "framework.schema.json")
    overlay_schema = load_json(data / "scoring-overlay.schema.json", "scoring-overlay.schema.json")
    case_schema = load_json(data / "case-record.schema.json", "case-record.schema.json")
    for label, doc in (("framework.json", framework), ("scoring-overlay.json", overlay),
                       ("scoring-overlay.schema.json", overlay_schema)):
        if not isinstance(doc, dict):
            raise InputError(f"{label} top level is not a JSON object")
    if not consumer.exists():
        raise InputError(f"reference consumer not found at {consumer}")

    framework_validator = make_validator(framework_schema, "framework.schema.json")
    overlay_validator = make_validator(overlay_schema, "scoring-overlay.schema.json")
    case_validator = make_validator(case_schema, "case-record.schema.json")
    scored_def = find_scored_record_def(overlay_schema)
    scored_validator = make_validator(
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": f"#/$defs/{scored_def}",
            "$defs": overlay_schema["$defs"],
        },
        f"scoring-overlay.schema.json $defs.{scored_def}",
    )

    failures: list[str] = []
    checked: list[str] = []
    ind_ids = indicator_ids(framework)

    def report(label: str, errors: list[str]) -> None:
        checked.append(label)
        if errors:
            failures.append(f"{label}: {len(errors)} error(s); first: {errors[0]}")

    # 1 and 2: the two published documents.
    report("docs/data/framework.json", schema_errors(framework_validator, framework))
    report("docs/data/scoring-overlay.json", schema_errors(overlay_validator, overlay))

    # 3 to 5: worked cases and templates.
    groups = (
        ("score-free worked cases", sorted((examples / "worked-cases").glob("*.json")), "case"),
        ("score-free template", sorted(examples.glob("*template*.json")), "case"),
        ("scored worked cases", sorted((scored_dir / "worked-cases").glob("*.json")), "scored"),
        ("scored template", sorted(scored_dir.glob("*template*.json")), "scored"),
    )
    records: dict[str, list] = {"case": [], "scored": []}
    for group_label, paths, kind in groups:
        if not paths:
            failures.append(f"{group_label}: no file found; this gate cannot pass with nothing to validate")
            continue
        for path in paths:
            label = str(path.relative_to(root))
            try:
                record = load_json(path, label)
            except InputError as exc:
                report(label, [str(exc)])
                continue
            validator = case_validator if kind == "case" else scored_validator
            errors = schema_errors(validator, record)
            if not errors:
                if kind == "case":
                    errors = case_record_join_errors(record, framework, ind_ids)
                else:
                    errors = scored_record_join_errors(record, overlay, ind_ids)
            if not errors:
                records[kind].append(record)
            report(label, errors)

    # Reference consumer, default mode: no overlay, no score in the output.
    code, out = run_consumer(consumer, [])
    if code != 0:
        failures.append(f"reference consumer exited {code} without the overlay (expected 0)")
    if "Validation (framework): clean." not in out:
        failures.append("reference consumer did not report a clean framework validation")
    if "Sample (one tactic per phase)" not in out:
        failures.append("reference consumer did not print the per-phase sample")
    leaked = [word for word in SCORE_WORDS if word in out]
    notice = overlay.get("notice") if isinstance(overlay.get("notice"), str) else ""
    if leaked or (notice and notice in out):
        failures.append(f"reference consumer printed score content without the opt-in flag ({leaked or 'notice'})")
    checked.append("reference consumer (no overlay)")

    # Reference consumer, opt-in mode: notice strictly before any score.
    code, out = run_consumer(consumer, ["--with-experimental-scores"])
    if code != 0:
        failures.append(f"reference consumer exited {code} with --with-experimental-scores (expected 0)")
    if not notice:
        failures.append("scoring-overlay.json carries no notice string")
    elif notice not in out:
        failures.append("reference consumer did not print the overlay's notice in opt-in mode")
    else:
        notice_at = out.index(notice)
        score_at = [out.index(word) for word in SCORE_WORDS if word in out]
        if not score_at:
            failures.append("reference consumer printed no score in opt-in mode")
        elif min(score_at) < notice_at:
            failures.append("reference consumer printed a score before the overlay's notice")
    checked.append("reference consumer (--with-experimental-scores)")

    # Negative controls: each of these must be rejected.
    controls = 0
    if records["case"]:
        bad = copy.deepcopy(records["case"][0])
        bad["type_band"] = "high"
        if not schema_errors(case_validator, bad):
            failures.append("negative control: a score field added to a score-free record validated clean")
        bad = copy.deepcopy(records["case"][0])
        bad["limitations_acknowledged"] = False
        if not schema_errors(case_validator, bad):
            failures.append("negative control: limitations_acknowledged false validated clean")
        controls += 2
    if records["scored"]:
        base = next((r for r in records["scored"] if BAND_RANK.get(r.get("type_band"), 0) > 0), None)
        if base is not None:
            bad = copy.deepcopy(base)
            bad["conditioned_priority"] = "low"
            if not (schema_errors(scored_validator, bad) or scored_record_join_errors(bad, overlay, ind_ids)):
                failures.append("negative control: a conditioned_priority below type_band was accepted")
            controls += 1
        bad = copy.deepcopy(records["scored"][0])
        entry_band = overlay["indicator_scores"][bad["indicator_id"]]["type_band"]
        other = "critical" if entry_band != "critical" else "high"
        bad["type_band"] = other
        bad["conditioned_priority"] = "critical"
        if not (schema_errors(scored_validator, bad) or scored_record_join_errors(bad, overlay, ind_ids)):
            failures.append("negative control: a type_band that differs from the overlay was accepted")
        controls += 1
    with tempfile.TemporaryDirectory() as tmp:
        invalid = Path(tmp) / "invalid-framework.json"
        invalid.write_text('{"schema_version": "3.0.0"}\n', encoding="utf-8")
        code, _out = run_consumer(consumer, ["--framework", str(invalid)])
        if code == 0:
            failures.append("negative control: the reference consumer exited 0 on a schema-invalid framework")
        controls += 1
    checked.append(f"{controls} negative controls")

    if failures:
        print(f"FAILED {NAME}: {len(failures)} problem(s):", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1
    print(
        f"PASSED {NAME}: {len(checked)} checks. Framework and overlay validate against their "
        f"schemas; {len(records['case'])} score-free and {len(records['scored'])} scored example "
        f"documents (worked cases and templates) validate and join; the reference consumer "
        f"runs without the overlay and prints the overlay notice before any score when opted in."
    )
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="Validate every shipped document against its schema.")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[2]),
        help="repository root (default: the checkout this script lives in)",
    )
    args = parser.parse_args()
    try:
        return run(Path(args.root))
    except InputError as exc:
        print(f"error: {NAME}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
