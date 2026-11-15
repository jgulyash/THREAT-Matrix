#!/usr/bin/env python3
"""THREAT Matrix Detection Mesh reference-resolution lint.

Checks the four mesh relations in framework.json:

  indicator.correlates_with          -> indicator IDs (IND-...), symmetric
  countermeasure.compensates_for     -> countermeasure IDs (CM-...) only
  countermeasure.mitigates           -> edges {indicator, function}
  response_protocol.coordinates_with -> response protocol IDs (RP-...)

For every relation: each referent must be a string in the canonical ID
grammar for its namespace, must resolve to an object that exists in the
document, must not point at the object that carries it (self-reference),
and must not be listed twice. correlates_with must also be symmetric: if
A lists B, B lists A.

compensates_for is countermeasure-to-countermeasure only. An indicator ID
in compensates_for is an error here, exactly as it is in validate.py and
in framework.schema.json; indicator coverage lives in mitigates.

A document with zero indicators fails: an empty or truncated file must
never report success.

Exit codes: 0 all references resolve; 1 one or more broken references;
2 the input could not be read (missing file, invalid JSON, wrong
top-level type). Standard library only.

Usage:
  python3 scripts/lint/mesh-refs.py [docs/data/framework.json]
"""
from __future__ import annotations

import json
import re
import sys

NAME = "mesh-refs"

# \Z, not $: Python's $ also matches before a trailing newline.
IND_PATTERN = re.compile(r"^IND-[FOI]?[0-9]{4}-[0-9]{2}\Z")
CM_PATTERN = re.compile(r"^CM-[FOI]?[0-9]{4}-[0-9]{2}\Z")
RP_PATTERN = re.compile(r"^RP-[FOI]?[0-9]{4}-[0-9]{2}\Z")

MITIGATES_FUNCTIONS = ("prevent", "detect", "deny", "unreviewed")


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


def iter_tactics(framework: dict, errors: list[str]):
    """Yield (matrix_key, tactic) for every well-formed tactic.

    Shape problems are recorded as errors instead of raising, so one
    malformed value never hides the rest of the report.
    """
    matrices = framework.get("matrices")
    if not isinstance(matrices, dict):
        raise InputError("top-level 'matrices' is missing or is not an object")
    for matrix_key, matrix_val in matrices.items():
        if not isinstance(matrix_val, dict):
            # Non-matrix siblings such as matrices.boundary_rule (a string).
            continue
        tactics = matrix_val.get("tactics")
        if not isinstance(tactics, list):
            errors.append(f"[{matrix_key}] 'tactics' is missing or is not an array")
            continue
        for index, tactic in enumerate(tactics):
            if not isinstance(tactic, dict):
                errors.append(f"[{matrix_key}] tactics[{index}] is not an object")
                continue
            yield matrix_key, tactic


def iter_children(tactic: dict, key: str, where: str, errors: list[str]):
    """Yield every well-formed child object under tactic[key]."""
    children = tactic.get(key)
    if children is None:
        return
    if not isinstance(children, list):
        errors.append(f"[{where}] '{key}' is not an array")
        return
    for index, child in enumerate(children):
        if not isinstance(child, dict):
            errors.append(f"[{where}] {key}[{index}] is not an object")
            continue
        yield child


def obj_id(obj: dict) -> str | None:
    value = obj.get("id")
    return value if isinstance(value, str) else None


def collect(framework: dict):
    """Return (errors, indicators, countermeasures, response_protocols).

    Each of the three collections is a list of (where, object) pairs.
    """
    errors: list[str] = []
    inds: list[tuple[str, dict]] = []
    cms: list[tuple[str, dict]] = []
    rps: list[tuple[str, dict]] = []
    for matrix_key, tactic in iter_tactics(framework, errors):
        tactic_id = obj_id(tactic) or "?"
        where = f"{matrix_key}/{tactic_id}"
        for target, key in ((inds, "indicators"), (cms, "countermeasures"), (rps, "response_protocols")):
            for child in iter_children(tactic, key, where, errors):
                if obj_id(child) is None:
                    errors.append(f"[{where}] a {key} entry has a missing or non-string id")
                    continue
                target.append((where, child))
    return errors, inds, cms, rps


def ref_list(obj: dict, field: str, where: str, errors: list[str]) -> list:
    value = obj.get(field)
    if value is None:
        return []
    if not isinstance(value, list):
        errors.append(f"[{where}] {field} is not an array")
        return []
    return value


def check_id_refs(
    items: list[tuple[str, dict]],
    field: str,
    pattern: re.Pattern,
    known: set[str],
    grammar: str,
    kind: str,
    errors: list[str],
) -> None:
    """Check a relation whose referents are plain ID strings."""
    for where, obj in items:
        own = obj["id"]
        loc = f"{where}/{own}"
        seen: set[str] = set()
        for ref in ref_list(obj, field, loc, errors):
            if not isinstance(ref, str):
                errors.append(f"[{loc}] {field}: entry {ref!r} is not a string")
                continue
            if ref in seen:
                errors.append(f"[{loc}] {field}: '{ref}' is listed more than once")
                continue
            seen.add(ref)
            if not pattern.match(ref):
                errors.append(f"[{loc}] {field}: '{ref}' does not match the {grammar} format")
            elif ref == own:
                errors.append(f"[{loc}] {field}: '{ref}' is a self-reference")
            elif ref not in known:
                errors.append(f"[{loc}] {field}: '{ref}' does not resolve to any {kind} in the document")


def check_mitigates(cms: list[tuple[str, dict]], ind_ids: set[str], errors: list[str]) -> None:
    for where, cm in cms:
        loc = f"{where}/{cm['id']}"
        seen: set[str] = set()
        for edge in ref_list(cm, "mitigates", loc, errors):
            if not isinstance(edge, dict):
                errors.append(f"[{loc}] mitigates: entry {edge!r} is not an object")
                continue
            ref = edge.get("indicator")
            function = edge.get("function")
            if not isinstance(ref, str):
                errors.append(f"[{loc}] mitigates: edge has a missing or non-string 'indicator'")
                continue
            if not isinstance(function, str) or function not in MITIGATES_FUNCTIONS:
                errors.append(
                    f"[{loc}] mitigates: edge to '{ref}' has function {function!r}; "
                    f"expected one of {', '.join(MITIGATES_FUNCTIONS)}"
                )
            extra = sorted(str(key) for key in set(edge) - {"indicator", "function"})
            if extra:
                errors.append(f"[{loc}] mitigates: edge to '{ref}' carries unexpected key(s) {extra}")
            if ref in seen:
                errors.append(f"[{loc}] mitigates: '{ref}' is listed more than once")
                continue
            seen.add(ref)
            if not IND_PATTERN.match(ref):
                errors.append(f"[{loc}] mitigates: '{ref}' does not match the IND-[FOI]XXXX-XX format")
            elif ref not in ind_ids:
                errors.append(f"[{loc}] mitigates: '{ref}' does not resolve to any indicator in the document")


def check_symmetry(inds: list[tuple[str, dict]]) -> list[str]:
    """correlates_with is undirected: if A lists B then B must list A."""
    corr: dict[str, set[str]] = {}
    for _where, ind in inds:
        refs = ind.get("correlates_with")
        corr[ind["id"]] = {r for r in refs if isinstance(r, str)} if isinstance(refs, list) else set()
    errors: list[str] = []
    for a in sorted(corr):
        for b in sorted(corr[a]):
            if b != a and b in corr and a not in corr[b]:
                errors.append(f"asymmetric correlates_with: '{a}' lists '{b}', but '{b}' does not list '{a}'")
    return errors


def duplicate_ids(items: list[tuple[str, dict]], kind: str) -> list[str]:
    seen: set[str] = set()
    errors: list[str] = []
    for _where, obj in items:
        if obj["id"] in seen:
            errors.append(f"duplicate {kind} id '{obj['id']}': references to it are ambiguous")
        seen.add(obj["id"])
    return errors


def run(path: str) -> int:
    framework = load_json(path, "framework document")
    if not isinstance(framework, dict):
        raise InputError(f"top level of {path} is not a JSON object")

    errors, inds, cms, rps = collect(framework)
    ind_ids = {obj["id"] for _w, obj in inds}
    cm_ids = {obj["id"] for _w, obj in cms}
    rp_ids = {obj["id"] for _w, obj in rps}

    if not inds:
        errors.append(
            "the document contains zero indicators; an empty or truncated "
            "framework document cannot pass this lint"
        )

    errors += duplicate_ids(inds, "indicator")
    errors += duplicate_ids(cms, "countermeasure")
    errors += duplicate_ids(rps, "response protocol")
    check_id_refs(inds, "correlates_with", IND_PATTERN, ind_ids, "IND-[FOI]XXXX-XX", "indicator", errors)
    check_id_refs(
        cms, "compensates_for", CM_PATTERN, cm_ids,
        "CM-[FOI]XXXX-XX (countermeasure IDs only; indicator coverage belongs in mitigates)",
        "countermeasure", errors,
    )
    check_mitigates(cms, ind_ids, errors)
    check_id_refs(rps, "coordinates_with", RP_PATTERN, rp_ids, "RP-[FOI]XXXX-XX", "response protocol", errors)
    errors += check_symmetry(inds)

    if errors:
        print(f"FAILED {NAME}: {len(errors)} problem(s):", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        print(
            "Mesh references must be well-formed IDs that resolve inside the "
            "document, without self-reference or duplicates.",
            file=sys.stderr,
        )
        return 1

    edges = sum(len(obj.get("mitigates") or []) for _w, obj in cms)
    print(
        f"PASSED {NAME}: {len(inds)} indicators, {len(cms)} countermeasures, "
        f"{len(rps)} response protocols, {edges} mitigates edges; every mesh "
        f"reference resolves, none is a self-reference or duplicate, and "
        f"correlates_with is symmetric."
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
        print("usage: mesh-refs.py [path/to/framework.json]")
        return 0
    if len(args) > 1:
        print("usage: mesh-refs.py [path/to/framework.json]", file=sys.stderr)
        return 2
    path = args[0] if args else "docs/data/framework.json"
    try:
        return run(path)
    except InputError as exc:
        print(f"error: {NAME}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
