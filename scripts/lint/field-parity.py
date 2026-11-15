#!/usr/bin/env python3
"""Cross-matrix field-parity gate for framework.json.

Three checks:

1. Field parity. Any tactic or indicator field that is populated on every
   object of at least one matrix must not be entirely absent from another
   matrix, unless the (matrix, field) pair is a documented matrix-specific
   design decision listed in ALLOWLIST.
2. Within-matrix mesh. Every matrix must carry at least one
   correlates_with edge between two of its own indicators.
3. Score-free vocabulary. framework.json carries no scoring fields; those
   live only in the separate experimental overlay
   (docs/data/scoring-overlay.json). Any scoring field found on an
   indicator, in a tactic's assessment_guidance, or at the top level is a
   violation.

This script never reads a score. Exit codes: 0 parity holds; 1 one or
more violations; 2 the input could not be read (missing file, invalid
JSON, wrong shape). Standard library only.

Usage: python3 scripts/lint/field-parity.py [path/to/framework.json]
"""
from __future__ import annotations

import json
import sys

NAME = "field-parity"

# Documented matrix-specific fields: (matrix, field) pairs that are allowed
# to be absent even though the field is universal elsewhere.
ALLOWLIST = {
    # Target-identity model: person matrix only.
    ("facility", "target_identity_scope"),
    ("organization", "target_identity_scope"),
    ("infrastructure", "target_identity_scope"),
    ("facility", "target_identity"),
    ("organization", "target_identity"),
    ("infrastructure", "target_identity"),
    # Siting model: facility matrix only.
    ("person", "facility_target_scope"),
    ("organization", "facility_target_scope"),
    ("infrastructure", "facility_target_scope"),
    ("person", "within_site_focus"),
    ("organization", "within_site_focus"),
    ("infrastructure", "within_site_focus"),
}

# Optional lifecycle fields are sparse by design and are never a parity gap.
LIFECYCLE_FIELDS = {
    "lifecycle_state",
    "deprecated_in",
    "superseded_by",
    "deprecation_reason",
    "reserved_reason",
}

# Scoring fields that belong to the overlay and must not appear here.
INDICATOR_SCORE_FIELDS = (
    "escalation_axes",
    "escalation_weight",
    "severity_band",
    "severity_floor",
    "axis_confidence",
    "axes",
    "type_weight",
    "type_band",
    "type_band_floor",
)
GUIDANCE_SCORE_FIELDS = ("escalation_priority",)
TOP_LEVEL_SCORE_FIELDS = ("escalation_rubric", "instance_conditioning", "indicator_scores", "tactic_priorities")


class InputError(Exception):
    """The input document could not be read or is not the expected shape."""


def load_json(path: str, label: str):
    try:
        with open(path, encoding="utf-8") as handle:
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


def populated(obj: dict, field: str) -> bool:
    """Key present with a meaningful value. Booleans count by presence."""
    if field not in obj:
        return False
    value = obj[field]
    if isinstance(value, bool):
        return True
    return value not in (None, "", [], {})


def scan(units_by_matrix: dict, level: str) -> list[str]:
    """Return parity violations for one unit level (tactic or indicator)."""
    fields: set[str] = set()
    for units in units_by_matrix.values():
        for unit in units:
            fields.update(key for key in unit if isinstance(key, str))

    violations = []
    for field in sorted(fields - LIFECYCLE_FIELDS):
        stats = {}
        for matrix_key, units in units_by_matrix.items():
            count = sum(1 for unit in units if populated(unit, field))
            stats[matrix_key] = (count, len(units))
        universal_in = [mk for mk, (count, total) in stats.items() if total and count == total]
        if not universal_in:
            continue
        for matrix_key, (count, total) in stats.items():
            if count == 0 and total > 0 and (matrix_key, field) not in ALLOWLIST:
                detail = ", ".join(f"{mk}={c}/{t}" for mk, (c, t) in stats.items())
                violations.append(
                    f"{level}.{field}: absent from '{matrix_key}' but universal in "
                    f"{universal_in} ({detail})"
                )
    return violations


def extract(framework) -> tuple[dict, dict]:
    """Return (tactics_by_matrix, indicators_by_matrix), shape-checked."""
    if not isinstance(framework, dict):
        raise InputError("top level is not a JSON object")
    matrices = framework.get("matrices")
    if not isinstance(matrices, dict):
        raise InputError("top-level 'matrices' is missing or is not an object")
    tactics_by_matrix: dict[str, list] = {}
    indicators_by_matrix: dict[str, list] = {}
    for matrix_key, matrix_val in matrices.items():
        if not isinstance(matrix_val, dict):
            continue  # non-matrix siblings such as matrices.boundary_rule
        tactics = matrix_val.get("tactics")
        if not isinstance(tactics, list):
            raise InputError(f"matrices.{matrix_key}.tactics is missing or is not an array")
        indicators = []
        for index, tactic in enumerate(tactics):
            if not isinstance(tactic, dict):
                raise InputError(f"matrices.{matrix_key}.tactics[{index}] is not an object")
            children = tactic.get("indicators", [])
            if not isinstance(children, list) or any(not isinstance(c, dict) for c in children):
                raise InputError(
                    f"matrices.{matrix_key}.tactics[{index}].indicators is not an array of objects"
                )
            indicators.extend(children)
        tactics_by_matrix[matrix_key] = tactics
        indicators_by_matrix[matrix_key] = indicators
    if not tactics_by_matrix:
        raise InputError("'matrices' contains no matrix objects")
    return tactics_by_matrix, indicators_by_matrix


def score_field_violations(framework: dict, tactics_by_matrix: dict, indicators_by_matrix: dict) -> list[str]:
    violations = []
    for field in TOP_LEVEL_SCORE_FIELDS:
        if field in framework:
            violations.append(f"score-free: top-level '{field}' belongs in the scoring overlay, not framework.json")
    for field in INDICATOR_SCORE_FIELDS:
        carriers = [
            ind.get("id", "?")
            for inds in indicators_by_matrix.values()
            for ind in inds
            if field in ind
        ]
        if carriers:
            violations.append(
                f"score-free: indicator field '{field}' present on {len(carriers)} indicator(s) "
                f"(first: {carriers[0]}); scores belong in the scoring overlay"
            )
    for field in GUIDANCE_SCORE_FIELDS:
        carriers = [
            tactic.get("id", "?")
            for tactics in tactics_by_matrix.values()
            for tactic in tactics
            if isinstance(tactic.get("assessment_guidance"), dict) and field in tactic["assessment_guidance"]
        ]
        if carriers:
            violations.append(
                f"score-free: assessment_guidance.{field} present on {len(carriers)} tactic(s) "
                f"(first: {carriers[0]}); it belongs in the overlay's tactic_priorities"
            )
    return violations


def run(path: str) -> int:
    framework = load_json(path, "framework document")
    tactics_by_matrix, indicators_by_matrix = extract(framework)

    violations = []
    for matrix_key, tactics in tactics_by_matrix.items():
        if not tactics:
            violations.append(f"matrix '{matrix_key}' has zero tactics")
        elif not indicators_by_matrix[matrix_key]:
            violations.append(f"matrix '{matrix_key}' has zero indicators")

    violations += scan(tactics_by_matrix, "tactic")
    violations += scan(indicators_by_matrix, "indicator")

    # Within-matrix mesh: a matrix's own indicator IDs define "within", so no
    # ID prefix table is needed and an added matrix is handled like the rest.
    for matrix_key, inds in indicators_by_matrix.items():
        own_ids = {ind.get("id") for ind in inds if isinstance(ind.get("id"), str)}
        within = 0
        for ind in inds:
            refs = ind.get("correlates_with")
            if isinstance(refs, list):
                within += sum(1 for ref in refs if isinstance(ref, str) and ref in own_ids)
        if inds and within == 0:
            violations.append(f"mesh: '{matrix_key}' has zero within-matrix correlates_with edges")

    violations += score_field_violations(framework, tactics_by_matrix, indicators_by_matrix)

    if violations:
        print(f"FAILED {NAME}: {len(violations)} violation(s):", file=sys.stderr)
        for violation in violations:
            print(f"  {violation}", file=sys.stderr)
        return 1
    print(
        f"PASSED {NAME}: no universal-versus-absent field drift across "
        f"{len(tactics_by_matrix)} matrices; within-matrix mesh present in all; "
        f"no scoring field in the vocabulary document."
    )
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
    args = sys.argv[1:]
    if args and args[0] in ("-h", "--help"):
        print("usage: field-parity.py [path/to/framework.json]")
        return 0
    if len(args) > 1:
        print("usage: field-parity.py [path/to/framework.json]", file=sys.stderr)
        return 2
    path = args[0] if args else "docs/data/framework.json"
    try:
        return run(path)
    except InputError as exc:
        print(f"error: {NAME}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
