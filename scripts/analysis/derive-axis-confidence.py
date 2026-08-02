#!/usr/bin/env python3
"""Derive per-indicator axis_confidence (Ruling 10-A, 2026-07-28 session).

axis_confidence is a categorical evidence-basis marker per escalation axis:
"established" / "inferred" / "thin". It is rule-derived, never hand-tuned, and
this script IS the derivation rule (living documentation). Confidence is
evidence basis, NOT severity: a thin axis is a wider error bar and a candidate
for earlier human review, never an automatic demotion.

Derivation rules (verbatim from the ruling):
- detectability: value <= 2.0 -> "thin" (the self_censoring_caveat band: very
  low detectability values carry wider uncertainty); value >= 6.0 ->
  "established"; else "inferred".
- blast_radius_potential: value within +/-0.5 of a documented base-rate anchor
  or tier bound for that matrix's re-derivation doc -> "established"; else
  "inferred". Anchor sets below cite their source documents.
- impact_potential and recoverability_inverse: "inferred" framework-wide, the
  honest default; upgrading them is future evidence-audit work.

Usage:
  python3 scripts/analysis/derive-axis-confidence.py --check   (default; verify
      every shipped axis_confidence matches the rules; exit 1 on mismatch)
  python3 scripts/analysis/derive-axis-confidence.py --apply   (insertion-only
      byte-safe splice: add axis_confidence to every indicator, positioned
      immediately before informs_axes; refuses if any indicator already has it)
"""
import json
import re
import sys

PATH = "docs/data/framework.json"

# Documented blast_radius anchors / tier bounds per matrix (+/-0.5 window):
# - person: escalation_rubric.blast_radius_guidance.method_collateral_base_rates
# - facility: the People method table is the documented base (V1.3 CHANGELOG
#   facility calibration paragraph: method base rates + the ~4.0 blast floor)
# - organization: tier bounds, DESIGN-b5-org-escalation-scoring.md
# - infrastructure: tier bounds, DESIGN-b5-infra-escalation-scoring.md
BLAST_ANCHORS = {
    "person": {2.0, 2.5, 3.0, 4.0, 7.0, 8.0, 9.0},
    "facility": {2.0, 2.5, 3.0, 4.0, 7.0, 8.0, 9.0},
    "organization": {2.0, 3.5, 4.0, 5.5, 6.5, 7.5, 8.5},
    "infrastructure": {2.5, 3.5, 4.0, 5.5, 6.0, 7.0, 7.5, 8.0, 9.0},
}
ANCHOR_WINDOW = 0.5


def derive(matrix_key: str, axes: dict) -> dict:
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
        if any(abs(blast - a) <= ANCHOR_WINDOW for a in anchors)
        else "inferred"
    )

    return {
        "impact_potential": "inferred",
        "blast_radius_potential": blast_conf,
        "recoverability_inverse": "inferred",
        "detectability": det_conf,
    }


def iter_indicators(data):
    for mk, mv in data["matrices"].items():
        if not isinstance(mv, dict):
            continue
        for tactic in mv.get("tactics", []):
            for ind in tactic.get("indicators", []):
                yield mk, ind


def cmd_check() -> int:
    data = json.load(open(PATH, encoding="utf-8"))
    missing, mismatched, total = [], [], 0
    for mk, ind in iter_indicators(data):
        total += 1
        expected = derive(mk, ind["escalation_axes"])
        got = ind.get("axis_confidence")
        if got is None:
            missing.append(ind["id"])
        elif got != expected:
            mismatched.append((ind["id"], got, expected))
    if missing:
        print(f"MISSING axis_confidence on {len(missing)}: {missing[:5]}...")
    for iid, got, exp in mismatched[:10]:
        print(f"MISMATCH {iid}: shipped {got} != rule {exp}")
    if missing or mismatched:
        return 1
    print(f"axis_confidence check PASSED: {total}/815 rule-consistent")
    return 0


def cmd_apply() -> int:
    raw = open(PATH, encoding="utf-8").read()
    data = json.loads(raw)
    values = {}
    for mk, ind in iter_indicators(data):
        if "axis_confidence" in ind:
            sys.exit(f"REFUSED: {ind['id']} already carries axis_confidence")
        values[ind["id"]] = derive(mk, ind["escalation_axes"])

    lines = raw.split("\n")
    out, last_ind_id, inserted = [], None, 0
    id_re = re.compile(r'^\s*"id": "(IND-[A-Z]?[0-9]{4}-[0-9]{2})",?$')
    for line in lines:
        m = id_re.match(line)
        if m:
            last_ind_id = m.group(1)
        stripped = line.lstrip()
        if stripped.startswith('"informs_axes":'):
            assert last_ind_id and last_ind_id in values, f"orphan informs_axes after {last_ind_id}"
            indent = line[: len(line) - len(stripped)]
            v = values[last_ind_id]
            out.append(
                f'{indent}"axis_confidence": {{ "impact_potential": "{v["impact_potential"]}", '
                f'"blast_radius_potential": "{v["blast_radius_potential"]}", '
                f'"recoverability_inverse": "{v["recoverability_inverse"]}", '
                f'"detectability": "{v["detectability"]}" }},'
            )
            inserted += 1
        out.append(line)
    assert inserted == len(values), f"inserted {inserted} != indicators {len(values)}"

    new_raw = "\n".join(out)
    # reverse proof: stripping exactly the inserted lines restores the original bytes
    reverse = "\n".join(
        ln for ln in new_raw.split("\n") if not ln.lstrip().startswith('"axis_confidence":')
    )
    assert reverse == raw, "reverse-edit proof FAILED"
    new_data = json.loads(new_raw)
    for mk, ind in iter_indicators(new_data):
        assert ind["axis_confidence"] == values[ind["id"]]
    open(PATH, "w", encoding="utf-8").write(new_raw)
    print(f"APPLIED axis_confidence to {inserted} indicators (insertion-only, reverse-proof passed)")
    dist = {}
    for v in values.values():
        for a, lv in v.items():
            dist.setdefault(a, {}).setdefault(lv, 0)
            dist[a][lv] += 1
    for a, d in dist.items():
        print(f"  {a}: {d}")
    return 0


if __name__ == "__main__":
    sys.exit(cmd_apply() if "--apply" in sys.argv else cmd_check())
