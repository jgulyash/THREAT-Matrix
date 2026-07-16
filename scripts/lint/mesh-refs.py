#!/usr/bin/env python3
"""THREAT Matrix Detection Mesh reference-resolution lint.

Validates that every value in:
  - indicator.correlates_with
  - countermeasure.compensates_for
  - response_protocol.coordinates_with
resolves to an existing ID of the appropriate type in framework.json,
AND matches the canonical ID grammar (IND-/CM-/RP- + optional matrix
letter [FOI] + XXXX-XX; People-matrix IDs carry no letter).

compensates_for referents may be countermeasure IDs (the transitional
dyadic form) or indicator IDs (the coverage form, the forward authoring
standard) — see framework.schema.json and the Gate 0 decision record.

Exits 0 if all references resolve cleanly; exits 1 with a structured
report of broken references otherwise. No external dependencies — uses
only the Python 3 standard library so it runs in any CI environment.

Usage:
  python3 scripts/lint/mesh-refs.py [docs/data/framework.json]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


IND_PATTERN = re.compile(r"^IND-[FOI]?[0-9]{4}-[0-9]{2}$")
CM_PATTERN = re.compile(r"^CM-[FOI]?[0-9]{4}-[0-9]{2}$")
RP_PATTERN = re.compile(r"^RP-[FOI]?[0-9]{4}-[0-9]{2}$")


def collect_ids(framework: dict) -> tuple[set[str], set[str], set[str]]:
    """Walk framework.json and collect every IND-*, CM-*, RP- id present."""
    inds: set[str] = set()
    cms: set[str] = set()
    rps: set[str] = set()
    matrices = framework.get("matrices", {})
    for matrix_val in matrices.values():
        if not isinstance(matrix_val, dict):
            # Skip non-matrix keys like boundary_rule (a string at the
            # matrices container level).
            continue
        for tactic in matrix_val.get("tactics", []) or []:
            for ind in tactic.get("indicators", []) or []:
                if isinstance(ind, dict) and "id" in ind:
                    inds.add(ind["id"])
            for cm in tactic.get("countermeasures", []) or []:
                if isinstance(cm, dict) and "id" in cm:
                    cms.add(cm["id"])
            for rp in tactic.get("response_protocols", []) or []:
                if isinstance(rp, dict) and "id" in rp:
                    rps.add(rp["id"])
    return inds, cms, rps


def check_references(
    framework: dict,
    inds: set[str],
    cms: set[str],
    rps: set[str],
) -> list[str]:
    """Return a list of broken-reference error messages."""
    errors: list[str] = []
    matrices = framework.get("matrices", {})
    for matrix_key, matrix_val in matrices.items():
        if not isinstance(matrix_val, dict):
            continue
        for tactic in matrix_val.get("tactics", []) or []:
            tactic_id = tactic.get("id", "?")
            for ind in tactic.get("indicators", []) or []:
                if not isinstance(ind, dict):
                    continue
                ind_id = ind.get("id", "?")
                for ref in ind.get("correlates_with", []) or []:
                    if not IND_PATTERN.match(ref):
                        errors.append(
                            f"[{matrix_key}/{tactic_id}/{ind_id}] correlates_with: "
                            f"'{ref}' does not match IND-[FOI]XXXX-XX format"
                        )
                    elif ref not in inds:
                        errors.append(
                            f"[{matrix_key}/{tactic_id}/{ind_id}] correlates_with: "
                            f"'{ref}' does not resolve to any indicator in framework.json"
                        )
            for cm in tactic.get("countermeasures", []) or []:
                if not isinstance(cm, dict):
                    continue
                cm_id = cm.get("id", "?")
                for ref in cm.get("compensates_for", []) or []:
                    # Transitional dyadic form (CM- referent) or coverage
                    # form (IND- referent) — each resolves in its own
                    # namespace.
                    if CM_PATTERN.match(ref):
                        if ref not in cms:
                            errors.append(
                                f"[{matrix_key}/{tactic_id}/{cm_id}] compensates_for: "
                                f"'{ref}' does not resolve to any countermeasure in framework.json"
                            )
                    elif IND_PATTERN.match(ref):
                        if ref not in inds:
                            errors.append(
                                f"[{matrix_key}/{tactic_id}/{cm_id}] compensates_for: "
                                f"'{ref}' does not resolve to any indicator in framework.json"
                            )
                    else:
                        errors.append(
                            f"[{matrix_key}/{tactic_id}/{cm_id}] compensates_for: "
                            f"'{ref}' does not match CM-[FOI]XXXX-XX or IND-[FOI]XXXX-XX format"
                        )
            for rp in tactic.get("response_protocols", []) or []:
                if not isinstance(rp, dict):
                    continue
                rp_id = rp.get("id", "?")
                for ref in rp.get("coordinates_with", []) or []:
                    if not RP_PATTERN.match(ref):
                        errors.append(
                            f"[{matrix_key}/{tactic_id}/{rp_id}] coordinates_with: "
                            f"'{ref}' does not match RP-[FOI]XXXX-XX format"
                        )
                    elif ref not in rps:
                        errors.append(
                            f"[{matrix_key}/{tactic_id}/{rp_id}] coordinates_with: "
                            f"'{ref}' does not resolve to any response_protocol in framework.json"
                        )
    return errors


def main() -> int:
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        path = Path("docs/data/framework.json")
    if not path.exists():
        print(
            f"✗ mesh-refs lint: framework.json not found at {path}",
            file=sys.stderr,
        )
        return 1
    try:
        framework = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        print(
            f"✗ mesh-refs lint: framework.json is not valid JSON ({exc})",
            file=sys.stderr,
        )
        return 1
    inds, cms, rps = collect_ids(framework)
    errors = check_references(framework, inds, cms, rps)
    if not errors:
        print(
            f"✓ mesh-refs lint PASSED — "
            f"{len(inds)} indicators, {len(cms)} countermeasures, "
            f"{len(rps)} response protocols; all mesh references resolve."
        )
        return 0
    print(
        f"✗ mesh-refs lint FAILED — {len(errors)} broken reference(s):",
        file=sys.stderr,
    )
    for err in errors:
        print(f"  {err}", file=sys.stderr)
    print("", file=sys.stderr)
    print(
        "Detection Mesh references must resolve to existing IDs in framework.json.",
        file=sys.stderr,
    )
    print(
        "Fix by either correcting the reference or adding the missing "
        "indicator/countermeasure/response_protocol.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
