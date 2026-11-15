#!/usr/bin/env python3
"""Check the experimental scoring overlay's axis_confidence against its rule.

axis_confidence is a categorical evidence-basis marker per scoring axis in
docs/data/scoring-overlay.json: "established", "inferred", or "thin". It is
derived by rule from the axis values, and this script is the executable
form of that rule. Confidence describes evidence basis, not severity: a
thin axis is a wider error bar and a candidate for earlier human review,
never an automatic demotion.

The overlay is experimental, non-normative, and unvalidated. This check
proves only that the stored labels are internally consistent with the
rule below. It says nothing about whether the scores are accurate.

Derivation rule:
- detectability: value at or below 2.0 derives "thin"; at or above 6.0
  derives "established"; otherwise "inferred".
- blast_radius_potential: value within 0.5 of an anchor for the
  indicator's matrix (BLAST_ANCHORS) derives "established"; otherwise
  "inferred".
- impact_potential and recoverability_inverse: "inferred" everywhere.

Inputs: the overlay supplies indicator_scores[id].axes and
indicator_scores[id].axis_confidence. framework.json is read only to map
each indicator ID to its matrix; no score is read from it (it has none).

This script only checks. It never writes to the overlay or to
framework.json. To see the value the rule derives for every indicator,
use --print-derived and review the output before any edit to the overlay.

Exit codes: 0 every label matches the rule; 1 mismatches, missing
entries, or entries for unknown indicators; 2 an input could not be read.

Usage:
  python3 scripts/analysis/derive-axis-confidence.py --check
  python3 scripts/analysis/derive-axis-confidence.py --check \\
      --framework docs/data/framework.json --overlay docs/data/scoring-overlay.json
  python3 scripts/analysis/derive-axis-confidence.py --print-derived
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

NAME = "derive-axis-confidence"
REPO = Path(__file__).resolve().parents[2]
DEFAULT_FRAMEWORK = REPO / "docs" / "data" / "framework.json"
DEFAULT_OVERLAY = REPO / "docs" / "data" / "scoring-overlay.json"

AXES = ("impact_potential", "blast_radius_potential", "recoverability_inverse", "detectability")

# Blast-radius anchors per matrix, compared with a +/-0.5 window.
# person and facility: the method collateral base rates in the overlay's
# rubric.blast_radius_guidance (the facility calibration shares the person
# table). organization and infrastructure: tier bounds that are defined
# here; they are not recorded anywhere else in the published data.
BLAST_ANCHORS = {
    "person": {2.0, 2.5, 3.0, 4.0, 7.0, 8.0, 9.0},
    "facility": {2.0, 2.5, 3.0, 4.0, 7.0, 8.0, 9.0},
    "organization": {2.0, 3.5, 4.0, 5.5, 6.5, 7.5, 8.5},
    "infrastructure": {2.5, 3.5, 4.0, 5.5, 6.0, 7.0, 7.5, 8.0, 9.0},
}
ANCHOR_WINDOW = 0.5


class InputError(Exception):
    """An input document could not be read or is not the expected shape."""


def derive(matrix_key: str, axes: dict) -> dict:
    """Return the rule-derived axis_confidence for one indicator's axes."""
    det = axes["detectability"]
    if det <= 2.0:
        det_conf = "thin"
    elif det >= 6.0:
        det_conf = "established"
    else:
        det_conf = "inferred"

    blast = axes["blast_radius_potential"]
    anchors = BLAST_ANCHORS[matrix_key]
    blast_conf = (
        "established"
        if any(abs(blast - anchor) <= ANCHOR_WINDOW for anchor in anchors)
        else "inferred"
    )

    return {
        "impact_potential": "inferred",
        "blast_radius_potential": blast_conf,
        "recoverability_inverse": "inferred",
        "detectability": det_conf,
    }


def load_json(path, label: str):
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


def indicator_matrix_map(framework) -> dict[str, str]:
    """Map every non-reserved indicator ID in the vocabulary to its matrix."""
    if not isinstance(framework, dict) or not isinstance(framework.get("matrices"), dict):
        raise InputError("framework document has no 'matrices' object")
    out: dict[str, str] = {}
    for matrix_key, matrix_val in framework["matrices"].items():
        if not isinstance(matrix_val, dict):
            continue
        tactics = matrix_val.get("tactics")
        if not isinstance(tactics, list):
            raise InputError(f"matrices.{matrix_key}.tactics is missing or is not an array")
        for tactic in tactics:
            if not isinstance(tactic, dict):
                continue
            for ind in tactic.get("indicators") or []:
                if not isinstance(ind, dict) or not isinstance(ind.get("id"), str):
                    continue
                if ind.get("lifecycle_state") == "reserved":
                    continue
                out[ind["id"]] = matrix_key
    if not out:
        raise InputError("framework document contains zero indicators")
    return out


def valid_axes(axes) -> bool:
    return isinstance(axes, dict) and all(
        isinstance(axes.get(axis), (int, float)) and not isinstance(axes.get(axis), bool)
        for axis in AXES
    )


def evaluate(framework, overlay):
    """Return (derived, problems, total). derived maps id -> rule output."""
    matrix_of = indicator_matrix_map(framework)
    if not isinstance(overlay, dict) or not isinstance(overlay.get("indicator_scores"), dict):
        raise InputError("overlay has no 'indicator_scores' object")
    scores = overlay["indicator_scores"]

    problems: list[str] = []
    derived: dict[str, dict] = {}
    for ind_id in sorted(set(matrix_of) - set(scores)):
        problems.append(f"MISSING {ind_id}: no indicator_scores entry in the overlay")
    for ind_id in sorted(set(scores) - set(matrix_of)):
        problems.append(f"UNKNOWN {ind_id}: overlay entry has no matching indicator in the framework")
    for ind_id in sorted(set(scores) & set(matrix_of)):
        entry = scores[ind_id]
        matrix_key = matrix_of[ind_id]
        if matrix_key not in BLAST_ANCHORS:
            problems.append(f"NO-ANCHORS {ind_id}: matrix '{matrix_key}' has no blast-radius anchor set")
            continue
        if not isinstance(entry, dict) or not valid_axes(entry.get("axes")):
            problems.append(f"BAD-AXES {ind_id}: 'axes' is missing or does not carry four numeric values")
            continue
        expected = derive(matrix_key, entry["axes"])
        derived[ind_id] = expected
        got = entry.get("axis_confidence")
        if got is None:
            problems.append(f"MISSING {ind_id}: entry has no axis_confidence")
        elif got != expected:
            diff = ", ".join(
                f"{axis}: stored {got.get(axis)!r}, rule {expected[axis]!r}"
                for axis in AXES
                if not isinstance(got, dict) or got.get(axis) != expected[axis]
            ) if isinstance(got, dict) else "axis_confidence is not an object"
            problems.append(f"MISMATCH {ind_id} ({matrix_key}): {diff}")
    return derived, problems, len(matrix_of)


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(
        description="Check the scoring overlay's axis_confidence against its derivation rule."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="verify stored labels (default)")
    mode.add_argument(
        "--print-derived",
        action="store_true",
        help="print the rule-derived labels for every indicator as JSON; writes nothing",
    )
    parser.add_argument("--framework", default=str(DEFAULT_FRAMEWORK))
    parser.add_argument("--overlay", default=str(DEFAULT_OVERLAY))
    args = parser.parse_args()

    try:
        framework = load_json(args.framework, "framework document")
        overlay = load_json(args.overlay, "scoring overlay")
        derived, problems, total = evaluate(framework, overlay)
    except InputError as exc:
        print(f"error: {NAME}: {exc}", file=sys.stderr)
        return 2

    if args.print_derived:
        json.dump(derived, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0

    if problems:
        for line in problems:
            print(line, file=sys.stderr)
        print(
            f"FAILED {NAME}: {len(problems)} problem(s) across {total} indicators.",
            file=sys.stderr,
        )
        return 1
    print(
        f"PASSED {NAME}: {len(derived)}/{total} overlay axis_confidence entries match "
        f"the derivation rule (consistency check only; the overlay is experimental "
        f"and unvalidated)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
