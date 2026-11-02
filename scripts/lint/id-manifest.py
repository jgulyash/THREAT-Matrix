#!/usr/bin/env python3
"""Generate the per-release ID manifest (schema 3.0.0).

Reads framework.json (read-only) and writes id-manifest-<version>.json, the
inventory of every identifier the release carries. The output shape is
defined by docs/data/id-manifest.schema.json. Comparing consecutive
manifests audits the docs/IDENTIFIERS.md no-reuse guarantee.

Namespace lists carry every active, deprecated, and superseded ID. IDs whose
lifecycle_state is reserved go to ids.reserved instead, whatever their
namespace. Every list is sorted and de-duplicated; a duplicate ID in the
source document is reported and makes the script exit 1 (validate.py V01 to
V04 own duplicate detection, but a manifest built over duplicates would be
silently wrong).

Optional: --previous <manifest> compares against an earlier manifest and
exits 1 if any earlier ID is missing from this one (dropped rather than
reserved).

No external dependencies.

Usage:
  python3 scripts/lint/id-manifest.py [--framework docs/data/framework.json]
                                      [--out-dir docs/data]
                                      [--generated 2026-11-02T00:00:00Z]
                                      [--previous docs/data/id-manifest-X.Y.Z.json]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

NAMESPACES = (
    "tactics",
    "actor_profiles",
    "indicators",
    "countermeasures",
    "response_protocols",
)


def iter_objects(data: dict):
    """Yield (namespace, object) for every identified object."""
    for matrix_val in (data.get("matrices") or {}).values():
        if not isinstance(matrix_val, dict):
            continue
        for tactic in matrix_val.get("tactics", []) or []:
            yield "tactics", tactic
            for kind in ("indicators", "countermeasures", "response_protocols"):
                for obj in tactic.get(kind, []) or []:
                    if isinstance(obj, dict):
                        yield kind, obj
    for profile in data.get("actor_profiles", []) or []:
        if isinstance(profile, dict):
            yield "actor_profiles", profile


def build_manifest(data: dict, generated: str) -> tuple[dict, list[str]]:
    buckets: dict[str, list[str]] = {ns: [] for ns in NAMESPACES}
    buckets["reserved"] = []
    for ns, obj in iter_objects(data):
        oid = obj.get("id")
        if not oid:
            continue
        target = "reserved" if obj.get("lifecycle_state") == "reserved" else ns
        buckets[target].append(oid)

    duplicates = []
    for name, ids in buckets.items():
        seen: set[str] = set()
        for oid in ids:
            if oid in seen:
                duplicates.append(f"{name}: {oid}")
            seen.add(oid)

    manifest = {
        "version": data.get("version"),
        "generated": generated,
        "ids": {name: sorted(set(ids)) for name, ids in buckets.items()},
    }
    return manifest, duplicates


def all_ids(manifest: dict) -> set[str]:
    return {oid for ids in manifest["ids"].values() for oid in ids}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--framework", default="docs/data/framework.json")
    parser.add_argument("--out-dir", default="docs/data")
    parser.add_argument(
        "--generated",
        help="UTC timestamp to stamp (default: now). Pin it for reproducible output.",
    )
    parser.add_argument("--previous", help="Earlier manifest to diff against.")
    args = parser.parse_args()

    framework_path = Path(args.framework)
    if not framework_path.exists():
        print(f"✗ id-manifest: framework.json not found at {framework_path}", file=sys.stderr)
        return 1
    data = json.loads(framework_path.read_text())

    version = data.get("version")
    if not isinstance(version, str) or not version:
        print("✗ id-manifest: framework.json carries no version", file=sys.stderr)
        return 1

    generated = args.generated or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest, duplicates = build_manifest(data, generated)
    if duplicates:
        for dup in duplicates:
            print(f"✗ id-manifest: duplicate id {dup}", file=sys.stderr)
        return 1

    status = 0
    if args.previous:
        previous = json.loads(Path(args.previous).read_text())
        missing = sorted(all_ids(previous) - all_ids(manifest))
        for oid in missing:
            print(
                f"✗ id-manifest: {oid} present in {previous.get('version')} is "
                f"missing from {version} (IDs are reserved, never dropped)",
                file=sys.stderr,
            )
        if missing:
            status = 1

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"id-manifest-{version}.json"
    out_path.write_text(json.dumps(manifest, indent=2) + "\n")

    counts = ", ".join(f"{k} {len(v)}" for k, v in manifest["ids"].items())
    print(f"✓ id-manifest: wrote {out_path} ({counts})")
    return status


if __name__ == "__main__":
    sys.exit(main())
