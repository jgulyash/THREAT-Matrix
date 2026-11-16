#!/usr/bin/env python3
"""Write and check the per-release ID manifest.

The manifest (docs/data/id-manifest.json, shape defined by
docs/data/id-manifest.schema.json) is the committed inventory of every
identifier a framework release carries. It turns the docs/IDENTIFIERS.md
guarantee (an identifier is never reused and never silently dropped) into
a gate.

Manifest sections:
  ids.<namespace>  every active, deprecated, or superseded ID, sorted
                   (tactics, actor_profiles, indicators, countermeasures,
                   response_protocols)
  ids.reserved     IDs that are held and carry no content: reserved actor
                   profile stubs in the document, plus any ID reserved by
                   hand for another namespace
  removed          IDs withdrawn from the document, each with removed_in
                   and a reason; a removed ID is never reused

Modes:

  --check FRAMEWORK MANIFEST [--baseline OLDER_MANIFEST ...]
      Fail unless the committed manifest describes the framework exactly.
      Detects: an ID in the manifest that is missing from the framework
      without a `removed` record; an ID in the framework that is missing
      from the manifest; a reserved or removed ID that is live again
      (reuse); an ID listed as both live and reserved; a duplicate ID; an
      ID in a different namespace than the manifest records; a malformed
      or unsorted manifest; a version mismatch. With --baseline
      (repeatable) it also compares against an older manifest, such as
      the committed published baseline
      docs/data/baselines/id-manifest-1.7.0.json or the previous commit's
      manifest. It fails if any ID in the baseline is missing from the
      framework and not listed under `removed` with a reason, if a
      baseline-reserved or baseline-removed ID is live, or if an ID moved
      to another namespace. Without a baseline, an ID deleted together
      with a regenerated manifest cannot be seen; always pass one.

  --write OUT [--framework F] [--previous MANIFEST] [--generated TS]
              [--removed ID=REASON ...] [--reserve ID ...]
      Build the manifest from the framework and write it to OUT. With
      --previous, `removed` records and hand-reserved IDs are carried
      forward and the same no-drop, no-reuse comparison runs first. The
      file is written only if every check passes; nothing is printed as
      success after a failure.

Exit codes: 0 success; 1 a check failed (nothing written); 2 an input
could not be read or the arguments were not usable. Standard library
only; if the jsonschema package is importable, the manifest is also
validated against docs/data/id-manifest.schema.json.

Usage:
  python3 scripts/lint/id-manifest.py --check docs/data/framework.json docs/data/id-manifest.json \\
      --baseline docs/data/baselines/id-manifest-1.7.0.json
  python3 scripts/lint/id-manifest.py --write docs/data/id-manifest.json --previous docs/data/id-manifest.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

NAME = "id-manifest"
REPO = Path(__file__).resolve().parents[2]
MANIFEST_SCHEMA = REPO / "docs" / "data" / "id-manifest.schema.json"

# The same ID grammars as docs/data/id-manifest.schema.json.
# \Z, not $: Python's $ also matches before a trailing newline.
NAMESPACE_PATTERNS = {
    "tactics": re.compile(r"^T[MFOI]0[1-4](0[1-9]|[1-9][0-9])\Z"),
    "actor_profiles": re.compile(r"^AP(00[1-9]|0[1-9][0-9]|[1-9][0-9]{2})\Z"),
    "indicators": re.compile(r"^IND-[FOI]?0[1-4](0[1-9]|[1-9][0-9])-(0[1-9]|[1-9][0-9])\Z"),
    "countermeasures": re.compile(r"^CM-[FOI]?0[1-4](0[1-9]|[1-9][0-9])-(0[1-9]|[1-9][0-9])\Z"),
    "response_protocols": re.compile(r"^RP-[FOI]?0[1-4](0[1-9]|[1-9][0-9])-(0[1-9]|[1-9][0-9])\Z"),
}
NAMESPACES = tuple(NAMESPACE_PATTERNS)
SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?\Z"
)
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class InputError(Exception):
    """An input could not be read or is not the expected shape."""


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


def namespace_of(identifier: str) -> str | None:
    for namespace, pattern in NAMESPACE_PATTERNS.items():
        if pattern.match(identifier):
            return namespace
    return None


def valid_timestamp(value) -> bool:
    if not isinstance(value, str) or not re.match(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z\Z", value):
        return False
    try:
        datetime.strptime(value, TIMESTAMP_FORMAT)
    except ValueError:
        return False
    return True


# ---------------------------------------------------------------------------
# Framework inventory
# ---------------------------------------------------------------------------

def iter_objects(data: dict, problems: list[str]):
    """Yield (namespace, where, object) for every identified object slot."""
    matrices = data.get("matrices")
    if not isinstance(matrices, dict):
        raise InputError("framework document has no 'matrices' object")
    for matrix_key, matrix_val in matrices.items():
        if not isinstance(matrix_val, dict):
            continue
        tactics = matrix_val.get("tactics")
        if not isinstance(tactics, list):
            problems.append(f"matrices.{matrix_key}.tactics is missing or is not an array")
            continue
        for t_index, tactic in enumerate(tactics):
            where = f"matrices.{matrix_key}.tactics[{t_index}]"
            if not isinstance(tactic, dict):
                problems.append(f"{where} is not an object")
                continue
            yield "tactics", where, tactic
            for kind in ("indicators", "countermeasures", "response_protocols"):
                children = tactic.get(kind)
                if children is None:
                    continue
                if not isinstance(children, list):
                    problems.append(f"{where}.{kind} is not an array")
                    continue
                for c_index, child in enumerate(children):
                    if not isinstance(child, dict):
                        problems.append(f"{where}.{kind}[{c_index}] is not an object")
                        continue
                    yield kind, f"{where}.{kind}[{c_index}]", child
    profiles = data.get("actor_profiles")
    if not isinstance(profiles, list):
        problems.append("actor_profiles is missing or is not an array")
        return
    for index, profile in enumerate(profiles):
        if not isinstance(profile, dict):
            problems.append(f"actor_profiles[{index}] is not an object")
            continue
        yield "actor_profiles", f"actor_profiles[{index}]", profile


def build_inventory(data) -> tuple[dict[str, list[str]], list[str]]:
    """Return (buckets, problems). buckets has the five namespaces + reserved."""
    if not isinstance(data, dict):
        raise InputError("framework document top level is not a JSON object")
    problems: list[str] = []
    buckets: dict[str, list[str]] = {namespace: [] for namespace in NAMESPACES}
    buckets["reserved"] = []
    first_seen: dict[str, str] = {}
    for namespace, where, obj in iter_objects(data, problems):
        identifier = obj.get("id")
        if not isinstance(identifier, str) or not identifier:
            problems.append(f"{where}: object has a missing or non-string id")
            continue
        if not NAMESPACE_PATTERNS[namespace].match(identifier):
            actual = namespace_of(identifier)
            if actual:
                problems.append(
                    f"{identifier}: found under {namespace} at {where}, but its form belongs to "
                    f"the {actual} namespace (an ID never changes namespace)"
                )
            else:
                problems.append(f"{identifier!r} at {where} does not match the {namespace} ID grammar")
            continue
        state = "reserved" if obj.get("lifecycle_state") == "reserved" else "live"
        if identifier in first_seen:
            if first_seen[identifier] != state:
                problems.append(f"{identifier}: appears both as a live object and as a reserved stub")
            else:
                problems.append(f"{identifier}: duplicate ID (appears more than once in the document)")
            continue
        first_seen[identifier] = state
        buckets["reserved" if state == "reserved" else namespace].append(identifier)
    if not buckets["tactics"] or not buckets["indicators"]:
        problems.append("the framework document has zero tactics or zero indicators")
    return {name: sorted(ids) for name, ids in buckets.items()}, problems


# ---------------------------------------------------------------------------
# Manifest validation and comparison
# ---------------------------------------------------------------------------

def manifest_problems(manifest, label: str) -> list[str]:
    """Structural and invariant checks on a manifest document."""
    if not isinstance(manifest, dict):
        return [f"{label}: top level is not a JSON object"]
    problems: list[str] = []
    unknown = sorted(set(manifest) - {"version", "generated", "ids", "removed"})
    if unknown:
        problems.append(f"{label}: unexpected top-level key(s) {unknown}")
    if not isinstance(manifest.get("version"), str) or not SEMVER.match(manifest["version"]):
        problems.append(f"{label}: 'version' {manifest.get('version')!r} is not a semantic version")
    if not valid_timestamp(manifest.get("generated")):
        problems.append(
            f"{label}: 'generated' {manifest.get('generated')!r} is not a real UTC timestamp "
            f"of the form YYYY-MM-DDTHH:MM:SSZ"
        )
    ids = manifest.get("ids")
    if not isinstance(ids, dict):
        return problems + [f"{label}: 'ids' is missing or is not an object"]
    unknown = sorted(set(ids) - set(NAMESPACES) - {"reserved"})
    if unknown:
        problems.append(f"{label}: unexpected key(s) under ids: {unknown}")

    owner: dict[str, str] = {}

    def claim(identifier: str, section: str) -> None:
        if identifier in owner:
            problems.append(
                f"{label}: {identifier} is listed in both {owner[identifier]} and {section}; "
                f"an ID belongs to exactly one section"
            )
        else:
            owner[identifier] = section

    for name in (*NAMESPACES, "reserved"):
        values = ids.get(name)
        if not isinstance(values, list):
            problems.append(f"{label}: ids.{name} is missing or is not an array")
            continue
        bad = [value for value in values if not isinstance(value, str)]
        if bad:
            problems.append(f"{label}: ids.{name} contains {len(bad)} non-string entr(ies)")
            continue
        if len(set(values)) != len(values):
            dupes = sorted({value for value in values if values.count(value) > 1})
            problems.append(f"{label}: ids.{name} lists {dupes[0]} more than once")
        if values != sorted(values):
            problems.append(f"{label}: ids.{name} is not sorted")
        for value in sorted(set(values)):
            if name == "reserved":
                if namespace_of(value) is None:
                    problems.append(f"{label}: ids.reserved entry {value!r} matches no ID grammar")
            elif not NAMESPACE_PATTERNS[name].match(value):
                problems.append(f"{label}: ids.{name} entry {value!r} does not match the {name} ID grammar")
            claim(value, f"ids.{name}")

    removed = manifest.get("removed", [])
    if not isinstance(removed, list):
        problems.append(f"{label}: 'removed' is not an array")
        removed = []
    removed_ids = []
    for index, entry in enumerate(removed):
        if not isinstance(entry, dict):
            problems.append(f"{label}: removed[{index}] is not an object")
            continue
        identifier = entry.get("id")
        if not isinstance(identifier, str) or namespace_of(identifier) is None:
            problems.append(f"{label}: removed[{index}].id {identifier!r} matches no ID grammar")
            continue
        removed_ids.append(identifier)
        if not isinstance(entry.get("reason"), str) or not entry["reason"].strip():
            problems.append(f"{label}: removed entry {identifier} has no reason")
        if not isinstance(entry.get("removed_in"), str) or not SEMVER.match(entry["removed_in"]):
            problems.append(f"{label}: removed entry {identifier} has no valid removed_in version")
        extra = sorted(set(entry) - {"id", "removed_in", "reason"})
        if extra:
            problems.append(f"{label}: removed entry {identifier} carries unexpected key(s) {extra}")
        claim(identifier, "removed")
    if removed_ids != sorted(removed_ids):
        problems.append(f"{label}: 'removed' is not sorted by id")
    return problems


def schema_problems(manifest, label: str) -> list[str]:
    """Validate against id-manifest.schema.json when jsonschema is available."""
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry
    except ImportError:
        return []
    if not MANIFEST_SCHEMA.exists():
        return []
    schema = load_json(MANIFEST_SCHEMA, "id-manifest.schema.json")
    try:
        validator = Draft202012Validator(
            schema, format_checker=Draft202012Validator.FORMAT_CHECKER, registry=Registry()
        )
        errors = list(validator.iter_errors(manifest))
    except Exception as exc:
        return [f"{label}: could not validate against id-manifest.schema.json ({exc.__class__.__name__})"]
    out = []
    for error in errors[:10]:
        location = "/".join(str(part) for part in error.absolute_path) or "(root)"
        out.append(f"{label}: schema error at {location}: {error.message[:120]}")
    if len(errors) > 10:
        out.append(f"{label}: ...and {len(errors) - 10} more schema error(s)")
    return out


def sections(manifest: dict) -> tuple[dict[str, str], set[str], set[str]]:
    """Return (live id -> namespace, reserved ids, removed ids)."""
    ids = manifest.get("ids") if isinstance(manifest.get("ids"), dict) else {}
    live = {
        identifier: namespace
        for namespace in NAMESPACES
        for identifier in (ids.get(namespace) or [])
        if isinstance(identifier, str)
    }
    reserved = {i for i in (ids.get("reserved") or []) if isinstance(i, str)}
    removed = {
        entry["id"] for entry in (manifest.get("removed") or [])
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
    }
    return live, reserved, removed


def compare_framework(buckets: dict[str, list[str]], version, manifest: dict) -> list[str]:
    """Problems where the manifest does not describe the framework exactly."""
    problems: list[str] = []
    live_m, reserved_m, removed_m = sections(manifest)
    live_f = {identifier: ns for ns in NAMESPACES for identifier in buckets[ns]}
    reserved_f = set(buckets["reserved"])

    if manifest.get("version") != version:
        problems.append(
            f"manifest version {manifest.get('version')!r} does not match the framework "
            f"version {version!r}; regenerate the manifest for this release"
        )
    for identifier in sorted(set(live_m) - set(live_f)):
        if identifier in reserved_f:
            problems.append(
                f"{identifier}: the manifest lists it as live, but the framework holds it as a "
                f"reserved stub; regenerate the manifest"
            )
        else:
            problems.append(
                f"{identifier}: present in the manifest but missing from the framework. An ID is "
                f"never dropped: restore it, or record it under `removed` with a reason"
            )
    for identifier in sorted(set(live_f) - set(live_m)):
        if identifier in reserved_m:
            problems.append(f"{identifier}: reserved in the manifest but live in the framework (a reserved ID is never reused)")
        elif identifier in removed_m:
            problems.append(f"{identifier}: recorded as removed in the manifest but live in the framework (a removed ID is never reused)")
        else:
            problems.append(f"{identifier}: live in the framework but not in the manifest; regenerate the manifest")
    for identifier in sorted(set(live_f) & set(live_m)):
        if live_f[identifier] != live_m[identifier]:
            problems.append(
                f"{identifier}: the manifest records it under {live_m[identifier]} but the framework "
                f"carries it under {live_f[identifier]} (an ID never changes namespace)"
            )
    for identifier in sorted(reserved_f - reserved_m):
        if identifier in removed_m:
            problems.append(f"{identifier}: recorded as removed in the manifest but present as a reserved stub in the framework")
        elif identifier not in live_m:
            problems.append(f"{identifier}: reserved stub in the framework but not in the manifest's reserved list; regenerate the manifest")
    return problems


def compare_manifests(old: dict, new: dict) -> list[str]:
    """Problems where `new` breaks the no-drop, no-reuse guarantee against `old`."""
    problems: list[str] = []
    live_old, reserved_old, removed_old = sections(old)
    live_new, reserved_new, removed_new = sections(new)
    old_label = f"{old.get('version')}"
    for identifier in sorted(set(live_old) | reserved_old | removed_old):
        in_new = identifier in live_new or identifier in reserved_new or identifier in removed_new
        if not in_new:
            problems.append(
                f"{identifier}: present in manifest {old_label} but absent from the new one. "
                f"An ID is never dropped: keep it, reserve it, or record it under `removed` with a reason"
            )
            continue
        if identifier in reserved_old and identifier in live_new:
            problems.append(f"{identifier}: reserved in manifest {old_label} but live now (a reserved ID is never reused)")
        if identifier in removed_old and identifier not in removed_new:
            problems.append(f"{identifier}: removed in manifest {old_label} but not recorded as removed now (a removed ID is never reused)")
        if identifier in live_old and identifier in live_new and live_old[identifier] != live_new[identifier]:
            problems.append(
                f"{identifier}: namespace changed from {live_old[identifier]} to {live_new[identifier]} "
                f"since manifest {old_label}"
            )
    return problems


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------

def fail(problems: list[str], headline: str) -> int:
    print(f"FAILED {NAME}: {headline} ({len(problems)} problem(s)):", file=sys.stderr)
    for problem in problems:
        print(f"  {problem}", file=sys.stderr)
    return 1


def cmd_check(framework_path: str, manifest_path: str, baseline_paths: list[str]) -> int:
    framework = load_json(framework_path, "framework document")
    manifest = load_json(manifest_path, "ID manifest")
    buckets, problems = build_inventory(framework)
    problems += manifest_problems(manifest, "manifest")
    if not problems:
        problems += schema_problems(manifest, "manifest")
    if not problems:
        problems += compare_framework(buckets, framework.get("version"), manifest)
    baseline_versions = []
    for baseline_path in baseline_paths:
        baseline = load_json(baseline_path, "baseline ID manifest")
        baseline_problems = manifest_problems(baseline, f"baseline manifest {baseline_path}")
        if baseline_problems:
            problems += baseline_problems
            continue
        baseline_versions.append(str(baseline.get("version")))
        if not problems:
            problems += compare_manifests(baseline, manifest)
            problems += compare_baseline_to_framework(baseline, buckets, manifest)
    if problems:
        return fail(problems, "the manifest, the framework, and the baseline(s) disagree"
                    if baseline_paths else "the manifest and the framework disagree")
    counts = ", ".join(f"{name} {len(buckets[name])}" for name in (*NAMESPACES, "reserved"))
    removed = len(manifest.get("removed") or [])
    against = (
        f"; no ID dropped, reused, or moved since baseline(s) {', '.join(baseline_versions)}"
        if baseline_versions else ""
    )
    print(
        f"PASSED {NAME}: manifest {manifest['version']} matches the framework exactly "
        f"({counts}; removed {removed}){against}."
    )
    return 0


def compare_baseline_to_framework(baseline: dict, buckets: dict[str, list[str]], manifest: dict) -> list[str]:
    """Check the baseline directly against the framework document.

    This does not rely on the current manifest's namespace lists, so an ID
    deleted from the framework together with a regenerated manifest is
    still caught. The only accepted reason for a baseline ID to be absent
    from the framework is a `removed` record with a reason.
    """
    problems: list[str] = []
    live_old, reserved_old, removed_old = sections(baseline)
    live_now = {identifier for namespace in NAMESPACES for identifier in buckets[namespace]}
    held_now = set(buckets["reserved"]) | sections(manifest)[1]
    removed_now = {
        entry["id"] for entry in (manifest.get("removed") or [])
        if isinstance(entry, dict) and isinstance(entry.get("id"), str)
        and isinstance(entry.get("reason"), str) and entry["reason"].strip()
    }
    label = baseline.get("version")
    for identifier in sorted(live_old):
        if identifier not in live_now and identifier not in held_now and identifier not in removed_now:
            problems.append(
                f"{identifier}: in baseline {label} but missing from the framework, and not listed "
                f"under `removed` with a reason"
            )
    for identifier in sorted(reserved_old | removed_old):
        if identifier in live_now:
            problems.append(
                f"{identifier}: reserved or removed in baseline {label} but live in the framework "
                f"(a held ID is never reused)"
            )
    return problems


def parse_removed(pairs: list[str], version: str) -> list[dict]:
    out = []
    for pair in pairs:
        identifier, sep, reason = pair.partition("=")
        identifier, reason = identifier.strip(), reason.strip()
        if not sep or not reason or namespace_of(identifier) is None:
            raise InputError(f"--removed expects ID=REASON with a valid ID and a non-empty reason, got {pair!r}")
        out.append({"id": identifier, "removed_in": version, "reason": reason})
    return out


def cmd_write(args) -> int:
    framework = load_json(args.framework, "framework document")
    buckets, problems = build_inventory(framework)
    version = framework.get("version")
    if not isinstance(version, str) or not SEMVER.match(version):
        problems.append(f"framework 'version' {version!r} is not a semantic version")
        version = "0.0.0"
    generated = args.generated or datetime.now(timezone.utc).strftime(TIMESTAMP_FORMAT)

    removed = {entry["id"]: entry for entry in parse_removed(args.removed or [], version)}
    reserved = set(buckets["reserved"])
    for identifier in args.reserve or []:
        if namespace_of(identifier) is None:
            raise InputError(f"--reserve expects a valid ID, got {identifier!r}")
        reserved.add(identifier)

    previous = None
    if args.previous:
        previous = load_json(args.previous, "previous ID manifest")
        previous_problems = manifest_problems(previous, "previous manifest")
        if previous_problems:
            return fail(previous_problems, "the previous manifest is not usable")
        _live_old, reserved_old, _removed_old = sections(previous)
        live_now = {identifier for ns in NAMESPACES for identifier in buckets[ns]}
        # Carry forward what only the manifest knows: hand-reserved IDs and
        # removal records. A carried ID that is live again is caught below.
        reserved |= {identifier for identifier in reserved_old if identifier not in live_now}
        for entry in previous.get("removed") or []:
            removed.setdefault(entry["id"], {key: entry[key] for key in ("id", "removed_in", "reason")})

    manifest = {
        "version": version,
        "generated": generated,
        "ids": {**{ns: buckets[ns] for ns in NAMESPACES}, "reserved": sorted(reserved - set(removed))},
    }
    if removed:
        manifest["removed"] = [removed[identifier] for identifier in sorted(removed)]

    if not problems:
        problems += manifest_problems(manifest, "new manifest")
    if not problems:
        problems += schema_problems(manifest, "new manifest")
    if not problems:
        problems += compare_framework(buckets, version, manifest)
    if previous is not None and not problems:
        problems += compare_manifests(previous, manifest)
    if problems:
        return fail(problems, f"nothing was written to {args.write}")

    out_path = Path(args.write)
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        handle = tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=str(out_path.parent), prefix=".id-manifest-", suffix=".tmp", delete=False
        )
        with handle:
            handle.write(json.dumps(manifest, indent=2) + "\n")
        os.replace(handle.name, out_path)
    except OSError as exc:
        raise InputError(f"could not write {out_path} ({exc.__class__.__name__})")

    counts = ", ".join(f"{name} {len(manifest['ids'][name])}" for name in (*NAMESPACES, "reserved"))
    print(f"PASSED {NAME}: wrote {out_path} for framework {version} ({counts}; removed {len(removed)}).")
    return 0


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="Write and check the per-release ID manifest.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", nargs=2, metavar=("FRAMEWORK", "MANIFEST"),
                      help="fail unless MANIFEST describes FRAMEWORK exactly")
    mode.add_argument("--write", metavar="OUT", help="build the manifest and write it to OUT")
    parser.add_argument("--baseline", metavar="OLDER_MANIFEST", action="append", default=[],
                        help="with --check: also compare against an older manifest (no drop, no reuse); "
                             "repeatable, for example the published baseline and the previous commit's manifest")
    parser.add_argument("--framework", default=str(REPO / "docs" / "data" / "framework.json"),
                        help="with --write: the framework document to inventory")
    parser.add_argument("--previous", metavar="MANIFEST",
                        help="with --write: carry forward removed and reserved records and compare against it")
    parser.add_argument("--generated", help="with --write: UTC timestamp YYYY-MM-DDTHH:MM:SSZ (default: now)")
    parser.add_argument("--removed", action="append", metavar="ID=REASON",
                        help="with --write: record an ID as removed in this release (repeatable)")
    parser.add_argument("--reserve", action="append", metavar="ID",
                        help="with --write: hold an ID that has no object in the document (repeatable)")
    args = parser.parse_args()

    try:
        if args.check:
            for flag in ("previous", "generated", "removed", "reserve"):
                if getattr(args, flag):
                    raise InputError(f"--{flag} is only valid with --write")
            return cmd_check(args.check[0], args.check[1], args.baseline)
        if args.baseline:
            raise InputError("--baseline is only valid with --check")
        if args.generated and not valid_timestamp(args.generated):
            raise InputError(f"--generated {args.generated!r} is not a real UTC timestamp of the form YYYY-MM-DDTHH:MM:SSZ")
        return cmd_write(args)
    except InputError as exc:
        print(f"error: {NAME}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
