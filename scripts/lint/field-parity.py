#!/usr/bin/env python3
"""field-parity.py — cross-matrix field-parity gate.

Guards the "complete matrix" standard: any field that is universally populated
in at least one matrix must not be entirely absent from another, unless the
(matrix, field) pair is a documented matrix-specific design decision listed in
ALLOWLIST. Also enforces that every live matrix carries a within-matrix
indicator correlation mesh.

Exit 0 = parity holds. Exit 1 = violations (drift like the V1.4/V1.5
Org/Infra field gaps that shipped silently).

Usage: python3 scripts/lint/field-parity.py [path/to/framework.json]
"""
import json
import sys

# Documented matrix-specific fields: (matrix, field) pairs that are ALLOWED
# to be absent even though the field is universal elsewhere. Each entry must
# cite its design decision.
ALLOWLIST = {
    # person-only target-identity model (V1.2.2 scope decision)
    ("facility", "target_identity_scope"),
    ("organization", "target_identity_scope"),
    ("infrastructure", "target_identity_scope"),
    ("facility", "target_identity"),
    ("organization", "target_identity"),
    ("infrastructure", "target_identity"),
    # facility-only siting model
    ("person", "facility_target_scope"),
    ("organization", "facility_target_scope"),
    ("infrastructure", "facility_target_scope"),
    ("person", "within_site_focus"),
    ("organization", "within_site_focus"),
    ("infrastructure", "within_site_focus"),
    # (modality / human_social facet migration COMPLETE V1.6: now universal, no carve-out)
    # (cpn_notes retired everywhere at the V1.6 facet migration; carve-out removed)
    # (conditioning_guidance authored 815/815 in V1.6: universal, no carve-out)
}

MATRIX_IND_PREFIX = {
    "person": "IND-0",
    "facility": "IND-F",
    "organization": "IND-O",
    "infrastructure": "IND-I",
}


def populated(obj, field):
    """Key present with a meaningful value. Booleans count by presence."""
    if field not in obj:
        return False
    v = obj[field]
    if isinstance(v, bool):
        return True
    return v not in (None, "", [], {})


def scan(units_by_matrix, level):
    """Return violations + report rows for one unit level (tactic/indicator)."""
    fields = set()
    for units in units_by_matrix.values():
        for u in units:
            fields.update(u.keys())

    violations = []
    for field in sorted(fields):
        stats = {}
        for mk, units in units_by_matrix.items():
            pop = sum(1 for u in units if populated(u, field))
            stats[mk] = (pop, len(units))
        universal_in = [mk for mk, (p, n) in stats.items() if n and p == n]
        if not universal_in:
            continue
        for mk, (p, n) in stats.items():
            if p == 0 and n > 0 and (mk, field) not in ALLOWLIST:
                detail = ", ".join(
                    f"{m}={pp}/{nn}" for m, (pp, nn) in stats.items()
                )
                violations.append(
                    f"{level}.{field}: absent from '{mk}' but universal in "
                    f"{universal_in} ({detail})"
                )
    return violations


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "docs/data/framework.json"
    fw = json.load(open(path))
    matrices = {
        mk: m
        for mk, m in fw["matrices"].items()
        if isinstance(m, dict) and "tactics" in m
    }

    tactics_by_matrix = {mk: m["tactics"] for mk, m in matrices.items()}
    indicators_by_matrix = {
        mk: [i for t in m["tactics"] for i in t.get("indicators", [])]
        for mk, m in matrices.items()
    }

    violations = []
    violations += scan(tactics_by_matrix, "tactic")
    violations += scan(indicators_by_matrix, "indicator")

    # Within-matrix mesh: every live matrix must carry internal
    # correlates_with edges (the "anticipate / what-next" layer).
    for mk, inds in indicators_by_matrix.items():
        prefix = MATRIX_IND_PREFIX[mk]
        within = sum(
            1
            for i in inds
            for c in i.get("correlates_with", [])
            if isinstance(c, str) and c.startswith(prefix)
        )
        if within == 0:
            violations.append(
                f"mesh: '{mk}' has zero within-matrix correlates_with edges"
            )

    if violations:
        print(f"✗ field-parity FAILED — {len(violations)} violation(s):")
        for v in violations:
            print(f"  ✗ {v}")
        sys.exit(1)
    print(
        "✓ field-parity PASSED — no universal-vs-absent field drift across "
        f"{len(matrices)} matrices; within-matrix mesh present in all."
    )


if __name__ == "__main__":
    main()
