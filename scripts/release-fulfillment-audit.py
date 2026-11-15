#!/usr/bin/env python3
"""THREAT Matrix promise-versus-fulfillment release audit.

Run before every release:  python3 scripts/release-fulfillment-audit.py

Why this exists: an emptiness check ("is this array empty?") misses a more
important class of gap, where a structure is populated but the document's
own description claims something the data does not deliver (for example, a
Detection Mesh axis that is named while zero links of that kind exist).
This audit applies that description-versus-data lens mechanically.

It reports; it does not gate. Review each FLAG before release. Some
partial fields are by design and are labelled as such.

Sections:
  1. Field fulfillment: schema-defined fields versus actual population.
  2. Detection Mesh: each named axis versus delivered links.
  3. Top-level structures that are scaffolded but empty.
  4. Experimental scoring overlay coverage (only if the overlay file is
     present; the vocabulary is complete without it).
  5. Description claims that need a manual check each release.

framework.json carries no scores, and this script reads none from it.

Exit codes: 0 the report was produced (flags do not change the exit
code); 2 an input could not be read or is not the expected shape.

Usage:
  python3 scripts/release-fulfillment-audit.py
      [--framework docs/data/framework.json]
      [--schema docs/data/framework.schema.json]
      [--overlay docs/data/scoring-overlay.json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NAME = "release-fulfillment-audit"
REPO = Path(__file__).resolve().parents[1]

# Partial population that is intentional. Reported, not flagged.
BY_DESIGN = {
    # Revealed-reading target fields: empty when the behavior reveals nothing.
    "target_identity", "facility_target_scope", "within_site_focus", "target_identity_scope",
    # Aftermath tactics only.
    "phase_4_track",
    # Optional lifecycle fields: absent on active objects.
    "lifecycle_state", "deprecated_in", "superseded_by", "deprecation_reason", "reserved_reason",
}


class InputError(Exception):
    """An input document could not be read or is not the expected shape."""


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


def rule(title: str) -> None:
    print("\n" + "=" * 72 + f"\n{title}\n" + "=" * 72)


def as_list(value) -> list:
    return value if isinstance(value, list) else []


def dicts(value) -> list[dict]:
    return [item for item in as_list(value) if isinstance(item, dict)]


def field_pop(items: list[dict], props, label: str) -> None:
    print(f"\n{label} (n={len(items)}):")
    if not items:
        print("  (none)  <-- FLAG")
        return
    for field in props:
        pop = sum(1 for item in items if item.get(field) not in (None, [], {}, ""))
        if pop == len(items):
            continue
        tag = "SHELL (0)" if pop == 0 else "partial"
        if field in BY_DESIGN:
            note = "  [by design]"
        else:
            note = "  <-- FLAG" if pop == 0 else "  <-- review"
        print(f"  {field:36s} {pop}/{len(items)}  {tag}{note}")


def schema_props(schema: dict, name: str) -> list[str]:
    """Property names of $defs.<name>, tolerant of schema restructuring."""
    node = schema.get("$defs", {}).get(name) if isinstance(schema.get("$defs"), dict) else None
    if not isinstance(node, dict):
        return []
    props = node.get("properties")
    return list(props) if isinstance(props, dict) else []


def run(args) -> int:
    fw = load_json(args.framework, "framework document")
    schema = load_json(args.schema, "framework schema")
    if not isinstance(fw, dict):
        raise InputError("framework document top level is not a JSON object")
    if not isinstance(schema, dict):
        raise InputError("framework schema top level is not a JSON object")
    matrices_raw = fw.get("matrices")
    if not isinstance(matrices_raw, dict):
        raise InputError("framework document has no 'matrices' object")
    matrices = {
        key: value for key, value in matrices_raw.items()
        if isinstance(value, dict) and isinstance(value.get("tactics"), list)
    }
    if not matrices:
        raise InputError("framework document has no matrix with a 'tactics' array")

    tactics = {key: dicts(value["tactics"]) for key, value in matrices.items()}
    all_tactics = [t for key in matrices for t in tactics[key]]
    all_inds = [i for t in all_tactics for i in dicts(t.get("indicators"))]

    print(
        f"THREAT Matrix release audit: content version {fw.get('version')!r}, "
        f"schema version {fw.get('schema_version')!r}"
    )
    print("Matrices: " + ", ".join(
        f"{key} ({value.get('maturity', 'maturity unset')}, {len(tactics[key])} tactics)"
        for key, value in matrices.items()
    ))

    # ---- 1. Field fulfillment ----
    rule("1. FIELD FULFILLMENT: schema-defined fields versus actual population")
    ind_props = schema_props(schema, "indicator") or sorted({k for i in all_inds for k in i})
    tac_props = schema_props(schema, "tactic") or sorted({k for t in all_tactics for k in t})
    field_pop(all_inds, ind_props, "INDICATOR fields")
    field_pop(all_tactics, tac_props, "TACTIC fields")
    profiles = [
        p for p in dicts(fw.get("actor_profiles"))
        if p.get("lifecycle_state", "active") != "reserved"
    ]
    field_pop(profiles, sorted({k for p in profiles for k in p}), "ACTOR_PROFILE fields (reserved stubs excluded)")

    # ---- 2. Detection Mesh axis delivery ----
    rule("2. DETECTION MESH: each named axis versus delivered links")
    meta = {}
    for key in matrices:
        for tactic in tactics[key]:
            for ind in dicts(tactic.get("indicators")):
                if isinstance(ind.get("id"), str):
                    meta[ind["id"]] = (key, tactic.get("phase"), ind.get("category"))
    cross_phase = cross_matrix = cross_domain = same = 0
    for key in matrices:
        for tactic in tactics[key]:
            for ind in dicts(tactic.get("indicators")):
                for ref in as_list(ind.get("correlates_with")):
                    if not isinstance(ref, str) or ref not in meta:
                        continue
                    other_matrix, other_phase, other_category = meta[ref]
                    if other_matrix != key:
                        cross_matrix += 1
                    elif other_phase != tactic.get("phase"):
                        cross_phase += 1
                    else:
                        same += 1
                    # Counted independently of the matrix and phase split.
                    if other_category != ind.get("category"):
                        cross_domain += 1

    def owner_map(container: str) -> dict[str, str]:
        return {
            item["id"]: key
            for key in matrices for tactic in tactics[key]
            for item in dicts(tactic.get(container)) if isinstance(item.get("id"), str)
        }

    def cross_matrix_refs(container: str, field: str, id_map: dict[str, str]) -> int:
        count = 0
        for key in matrices:
            for tactic in tactics[key]:
                for item in dicts(tactic.get(container)):
                    for ref in as_list(item.get(field)):
                        if isinstance(ref, str) and id_map.get(ref) not in (None, key):
                            count += 1
        return count

    delivered = {
        "cross_phase": cross_phase,
        "cross_matrix": cross_matrix,
        "cross_domain": cross_domain,
        "cross_countermeasure": cross_matrix_refs("countermeasures", "compensates_for", owner_map("countermeasures")),
        "cross_stakeholder": cross_matrix_refs("response_protocols", "coordinates_with", owner_map("response_protocols")),
    }
    mesh = fw.get("detection_mesh") if isinstance(fw.get("detection_mesh"), dict) else {}
    axes = [a.get("name") for a in dicts(mesh.get("axes"))]
    print(f"  named mesh axes: {axes}")
    if not axes:
        print("  no detection_mesh.axes found  <-- FLAG")
    for axis in axes:
        count = delivered.get(axis)
        if count is None:
            print(f"  {str(axis):22s} : n/a  <-- add a delivery measure for this axis")
        else:
            print(f"  {str(axis):22s} : {count} delivered" + ("" if count > 0 else "  <-- FLAG: named but 0 delivered"))
    print(f"  (within-matrix same-phase correlates_with links: {same})")
    print("  Measures: cross_phase and cross_matrix partition correlates_with links by")
    print("  the two indicators' phase and matrix. cross_domain counts correlates_with")
    print("  links whose two indicators have a different 'category' (detection domain);")
    print("  it overlaps the other two. cross_countermeasure and cross_stakeholder count")
    print("  compensates_for and coordinates_with references that cross a matrix.")
    edges = [
        edge for t in all_tactics for cm in dicts(t.get("countermeasures"))
        for edge in dicts(cm.get("mitigates"))
    ]
    unreviewed = sum(1 for edge in edges if edge.get("function") == "unreviewed")
    print(f"  mitigates edges: {len(edges)} total, {unreviewed} with function 'unreviewed'"
          + ("  <-- review: unreviewed edges remain" if unreviewed else ""))

    # ---- 3. Empty top-level structures ----
    rule("3. TOP-LEVEL STRUCTURES: scaffolded but empty")
    flagged = False
    for key, value in fw.items():
        if isinstance(value, (list, dict)) and len(value) == 0:
            print(f"  {key}: empty  <-- FLAG")
            flagged = True
    for key in matrices:
        if not tactics[key]:
            print(f"  matrix {key}: 0 tactics  <-- FLAG (empty matrix scaffold)")
            flagged = True
    if not flagged:
        print("  none")

    # ---- 4. Experimental overlay coverage ----
    rule("4. EXPERIMENTAL SCORING OVERLAY: coverage (non-normative, optional)")
    overlay_path = Path(args.overlay)
    if not overlay_path.exists():
        print(f"  overlay not present at {overlay_path}; the vocabulary is complete without it.")
    else:
        overlay = load_json(overlay_path, "scoring overlay")
        scores = overlay.get("indicator_scores") if isinstance(overlay, dict) else None
        if not isinstance(scores, dict):
            print("  overlay has no indicator_scores object  <-- FLAG")
        else:
            live = {
                i["id"] for i in all_inds
                if isinstance(i.get("id"), str) and i.get("lifecycle_state") != "reserved"
            }
            missing = sorted(live - set(scores))
            extra = sorted(set(scores) - live)
            print(f"  overlay_version {overlay.get('overlay_version')!r}, applies_to_framework_version "
                  f"{overlay.get('applies_to_framework_version')!r}, status {overlay.get('status')!r}, "
                  f"validation_status {overlay.get('validation_status')!r}")
            if overlay.get("applies_to_framework_version") != fw.get("version"):
                print("  applies_to_framework_version differs from the framework version  <-- FLAG")
            print(f"  indicator_scores: {len(scores)} entries for {len(live)} indicators; "
                  f"missing {len(missing)}, extra {len(extra)}"
                  + ("  <-- FLAG" if missing or extra else ""))
            priorities = overlay.get("tactic_priorities")
            if isinstance(priorities, dict):
                tactic_ids = {t.get("id") for t in all_tactics}
                unknown = sorted(set(priorities) - tactic_ids)
                print(f"  tactic_priorities: {len(priorities)} entries for {len(tactic_ids)} tactics; "
                      f"unknown tactic ids {len(unknown)}" + ("  <-- FLAG" if unknown else ""))
        print("  This section reports coverage only. It does not assess whether any score is accurate.")

    # ---- 5. Manual checks ----
    rule("5. DESCRIPTION CLAIMS: verify by hand each release (data cannot self-check these)")
    consumer_refs = len(re.findall(r"consumer|downstream|triage tooling", json.dumps(fw), flags=re.I))
    print(f"""  [ ] detection_mesh.principle prose matches the axis-delivery numbers in
      section 2 above.
  [ ] {consumer_refs} 'consumer', 'downstream', or 'triage tooling' references in the
      document describe tooling that may not exist. Each is labelled as
      guidance or roadmap, not implied as shipped.
  [ ] Matrices labelled draft are presented as draft everywhere they appear.
  [ ] No text in framework.json presents a score, band, or priority; all
      scoring lives in the experimental overlay and is described there as
      experimental, non-normative, and unvalidated.
  [ ] Any field or object added this cycle whose description promises
      behavior is populated where the description says it is.""")

    print("\n" + "=" * 72)
    print("Audit complete. FLAG = the schema or a description promises something the data does not meet.")
    print("Review every FLAG before release.")
    print("=" * 72)
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="THREAT Matrix promise-versus-fulfillment release audit.")
    parser.add_argument("--framework", default=str(REPO / "docs" / "data" / "framework.json"))
    parser.add_argument("--schema", default=str(REPO / "docs" / "data" / "framework.schema.json"))
    parser.add_argument("--overlay", default=str(REPO / "docs" / "data" / "scoring-overlay.json"))
    args = parser.parse_args()
    try:
        return run(args)
    except InputError as exc:
        print(f"error: {NAME}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
