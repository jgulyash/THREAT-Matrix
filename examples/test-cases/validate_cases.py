#!/usr/bin/env python3
"""Conditioned-assessment case validator for the examples/test-cases suites.

Runs every case record through three layers:

  C1  Schema     — validates against $defs/conditioned_assessment in
                   docs/data/framework.schema.json (requires: pip install jsonschema)
  C2  Cross-ref  — indicator_id must exist in docs/data/framework.json, and the
                   record's type_severity_band must equal that indicator's
                   authored severity_band (a record cannot misquote the type score)
  C3  Escalate-only — conditioned_priority must be >= type_severity_band in band
                   order low < medium < high < critical. JSON Schema cannot compare
                   the two enums, so this invariant is enforced HERE, not in C1.

Default run validates the fictional suite, the retrospective-mapping records, and
the shipped worked-cases (all must pass all three layers), then runs the
contract-stress-tests manifest, where each fixture declares its EXPECTED outcome:
a fixture passes when validation produces exactly the expected result (including
"schema accepts this but a downstream check must reject it" cases — that gap is
the point of those fixtures).

Usage:
  python3 examples/test-cases/validate_cases.py            # everything
  python3 examples/test-cases/validate_cases.py --no-stress  # positive suites only
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

try:
    import jsonschema
except ImportError:  # pragma: no cover
    sys.exit("requires: pip install jsonschema")

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
FRAMEWORK = REPO / "docs" / "data" / "framework.json"
SCHEMA = REPO / "docs" / "data" / "framework.schema.json"

BAND_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}

POSITIVE_DIRS = [
    HERE / "fictional-suite",
    HERE / "retrospective-mapping",
    REPO / "examples" / "worked-cases",
]
STRESS_MANIFEST = HERE / "contract-stress-tests" / "manifest.json"


def load_indicator_index() -> dict:
    data = json.loads(FRAMEWORK.read_text())
    index = {}
    for matrix in data["matrices"].values():
        if not isinstance(matrix, dict) or "tactics" not in matrix:
            continue
        for tactic in matrix["tactics"]:
            for ind in tactic.get("indicators", []):
                index[ind["id"]] = ind
    return index


def make_validator() -> jsonschema.Validator:
    schema = json.loads(SCHEMA.read_text())
    wrapper = {
        "$schema": schema.get("$schema", "https://json-schema.org/draft/2020-12/schema"),
        "$defs": schema["$defs"],
        "$ref": "#/$defs/conditioned_assessment",
    }
    return jsonschema.Draft202012Validator(wrapper)


def check_record(record: dict, validator, indicators) -> list[tuple[str, str]]:
    """Return a list of (check_id, message) failures. Empty list = fully valid."""
    failures = []
    errors = sorted(validator.iter_errors(record), key=lambda e: list(e.absolute_path))
    for e in errors:
        loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
        failures.append(("C1", f"schema: {loc}: {e.message}"))
    if errors:
        return failures  # cross-checks assume schema shape

    ind_id = record["indicator_id"]
    ind = indicators.get(ind_id)
    if ind is None:
        failures.append(("C2", f"cross-ref: indicator {ind_id} does not exist in framework.json"))
    elif record["type_severity_band"] != ind["severity_band"]:
        failures.append((
            "C2",
            f"cross-ref: type_severity_band '{record['type_severity_band']}' misquotes "
            f"{ind_id}'s authored severity_band '{ind['severity_band']}'",
        ))

    tb, cp = record["type_severity_band"], record["conditioned_priority"]
    if BAND_ORDER[cp] < BAND_ORDER[tb]:
        failures.append((
            "C3",
            f"escalate-only: conditioned_priority '{cp}' is BELOW type band '{tb}' — "
            "a demotion the contract forbids and the schema alone cannot catch",
        ))
    return failures


def run_positive(validator, indicators) -> int:
    bad = 0
    for d in POSITIVE_DIRS:
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.json")):
            if f.name == "instance-record-template.json":
                continue
            failures = check_record(json.loads(f.read_text()), validator, indicators)
            rel = f.relative_to(REPO)
            if failures:
                bad += 1
                for cid, msg in failures:
                    print(f"  FAIL [{cid}] {rel}: {msg}")
            else:
                print(f"  ok        {rel}")
    return bad


def run_stress(validator, indicators) -> int:
    if not STRESS_MANIFEST.is_file():
        print("  (no stress manifest — skipped)")
        return 0
    manifest = json.loads(STRESS_MANIFEST.read_text())
    bad = 0
    for entry in manifest["fixtures"]:
        f = STRESS_MANIFEST.parent / entry["file"]
        record = json.loads(f.read_text())
        failures = check_record(record, validator, indicators)
        fired = sorted({cid for cid, _ in failures})
        expected = sorted(entry["expect_failures"])  # [] means must be fully valid
        if fired == expected:
            verdict = "rejected by " + ",".join(fired) if fired else "accepted"
            print(f"  ok        {entry['file']}: {verdict} as expected — {entry['title']}")
        else:
            bad += 1
            print(
                f"  FAIL      {entry['file']}: expected failures {expected or '[none]'} "
                f"but got {fired or '[none]'} — {entry['title']}"
            )
            for cid, msg in failures:
                print(f"            [{cid}] {msg}")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-stress", action="store_true", help="skip the stress-test manifest")
    args = ap.parse_args()

    validator = make_validator()
    indicators = load_indicator_index()
    print(f"indicator index: {len(indicators)} ids")

    print("\n== positive suites (must pass C1+C2+C3) ==")
    bad = run_positive(validator, indicators)

    if not args.no_stress:
        print("\n== contract stress tests (must match declared expectations) ==")
        bad += run_stress(validator, indicators)

    print(f"\n{'PASS' if bad == 0 else 'FAIL'} — {bad} problem(s)")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
