"""
THREAT Matrix reference consumer.

A minimum viable consumer that demonstrates the THREAT Matrix open standard
contract end-to-end:

1. Loads framework.json from a local path or URL.
2. Validates the loaded document against framework.schema.json.
3. Demonstrates two filters useful to most consumers:
   - Phase filter: tactics in a given Threat Lifecycle phase.
   - Actor profile filter: tactics associated with a given actor profile ID.
4. Prints a structured summary.

Usage:
    python3 examples/python_consumer.py
    python3 examples/python_consumer.py --phase 1
    python3 examples/python_consumer.py --actor AP005
    python3 examples/python_consumer.py --framework /path/to/framework.json

Requires: jsonschema (pip install jsonschema)

This file is the reference consumer for the THREAT Matrix standard.
It is intentionally small and dependency-light. Build your own consumer
by starting from this file or from scratch.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("This consumer requires the `jsonschema` package: pip install jsonschema", file=sys.stderr)
    sys.exit(1)


HERE = Path(__file__).resolve().parent
DEFAULT_FRAMEWORK = HERE.parent / "docs" / "data" / "framework.json"
DEFAULT_SCHEMA = HERE.parent / "docs" / "data" / "framework.schema.json"


def load(path: Path) -> Any:
    with path.open() as f:
        return json.load(f)


def validate(framework: dict, schema: dict) -> int:
    """Run JSON Schema validation. Returns the error count (0 = clean)."""
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(framework))
    if errors:
        print(f"Validation: {len(errors)} schema error(s).")
        for e in errors[:5]:
            location = "/".join(str(p) for p in e.absolute_path) or "(root)"
            print(f"  {location}: {e.message[:120]}")
        if len(errors) > 5:
            print(f"  ...and {len(errors) - 5} more")
    else:
        print("Validation: clean.")
    return len(errors)


def all_tactics(framework: dict) -> list[dict]:
    """Return every tactic across every matrix as a flat list."""
    out: list[dict] = []
    for matrix_key, matrix in framework.get("matrices", {}).items():
        if not isinstance(matrix, dict):
            continue  # skip non-matrix siblings (e.g. matrices.boundary_rule)
        for tactic in matrix.get("tactics", []):
            tactic_with_matrix = dict(tactic)
            tactic_with_matrix.setdefault("matrix", matrix_key)
            out.append(tactic_with_matrix)
    return out


def filter_by_phase(tactics: list[dict], phase: int) -> list[dict]:
    """Return tactics in the given Threat Lifecycle phase (1-4)."""
    return [t for t in tactics if t.get("phase") == phase]


def filter_by_actor(tactics: list[dict], actor_id: str) -> list[dict]:
    """Return tactics associated with the given actor profile ID."""
    out: list[dict] = []
    for t in tactics:
        for assoc in t.get("actor_associations", []) or []:
            if isinstance(assoc, dict) and assoc.get("actor_id") == actor_id:
                out.append(t)
                break
            if isinstance(assoc, str) and assoc == actor_id:
                out.append(t)
                break
    return out


def print_summary(framework: dict) -> None:
    name = framework.get("full_name") or framework.get("name", "(unnamed)")
    version = framework.get("version", "?")
    schema_version = framework.get("schema_version", "?")
    matrices = {k: v for k, v in framework.get("matrices", {}).items() if isinstance(v, dict)}
    profiles = framework.get("actor_profiles", [])
    bib = framework.get("bibliography", {})

    print(f"\n{name}")
    print(f"  Framework version : {version}")
    print(f"  Schema version    : {schema_version}")
    print(f"  Matrices          : {len(matrices)} ({', '.join(matrices.keys())})")
    print(f"  Tactics           : {sum(len(m.get('tactics', [])) for m in matrices.values())}")
    print(f"  Actor profiles    : {len(profiles)}")
    print(f"  Bibliography refs : {len(bib)}")
    if "phase_mappings" in framework:
        print(f"  Phase mappings    : {len(framework['phase_mappings'])} phases mapped")
    if "detection_mesh" in framework:
        axes = framework["detection_mesh"].get("axes", [])
        print(f"  Detection Mesh    : {len(axes)} axes")


def print_tactic_brief(tactic: dict) -> None:
    print(f"  {tactic['id']:>8}  ({tactic.get('matrix', '?')}/phase-{tactic.get('phase', '?')})  {tactic.get('name', '')}")


BAND_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}
BAND_BY_RANK = {v: k for k, v in BAND_RANK.items()}


def conditioned_priority(type_band: str, instance_raise_to: str) -> str:
    """Escalate-only join: the case priority is the MAX of the indicator's
    type-level band and the raise the instance evidence argues for. There is
    deliberately no lowering path — the false-LOW (a mild type with a screaming
    instance) is the deadliest miss, so an instance can only raise the floor,
    never sink below it. The held-vs-raised label is derived by comparing the
    result to the type band, not stored (see $defs.conditioned_assessment)."""
    return BAND_BY_RANK[max(BAND_RANK[type_band], BAND_RANK[instance_raise_to])]


def demo_instance_join(framework: dict) -> None:
    """Illustrative only: the framework ships NO instances. This joins one
    indicator's type-level score to a fictional instance record to show the
    escalate-only conditioned_priority computation a consumer performs."""
    # Find a real indicator with a severity_band to condition.
    example = None
    for t in all_tactics(framework):
        for ind in t.get("indicators", []):
            if ind.get("severity_band"):
                example = ind
                break
        if example:
            break
    if not example:
        return
    type_band = example["severity_band"]
    # Fictional instance: a specific, capable, accelerating, proximate case.
    # The framework does not ship this; a consumer holds it case-side.
    fictional_instance_argues_for = "critical"
    result = conditioned_priority(type_band, fictional_instance_argues_for)
    effect = "raised" if BAND_RANK[result] > BAND_RANK[type_band] else "held"
    print("\nInstance-conditioning join (illustrative; framework ships no instances):")
    print(f"  Indicator            : {example['id']} (type band: {type_band})")
    print(f"  Fictional instance   : argues for {fictional_instance_argues_for}")
    print(f"  Conditioned priority : {result}  [{effect}, escalate-only max]")


def main() -> int:
    parser = argparse.ArgumentParser(description="THREAT Matrix reference consumer.")
    parser.add_argument("--framework", type=Path, default=DEFAULT_FRAMEWORK,
                        help="Path to framework.json")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA,
                        help="Path to framework.schema.json")
    parser.add_argument("--phase", type=int, choices=[1, 2, 3, 4],
                        help="Filter tactics by Threat Lifecycle phase")
    parser.add_argument("--actor", type=str,
                        help="Filter tactics by actor profile ID (e.g., AP005)")
    parser.add_argument("--no-validate", action="store_true",
                        help="Skip JSON Schema validation")
    args = parser.parse_args()

    if not args.framework.exists():
        print(f"framework.json not found: {args.framework}", file=sys.stderr)
        return 2
    if not args.schema.exists() and not args.no_validate:
        print(f"schema not found: {args.schema} (use --no-validate to skip)", file=sys.stderr)
        return 2

    framework = load(args.framework)
    print_summary(framework)

    if not args.no_validate:
        schema = load(args.schema)
        validate(framework, schema)

    tactics = all_tactics(framework)

    if args.phase:
        filtered = filter_by_phase(tactics, args.phase)
        print(f"\nPhase {args.phase} tactics ({len(filtered)}):")
        for t in filtered:
            print_tactic_brief(t)

    if args.actor:
        filtered = filter_by_actor(tactics, args.actor)
        print(f"\nTactics associated with {args.actor} ({len(filtered)}):")
        for t in filtered:
            print_tactic_brief(t)

    if not args.phase and not args.actor:
        # Default behavior: show one tactic from each phase as a smoke test.
        print("\nSample (one tactic per phase):")
        for phase in (1, 2, 3, 4):
            phase_tactics = filter_by_phase(tactics, phase)
            if phase_tactics:
                print_tactic_brief(phase_tactics[0])
        demo_instance_join(framework)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
