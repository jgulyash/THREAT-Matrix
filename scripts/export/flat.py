#!/usr/bin/env python3
"""Write a flat distribution of the THREAT Matrix vocabulary.

framework.json nests indicators, countermeasures, and response protocols
inside tactics inside matrices. This script writes the same content as
flat files that load directly into a table, a graph, or a search index:

  tactics.jsonl             one tactic per line, without nested children
  indicators.jsonl          one indicator per line
  countermeasures.jsonl     one countermeasure per line
  response_protocols.jsonl  one response protocol per line
  actor_profiles.jsonl      one actor profile per line (reserved stubs
                            included, marked by lifecycle_state)
  bibliography.jsonl        one source per line, its key as "id"
  relationships.jsonl       one edge per line:
                            {"source", "relation", "target", "attrs"}
  index.json                framework version, object counts, and the
                            SHA-256 of every file

Every object line carries its own "id" and "matrix"; indicators,
countermeasures, and response protocols also carry "tactic_id" (their
parent). Relations exported: correlates_with, mitigates (attrs.function),
compensates_for, coordinates_with, actor_associations (attrs hold the
association's other fields), related_tactics, source_refs.

Output is deterministic: objects sorted by id, edges sorted by relation,
source, target; keys in a stable order; no timestamp. The same input
always produces byte-identical files.

Scores are never included by default; the vocabulary has none. With
--with-experimental-scores the experimental overlay is exported to a
separate scores.jsonl, and index.json carries the overlay's notice. The
overlay is non-normative and unvalidated; it scores behavior types, never
a person.

After writing, the script re-reads every file and checks that the flat
files round-trip to the same object counts as the source and that each
file matches its recorded SHA-256. Generated output is not for commit;
write it to out/ or build/ (both ignored by git).

Exit codes: 0 written and self-check passed; 1 self-check failed or the
source has duplicate ids; 2 an input could not be read or the output
directory was not usable. Standard library only.

Usage:
  python3 scripts/export/flat.py --out out/flat
  python3 scripts/export/flat.py --out out/flat-scored --with-experimental-scores
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

NAME = "export-flat"
REPO = Path(__file__).resolve().parents[2]
CHILD_KINDS = ("indicators", "countermeasures", "response_protocols")
OBJECT_FILES = ("tactics", "indicators", "countermeasures", "response_protocols", "actor_profiles", "bibliography")
SCORES_FILE = "scores.jsonl"


class InputError(Exception):
    """An input could not be read or the output directory is not usable."""


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


def edge(source: str, relation: str, target: str, attrs: dict | None = None) -> dict:
    return {"source": source, "relation": relation, "target": target, "attrs": attrs or {}}


def string_refs(obj: dict, field: str) -> list[str]:
    value = obj.get(field)
    return [ref for ref in value if isinstance(ref, str)] if isinstance(value, list) else []


def flatten(framework) -> tuple[dict[str, list[dict]], list[dict], list[str]]:
    """Return (objects by file, edges, problems)."""
    if not isinstance(framework, dict):
        raise InputError("framework document top level is not a JSON object")
    matrices = framework.get("matrices")
    if not isinstance(matrices, dict):
        raise InputError("framework document has no 'matrices' object")

    objects: dict[str, list[dict]] = {name: [] for name in OBJECT_FILES}
    edges: list[dict] = []
    problems: list[str] = []

    for matrix_key, matrix in matrices.items():
        if not isinstance(matrix, dict):
            continue
        tactics = matrix.get("tactics")
        if not isinstance(tactics, list):
            raise InputError(f"matrices.{matrix_key}.tactics is missing or is not an array")
        for tactic in tactics:
            if not isinstance(tactic, dict) or not isinstance(tactic.get("id"), str):
                problems.append(f"matrices.{matrix_key}: a tactic is not an object with a string id")
                continue
            tactic_id = tactic["id"]
            row = {"id": tactic_id, "matrix": matrix_key}
            row.update({k: v for k, v in tactic.items() if k not in CHILD_KINDS and k not in ("id", "matrix")})
            objects["tactics"].append(row)
            for ref in string_refs(tactic, "related_tactics"):
                edges.append(edge(tactic_id, "related_tactics", ref))
            for ref in string_refs(tactic, "source_refs"):
                edges.append(edge(tactic_id, "source_refs", ref))
            for assoc in tactic.get("actor_associations") or []:
                if isinstance(assoc, dict) and isinstance(assoc.get("actor_id"), str):
                    attrs = {k: v for k, v in assoc.items() if k != "actor_id"}
                    edges.append(edge(tactic_id, "actor_associations", assoc["actor_id"], attrs))
            for kind in CHILD_KINDS:
                for child in tactic.get(kind) or []:
                    if not isinstance(child, dict) or not isinstance(child.get("id"), str):
                        problems.append(f"{tactic_id}: a {kind} entry is not an object with a string id")
                        continue
                    child_id = child["id"]
                    child_row = {"id": child_id, "tactic_id": tactic_id, "matrix": matrix_key}
                    child_row.update({k: v for k, v in child.items() if k not in ("id", "tactic_id", "matrix")})
                    objects[kind].append(child_row)
                    for ref in string_refs(child, "source_refs"):
                        edges.append(edge(child_id, "source_refs", ref))
                    if kind == "indicators":
                        for ref in string_refs(child, "correlates_with"):
                            edges.append(edge(child_id, "correlates_with", ref))
                    elif kind == "countermeasures":
                        for ref in string_refs(child, "compensates_for"):
                            edges.append(edge(child_id, "compensates_for", ref))
                        for item in child.get("mitigates") or []:
                            if isinstance(item, dict) and isinstance(item.get("indicator"), str):
                                attrs = {k: v for k, v in item.items() if k != "indicator"}
                                edges.append(edge(child_id, "mitigates", item["indicator"], attrs))
                    else:
                        for ref in string_refs(child, "coordinates_with"):
                            edges.append(edge(child_id, "coordinates_with", ref))

    for profile in framework.get("actor_profiles") or []:
        if not isinstance(profile, dict) or not isinstance(profile.get("id"), str):
            problems.append("actor_profiles: an entry is not an object with a string id")
            continue
        row = {"id": profile["id"]}
        row.update({k: v for k, v in profile.items() if k != "id"})
        objects["actor_profiles"].append(row)
        for ref in string_refs(profile, "source_refs"):
            edges.append(edge(profile["id"], "source_refs", ref))

    bibliography = framework.get("bibliography")
    if isinstance(bibliography, dict):
        for key, entry in bibliography.items():
            row = {"id": key}
            if isinstance(entry, dict):
                row.update({k: v for k, v in entry.items() if k != "id"})
            objects["bibliography"].append(row)

    for name, rows in objects.items():
        ids = [row["id"] for row in rows]
        dupes = sorted({i for i in ids if ids.count(i) > 1}) if len(set(ids)) != len(ids) else []
        for dupe in dupes:
            problems.append(f"{name}: duplicate id {dupe}")
        rows.sort(key=lambda row: row["id"])
    edges.sort(key=lambda e: (e["relation"], e["source"], e["target"], json.dumps(e["attrs"], sort_keys=True)))
    return objects, edges, problems


def source_counts(framework: dict) -> dict[str, int]:
    """Count objects straight from the nested document, independently of flatten()."""
    counts = dict.fromkeys(OBJECT_FILES, 0)
    for matrix in framework["matrices"].values():
        if not isinstance(matrix, dict):
            continue
        for tactic in matrix.get("tactics") or []:
            counts["tactics"] += 1
            if isinstance(tactic, dict):
                for kind in CHILD_KINDS:
                    counts[kind] += len(tactic.get(kind) or [])
    counts["actor_profiles"] = len(framework.get("actor_profiles") or [])
    counts["bibliography"] = len(framework.get("bibliography") or {})
    return counts


def score_rows(overlay, indicator_ids: set[str]) -> list[dict]:
    if not isinstance(overlay, dict) or not isinstance(overlay.get("indicator_scores"), dict):
        raise InputError("scoring overlay has no 'indicator_scores' object")
    rows = []
    for ind_id, entry in overlay["indicator_scores"].items():
        row = {"id": ind_id, "kind": "indicator_type_score"}
        if isinstance(entry, dict):
            row.update(entry)
        rows.append(row)
    priorities = overlay.get("tactic_priorities")
    for tactic_id, priority in (priorities.items() if isinstance(priorities, dict) else []):
        rows.append({"id": tactic_id, "kind": "tactic_priority", "priority": priority})
    rows.sort(key=lambda row: (row["kind"], row["id"]))
    return rows


def jsonl_bytes(rows: list[dict]) -> bytes:
    lines = [json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows]
    return ("\n".join(lines) + ("\n" if lines else "")).encode("utf-8")


def self_check(out_dir: Path, index: dict, expected: dict[str, int]) -> list[str]:
    """Re-read the written files; compare counts and hashes."""
    problems = []
    for name, meta in index["files"].items():
        path = out_dir / name
        try:
            data = path.read_bytes()
        except OSError:
            problems.append(f"{name}: could not be re-read")
            continue
        if hashlib.sha256(data).hexdigest() != meta["sha256"]:
            problems.append(f"{name}: SHA-256 does not match index.json")
        try:
            rows = [json.loads(line) for line in data.decode("utf-8").splitlines()]
        except (UnicodeDecodeError, json.JSONDecodeError):
            problems.append(f"{name}: a line is not valid JSON")
            continue
        if len(rows) != meta["count"]:
            problems.append(f"{name}: {len(rows)} line(s) but index.json records {meta['count']}")
        stem = name[: -len(".jsonl")]
        if stem in expected and len(rows) != expected[stem]:
            problems.append(f"{name}: {len(rows)} object(s) but the source document has {expected[stem]}")
        if stem in expected and len({row.get("id") for row in rows}) != len(rows):
            problems.append(f"{name}: ids are not unique")
    return problems


def run(args) -> int:
    framework = load_json(args.framework, "framework document")
    objects, edges, problems = flatten(framework)
    if problems:
        print(f"FAILED {NAME}: the source document cannot be flattened ({len(problems)} problem(s)):", file=sys.stderr)
        for problem in problems[:20]:
            print(f"  {problem}", file=sys.stderr)
        return 1

    payloads: dict[str, tuple[bytes, int]] = {}
    for name in OBJECT_FILES:
        payloads[f"{name}.jsonl"] = (jsonl_bytes(objects[name]), len(objects[name]))
    payloads["relationships.jsonl"] = (jsonl_bytes(edges), len(edges))

    index = {
        "name": framework.get("name"),
        "full_name": framework.get("full_name"),
        "framework_version": framework.get("version"),
        "schema_version": framework.get("schema_version"),
        "license": framework.get("license"),
        "format": "THREAT Matrix flat distribution, JSON Lines, one object per line",
        "matrices": {
            key: {"maturity": value.get("maturity"), "tactics": sum(1 for t in objects["tactics"] if t["matrix"] == key)}
            for key, value in framework["matrices"].items() if isinstance(value, dict)
        },
        "relations": {},
        "includes_experimental_scores": False,
        "not_included": "Top-level reference blocks of framework.json (phase_mappings, detection_mesh, "
                        "ai_architecture, warden_integration, matrices.boundary_rule, matrix scope text) "
                        "are not part of the flat distribution; read them from framework.json.",
        "files": {},
    }
    for item in edges:
        index["relations"][item["relation"]] = index["relations"].get(item["relation"], 0) + 1

    if args.with_experimental_scores:
        overlay = load_json(args.overlay, "scoring overlay")
        rows = score_rows(overlay, {row["id"] for row in objects["indicators"]})
        if overlay.get("applies_to_framework_version") != framework.get("version"):
            raise InputError(
                f"the overlay applies to framework version {overlay.get('applies_to_framework_version')!r}, "
                f"not {framework.get('version')!r}; refusing to export them together"
            )
        payloads[SCORES_FILE] = (jsonl_bytes(rows), len(rows))
        index["includes_experimental_scores"] = True
        index["experimental_scores"] = {
            "file": SCORES_FILE,
            "notice": overlay.get("notice"),
            "overlay_version": overlay.get("overlay_version"),
            "applies_to_framework_version": overlay.get("applies_to_framework_version"),
            "status": overlay.get("status"),
            "normative": overlay.get("normative"),
            "validation_status": overlay.get("validation_status"),
            "scope": overlay.get("scope"),
            "not_a_risk_score": overlay.get("not_a_risk_score"),
            "not_exported": "rubric and instance_conditioning; read them from scoring-overlay.json",
        }

    for name in sorted(payloads):
        data, count = payloads[name]
        index["files"][name] = {"count": count, "sha256": hashlib.sha256(data).hexdigest()}

    out_dir = Path(args.out)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        stale = out_dir / SCORES_FILE
        if not args.with_experimental_scores and stale.exists():
            raise InputError(
                f"{stale} exists from an earlier scored export. A score-free export must not sit next "
                f"to a scores file; choose an empty output directory"
            )
        for name, (data, _count) in payloads.items():
            (out_dir / name).write_bytes(data)
        (out_dir / "index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except OSError as exc:
        raise InputError(f"could not write to {out_dir} ({exc.__class__.__name__})")

    written_index = load_json(out_dir / "index.json", "index.json")
    failures = self_check(out_dir, written_index, source_counts(framework))
    if failures:
        print(f"FAILED {NAME}: self-check found {len(failures)} problem(s):", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    counts = ", ".join(f"{name} {len(objects[name])}" for name in OBJECT_FILES)
    scored = "; experimental scores in scores.jsonl (see the notice in index.json)" if args.with_experimental_scores else "; no scores"
    print(
        f"PASSED {NAME}: wrote {len(payloads) + 1} files to {out_dir} for framework "
        f"{framework.get('version')} ({counts}, relationships {len(edges)}{scored}). "
        f"Self-check: counts round-trip and every SHA-256 matches."
    )
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="Write a flat JSON Lines distribution of the vocabulary.")
    parser.add_argument("--out", required=True, help="output directory (use out/ or build/, which git ignores)")
    parser.add_argument("--framework", default=str(REPO / "docs" / "data" / "framework.json"))
    parser.add_argument("--with-experimental-scores", action="store_true",
                        help="also export the experimental, non-normative scoring overlay to scores.jsonl")
    parser.add_argument("--overlay", default=str(REPO / "docs" / "data" / "scoring-overlay.json"))
    args = parser.parse_args()
    try:
        return run(args)
    except InputError as exc:
        print(f"error: {NAME}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
