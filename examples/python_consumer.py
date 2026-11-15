"""
THREAT Matrix reference consumer.

A minimum viable consumer of the THREAT Matrix open vocabulary. It shows
the contract end to end using only the vocabulary document:

1. Loads framework.json from a local file path. It never fetches from the
   network; download the file first if you want a published copy.
2. Validates the document against framework.schema.json (JSON Schema
   2020-12, with format checking). Exits 1 if the document is invalid.
3. Hides reserved identifiers, as the lifecycle contract requires.
4. Demonstrates two filters useful to most consumers:
   - Phase filter: tactics in a given Threat Lifecycle phase.
   - Actor profile filter: tactics associated with a given actor profile ID.
5. Prints a structured summary.

The vocabulary carries no scores, and by default this consumer reads and
prints none. The experimental scoring overlay is a separate file and an
explicit opt-in: pass --with-experimental-scores to load it. The overlay's
own notice is printed before any score. The overlay is non-normative and
unvalidated; it scores behavior types, never a person.

Usage:
    python3 examples/python_consumer.py
    python3 examples/python_consumer.py --phase 1
    python3 examples/python_consumer.py --actor AP005
    python3 examples/python_consumer.py --framework /path/to/framework.json
    python3 examples/python_consumer.py --with-experimental-scores

Exit codes: 0 success; 1 a document failed validation; 2 a file could not
be read or an argument was not usable.

Requires: jsonschema 4.18 or later (pip install jsonschema)

This file is intentionally small. Build your own consumer by starting from
it or from scratch.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry
except ImportError:
    print("This consumer requires the `jsonschema` package (4.18 or later): pip install jsonschema", file=sys.stderr)
    sys.exit(2)


HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "docs" / "data"
DEFAULT_FRAMEWORK = DATA / "framework.json"
DEFAULT_SCHEMA = DATA / "framework.schema.json"
DEFAULT_OVERLAY = DATA / "scoring-overlay.json"
DEFAULT_OVERLAY_SCHEMA = DATA / "scoring-overlay.schema.json"


class InputError(Exception):
    """A file could not be read or is not the expected shape."""


def load(path: Path, label: str) -> Any:
    """Read a local JSON file. Local paths only; nothing is fetched."""
    text = str(path)
    if "://" in text or text.startswith(("http:", "https:")):
        raise InputError(f"{label}: '{text}' looks like a URL; this consumer reads local files only")
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise InputError(f"{label} not found: {path}")
    except UnicodeDecodeError:
        raise InputError(f"{label} is not valid UTF-8: {path}")
    except json.JSONDecodeError as exc:
        raise InputError(f"{label} is not valid JSON: {path} ({exc.msg}, line {exc.lineno})")
    except RecursionError:
        raise InputError(f"{label} is nested too deeply to parse: {path}")
    except OSError as exc:
        raise InputError(f"{label} could not be read: {path} ({exc.__class__.__name__})")


def validate(document: Any, schema: Any, label: str) -> int:
    """Run JSON Schema validation. Returns the error count (0 = clean).

    The empty Registry means a $ref can resolve only inside the schema
    document itself: validation never retrieves anything remote.
    """
    try:
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(
            schema,
            format_checker=Draft202012Validator.FORMAT_CHECKER,
            registry=Registry(),
        )
        errors = sorted(validator.iter_errors(document), key=lambda e: list(map(str, e.absolute_path)))
    except Exception as exc:  # unusable schema or unresolvable reference
        print(f"Validation ({label}): could not run ({exc.__class__.__name__}: {str(exc)[:160]})")
        return 1
    if errors:
        print(f"Validation ({label}): {len(errors)} schema error(s).")
        for error in errors[:5]:
            location = "/".join(str(part) for part in error.absolute_path) or "(root)"
            print(f"  {location}: {error.message[:120]}")
        if len(errors) > 5:
            print(f"  ...and {len(errors) - 5} more")
    else:
        print(f"Validation ({label}): clean.")
    return len(errors)


def is_reserved(obj: Any) -> bool:
    return isinstance(obj, dict) and obj.get("lifecycle_state") == "reserved"


def matrix_objects(framework: dict) -> dict[str, dict]:
    """Return the matrix objects, skipping non-matrix siblings."""
    matrices = framework.get("matrices")
    if not isinstance(matrices, dict):
        return {}
    return {key: value for key, value in matrices.items() if isinstance(value, dict)}


def all_tactics(framework: dict) -> list[dict]:
    """Return every non-reserved tactic across every matrix as a flat list."""
    out: list[dict] = []
    for matrix_key, matrix in matrix_objects(framework).items():
        for tactic in matrix.get("tactics") or []:
            if not isinstance(tactic, dict) or is_reserved(tactic):
                continue
            tactic_with_matrix = dict(tactic)
            tactic_with_matrix.setdefault("matrix", matrix_key)
            out.append(tactic_with_matrix)
    return out


def live_profiles(framework: dict) -> list[dict]:
    """Actor profiles a consumer may show. Reserved stubs are hidden."""
    return [
        profile for profile in framework.get("actor_profiles") or []
        if isinstance(profile, dict) and not is_reserved(profile)
    ]


def filter_by_phase(tactics: list[dict], phase: int) -> list[dict]:
    """Return tactics in the given Threat Lifecycle phase (1-4)."""
    return [t for t in tactics if t.get("phase") == phase]


def filter_by_actor(tactics: list[dict], actor_id: str) -> list[dict]:
    """Return tactics associated with the given actor profile ID."""
    out: list[dict] = []
    for tactic in tactics:
        for assoc in tactic.get("actor_associations") or []:
            if isinstance(assoc, dict) and assoc.get("actor_id") == actor_id:
                out.append(tactic)
                break
    return out


def print_summary(framework: dict) -> None:
    name = framework.get("full_name") or framework.get("name", "(unnamed)")
    matrices = matrix_objects(framework)
    tactics = all_tactics(framework)
    indicators = sum(len(t.get("indicators") or []) for t in tactics)
    bibliography = framework.get("bibliography")

    print(f"\n{name}")
    print(f"  Framework version : {framework.get('version', '?')}")
    print(f"  Schema version    : {framework.get('schema_version', '?')}")
    print(f"  Matrices          : {len(matrices)}")
    for key, matrix in matrices.items():
        count = len([t for t in tactics if t.get("matrix") == key])
        print(f"    {key:<15} maturity: {matrix.get('maturity', 'unset'):<6} tactics: {count}")
    print(f"  Tactics           : {len(tactics)}")
    print(f"  Indicators        : {indicators}")
    print(f"  Actor profiles    : {len(live_profiles(framework))} (reserved identifiers hidden)")
    print(f"  Bibliography refs : {len(bibliography) if isinstance(bibliography, dict) else 0}")
    mesh = framework.get("detection_mesh")
    if isinstance(mesh, dict):
        print(f"  Detection Mesh    : {len(mesh.get('axes') or [])} axes")


def print_tactic_brief(tactic: dict) -> None:
    state = tactic.get("lifecycle_state", "active")
    suffix = "" if state == "active" else f"  [{state}]"
    print(
        f"  {str(tactic.get('id', '?')):>8}  ({tactic.get('matrix', '?')}/phase-{tactic.get('phase', '?')})  "
        f"{tactic.get('name', '')}{suffix}"
    )


# ---------------------------------------------------------------------------
# Experimental scoring overlay (opt-in only)
# ---------------------------------------------------------------------------

BAND_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}
BAND_BY_RANK = {rank: band for band, rank in BAND_RANK.items()}


def conditioned_priority(type_band: str, instance_raise_to: str) -> str:
    """Escalate-only join from the experimental overlay: the case priority
    is the higher of the behavior type's band and the band the case evidence
    argues for. There is no lowering path."""
    return BAND_BY_RANK[max(BAND_RANK[type_band], BAND_RANK[instance_raise_to])]


def show_experimental_scores(framework: dict, overlay: dict, tactics: list[dict]) -> int:
    """Print the overlay notice, then a small sample of type-level scores.

    Returns 0 on success, 1 if the overlay does not fit this framework.
    """
    # The notice comes first. No score is printed above this line.
    print("\nEXPERIMENTAL SCORING OVERLAY (opt-in; non-normative)")
    print(f"  NOTICE: {overlay.get('notice', '(overlay carries no notice; treat every value as unvalidated)')}")
    print(
        f"  overlay_version {overlay.get('overlay_version', '?')} | status {overlay.get('status', '?')} | "
        f"validation_status {overlay.get('validation_status', '?')} | normative {overlay.get('normative', '?')}"
    )
    applies_to = overlay.get("applies_to_framework_version")
    if applies_to != framework.get("version"):
        print(
            f"  The overlay applies to framework version {applies_to!r}, but this document is "
            f"{framework.get('version')!r}. Refusing to join them."
        )
        return 1
    scores = overlay.get("indicator_scores")
    if not isinstance(scores, dict):
        print("  The overlay has no indicator_scores object. Nothing to show.")
        return 1

    example = None
    for tactic in tactics:
        for indicator in tactic.get("indicators") or []:
            entry = scores.get(indicator.get("id")) if isinstance(indicator, dict) else None
            if isinstance(entry, dict) and entry.get("type_band") in BAND_RANK:
                example = (tactic, indicator, entry)
                break
        if example:
            break
    if not example:
        print("  No scored indicator found for the listed tactics.")
        return 0
    tactic, indicator, entry = example
    type_band = entry["type_band"]
    print("\n  Sample (one behavior type; a type-level value, never a score of a person):")
    print(f"    Indicator   : {indicator['id']} in {tactic.get('id')}")
    print(f"    type_weight : {entry.get('type_weight')}")
    print(f"    type_band   : {type_band}")
    if "type_band_floor" in entry:
        print(f"    type_band_floor : {entry['type_band_floor']}")

    # Illustration only: the framework and the overlay ship no case data.
    fictional_instance_argues_for = "critical"
    result = conditioned_priority(type_band, fictional_instance_argues_for)
    effect = "raised" if BAND_RANK[result] > BAND_RANK[type_band] else "held"
    print("\n  Instance-conditioning join (illustrative; fictional instance):")
    print(f"    Fictional instance   : argues for {fictional_instance_argues_for}")
    print(f"    Conditioned priority : {result}  [{effect}, escalate-only max]")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="THREAT Matrix reference consumer (local files only).")
    parser.add_argument("--framework", type=Path, default=DEFAULT_FRAMEWORK,
                        help="Local path to framework.json")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA,
                        help="Local path to framework.schema.json")
    parser.add_argument("--phase", type=int, choices=[1, 2, 3, 4],
                        help="Filter tactics by Threat Lifecycle phase")
    parser.add_argument("--actor", type=str,
                        help="Filter tactics by actor profile ID (e.g., AP005)")
    parser.add_argument("--no-validate", action="store_true",
                        help="Skip JSON Schema validation")
    parser.add_argument("--with-experimental-scores", action="store_true",
                        help="Opt in to the experimental, non-normative scoring overlay. "
                             "Its notice is printed before any score.")
    parser.add_argument("--overlay", type=Path, default=DEFAULT_OVERLAY,
                        help="Local path to scoring-overlay.json (used only with --with-experimental-scores)")
    parser.add_argument("--overlay-schema", type=Path, default=DEFAULT_OVERLAY_SCHEMA,
                        help="Local path to scoring-overlay.schema.json")
    args = parser.parse_args()

    try:
        framework = load(args.framework, "framework.json")
        if not isinstance(framework, dict):
            raise InputError(f"framework.json top level is not a JSON object: {args.framework}")
        schema = None if args.no_validate else load(args.schema, "framework schema")
        overlay = overlay_schema = None
        if args.with_experimental_scores:
            overlay = load(args.overlay, "scoring overlay")
            if not isinstance(overlay, dict):
                raise InputError(f"scoring overlay top level is not a JSON object: {args.overlay}")
            if not args.no_validate:
                overlay_schema = load(args.overlay_schema, "scoring overlay schema")
    except InputError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    status = 0
    print_summary(framework)

    if schema is not None and validate(framework, schema, "framework") > 0:
        status = 1

    tactics = all_tactics(framework)

    if args.phase:
        filtered = filter_by_phase(tactics, args.phase)
        print(f"\nPhase {args.phase} tactics ({len(filtered)}):")
        for tactic in filtered:
            print_tactic_brief(tactic)

    if args.actor:
        actor_id = args.actor.strip().upper()
        known = {p.get("id") for p in framework.get("actor_profiles") or [] if isinstance(p, dict)}
        live = {p.get("id") for p in live_profiles(framework)}
        if actor_id not in known:
            print(f"\nActor profile {actor_id} does not exist in this document.")
            status = status or 2
        elif actor_id not in live:
            print(f"\nActor profile {actor_id} is a reserved identifier with no content; nothing to list.")
        else:
            filtered = filter_by_actor(tactics, actor_id)
            print(f"\nTactics associated with {actor_id} ({len(filtered)}):")
            for tactic in filtered:
                print_tactic_brief(tactic)

    if not args.phase and not args.actor:
        # Default behavior: show one tactic from each phase as a smoke test.
        print("\nSample (one tactic per phase):")
        for phase in (1, 2, 3, 4):
            phase_tactics = filter_by_phase(tactics, phase)
            if phase_tactics:
                print_tactic_brief(phase_tactics[0])

    if overlay is not None:
        if overlay_schema is not None and validate(overlay, overlay_schema, "scoring overlay") > 0:
            print("The overlay failed validation; no score will be shown.")
            status = 1
        elif show_experimental_scores(framework, overlay, tactics) != 0:
            status = status or 1
    else:
        print("\nNo scores shown: the vocabulary carries none. The experimental scoring")
        print("overlay is a separate opt-in (--with-experimental-scores).")

    return status


if __name__ == "__main__":
    raise SystemExit(main())
