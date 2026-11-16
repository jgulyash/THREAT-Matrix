#!/usr/bin/env python3
"""THREAT Matrix validator: vocabulary, experimental overlay, scored records.

The vocabulary (docs/data/framework.json) carries no scores. The experimental
scoring overlay (docs/data/scoring-overlay.json) is a separate, opt-in,
non-normative document. This validator gates each of them and the join
between them.

Modes:

  python3 scripts/lint/validate.py docs/data/framework.json
      Vocabulary checks: structure, identifiers, references, lifecycle,
      bibliography, strings, and the JSON Schema when jsonschema is installed.

  python3 scripts/lint/validate.py docs/data/framework.json --overlay docs/data/scoring-overlay.json
      Vocabulary checks plus the overlay checks: the overlay scores exactly
      the indicators of the vocabulary, every weight is the composite of its
      four axes, every band follows from the stored weight and the floor, and
      every axis_confidence follows from the derivation rule. A missing or
      non-numeric axis, weight, or band is a failure, never a skip.

  python3 scripts/lint/validate.py docs/data/framework.json --overlay O --records DIR
      Adds the scored-record gate: every JSON file in DIR must be a scored
      case record whose indicator exists, whose type_band equals the
      overlay's authored band for that indicator, and whose
      conditioned_priority is not below it.

  python3 scripts/lint/validate.py docs/data/framework.json --coverage FILE
      Adds the coverage-document gate (docs/data/coverage.schema.json plus
      the rules a schema cannot express).

  python3 scripts/lint/validate.py docs/data/framework.json --fixtures scripts/lint/fixtures
      Runs the fixture harness (see scripts/lint/fixtures/README.md).

Options:
  --no-schema        skip the JSON Schema checks. Without this flag the
                     schemas are always run and a missing jsonschema package
                     is a failure. A run with --no-schema says so in its
                     summary and must not be used as a release gate.
  --require-schema   accepted for compatibility; schema validation is
                     required by default.
  --print-schema-pins  print the constraint digests of the schema files
                     (see SCHEMA_PINS) and exit.
  --schema-dir DIR   directory holding the *.schema.json files (default: the
                     directory of the framework file).

Every check has a stable id. On failure a check prints one line per offending
object:

  ✗ [Vnn] <object-id>: <message>

Exit code 0 when every check in scope is green, 1 otherwise. The validator
never prints PASSED for a document that lacks the top-level structure or
holds no tactics or indicators.

The JSON Schema checks need the jsonschema package (pip install jsonschema).
Everything else uses only the Python 3 standard library.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.util
import json
import math
import re
import shutil
import sys
import tempfile
from pathlib import Path

try:  # optional dependency
    import jsonschema  # type: ignore
except Exception:  # pragma: no cover - exercised only without the package
    jsonschema = None


# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

# Checks listed here are reported as warnings instead of failures while a
# known data fix is in flight. Map of check id to the reason. Keep empty
# unless a data owner has an open fix; every entry must be listed in the
# release notes.
PENDING_DATA_FIX: dict[str, str] = {}

MATRIX_KEYS = ("person", "facility", "organization", "infrastructure")
MATRIX_PREFIX = {
    "person": "TM",
    "facility": "TF",
    "infrastructure": "TI",
    "organization": "TO",
}
MATRIX_LETTER = {
    "person": "",
    "facility": "F",
    "infrastructure": "I",
    "organization": "O",
}
MATURITY_VALUES = {"core", "draft"}

PHASE_NAMES = {
    1: "Target Development",
    2: "Mobilization",
    3: "Execution",
    4: "Aftermath",
}
PHASE_KEYS = {
    1: "target_development",
    2: "mobilization",
    3: "execution",
    4: "aftermath",
}
PHASE_4_TRACKS = {"evasion", "attribution"}

BAND_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}
FLOOR_VALUES = {"high", "critical"}
AXES = (
    "impact_potential",
    "blast_radius_potential",
    "recoverability_inverse",
    "detectability",
)
CONFIDENCE_LEVELS = {"established", "inferred", "thin"}
# The stored weight is the composite rounded to two decimals, so the true
# rounding error is at most 0.005.
WEIGHT_TOLERANCE = 0.005
TACTIC_PRIORITY_VALUES = {"Urgent", "Immediate", "Priority", "Routine"}

EXPECTED_SCHEMA_VERSION = "3.0.0"
EVIDENCE_BASIS_VALUES = {
    "practice_led",
    "practice_and_literature",
    "literature_led",
    "literature_only",
}
EVIDENCE_BASIS_RENAMES = {
    "operational_primary": "practice_led",
    "hybrid": "practice_and_literature",
    "literature_primary": "literature_led",
}
LIFECYCLE_STATES = {"active", "deprecated", "superseded", "reserved"}
LIFECYCLE_DETAIL_FIELDS = (
    "deprecated_in",
    "superseded_by",
    "deprecation_reason",
    "reserved_reason",
)
RESERVED_ALLOWED_KEYS = {"id", "lifecycle_state", "reserved_reason"}
# Only this namespace may hold reserved objects in schema 3.0.0.
RESERVABLE_NAMESPACES = {"actor_profile"}

# Patterns mirror the JSON Schemas. They are always applied with
# re.fullmatch, so a trailing newline never matches. Digits are ASCII only.
SEMVER = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(-(0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(\.(0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?"
)
_SEQ = r"(0[1-9]|[1-9][0-9])"
TACTIC_ID = re.compile(rf"T[MFOI]0[1-4]{_SEQ}")
CHILD_ID = {
    "IND": re.compile(rf"IND-[FOI]?0[1-4]{_SEQ}-{_SEQ}"),
    "CM": re.compile(rf"CM-[FOI]?0[1-4]{_SEQ}-{_SEQ}"),
    "RP": re.compile(rf"RP-[FOI]?0[1-4]{_SEQ}-{_SEQ}"),
}
ACTOR_ID = re.compile(r"AP(00[1-9]|0[1-9][0-9]|[1-9][0-9]{2})")
ID_SHAPED = re.compile(r"(IND|CM|RP)-[FOI]?[0-9]{4}-[0-9]{2}")
BIB_KEY = re.compile(r"[A-Z][A-Z0-9]*(-[A-Z0-9]+)+")
ID_LETTER = re.compile(r"(?:IND|CM|RP)-([FOI]?)[0-9]{4}-[0-9]{2}")
HTTP_URL = re.compile(r"https?://[^\s]+")
DOI = re.compile(r"10\.[0-9]{4,9}/[^\s]+")
_DAY = r"(0[1-9]|[12][0-9]|3[01])"
_MONTH = r"(0[1-9]|1[0-2])"
BIB_DATE = re.compile(
    rf"[0-9]{{4}}(-{_MONTH}(-{_DAY})?)?"
    rf"|[0-9]{{4}}-[0-9]{{4}}"
    rf"|n\.d\.( \(accessed [0-9]{{4}}-{_MONTH}-{_DAY}\))?"
)
ISO_DATE = re.compile(rf"[0-9]{{4}}-{_MONTH}-{_DAY}")

INSTANCE_FACTORS = (
    "target_focus",
    "pathway_stage",
    "means_in_hand",
    "tempo_trajectory",
    "proximity_access",
    "source_credibility",
)
INSTANCE_FACTOR_VALUES = {
    "target_focus": {"diffuse", "narrowing", "specific_target", "unknown"},
    "pathway_stage": {
        "grievance", "ideation", "research_planning", "preparation",
        "breach_or_probing", "attack", "aftermath", "unknown",
    },
    "means_in_hand": {
        "unknown", "assessed_absent", "partial", "assessed_present",
        "confirmed_present",
    },
    "tempo_trajectory": {"accelerating", "steady", "stalling", "unknown"},
    "proximity_access": {
        "no_known_access", "seeking_access", "has_access",
        "at_or_near_target", "unknown",
    },
    "source_credibility": {"high", "moderate", "low", "unknown"},
}
RECORD_REQUIRED = ("indicator_id", "type_band", "instance", "conditioned_priority")
RECORD_OPTIONAL = (
    "framework_version",
    "overlay_version",
    "primary_objective_evidence_tier",
    "disposition",
)
EVIDENCE_TIERS = {"stated", "strongly_inferred", "weakly_inferred", "contested", "unknown"}
DISPOSITIONS = {
    "no_threat_identified", "transient_no_further_action", "active_monitoring",
    "heightened_monitoring", "referred_out", "disrupted_by_interdiction",
    "closed_benign", "closed_resolved",
}

MODALITY_VALUES = {"physical", "cyber", "cyber_physical", "human_social"}
CROSSING_MECHANISMS = {"digital", "electromagnetic", "physical_implant"}
MITIGATES_FUNCTIONS = {"prevent", "detect", "deny", "unreviewed"}

# Fields that carried scores before the split. None may appear in the
# vocabulary.
RETIRED_INDICATOR_FIELDS = (
    "escalation_axes",
    "escalation_weight",
    "severity_band",
    "severity_floor",
    "axis_confidence",
    "conditioned_priority",
    "type_weight",
    "type_band",
    "type_band_floor",
    "axes",
)
RETIRED_TOP_LEVEL = ("escalation_rubric", "instance_conditioning", "indicator_scores", "tactic_priorities", "rubric")

FRAMEWORK_REQUIRED_KEYS = (
    "name",
    "full_name",
    "version",
    "schema_version",
    "license",
    "matrices",
    "actor_profiles",
    "bibliography",
)
OVERLAY_REQUIRED_KEYS = (
    "name",
    "overlay_version",
    "applies_to_framework_version",
    "status",
    "normative",
    "validation_status",
    "scope",
    "not_a_risk_score",
    "notice",
    "rubric",
    "instance_conditioning",
    "tactic_priorities",
    "indicator_scores",
)
OVERLAY_CONSTANTS = {
    "status": "experimental",
    "validation_status": "unvalidated",
    "normative": False,
    "scope": "type_level",
    "not_a_risk_score": True,
}
SCORE_ENTRY_KEYS = {"axes", "type_weight", "type_band", "type_band_floor", "axis_confidence"}

# Check registry: id -> (title, scope). Scopes: framework, overlay, records,
# coverage. Ids V13, V14, V15, V18, and V20 kept their numbers when the
# scores moved out of the vocabulary; they now run in overlay and record
# scope.
CHECKS: dict[str, tuple[str, str]] = {
    "V01": ("duplicate tactic id", "framework"),
    "V02": ("duplicate indicator id", "framework"),
    "V03": ("duplicate countermeasure id", "framework"),
    "V04": ("duplicate response-protocol id", "framework"),
    "V05": ("duplicate JSON object key", "framework"),
    "V06": ("dangling correlates_with", "framework"),
    "V07": ("dangling or mistyped compensates_for", "framework"),
    "V08": ("dangling coordinates_with", "framework"),
    "V09": ("dangling source_refs bibliography key", "framework"),
    "V10": ("dangling cross-matrix correlates_with", "framework"),
    "V11": ("tactic id prefix vs matrix key", "framework"),
    "V12": ("child id letter and digits vs parent tactic", "framework"),
    "V16": ("phase range and phase_name", "framework"),
    "V17": ("phase_4_track presence and value", "framework"),
    "V19": ("tactic matrix field vs containing key", "framework"),
    "V21": ("modality facet presence, enum, and cross-field invariants", "framework"),
    "V22": ("conditioning_guidance shape, factor enum, and voice constraints", "framework"),
    "V23": ("mitigates edge shape and dangling indicator ref", "framework"),
    "V24": ("schema_version pin and SemVer content version", "framework"),
    "V25": ("evidence_basis uses the 3.0.0 values", "framework"),
    "V26": ("lifecycle contract", "framework"),
    "V27": ("bibliography key format on source_refs and bibliography keys", "framework"),
    "V28": ("document structure and non-empty content", "framework"),
    "V29": ("no scoring field in the vocabulary", "framework"),
    "V30": ("duplicate actor profile id", "framework"),
    "V31": ("actor_associations resolve to a non-reserved profile, no repeats", "framework"),
    "V32": ("tactic references resolve (related_tactics, v2_tactic_associations)", "framework"),
    "V33": ("self-reference or repeated entry in a relation", "framework"),
    "V34": ("tactic number encodes its phase", "framework"),
    "V35": ("phase_relevance contains the parent tactic's phase", "framework"),
    "V36": ("bibliography entries cited and well formed (url, doi, date)", "framework"),
    "V37": ("identifier grammar (exact match, no whitespace, no zero sequence)", "framework"),
    "V38": ("non-finite number (NaN or Infinity)", "framework"),
    "V39": ("JSON Schema: framework.schema.json", "framework"),
    "V40": ("empty string or leading or trailing whitespace", "framework"),
    "V50": ("actor category and label agree; matrix-scoped fields sit in their matrix", "framework"),
    "V13": ("type_band vs stored type_weight and floor", "overlay"),
    "V14": ("type_weight vs axes composite; axes and weight present and numeric", "overlay"),
    "V15": ("type_band_floor invalid or band below floor", "overlay"),
    "V20": ("axis_confidence complete, valid, and rule-derived", "overlay"),
    "V41": ("overlay document structure, constants, and version binding", "overlay"),
    "V42": ("indicator_scores keys equal the vocabulary's indicator ids", "overlay"),
    "V43": ("tactic_priorities has exactly one valid entry per tactic", "overlay"),
    "V44": ("axes to one decimal, weight to two decimals", "overlay"),
    "V45": ("rubric thresholds, base rates, and instance factors", "overlay"),
    "V46": ("JSON Schema: scoring-overlay.schema.json", "overlay"),
    "V51": ("floored indicators equal rubric.type_band_floor_rule.floored_indicators", "overlay"),
    "V18": ("conditioned_priority below the type band", "records"),
    "V47": ("record band fidelity: indicator exists and type_band is the authored band", "records"),
    "V48": ("scored case record shape", "records"),
    "V49": ("coverage document", "coverage"),
}
SCHEMA_CHECKS = {"V39", "V46"}

# Dash-like characters banned from conditioning_guidance.guidance: figure
# dash, en dash, em dash, horizontal bar, minus sign.
BANNED_DASHES = "\u2012\u2013\u2014\u2015\u2212"

CATEGORY_LABELS = {
    "lone_actor": "Lone Actor",
    "insider": "Insider",
    "criminal": "Criminal",
    "corporate_espionage": "Corporate Espionage",
    "ideological": "Ideological",
    "nation_state": "Nation-State",
    "customer_aggressor": "Customer/Client Aggressor",
}
# Sub-dimension fields that belong to one matrix only: (object kind, field) -> matrix.
MATRIX_SCOPED_FIELDS = {
    ("tactic", "target_identity_scope"): "person",
    ("indicator", "target_identity"): "person",
    ("countermeasure", "target_identity"): "person",
    ("indicator", "facility_target_scope"): "facility",
    ("indicator", "within_site_focus"): "facility",
}

# Constraint digests of the schema files. A digest covers every keyword of
# the schema except annotations (description, title, default, $comment), so
# loosening a required list, an enum, a pattern, or additionalProperties
# changes it and fails the schema check. After an intended schema change,
# run `validate.py --print-schema-pins` and paste the new values here in
# the same commit; the diff of this table is the review record.
SCHEMA_PINS = {
    "framework.schema.json": "32190a59bbbff6283a1ca8e8",
    "scoring-overlay.schema.json": "06250c754d6eabbb234d859f",
    "coverage.schema.json": "ff6e4c1ce267d6a1fc6cdb98",
}
_ANNOTATIONS = ("description", "title", "default", "$comment")
_NAME_MAPS = ("properties", "$defs", "patternProperties", "dependentSchemas", "dependentRequired")


def _constraints(node, names: bool = False):
    """Copy of a schema with annotation keywords removed. Inside a map of
    names (properties, $defs) the keys are names, not keywords."""
    if isinstance(node, dict):
        out = {}
        for key, value in node.items():
            if not names and key in _ANNOTATIONS:
                continue
            out[key] = _constraints(value, (not names) and key in _NAME_MAPS)
        return out
    if isinstance(node, list):
        return [_constraints(item) for item in node]
    return node


def schema_digest(schema) -> str:
    canonical = json.dumps(_constraints(schema), sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:24]
SCOPE_ORDER = ("framework", "overlay", "records", "coverage")


def check_ids(scopes) -> list[str]:
    return [cid for cid, (_t, scope) in CHECKS.items() if scope in scopes]


# ----------------------------------------------------------------------
# Small helpers
# ----------------------------------------------------------------------


class Results:
    """Failure lines per check id, plus skipped checks and notes."""

    def __init__(self) -> None:
        self.failures: dict[str, list[str]] = {cid: [] for cid in CHECKS}
        self.skipped: dict[str, str] = {}
        self.notes: list[str] = []

    def fail(self, check_id: str, object_id, message: str) -> None:
        self.failures[check_id].append(f"  ✗ [{check_id}] {show(object_id)}: {message}")

    def fired(self, scopes=SCOPE_ORDER) -> list[str]:
        return [cid for cid in check_ids(scopes) if self.failures[cid]]


def show(value) -> str:
    """Printable form of an id that may not be a string."""
    if isinstance(value, str):
        return value if value == value.strip() and value else repr(value)
    return repr(value)


def is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def as_list(value) -> list:
    return value if isinstance(value, list) else []


def as_dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def full(pattern: re.Pattern, value) -> bool:
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def semver_tuple(value: str) -> tuple[int, int, int]:
    core = re.split(r"[-+]", value, maxsplit=1)[0]
    major, minor, patch = core.split(".")
    return int(major), int(minor), int(patch)


def load_document(raw_text: str):
    """Parse JSON strictly. Return (data, duplicate_keys, nonfinite_tokens).

    json.loads keeps the last value of a repeated key and accepts the bare
    tokens NaN and Infinity, which are not JSON. Both are collected here so
    the caller can fail on them. A number such as 1e999 parses to infinity
    without a token and is caught later by the non-finite walk.
    """
    duplicates: list[str] = []
    nonfinite: list[str] = []

    def hook(pairs):
        seen: set[str] = set()
        for key, _value in pairs:
            if key in seen:
                duplicates.append(key)
            else:
                seen.add(key)
        return dict(pairs)

    def constant(token):
        nonfinite.append(token)
        return None

    data = json.loads(raw_text, object_pairs_hook=hook, parse_constant=constant)
    return data, duplicates, nonfinite


def walk_values(node, path=""):
    """Yield (path, value) for every scalar in a parsed document."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield from walk_values(value, f"{path}.{key}" if path else str(key))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk_values(value, f"{path}.{index}")
    else:
        yield path, node


def check_non_finite(results: Results, tokens, data, label: str) -> None:
    """V38: bare NaN or Infinity tokens, and numbers that overflow."""
    for token in tokens:
        results.fail("V38", label, f"bare token {token} is not JSON; browsers cannot parse the file")
    for path, value in walk_values(data):
        if isinstance(value, float) and not math.isfinite(value):
            results.fail("V38", f"{label}:{path}", "number is not finite")


def check_strings(results: Results, data, label: str) -> None:
    """V40: no empty string and no leading or trailing whitespace anywhere."""
    for path, value in walk_values(data):
        if not isinstance(value, str):
            continue
        if value == "":
            results.fail("V40", f"{label}:{path}", "string is empty")
        elif value != value.strip():
            results.fail("V40", f"{label}:{path}", "string has leading or trailing whitespace")


# ----------------------------------------------------------------------
# JSON Schema
# ----------------------------------------------------------------------


def schema_check(results: Results, check_id: str, schema_path: Path, instance,
                 require: bool, pointer: str | None = None, label: str = "") -> None:
    """Validate instance against a schema file (or one of its $defs)."""
    if jsonschema is None:
        results.fail(
            check_id,
            schema_path.name,
            "the jsonschema package is not importable; install it (pip install jsonschema). "
            "Schema validation is required unless --no-schema is passed explicitly",
        )
        return
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        results.fail(check_id, schema_path.name, f"schema could not be read ({exc.__class__.__name__})")
        return
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema.SchemaError
        results.fail(check_id, schema_path.name, f"schema is not valid Draft 2020-12 ({str(exc)[:160]})")
        return
    pinned = SCHEMA_PINS.get(schema_path.name)
    digest = schema_digest(schema)
    if pinned is not None and digest != pinned:
        results.fail(
            check_id,
            schema_path.name,
            f"schema constraint digest {digest} does not equal the pinned {pinned}: a required list, enum, "
            f"pattern, or other constraint changed. If the change is intended, update SCHEMA_PINS in "
            f"scripts/lint/validate.py (validate.py --print-schema-pins)",
        )
    if pointer:
        schema = {"$schema": schema.get("$schema"), "$ref": f"#/$defs/{pointer}", "$defs": schema.get("$defs", {})}
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    count = 0
    for error in validator.iter_errors(instance):
        count += 1
        if count > 25:
            continue
        where = "/".join(str(part) for part in error.absolute_path) or "(root)"
        results.fail(check_id, f"{label}{where}", " ".join(error.message.split())[:300])
    if count > 25:
        results.fail(check_id, label or schema_path.name, f"{count - 25} further schema error(s) not shown")


# ----------------------------------------------------------------------
# Vocabulary checks
# ----------------------------------------------------------------------


class Context:
    """What the overlay and record checks need from the vocabulary."""

    def __init__(self) -> None:
        self.version: str | None = None
        self.tactic_ids: set[str] = set()
        self.indicator_matrix: dict[str, str] = {}
        self.cm_ids: set[str] = set()
        self.usable = False


def iter_tactics(data: dict):
    """Yield (matrix_key, tactic) for every tactic object."""
    for matrix_key, matrix_val in as_dict(data.get("matrices")).items():
        if not isinstance(matrix_val, dict):
            continue
        for tactic in as_list(matrix_val.get("tactics")):
            if isinstance(tactic, dict):
                yield matrix_key, tactic


def lifecycle_state(obj: dict) -> str:
    state = obj.get("lifecycle_state", "active")
    return state if isinstance(state, str) else "<invalid>"


def id_letter(id_str) -> str | None:
    match = ID_LETTER.fullmatch(id_str) if isinstance(id_str, str) else None
    return None if match is None else match.group(1)


def check_structure(results: Results, data) -> bool:
    """V28. Return False when the document is too broken to check further."""
    if not isinstance(data, dict):
        results.fail("V28", "framework", "top level is not a JSON object")
        return False
    for key in FRAMEWORK_REQUIRED_KEYS:
        if key not in data:
            results.fail("V28", "framework", f"required top-level key '{key}' is missing")
    matrices = data.get("matrices")
    if not isinstance(matrices, dict):
        results.fail("V28", "matrices", "matrices is missing or not an object")
        return False
    for key in matrices:
        if key not in MATRIX_KEYS and key != "boundary_rule":
            results.fail("V28", f"matrices.{key}", "unknown matrix key")
    total_tactics = 0
    total_indicators = 0
    for key in MATRIX_KEYS:
        matrix = matrices.get(key)
        if not isinstance(matrix, dict):
            results.fail("V28", f"matrices.{key}", "matrix is missing or not an object")
            continue
        maturity = matrix.get("maturity")
        if not isinstance(maturity, str) or maturity not in MATURITY_VALUES:
            results.fail(
                "V28",
                f"matrices.{key}",
                f"maturity {show(maturity)} must be core or draft",
            )
        tactics = matrix.get("tactics")
        if not isinstance(tactics, list) or not tactics:
            results.fail("V28", f"matrices.{key}", "tactics is missing, not a list, or empty")
            continue
        for index, tactic in enumerate(tactics):
            if not isinstance(tactic, dict):
                results.fail("V28", f"matrices.{key}.tactics.{index}", "tactic is not an object")
                continue
            total_tactics += 1
            tid = tactic.get("id", f"matrices.{key}.tactics.{index}")
            for kind in ("indicators", "countermeasures", "response_protocols"):
                children = tactic.get(kind)
                if not isinstance(children, list):
                    results.fail("V28", tid, f"{kind} is missing or not a list")
                    continue
                for child_index, child in enumerate(children):
                    if not isinstance(child, dict):
                        results.fail("V28", tid, f"{kind}.{child_index} is not an object")
            indicators = [c for c in as_list(tactic.get("indicators")) if isinstance(c, dict)]
            if not indicators:
                results.fail("V28", tid, "tactic has no indicators")
            total_indicators += len(indicators)
    if total_tactics == 0:
        results.fail("V28", "framework", "document holds zero tactics")
    if total_indicators == 0:
        results.fail("V28", "framework", "document holds zero indicators")
    profiles = data.get("actor_profiles")
    if not isinstance(profiles, list) or not profiles:
        results.fail("V28", "actor_profiles", "actor_profiles is missing, not a list, or empty")
    else:
        for index, profile in enumerate(profiles):
            if not isinstance(profile, dict):
                results.fail("V28", f"actor_profiles.{index}", "actor profile is not an object")
    bibliography = data.get("bibliography")
    if not isinstance(bibliography, dict) or not bibliography:
        results.fail("V28", "bibliography", "bibliography is missing, not an object, or empty")
    return True


def check_framework(raw_text: str, schema_dir: Path | None, require_schema: bool,
                    run_schema: bool = True) -> tuple[Results, Context, object]:
    """Run every vocabulary check. Return (results, context, data)."""
    results = Results()
    ctx = Context()
    data, duplicates, nonfinite = load_document(raw_text)

    for key in duplicates:
        results.fail("V05", key, "JSON object key appears more than once")
    check_non_finite(results, nonfinite, data, "framework")

    if not check_structure(results, data):
        return results, ctx, data
    check_strings(results, data, "framework")
    if run_schema and schema_dir is not None:
        schema_check(results, "V39", schema_dir / "framework.schema.json", data, require_schema)
    elif not run_schema:
        results.skipped["V39"] = "schema checks switched off"

    fail = results.fail
    bibliography = as_dict(data.get("bibliography"))
    bib_keys = set(bibliography)
    cited: set[str] = set()

    # V24 schema_version pin and content version.
    declared = data.get("schema_version")
    if declared != EXPECTED_SCHEMA_VERSION:
        fail(
            "V24",
            "framework",
            f"schema_version is {show(declared)} but this validator targets "
            f"{EXPECTED_SCHEMA_VERSION}; migrate the document or run the validator "
            f"that matches its schema version",
        )
    version = data.get("version")
    if not full(SEMVER, version):
        fail("V24", "framework", f"version {show(version)} is not SemVer 2.0.0")
    else:
        ctx.version = version

    # V29 retired top-level scoring blocks.
    for key in RETIRED_TOP_LEVEL:
        if key in data:
            fail("V29", "framework", f"top-level '{key}' belongs in the scoring overlay, not the vocabulary")

    # Actor profiles: V30 duplicates, V37 grammar.
    profiles: dict[str, dict] = {}
    for profile in as_list(data.get("actor_profiles")):
        if not isinstance(profile, dict):
            continue
        pid = profile.get("id")
        if not full(ACTOR_ID, pid):
            fail("V37", pid, "actor profile id does not match AP followed by three digits (001 or higher)")
        category = profile.get("category")
        if isinstance(category, str) and category in CATEGORY_LABELS:
            if profile.get("category_label") != CATEGORY_LABELS[category]:
                fail(
                    "V50",
                    pid,
                    f"category_label {show(profile.get('category_label'))} does not match category "
                    f"'{category}' (expected '{CATEGORY_LABELS[category]}')",
                )
        if not isinstance(pid, str):
            continue
        if pid in profiles:
            fail("V30", pid, "actor profile id is not unique")
        else:
            profiles[pid] = profile

    # Id sets, first pass.
    tactics: dict[str, dict] = {}
    indicators: dict[str, dict] = {}
    countermeasures: dict[str, dict] = {}
    protocols: dict[str, dict] = {}
    for matrix_key, tactic in iter_tactics(data):
        tid = tactic.get("id")
        if isinstance(tid, str):
            tactics.setdefault(tid, tactic)
        for kind, bucket in (
            ("indicators", indicators),
            ("countermeasures", countermeasures),
            ("response_protocols", protocols),
        ):
            for child in as_list(tactic.get(kind)):
                if isinstance(child, dict) and isinstance(child.get("id"), str):
                    bucket.setdefault(child["id"], child)
                    if kind == "indicators":
                        ctx.indicator_matrix.setdefault(child["id"], matrix_key)
    ctx.tactic_ids = set(tactics)
    ctx.cm_ids = set(countermeasures)

    def source_refs(object_id, obj) -> None:
        refs = obj.get("source_refs")
        seen: set = set()
        for ref in as_list(refs):
            if not isinstance(ref, str):
                fail("V27", object_id, f"source_refs entry {show(ref)} is not a string")
                continue
            if not full(BIB_KEY, ref) or full(ID_SHAPED, ref):
                fail("V27", object_id, f"source_refs {show(ref)} does not match the bibliography key format")
            if ref not in bib_keys:
                fail("V09", object_id, f"source_refs {show(ref)} is not a bibliography key")
            else:
                cited.add(ref)
            if ref in seen:
                fail("V33", object_id, f"source_refs lists {show(ref)} more than once")
            seen.add(ref)

    def relation(check_dangling, object_id, obj, field, targets, pattern, what) -> None:
        """Shared checks for a list of id references held by an object."""
        seen: set = set()
        for ref in as_list(obj.get(field)):
            if not isinstance(ref, str):
                fail("V37", object_id, f"{field} entry {show(ref)} is not a string")
                continue
            if ref in seen:
                fail("V33", object_id, f"{field} lists {show(ref)} more than once")
            seen.add(ref)
            if ref == object_id:
                fail("V33", object_id, f"{field} refers to the object itself")
                continue
            if ref in targets:
                continue
            if not full(pattern, ref):
                fail("V37", object_id, f"{field} {show(ref)} is not a well-formed {what} id")
            check_dangling(ref)

    seen_tactic: set[str] = set()
    seen_ind: set[str] = set()
    seen_cm: set[str] = set()
    seen_rp: set[str] = set()

    for matrix_key, tactic in iter_tactics(data):
        tid = tactic.get("id", "<no-id>")
        state = lifecycle_state(tactic)

        if not full(TACTIC_ID, tid):
            fail("V37", tid, "tactic id does not match T, matrix letter, phase 01 to 04, sequence 01 or higher")
        if isinstance(tid, str):
            if tid in seen_tactic:
                fail("V01", tid, "tactic id is not unique across all matrices")
            seen_tactic.add(tid)

        # V11 tactic id prefix vs matrix key.
        expected_prefix = MATRIX_PREFIX.get(matrix_key)
        if expected_prefix and not str(tid).startswith(expected_prefix):
            fail(
                "V11",
                tid,
                f"id prefix does not match matrix '{matrix_key}' (expected prefix {expected_prefix})",
            )

        # V19 tactic matrix field vs containing key.
        if tactic.get("matrix") != matrix_key:
            fail(
                "V19",
                tid,
                f"matrix field {show(tactic.get('matrix'))} differs from containing matrix key '{matrix_key}'",
            )

        # V16 phase range and phase_name. A boolean is not a phase.
        phase = tactic.get("phase")
        if isinstance(phase, bool) or not isinstance(phase, int) or phase not in PHASE_NAMES:
            fail("V16", tid, f"phase {show(phase)} is not an integer from 1 to 4")
            phase = None
        else:
            expected_name = PHASE_NAMES[phase]
            if tactic.get("phase_name") != expected_name:
                fail(
                    "V16",
                    tid,
                    f"phase_name {show(tactic.get('phase_name'))} does not match phase {phase} "
                    f"(expected '{expected_name}')",
                )
            # V34 the id's phase digits.
            if isinstance(tid, str) and len(tid) >= 4 and tid[2:4] != f"0{phase}":
                fail(
                    "V34",
                    tid,
                    f"id encodes phase '{tid[2:4]}' but the tactic's phase is {phase}",
                )

        # V17 phase_4_track presence and value.
        track = tactic.get("phase_4_track")
        if phase == 4:
            if not isinstance(track, str) or track not in PHASE_4_TRACKS:
                fail(
                    "V17",
                    tid,
                    f"phase-4 tactic has missing or invalid phase_4_track {show(track)} "
                    f"(expected evasion or attribution)",
                )
        elif phase in (1, 2, 3) and track is not None:
            fail(
                "V17",
                tid,
                f"phase_4_track {show(track)} is present on a phase-{phase} tactic (forbidden below phase 4)",
            )

        # V25 evidence_basis.
        basis = tactic.get("evidence_basis")
        if not isinstance(basis, str) or basis not in EVIDENCE_BASIS_VALUES:
            hint = EVIDENCE_BASIS_RENAMES.get(basis) if isinstance(basis, str) else None
            suffix = f" (retired 2.x value; rename to '{hint}')" if hint else ""
            fail("V25", tid, f"evidence_basis {show(basis)} is not valid{suffix}")

        # V29 retired tactic-level scoring field.
        if "escalation_priority" in as_dict(tactic.get("assessment_guidance")):
            fail("V29", tid, "assessment_guidance.escalation_priority belongs in the overlay's tactic_priorities")

        def scoped_fields(kind, object_id, obj, _matrix=matrix_key):
            # V50 a matrix-scoped sub-dimension field outside its matrix.
            for (scoped_kind, field), home in MATRIX_SCOPED_FIELDS.items():
                if scoped_kind == kind and field in obj and _matrix != home:
                    fail("V50", object_id, f"'{field}' is a {home}-matrix field and may not appear in the {_matrix} matrix")

        scoped_fields("tactic", tid, tactic)
        source_refs(tid, tactic)

        # V32 related_tactics.
        relation(
            lambda ref, _tid=tid: fail("V32", _tid, f"related_tactics {show(ref)} resolves to no tactic"),
            tid, tactic, "related_tactics", ctx.tactic_ids, TACTIC_ID, "tactic",
        )

        # V31 actor_associations.
        seen_assoc: set = set()
        for assoc in as_list(tactic.get("actor_associations")):
            if not isinstance(assoc, dict):
                fail("V31", tid, "actor_associations entry is not an object")
                continue
            actor_id = assoc.get("actor_id")
            if not full(ACTOR_ID, actor_id):
                fail("V37", tid, f"actor_associations actor_id {show(actor_id)} is not a well-formed actor profile id")
            target = profiles.get(actor_id) if isinstance(actor_id, str) else None
            if target is None:
                fail("V31", tid, f"actor_associations actor_id {show(actor_id)} resolves to no actor profile")
            elif lifecycle_state(target) == "reserved":
                fail("V31", tid, f"actor_associations actor_id {show(actor_id)} is a reserved profile")
            pair = (show(actor_id), show(assoc.get("employment_status")))
            if pair in seen_assoc:
                fail("V31", tid, f"actor_associations repeats actor_id {show(actor_id)} with the same employment_status")
            seen_assoc.add(pair)

        letter = MATRIX_LETTER.get(matrix_key, "")
        digits = str(tid)[2:]
        phase_key = PHASE_KEYS.get(phase)

        def child_common(kind, prefix, child, seen, dup_check):
            cid = child.get("id", "<no-id>")
            if not full(CHILD_ID[prefix], cid):
                fail("V37", cid, f"{kind} id does not match the {prefix} id grammar")
            if isinstance(cid, str):
                if cid in seen:
                    fail(dup_check, cid, f"{kind} id is not unique")
                seen.add(cid)
            # V12 child id must embed the matrix letter and parent digits.
            expected = re.compile(rf"{prefix}-{re.escape(letter)}{re.escape(digits)}-[0-9]{{2}}")
            if not full(expected, cid):
                fail(
                    "V12",
                    cid,
                    f"id does not embed parent tactic {show(tid)} (expected {prefix}-{letter}{digits}-NN)",
                )
            source_refs(cid, child)
            return cid

        def phase_relevance(cid, child):
            # V35 the parent tactic's phase must be listed.
            relevance = child.get("phase_relevance")
            if phase_key and isinstance(relevance, list) and phase_key not in relevance:
                fail(
                    "V35",
                    cid,
                    f"phase_relevance {relevance} omits the parent tactic's phase '{phase_key}'",
                )

        for ind in as_list(tactic.get("indicators")):
            if not isinstance(ind, dict):
                continue
            iid = child_common("indicator", "IND", ind, seen_ind, "V02")
            phase_relevance(iid, ind)
            scoped_fields("indicator", iid, ind)
            for field in RETIRED_INDICATOR_FIELDS:
                if field in ind:
                    fail("V29", iid, f"'{field}' is a scoring field; scores live in the overlay, not the vocabulary")
            source_letter = id_letter(iid)

            def dangling_correlate(ref, _iid=iid, _letter=source_letter):
                ref_letter = id_letter(ref)
                if ref_letter is not None and ref_letter != _letter:
                    fail("V10", _iid, f"cross-matrix correlates_with {show(ref)} resolves to no indicator")
                else:
                    fail("V06", _iid, f"correlates_with {show(ref)} resolves to no indicator")

            relation(dangling_correlate, iid, ind, "correlates_with", indicators, CHILD_ID["IND"], "indicator")
            _check_modality(fail, iid, ind)
            _check_conditioning_guidance(fail, iid, ind)

        for cm in as_list(tactic.get("countermeasures")):
            if not isinstance(cm, dict):
                continue
            cid = child_common("countermeasure", "CM", cm, seen_cm, "V03")
            phase_relevance(cid, cm)
            scoped_fields("countermeasure", cid, cm)

            def dangling_comp(ref, _cid=cid):
                if ref.startswith("IND-"):
                    fail(
                        "V07",
                        _cid,
                        f"compensates_for {show(ref)} targets an indicator; indicator coverage belongs in mitigates",
                    )
                else:
                    fail("V07", _cid, f"compensates_for {show(ref)} resolves to no countermeasure")

            relation(dangling_comp, cid, cm, "compensates_for", countermeasures, CHILD_ID["CM"], "countermeasure")
            seen_edges: set = set()
            for edge in as_list(cm.get("mitigates")):
                if not isinstance(edge, dict):
                    fail("V23", cid, "mitigates entry is not an edge object")
                    continue
                ref = edge.get("indicator")
                func = edge.get("function")
                if set(edge) - {"indicator", "function"}:
                    fail("V23", cid, f"mitigates edge carries unknown keys {sorted(set(edge) - {'indicator', 'function'})}")
                if not isinstance(func, str) or func not in MITIGATES_FUNCTIONS:
                    fail("V23", cid, f"mitigates edge {show(ref)} has invalid function {show(func)}")
                if not isinstance(ref, str) or ref not in indicators:
                    fail("V23", cid, f"mitigates {show(ref)} resolves to no indicator")
                if isinstance(ref, str):
                    if ref in seen_edges:
                        fail("V33", cid, f"mitigates names indicator {show(ref)} more than once")
                    seen_edges.add(ref)

        for rp in as_list(tactic.get("response_protocols")):
            if not isinstance(rp, dict):
                continue
            rid = child_common("response protocol", "RP", rp, seen_rp, "V04")
            relation(
                lambda ref, _rid=rid: fail("V08", _rid, f"coordinates_with {show(ref)} resolves to no response_protocol"),
                rid, rp, "coordinates_with", protocols, CHILD_ID["RP"], "response-protocol",
            )

    # V32 profile-to-tactic associations.
    for pid, profile in profiles.items():
        seen_v2: set = set()
        for assoc in as_list(profile.get("v2_tactic_associations")):
            ref = assoc.get("tactic_id") if isinstance(assoc, dict) else None
            if not isinstance(ref, str) or ref not in ctx.tactic_ids:
                fail("V32", pid, f"v2_tactic_associations tactic_id {show(ref)} resolves to no tactic")
            if ref in seen_v2:
                fail("V33", pid, f"v2_tactic_associations names tactic {show(ref)} more than once")
            seen_v2.add(ref if isinstance(ref, str) else repr(ref))

    # V26 lifecycle contract.
    namespaces = {
        "tactic": (tactics, TACTIC_ID),
        "indicator": (indicators, CHILD_ID["IND"]),
        "countermeasure": (countermeasures, CHILD_ID["CM"]),
        "response_protocol": (protocols, CHILD_ID["RP"]),
        "actor_profile": (profiles, ACTOR_ID),
    }
    for ns, (members, pattern) in namespaces.items():
        for oid, obj in members.items():
            _check_lifecycle(fail, ns, oid, obj, members, pattern, ctx.version)

    # V27 bibliography key format; V36 entries cited and well formed.
    for key, entry in bibliography.items():
        if not full(BIB_KEY, key) or full(ID_SHAPED, key):
            fail("V27", key, "bibliography key does not match the key format")
        if key not in cited:
            fail("V36", key, "bibliography entry is cited by no source_refs")
        if not isinstance(entry, dict):
            fail("V36", key, "bibliography entry is not an object")
            continue
        url = entry.get("url")
        if url is not None and not full(HTTP_URL, url):
            fail("V36", key, f"url {show(url)} is not null or an http(s) URL without whitespace")
        doi = entry.get("doi")
        if doi is not None and not full(DOI, doi):
            fail("V36", key, f"doi {show(doi)} is not null or a bare DOI (10.NNNN/suffix)")
        date = entry.get("date")
        if not full(BIB_DATE, date):
            fail("V36", key, f"date {show(date)} is not YYYY, YYYY-MM, YYYY-MM-DD, YYYY-YYYY, or n.d.")
        elif re.fullmatch(r"[0-9]{4}-[0-9]{4}", date) and int(date[:4]) >= int(date[5:]):
            fail("V36", key, f"date {show(date)} is a year range that does not run forward")
        elif ISO_DATE.fullmatch(date):
            try:
                datetime.date.fromisoformat(date)
            except ValueError:
                fail("V36", key, f"date {show(date)} is not a real calendar date")

    ctx.usable = True
    return results, ctx, data


def _check_lifecycle(fail, ns, oid, obj, members, pattern, doc_version) -> None:
    """V26. The lifecycle contract of the build spec:

    active (or absent): no lifecycle detail field.
    deprecated: deprecated_in and deprecation_reason; no superseded_by.
    superseded: those plus superseded_by, which resolves to an ACTIVE object
        of the same namespace, is not the object itself, and closes no cycle.
    reserved: actor profiles only, carrying only id, lifecycle_state, and a
        non-empty reserved_reason.
    """
    raw_state = obj.get("lifecycle_state", "active")
    if not isinstance(raw_state, str) or raw_state not in LIFECYCLE_STATES:
        fail("V26", oid, f"lifecycle_state {show(raw_state)} is not valid")
        return
    state = raw_state

    if state == "reserved":
        if ns not in RESERVABLE_NAMESPACES:
            fail(
                "V26",
                oid,
                f"a {ns.replace('_', ' ')} may not be reserved; only actor profiles may, and "
                f"other reserved ids are recorded in the id manifest",
            )
            return
        extra = sorted(set(obj) - RESERVED_ALLOWED_KEYS)
        if extra:
            fail("V26", oid, f"reserved object carries content beyond id, lifecycle_state, reserved_reason: {extra}")
        reason = obj.get("reserved_reason")
        if not isinstance(reason, str) or not reason.strip():
            fail("V26", oid, "reserved state requires a non-empty reserved_reason")
        return

    if "reserved_reason" in obj:
        fail("V26", oid, f"reserved_reason is only legal on reserved state (state is '{state}')")

    if state == "active":
        for field in ("deprecated_in", "superseded_by", "deprecation_reason"):
            if field in obj:
                fail("V26", oid, f"active object carries lifecycle field '{field}'")
        return

    # deprecated or superseded
    deprecated_in = obj.get("deprecated_in")
    if deprecated_in is None:
        fail("V26", oid, f"{state} state requires deprecated_in")
    elif not full(SEMVER, deprecated_in):
        fail("V26", oid, f"deprecated_in {show(deprecated_in)} is not SemVer")
    elif doc_version and semver_tuple(deprecated_in) > semver_tuple(doc_version):
        fail(
            "V26",
            oid,
            f"deprecated_in {deprecated_in} is later than the document version {doc_version}",
        )
    reason = obj.get("deprecation_reason")
    if not isinstance(reason, str) or not reason.strip():
        fail("V26", oid, f"{state} state requires a non-empty deprecation_reason")

    successor = obj.get("superseded_by")
    if state == "deprecated":
        if successor is not None:
            fail("V26", oid, "superseded_by is only legal on superseded state (state is 'deprecated')")
        return

    if successor is None:
        fail("V26", oid, "superseded state requires superseded_by")
    elif not isinstance(successor, str) or not full(pattern, successor):
        fail("V26", oid, f"superseded_by {show(successor)} is not a well-formed {ns} id")
    elif successor == oid:
        fail("V26", oid, "superseded_by points at itself")
    elif successor not in members:
        fail(
            "V26",
            oid,
            f"superseded_by {show(successor)} resolves to no {ns} (same-namespace replacement required)",
        )
    else:
        # Walk the chain to report a cycle by name, then require an active target.
        seen = {oid}
        cursor = successor
        while isinstance(cursor, str) and cursor in members and cursor not in seen:
            seen.add(cursor)
            cursor = members[cursor].get("superseded_by")
        if isinstance(cursor, str) and cursor in seen:
            fail("V26", oid, f"superseded_by chain forms a cycle through {show(cursor)}")
        target_state = lifecycle_state(members[successor])
        if target_state != "active":
            fail(
                "V26",
                oid,
                f"superseded_by {show(successor)} is {target_state}; the replacement must be active",
            )


def _check_conditioning_guidance(fail, ind_id, ind) -> None:
    """V22 conditioning_guidance contract. Optional field; when present it
    carries exactly probe_factors (1 to 6 unique instance-factor names) and
    guidance (a non-empty string of at most 420 characters with no em or en
    dash)."""
    cg = ind.get("conditioning_guidance")
    if cg is None:
        return
    if not isinstance(cg, dict):
        fail("V22", ind_id, "conditioning_guidance must be an object")
        return
    if set(cg) != {"probe_factors", "guidance"}:
        fail("V22", ind_id, "conditioning_guidance requires exactly probe_factors and guidance")
        return
    pf = cg["probe_factors"]
    if not isinstance(pf, list) or not 1 <= len(pf) <= 6:
        fail("V22", ind_id, "probe_factors must be a list of 1 to 6 names")
    else:
        for name in pf:
            if not isinstance(name, str) or name not in INSTANCE_FACTORS:
                fail("V22", ind_id, f"probe_factors {show(name)} is not an instance factor")
        if len(pf) != len(set(map(str, pf))):
            fail("V22", ind_id, "probe_factors entries must be unique")
    guidance = cg["guidance"]
    if not isinstance(guidance, str) or not guidance.strip():
        fail("V22", ind_id, "guidance must be a non-empty string")
    else:
        if len(guidance) > 420:
            fail("V22", ind_id, f"guidance is {len(guidance)} chars; max is 420")
        if any(ch in guidance for ch in BANNED_DASHES):
            fail("V22", ind_id, "guidance contains an em or en dash or another dash-like character")


def _check_modality(fail, ind_id, ind) -> None:
    """V21 modality facet contract: modality (enum) and human_social (bool)
    are required; a human_social modality forces human_social true; and
    crossing_mechanism appears exactly when modality is cyber_physical."""
    modality = ind.get("modality")
    human_social = ind.get("human_social")
    mechanism = ind.get("crossing_mechanism")
    if modality is None:
        fail("V21", ind_id, "modality is missing")
    elif not isinstance(modality, str) or modality not in MODALITY_VALUES:
        fail("V21", ind_id, f"modality {show(modality)} is not a valid value")
    if not isinstance(human_social, bool):
        fail("V21", ind_id, "human_social must be a boolean and present")
    if modality == "human_social" and human_social is not True:
        fail("V21", ind_id, "modality human_social requires human_social true")
    if modality == "cyber_physical":
        if not isinstance(mechanism, str) or mechanism not in CROSSING_MECHANISMS:
            fail("V21", ind_id, "cyber_physical modality requires a valid crossing_mechanism")
    elif mechanism is not None:
        fail("V21", ind_id, "crossing_mechanism is only legal on cyber_physical modality")


# ----------------------------------------------------------------------
# Overlay checks
# ----------------------------------------------------------------------

# Internal copy of the axis_confidence derivation rule. The executable rule
# lives in scripts/analysis/derive-axis-confidence.py; when that file is
# importable and still exposes derive and BLAST_ANCHORS it is used, and this
# copy is the fallback.
BLAST_ANCHORS_FALLBACK = {
    "person": {2.0, 2.5, 3.0, 4.0, 7.0, 8.0, 9.0},
    "facility": {2.0, 2.5, 3.0, 4.0, 7.0, 8.0, 9.0},
    "organization": {2.0, 3.5, 4.0, 5.5, 6.5, 7.5, 8.5},
    "infrastructure": {2.5, 3.5, 4.0, 5.5, 6.0, 7.0, 7.5, 8.0, 9.0},
}


def _derive_fallback(matrix_key: str, axes: dict) -> dict:
    det = axes["detectability"]
    if det <= 2.0:
        det_conf = "thin"
    elif det >= 6.0:
        det_conf = "established"
    else:
        det_conf = "inferred"
    blast = axes["blast_radius_potential"]
    anchors = BLAST_ANCHORS_FALLBACK[matrix_key]
    blast_conf = "established" if any(abs(blast - a) <= 0.5 for a in anchors) else "inferred"
    return {
        "impact_potential": "inferred",
        "blast_radius_potential": blast_conf,
        "recoverability_inverse": "inferred",
        "detectability": det_conf,
    }


def load_confidence_rule():
    """Return (derive, source_label)."""
    path = Path(__file__).resolve().parents[1] / "analysis" / "derive-axis-confidence.py"
    try:
        spec = importlib.util.spec_from_file_location("_tm_axis_confidence_rule", path)
        module = importlib.util.module_from_spec(spec)
        dont_write = sys.dont_write_bytecode
        sys.dont_write_bytecode = True
        try:
            spec.loader.exec_module(module)
        finally:
            sys.dont_write_bytecode = dont_write
        derive = getattr(module, "derive")
        anchors = getattr(module, "BLAST_ANCHORS")
        if not callable(derive) or not isinstance(anchors, dict) or set(anchors) != set(MATRIX_KEYS):
            raise AttributeError("unexpected shape")
        probe = derive("person", {axis: 5.0 for axis in AXES})
        if set(probe) != set(AXES):
            raise AttributeError("unexpected result shape")
        return derive, "scripts/analysis/derive-axis-confidence.py"
    except Exception:
        return _derive_fallback, "internal copy (scripts/analysis/derive-axis-confidence.py not usable)"


def band_for_weight(weight: float, thresholds: dict) -> str:
    if weight >= thresholds["critical"]:
        return "critical"
    if weight >= thresholds["high"]:
        return "high"
    if weight >= thresholds["medium"]:
        return "medium"
    return "low"


def check_overlay(results: Results, raw_text: str, ctx: Context, schema_dir: Path | None,
                  require_schema: bool, run_schema: bool = True):
    """Run every overlay check against the vocabulary context. Return the
    parsed overlay (or None when it is not an object)."""
    fail = results.fail
    overlay, duplicates, nonfinite = load_document(raw_text)
    for key in duplicates:
        fail("V41", key, "JSON object key appears more than once in the overlay")
    check_non_finite(results, nonfinite, overlay, "overlay")
    if not isinstance(overlay, dict):
        fail("V41", "overlay", "top level is not a JSON object")
        return None
    check_strings(results, overlay, "overlay")
    if run_schema and schema_dir is not None:
        schema_check(results, "V46", schema_dir / "scoring-overlay.schema.json", overlay, require_schema)
    elif not run_schema:
        results.skipped["V46"] = "schema checks switched off"

    # V41 structure, constants, version binding.
    for key in OVERLAY_REQUIRED_KEYS:
        if key not in overlay:
            fail("V41", "overlay", f"required top-level key '{key}' is missing")
    for key in overlay:
        if key not in OVERLAY_REQUIRED_KEYS:
            fail("V41", "overlay", f"unknown top-level key '{key}'")
    for key, expected in OVERLAY_CONSTANTS.items():
        if key in overlay and (overlay[key] != expected or type(overlay[key]) is not type(expected)):
            fail("V41", "overlay", f"{key} must be {json.dumps(expected)} (found {show(overlay[key])})")
    if "overlay_version" in overlay and not full(SEMVER, overlay["overlay_version"]):
        fail("V41", "overlay", f"overlay_version {show(overlay['overlay_version'])} is not SemVer")
    applies = overlay.get("applies_to_framework_version")
    if applies is not None and applies != ctx.version:
        fail(
            "V41",
            "overlay",
            f"applies_to_framework_version {show(applies)} does not equal the framework version {show(ctx.version)}",
        )

    # V45 rubric numerics and instance factors.
    rubric = as_dict(overlay.get("rubric"))
    thresholds = rubric.get("type_band_thresholds")
    thresholds_ok = False
    if not isinstance(thresholds, dict) or set(thresholds) != set(BAND_RANK):
        fail("V45", "rubric.type_band_thresholds", "must carry exactly low, medium, high, critical")
    elif not all(is_number(thresholds[band]) for band in BAND_RANK):
        fail("V45", "rubric.type_band_thresholds", "every threshold must be a finite number")
    else:
        ordered = [thresholds[band] for band in ("low", "medium", "high", "critical")]
        if ordered[0] != 0:
            fail("V45", "rubric.type_band_thresholds", f"low must be 0 (found {ordered[0]})")
        elif not all(a < b for a, b in zip(ordered, ordered[1:])):
            fail("V45", "rubric.type_band_thresholds", f"thresholds must be strictly increasing (found {ordered})")
        elif ordered[-1] > 10:
            fail("V45", "rubric.type_band_thresholds", f"critical must not exceed 10 (found {ordered[-1]})")
        else:
            thresholds_ok = True
    rates = as_dict(as_dict(rubric.get("blast_radius_guidance")).get("method_collateral_base_rates"))
    for key, value in rates.items():
        if key == "note":
            continue
        if not is_number(value) or not 0 <= value <= 10:
            fail("V45", f"rubric.blast_radius_guidance.method_collateral_base_rates.{key}",
                 f"base rate {show(value)} is not a number from 0 to 10")
    if "rubric_version" in rubric and not full(SEMVER, rubric["rubric_version"]):
        fail("V45", "rubric.rubric_version", f"{show(rubric['rubric_version'])} is not SemVer")
    factors = as_dict(overlay.get("instance_conditioning")).get("factors")
    if not isinstance(factors, list) or sorted(map(str, factors)) != sorted(INSTANCE_FACTORS):
        fail("V45", "instance_conditioning.factors", f"must list exactly the six instance factors (found {show(factors)})")

    # V43 tactic priorities.
    priorities = overlay.get("tactic_priorities")
    if not isinstance(priorities, dict) or not priorities:
        fail("V43", "tactic_priorities", "missing, not an object, or empty")
    else:
        for tid, value in priorities.items():
            if tid not in ctx.tactic_ids:
                fail("V43", tid, "tactic_priorities key is not a tactic id of the vocabulary")
            if not isinstance(value, str) or value not in TACTIC_PRIORITY_VALUES:
                fail("V43", tid, f"priority {show(value)} is not Urgent, Immediate, Priority, or Routine")
        for tid in sorted(ctx.tactic_ids - set(priorities)):
            fail("V43", tid, "tactic of the vocabulary has no tactic_priorities entry")

    # V42 key set.
    scores = overlay.get("indicator_scores")
    if not isinstance(scores, dict) or not scores:
        fail("V42", "indicator_scores", "missing, not an object, or empty")
        return overlay
    expected_ids = set(ctx.indicator_matrix)
    missing = sorted(expected_ids - set(scores))
    extra = sorted(set(scores) - expected_ids)
    for iid in missing[:20]:
        fail("V42", iid, "indicator of the vocabulary has no score entry")
    if len(missing) > 20:
        fail("V42", "indicator_scores", f"{len(missing) - 20} further missing indicator(s) not shown")
    for iid in extra[:20]:
        fail("V42", iid, "score entry names no indicator of the vocabulary")
    if len(extra) > 20:
        fail("V42", "indicator_scores", f"{len(extra) - 20} further unknown indicator(s) not shown")

    # V51 the floored set must equal the published list.
    listed = as_dict(rubric.get("type_band_floor_rule")).get("floored_indicators")
    carrying = {iid for iid, entry in scores.items() if isinstance(entry, dict) and "type_band_floor" in entry}
    if not isinstance(listed, list) or not all(isinstance(item, str) for item in listed):
        fail("V51", "rubric.type_band_floor_rule.floored_indicators", "missing or not a list of indicator ids")
    else:
        if len(set(listed)) != len(listed):
            fail("V51", "rubric.type_band_floor_rule.floored_indicators", "list repeats an indicator id")
        for iid in sorted(carrying - set(listed)):
            fail("V51", iid, "carries a type_band_floor but is not in rubric.type_band_floor_rule.floored_indicators")
        for iid in sorted(set(listed) - carrying):
            fail("V51", iid, "is in rubric.type_band_floor_rule.floored_indicators but carries no type_band_floor")

    derive, _source = load_confidence_rule()

    for iid, entry in scores.items():
        if not isinstance(entry, dict):
            fail("V14", iid, "score entry is not an object")
            fail("V13", iid, "score entry is not an object")
            continue
        for key in sorted(set(entry) - SCORE_ENTRY_KEYS):
            fail("V41", iid, f"score entry carries unknown key '{key}'")

        # V14 axes present and numeric; weight present and numeric; composite.
        axes = entry.get("axes")
        axes_ok = False
        if not isinstance(axes, dict):
            fail("V14", iid, "axes is missing or not an object")
        else:
            problems = [axis for axis in AXES if axis not in axes]
            unknown = sorted(set(axes) - set(AXES))
            if problems:
                fail("V14", iid, f"axes is missing {problems}")
            if unknown:
                fail("V14", iid, f"axes carries unknown keys {unknown}")
            bad = [axis for axis in AXES if axis in axes and not (is_number(axes[axis]) and 0 <= axes[axis] <= 10)]
            if bad:
                fail("V14", iid, f"axes values are not numbers from 0 to 10: {bad}")
            axes_ok = not problems and not unknown and not bad
        weight = entry.get("type_weight")
        weight_ok = is_number(weight) and 0 <= weight <= 10
        if not weight_ok:
            fail("V14", iid, f"type_weight {show(weight)} is missing or not a number from 0 to 10")
        if axes_ok and weight_ok:
            composite = (
                axes["impact_potential"]
                * axes["blast_radius_potential"]
                * axes["recoverability_inverse"]
                * (10 - axes["detectability"])
            ) ** 0.25
            if abs(composite - weight) > WEIGHT_TOLERANCE:
                fail(
                    "V14",
                    iid,
                    f"type_weight {weight} deviates from the axes composite {composite:.4f} "
                    f"by more than {WEIGHT_TOLERANCE}",
                )

        # V44 recorded precision.
        if axes_ok:
            for axis in AXES:
                if round(axes[axis], 1) != axes[axis]:
                    fail("V44", iid, f"axis {axis} value {axes[axis]} is not recorded to one decimal place")
        if weight_ok and round(weight, 2) != weight:
            fail("V44", iid, f"type_weight {weight} is not recorded to two decimal places")

        # V15 floor value.
        floor = entry.get("type_band_floor")
        floor_ok = True
        if "type_band_floor" in entry and (not isinstance(floor, str) or floor not in FLOOR_VALUES):
            fail("V15", iid, f"type_band_floor {show(floor)} is not high or critical")
            floor_ok = False

        # V13 band present, valid, and derived from the stored weight.
        band = entry.get("type_band")
        band_ok = isinstance(band, str) and band in BAND_RANK
        if not band_ok:
            fail("V13", iid, f"type_band {show(band)} is missing or not low, medium, high, or critical")
        elif not weight_ok:
            fail("V13", iid, "type_band cannot be derived because type_weight is missing or not numeric")
        elif not thresholds_ok:
            fail("V13", iid, "type_band cannot be derived because rubric.type_band_thresholds is not usable")
        else:
            implied = band_for_weight(weight, thresholds)
            expected = implied
            if floor_ok and floor is not None and BAND_RANK[floor] > BAND_RANK[implied]:
                expected = floor
            if band != expected:
                fail(
                    "V13",
                    iid,
                    f"type_band '{band}' contradicts the stored type_weight {weight}"
                    f"{' with floor ' + floor if floor_ok and floor else ''} (expected '{expected}')",
                )
        if band_ok and floor_ok and floor is not None and BAND_RANK[band] < BAND_RANK[floor]:
            fail("V15", iid, f"type_band '{band}' is below type_band_floor '{floor}'")

        # V20 axis_confidence complete, valid, rule-derived.
        confidence = entry.get("axis_confidence")
        if not isinstance(confidence, dict):
            fail("V20", iid, "axis_confidence is missing or not an object")
            continue
        conf_ok = True
        for axis in AXES:
            if axis not in confidence:
                fail("V20", iid, f"axis_confidence is missing '{axis}'")
                conf_ok = False
        for axis, level in confidence.items():
            if axis not in AXES:
                fail("V20", iid, f"axis_confidence key {show(axis)} is not a scoring axis")
                conf_ok = False
            if not isinstance(level, str) or level not in CONFIDENCE_LEVELS:
                fail("V20", iid, f"axis_confidence value {show(level)} is not established, inferred, or thin")
                conf_ok = False
        matrix_key = ctx.indicator_matrix.get(iid)
        if conf_ok and axes_ok and matrix_key in MATRIX_KEYS:
            try:
                derived = derive(matrix_key, axes)
            except Exception:
                derived = _derive_fallback(matrix_key, axes)
            if derived != confidence:
                diffs = [
                    f"{axis} stored {confidence[axis]} rule {derived.get(axis)}"
                    for axis in AXES
                    if confidence[axis] != derived.get(axis)
                ]
                fail("V20", iid, "axis_confidence differs from the derivation rule: " + "; ".join(diffs))

    return overlay


# ----------------------------------------------------------------------
# Scored case records
# ----------------------------------------------------------------------


def check_record(results: Results, name: str, record, ctx: Context, overlay: dict,
                 schema_dir: Path | None, require_schema: bool, run_schema: bool = True) -> None:
    """V18, V47, V48 for one scored case record."""
    fail = results.fail
    if not isinstance(record, dict):
        fail("V48", name, "file is not a scored case record (top level is not an object)")
        return
    for key in RECORD_REQUIRED:
        if key not in record:
            fail("V48", name, f"required key '{key}' is missing; every JSON file in the records directory must be a scored case record")
    for key in record:
        if key not in RECORD_REQUIRED and key not in RECORD_OPTIONAL:
            fail("V48", name, f"unknown key '{key}'")
    stated = record.get("type_band")
    priority = record.get("conditioned_priority")
    if "type_band" in record and (not isinstance(stated, str) or stated not in BAND_RANK):
        fail("V48", name, f"type_band {show(stated)} is not low, medium, high, or critical")
    if "conditioned_priority" in record and (not isinstance(priority, str) or priority not in BAND_RANK):
        fail("V48", name, f"conditioned_priority {show(priority)} is not low, medium, high, or critical")
    instance = record.get("instance")
    if "instance" in record:
        if not isinstance(instance, dict):
            fail("V48", name, "instance is not an object")
        else:
            for factor in INSTANCE_FACTORS:
                value = instance.get(factor)
                if not isinstance(value, str) or value not in INSTANCE_FACTOR_VALUES[factor]:
                    fail("V48", name, f"instance.{factor} {show(value)} is missing or not a valid value")
            for key in instance:
                if key not in INSTANCE_FACTORS and key != "basis":
                    fail("V48", name, f"instance carries unknown key '{key}'")
    tier = record.get("primary_objective_evidence_tier")
    if tier is not None and (not isinstance(tier, str) or tier not in EVIDENCE_TIERS):
        fail("V48", name, f"primary_objective_evidence_tier {show(tier)} is not valid")
    disposition = record.get("disposition")
    if disposition is not None and (not isinstance(disposition, str) or disposition not in DISPOSITIONS):
        fail("V48", name, f"disposition {show(disposition)} is not valid")
    check_strings_record = Results()
    check_strings(check_strings_record, record, name)
    for line in check_strings_record.failures["V40"]:
        results.failures["V48"].append(line.replace("[V40]", "[V48]"))
    if run_schema and schema_dir is not None:
        before = len(results.failures["V48"])
        schema_check(results, "V48", schema_dir / "scoring-overlay.schema.json", record,
                     require_schema, pointer="scored_case_record", label=f"{name}:")
        if "V48" in results.skipped and len(results.failures["V48"]) == before:
            # The native shape checks above still ran; the schema pass did not.
            results.skipped.pop("V48")
            note = "V48 ran its native shape checks only (jsonschema is not installed)"
            if note not in results.notes:
                results.notes.append(note)

    # V47 band fidelity.
    indicator_id = record.get("indicator_id")
    scores = as_dict(as_dict(overlay).get("indicator_scores"))
    authored = None
    if not isinstance(indicator_id, str) or indicator_id not in ctx.indicator_matrix:
        fail("V47", name, f"indicator_id {show(indicator_id)} is not an indicator of the vocabulary")
    else:
        authored = as_dict(scores.get(indicator_id)).get("type_band")
        if not isinstance(authored, str) or authored not in BAND_RANK:
            fail("V47", name, f"the overlay holds no usable type_band for {indicator_id}")
            authored = None
        elif stated != authored:
            fail(
                "V47",
                name,
                f"type_band {show(stated)} misquotes {indicator_id}: the overlay's authored type_band is '{authored}'",
            )
    if "framework_version" in record and record["framework_version"] != ctx.version:
        fail("V47", name, f"framework_version {show(record['framework_version'])} is not the framework version {show(ctx.version)}")
    overlay_version = as_dict(overlay).get("overlay_version")
    if "overlay_version" in record and record["overlay_version"] != overlay_version:
        fail("V47", name, f"overlay_version {show(record['overlay_version'])} is not the overlay version {show(overlay_version)}")

    # V18 escalate-only, against the stated band and the authored band.
    if isinstance(priority, str) and priority in BAND_RANK:
        if isinstance(stated, str) and stated in BAND_RANK and BAND_RANK[priority] < BAND_RANK[stated]:
            fail("V18", name, f"conditioned_priority '{priority}' is below the stated type_band '{stated}'")
        if authored is not None and BAND_RANK[priority] < BAND_RANK[authored]:
            fail("V18", name, f"conditioned_priority '{priority}' is below the authored type_band '{authored}' of {indicator_id}")


def check_records_dir(results: Results, records_dir: Path, ctx: Context, overlay,
                      schema_dir: Path | None, require_schema: bool, run_schema: bool = True) -> int:
    """Check every JSON file under the directory, subdirectories included,
    matching the .json suffix in any letter case. Return the file count."""
    if not records_dir.is_dir():
        results.fail("V48", str(records_dir), "records directory does not exist")
        return 0
    files = sorted(p for p in records_dir.rglob("*") if p.suffix.lower() == ".json" and p.is_file())
    if not files:
        results.fail("V48", str(records_dir), "records directory holds no JSON file; nothing was checked")
        return 0
    for file_path in files:
        path = file_path
        name = file_path.relative_to(records_dir).as_posix()
        try:
            record, duplicates, nonfinite = load_document(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, RecursionError) as exc:
            results.fail("V48", name, f"file is not readable JSON ({exc.__class__.__name__})")
            continue
        for key in duplicates:
            results.fail("V48", name, f"JSON object key '{key}' appears more than once")
        check_non_finite(results, nonfinite, record, name)
        check_record(results, name, record, ctx, overlay, schema_dir, require_schema, run_schema)
    return len(files)


# ----------------------------------------------------------------------
# Coverage documents
# ----------------------------------------------------------------------


def check_coverage(results: Results, name: str, document, ctx: Context,
                   schema_dir: Path | None, require_schema: bool, run_schema: bool = True) -> None:
    """V49: the coverage schema plus the rules it cannot express."""
    fail = results.fail
    if not isinstance(document, dict) or not document:
        fail("V49", name, "coverage document is not a non-empty object")
        return
    if run_schema and schema_dir is not None:
        before = len(results.failures["V49"])
        schema_check(results, "V49", schema_dir / "coverage.schema.json", document, require_schema, label=f"{name}:")
        if "V49" in results.skipped and len(results.failures["V49"]) == before:
            results.skipped.pop("V49")
            note = "V49 ran its native checks only (jsonschema is not installed)"
            if note not in results.notes:
                results.notes.append(note)
    for key in document:
        if key not in ("cm_deployment_record", "coverage_derivation"):
            fail("V49", name, f"unknown top-level key '{key}'")

    today = datetime.date.today()

    def real_date(where, value, allow_future=False):
        if value is None:
            return
        if not full(ISO_DATE, value):
            fail("V49", name, f"{where} {show(value)} is not a YYYY-MM-DD date")
            return
        try:
            parsed = datetime.date.fromisoformat(value)
        except ValueError:
            fail("V49", name, f"{where} {show(value)} is not a real calendar date")
            return
        if not allow_future and parsed > today:
            fail("V49", name, f"{where} {value} is in the future")

    record = document.get("cm_deployment_record")
    if record is not None:
        if not isinstance(record, dict):
            fail("V49", name, "cm_deployment_record is not an object")
        else:
            real_date("cm_deployment_record.reviewed", record.get("reviewed"))
            seen: set = set()
            for index, deployment in enumerate(as_list(record.get("deployments"))):
                if not isinstance(deployment, dict):
                    fail("V49", name, f"deployments.{index} is not an object")
                    continue
                cm_id = deployment.get("cm_id")
                if not isinstance(cm_id, str) or cm_id not in ctx.cm_ids:
                    fail("V49", name, f"deployments.{index} cm_id {show(cm_id)} is not a countermeasure of the vocabulary")
                if isinstance(cm_id, str):
                    if cm_id in seen:
                        fail("V49", name, f"cm_id {show(cm_id)} appears in more than one deployment entry")
                    seen.add(cm_id)
                real_date(f"deployments.{index}.verified", deployment.get("verified"))
    derivation = document.get("coverage_derivation")
    if derivation is not None:
        if not isinstance(derivation, dict):
            fail("V49", name, "coverage_derivation is not an object")
        else:
            indicator_id = derivation.get("indicator_id")
            if not isinstance(indicator_id, str) or indicator_id not in ctx.indicator_matrix:
                fail("V49", name, f"coverage_derivation indicator_id {show(indicator_id)} is not an indicator of the vocabulary")
            real_date("coverage_derivation.derivation_date", derivation.get("derivation_date"))
            real_date("coverage_derivation.disposition_review_date", derivation.get("disposition_review_date"), allow_future=True)
            if ("disposition" in derivation) != ("disposition_review_date" in derivation):
                fail("V49", name, "disposition and disposition_review_date must appear together")
            if derivation.get("coverage_band") == "exposed" and "disposition" not in derivation:
                fail("V49", name, "an exposed derivation requires a disposition")
            if isinstance(record, dict):
                # Rules that apply when one document carries both parts.
                if derivation.get("protected_target") != record.get("protected_target"):
                    fail("V49", name, "coverage_derivation protected_target differs from the deployment record's protected_target")
                contributing = [
                    d for d in as_list(record.get("deployments"))
                    if isinstance(d, dict) and d.get("status") in ("deployed", "partial")
                ]
                if derivation.get("coverage_band") == "covered" and not contributing:
                    fail("V49", name, "coverage_band is covered but the deployment record holds no deployed or partial countermeasure")
            for cm_id in as_list(derivation.get("missing_critical_path")):
                if not isinstance(cm_id, str) or cm_id not in ctx.cm_ids:
                    fail("V49", name, f"missing_critical_path {show(cm_id)} is not a countermeasure of the vocabulary")


# ----------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------


def print_report(results: Results, scopes) -> bool:
    """Print the per-check summary. Return True when every check in scope
    passed (a check listed in PENDING_DATA_FIX warns instead of failing)."""
    all_green = True
    ids = check_ids(scopes)
    green = 0
    for check_id in ids:
        title = CHECKS[check_id][0]
        failures = results.failures[check_id]
        if check_id in results.skipped and not failures:
            print(f"- [{check_id}] {title} (SKIPPED: {results.skipped[check_id]})")
            continue
        if failures and check_id in PENDING_DATA_FIX:
            print(f"⚠ [{check_id}] {title} ({len(failures)} warning(s); PENDING_DATA_FIX: {PENDING_DATA_FIX[check_id]})")
            for line in failures:
                print(line.replace("✗", "⚠", 1))
            continue
        if failures:
            all_green = False
            print(f"✗ [{check_id}] {title} ({len(failures)} failure(s))")
            for line in failures[:200]:
                print(line)
            if len(failures) > 200:
                print(f"  ... {len(failures) - 200} further line(s) not shown")
        else:
            green += 1
            print(f"✓ [{check_id}] {title}")
    print("")
    for note in results.notes:
        print(f"note: {note}")
    skipped = [cid for cid in ids if cid in results.skipped and not results.failures[cid]]
    if skipped:
        print(
            f"⚠ {len(skipped)} check(s) skipped ({', '.join(skipped)}): "
            f"{'; '.join(sorted(set(results.skipped[c] for c in skipped)))}. "
            f"This run is not a release gate."
        )
    if all_green:
        print(f"✓ validate PASSED: {green} of {len(ids)} checks green, {len(skipped)} skipped, 0 failed.")
    else:
        failed = sum(1 for cid in ids if results.failures[cid] and cid not in PENDING_DATA_FIX)
        print(f"✗ validate FAILED: {failed} check(s) reported problems.")
    return all_green


# ----------------------------------------------------------------------
# Fixture harness
# ----------------------------------------------------------------------


class MutationError(Exception):
    """A fixture mutation could not be applied as written."""


_SELECTOR = re.compile(r"\[([A-Za-z_]+)=(.*)\]")


def _step(node, part: str):
    """Follow one path segment. Segments: a dict key, a list index, or a
    selector [key=value] that picks the list element whose key equals value."""
    selector = _SELECTOR.fullmatch(part)
    if selector:
        if not isinstance(node, list):
            raise MutationError(f"selector {part} applied to a non-list")
        key, value = selector.group(1), selector.group(2)
        matches = [item for item in node if isinstance(item, dict) and item.get(key) == value]
        if len(matches) != 1:
            raise MutationError(f"selector {part} matched {len(matches)} element(s), expected 1")
        return matches[0]
    if isinstance(node, list):
        try:
            return node[int(part)]
        except (ValueError, IndexError):
            raise MutationError(f"list index '{part}' does not exist")
    if isinstance(node, dict):
        if part not in node:
            raise MutationError(f"key '{part}' does not exist")
        return node[part]
    raise MutationError(f"cannot descend into a scalar at '{part}'")


def _resolve(root, path: str):
    node = root
    for part in path.split("."):
        node = _step(node, part)
    return node


def _resolve_parent(root, path: str):
    parts = path.split(".")
    node = root
    for part in parts[:-1]:
        node = _step(node, part)
    return node, parts[-1]


def _index_of(parent: list, item) -> int:
    for index, candidate in enumerate(parent):
        if candidate is item:
            return index
    raise MutationError("selected element not found")


def apply_data_op(data, op: dict) -> None:
    """Apply one mutation in place. Every op must change the document:
    set   the path must exist and the new value must differ
    add   the key must NOT exist yet (dict parents only)
    append the path must be a list
    del   the path must exist
    """
    kind = op.get("op")
    path = op.get("path")
    if not isinstance(path, str) or not path:
        raise MutationError(f"op '{kind}' has no path")
    if kind == "set":
        parent, key = _resolve_parent(data, path)
        current = _step(parent, key)
        if current == op["value"] and type(current) is type(op["value"]):
            raise MutationError(f"set at '{path}' does not change the value")
        if isinstance(parent, list):
            parent[_index_of(parent, current)] = op["value"]
        else:
            parent[key] = op["value"]
    elif kind == "add":
        parent, key = _resolve_parent(data, path)
        if not isinstance(parent, dict):
            raise MutationError(f"add at '{path}' needs an object parent")
        if key in parent:
            raise MutationError(f"add at '{path}': key already exists (use set)")
        parent[key] = op["value"]
    elif kind == "append":
        target = _resolve(data, path)
        if not isinstance(target, list):
            raise MutationError(f"append at '{path}': target is not a list")
        target.append(op["value"])
    elif kind == "del":
        parent, key = _resolve_parent(data, path)
        current = _step(parent, key)
        if isinstance(parent, list):
            parent.pop(_index_of(parent, current))
        else:
            del parent[key]
    else:
        raise MutationError(f"unknown op '{kind}'")


def apply_mutations(raw_text: str, mutations) -> str:
    """Apply a fixture's mutations to a document's text and return the new
    text. raw_replace ops edit the text; the rest edit the parsed data."""
    if not isinstance(mutations, list) or not mutations:
        raise MutationError("fixture has no mutations")
    data_ops = [op for op in mutations if op.get("op") != "raw_replace"]
    text = raw_text
    for op in mutations:
        if op.get("op") != "raw_replace":
            continue
        count = op.get("count", 1)
        if text.count(op["find"]) < count:
            raise MutationError(f"raw_replace: text {op['find'][:40]!r} occurs fewer than {count} time(s)")
        if op["find"] == op["replace"]:
            raise MutationError("raw_replace does not change the text")
        text = text.replace(op["find"], op["replace"], count)
    if data_ops:
        if text != raw_text:
            raise MutationError("a fixture may not mix raw_replace with data ops")
        data = json.loads(raw_text)
        before = json.dumps(data, ensure_ascii=False)
        for op in data_ops:
            apply_data_op(data, op)
        text = json.dumps(data, ensure_ascii=False)
        if text == before:
            raise MutationError("mutations leave the document unchanged")
    if text == raw_text:
        raise MutationError("mutations leave the document unchanged")
    return text


class Harness:
    def __init__(self, framework_raw: str, overlay_raw: str | None, schema_dir: Path, require_schema: bool):
        self.framework_raw = framework_raw
        self.overlay_raw = overlay_raw
        self.schema_dir = schema_dir
        self.require_schema = require_schema
        self.have_schema = jsonschema is not None
        # Set by the baseline run: the canonical vocabulary context and the
        # canonical overlay, which record and coverage fixtures are checked
        # against (the baseline has already proved both clean).
        self.canon_ctx: Context | None = None
        self.canon_overlay: dict | None = None

    def run(self, target: str, framework_raw: str, overlay_raw: str | None, document,
            run_schema: bool) -> Results:
        """Run the checks one fixture needs and return the results."""
        if target == "coverage":
            results = Results()
            check_coverage(results, "fixture", document, self.canon_ctx, self.schema_dir, self.require_schema, run_schema)
            return results
        if target == "record":
            if self.canon_overlay is None:
                raise MutationError("fixture targets a scored record but no overlay document is available")
            results = Results()
            check_record(results, "fixture", document, self.canon_ctx, self.canon_overlay,
                         self.schema_dir, self.require_schema, run_schema)
            return results
        results, ctx, _data = check_framework(framework_raw, self.schema_dir, self.require_schema, run_schema)
        if target == "framework":
            return results
        if overlay_raw is None:
            raise MutationError("fixture targets the overlay but no overlay document is available")
        if ctx.usable:
            check_overlay(results, overlay_raw, ctx, self.schema_dir, self.require_schema, run_schema)
        return results


SCHEMA_TARGETS = {
    "framework_schema": ("framework", "framework.schema.json"),
    "overlay_schema": ("overlay", "scoring-overlay.schema.json"),
}
TARGET_SCOPES = {
    "framework_schema": ("framework",),
    "overlay_schema": ("framework", "overlay"),
    "framework": ("framework",),
    "overlay": ("framework", "overlay"),
    "record": ("framework", "overlay", "records"),
    "coverage": ("framework", "coverage"),
}


def run_fixture(harness: Harness, fixture: dict):
    """Run one fixture. Return (status, fired, note). Status is one of
    pass, fail, skip."""
    target = fixture.get("target", "framework")
    if target not in TARGET_SCOPES:
        return "fail", [], f"unknown target '{target}'"
    expect = fixture.get("expect", "fail")
    if expect not in ("fail", "pass"):
        return "fail", [], f"unknown expect '{expect}'"
    expected = fixture.get("expected_check")
    if expected not in CHECKS:
        return "fail", [], f"expected_check '{expected}' is not a known check id"
    if expect == "fail" and CHECKS[expected][1] not in TARGET_SCOPES[target]:
        return "fail", [], f"expected_check {expected} does not run for target '{target}'"
    scopes = TARGET_SCOPES[target]
    needs_schema = expected in SCHEMA_CHECKS or expect == "pass" or target in ("record", "coverage")
    if expect == "fail" and not (isinstance(fixture.get("expected_message"), str) and fixture["expected_message"]):
        return "fail", [], "a negative fixture must name an expected_message (text one failure line must contain)"

    framework_raw = harness.framework_raw
    overlay_raw = harness.overlay_raw
    document = None
    if target in SCHEMA_TARGETS:
        # Harness self-test: mutate a SCHEMA file and require the schema
        # check to notice, with the canonical documents left untouched.
        doc_target, schema_name = SCHEMA_TARGETS[target]
        tmp = Path(tempfile.mkdtemp(prefix="tm-schema-fixture-"))
        try:
            for schema_file in harness.schema_dir.glob("*.schema.json"):
                shutil.copy(schema_file, tmp / schema_file.name)
            try:
                mutated = apply_mutations((tmp / schema_name).read_text(encoding="utf-8"), fixture.get("mutations"))
            except (MutationError, KeyError, TypeError, ValueError) as exc:
                return "fail", [], f"mutation did not apply: {exc}"
            (tmp / schema_name).write_text(mutated, encoding="utf-8")
            original_dir = harness.schema_dir
            harness.schema_dir = tmp
            try:
                results = harness.run(doc_target, framework_raw, overlay_raw, None, True)
            finally:
                harness.schema_dir = original_dir
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        fired = results.fired(scopes)
        if expected not in fired:
            return "fail", fired, f"expected {expected} did not fire on the mutated schema"
        needle = fixture["expected_message"]
        if not any(needle in line for line in results.failures[expected]):
            return "fail", fired, f"{expected} fired but no failure line contains {needle!r}"
        return "pass", fired, "ok"
    try:
        if target == "framework":
            framework_raw = apply_mutations(framework_raw, fixture.get("mutations"))
        elif target == "overlay":
            if overlay_raw is None:
                return "fail", [], "no overlay document available (pass --overlay or keep scoring-overlay.json beside the framework file)"
            overlay_raw = apply_mutations(overlay_raw, fixture.get("mutations"))
        else:
            base = fixture.get("base")
            if not isinstance(base, dict):
                return "fail", [], f"a {target} fixture needs a 'base' document"
            base_results = harness.run(target, framework_raw, overlay_raw, base, True)
            base_fired = base_results.fired(scopes)
            if base_fired:
                return "fail", base_fired, "the fixture's base document does not pass on its own"
            document = json.loads(apply_mutations(json.dumps(base), fixture.get("mutations")))
    except MutationError as exc:
        return "fail", [], f"mutation did not apply: {exc}"
    except (KeyError, TypeError, ValueError) as exc:
        return "fail", [], f"mutation did not apply ({exc.__class__.__name__}: {exc})"

    try:
        results = harness.run(target, framework_raw, overlay_raw, document, needs_schema)
    except json.JSONDecodeError as exc:
        return "fail", [], f"mutated document is not parseable JSON ({exc.msg})"
    fired = results.fired(scopes)

    if expect == "pass":
        if fired:
            return "fail", fired, "positive fixture introduced failures"
        return "pass", fired, "ok"
    if expected not in fired:
        return "fail", fired, f"expected {expected} did not fire" if fired else "validation passed clean on mutated data"
    needle = fixture.get("expected_message")
    if needle and not any(needle in line for line in results.failures[expected]):
        return "fail", fired, f"{expected} fired but no failure line contains {needle!r}"
    return "pass", fired, "ok"


def run_fixture_harness(framework_raw: str, overlay_raw: str | None, fixtures_dir: Path,
                        schema_dir: Path, require_schema: bool) -> int:
    """Run every fixture in the manifest. Return 0 only when:
    the canonical documents pass every check on their own; the manifest
    lists at least one fixture and every fixture file in the directory;
    every fixture behaves as declared; and every check id has at least one
    negative fixture."""
    problems: list[str] = []
    manifest_path = fixtures_dir / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        names = manifest["fixtures"]
        assert isinstance(names, list)
    except Exception as exc:
        print(f"✗ fixture harness: manifest.json is missing or unreadable in {fixtures_dir} ({exc.__class__.__name__})")
        return 1
    if not names:
        print("✗ fixture harness FAILED: the manifest lists zero fixtures.")
        return 1
    if len(set(names)) != len(names):
        problems.append("the manifest lists a fixture more than once")
    on_disk = sorted(p.name for p in fixtures_dir.glob("*.json") if p.name != "manifest.json")
    for name in on_disk:
        if name not in names:
            problems.append(f"fixture file {name} is not listed in the manifest")

    if jsonschema is None:
        print(
            "✗ fixture harness FAILED: the jsonschema package is not importable. The harness cannot prove "
            "the schema fixtures without it and does not run in part (pip install jsonschema)."
        )
        return 1
    harness = Harness(framework_raw, overlay_raw, schema_dir, require_schema)

    # Baseline: the canonical documents must pass on their own, otherwise a
    # fixture could pass on a failure that was already there.
    baseline, ctx, _data = check_framework(framework_raw, schema_dir, require_schema)
    baseline_scopes = ["framework"]
    harness.canon_ctx = ctx
    if overlay_raw is not None and ctx.usable:
        harness.canon_overlay = check_overlay(baseline, overlay_raw, ctx, schema_dir, require_schema)
        baseline_scopes.append("overlay")
    baseline_fired = baseline.fired(baseline_scopes)
    if baseline_fired:
        print(
            f"✗ fixture harness FAILED: the canonical documents do not pass on their own "
            f"(fired: {', '.join(baseline_fired)}). Fix the baseline first."
        )
        return 1

    print(f"Fixture harness: {len(names)} fixture(s); baseline clean ({', '.join(baseline_scopes)})")
    print("")
    covered: set[str] = set()
    counts = {"pass": 0, "fail": 0, "skip": 0}
    seen_ids: set[str] = set()
    for name in names:
        path = fixtures_dir / str(name)
        try:
            fixture = json.loads(path.read_text(encoding="utf-8"))
            assert isinstance(fixture, dict)
        except Exception as exc:
            counts["fail"] += 1
            print(f"✗ {name}: fixture file is missing or unreadable ({exc.__class__.__name__})")
            continue
        fid = fixture.get("id", name)
        if fid in seen_ids:
            problems.append(f"fixture id {fid} is used more than once")
        seen_ids.add(fid)
        try:
            status, fired, note = run_fixture(harness, fixture)
        except Exception as exc:  # a fixture must never crash the harness
            status, fired, note = "fail", [], f"harness error {exc.__class__.__name__}: {exc}"
        counts[status] += 1
        expected = fixture.get("expected_check", "?")
        positive = fixture.get("expect") == "pass"
        label = f"accepts ({expected})" if positive else f"expects {expected}"
        also = [cid for cid in fired if cid != expected]
        tail = f"; also fired: {', '.join(also)}" if also and not positive else ""
        if status == "pass":
            if not positive:
                covered.add(expected)
            print(f"✓ {fid} {label}{tail}")
        elif status == "skip":
            if not positive:
                covered.add(expected)
            print(f"- {fid} {label}: SKIPPED ({note})")
        else:
            print(f"✗ {fid} {label}: {note} (fired: {', '.join(fired) if fired else 'none'})")

    uncovered = [cid for cid in CHECKS if cid not in covered]
    for cid in uncovered:
        problems.append(f"check {cid} ({CHECKS[cid][0]}) has no passing negative fixture")
    print("")
    for problem in problems:
        print(f"✗ {problem}")
    total = len(names)
    if counts["fail"] or problems:
        print(
            f"✗ fixture harness FAILED: {counts['pass']}/{total} fixtures behave as expected, "
            f"{counts['fail']} failed, {counts['skip']} skipped, {len(problems)} harness problem(s)."
        )
        return 1
    skipped = f", {counts['skip']} skipped (jsonschema not installed)" if counts["skip"] else ""
    print(
        f"✓ fixture harness PASSED: {counts['pass']}/{total} fixtures behave as expected{skipped}; "
        f"every one of the {len(CHECKS)} checks has a negative fixture."
    )
    return 0


# ----------------------------------------------------------------------
# Command line
# ----------------------------------------------------------------------


def read_text(path: Path, label: str) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"✗ validate: {label} not found at {path}", file=sys.stderr)
    except UnicodeDecodeError:
        print(f"✗ validate: {label} at {path} is not valid UTF-8", file=sys.stderr)
    except OSError as exc:
        print(f"✗ validate: {label} at {path} could not be read ({exc.__class__.__name__})", file=sys.stderr)
    return None


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    parser = argparse.ArgumentParser(
        prog="validate.py",
        description="Validate the THREAT Matrix vocabulary, the experimental scoring overlay, and scored case records.",
    )
    parser.add_argument("framework", nargs="?", default="docs/data/framework.json")
    parser.add_argument("--overlay", help="path to scoring-overlay.json")
    parser.add_argument("--records", help="directory of scored case records (requires --overlay)")
    parser.add_argument("--coverage", help="path to a coverage document")
    parser.add_argument("--fixtures", help="directory of fixtures; runs the fixture harness")
    parser.add_argument("--require-schema", action="store_true",
                        help="accepted for compatibility; schema validation is required by default")
    parser.add_argument("--no-schema", action="store_true",
                        help="skip the JSON Schema checks (not a release gate)")
    parser.add_argument("--print-schema-pins", action="store_true",
                        help="print the constraint digests of the schema files and exit")
    parser.add_argument("--schema-dir", help="directory holding the *.schema.json files")
    args = parser.parse_args(argv)

    if args.records and not args.overlay:
        print("✗ validate: --records requires --overlay", file=sys.stderr)
        return 1

    framework_path = Path(args.framework)
    framework_raw = read_text(framework_path, "framework.json")
    if framework_raw is None:
        return 1
    schema_dir = Path(args.schema_dir) if args.schema_dir else framework_path.resolve().parent
    run_schema = not args.no_schema
    if args.no_schema and args.require_schema:
        print("✗ validate: --no-schema and --require-schema contradict each other", file=sys.stderr)
        return 1
    if args.print_schema_pins:
        for schema_name in SCHEMA_PINS:
            try:
                digest = schema_digest(json.loads((schema_dir / schema_name).read_text(encoding="utf-8")))
            except (OSError, ValueError) as exc:
                digest = f"unreadable ({exc.__class__.__name__})"
            print(f'    "{schema_name}": "{digest}",')
        return 0

    overlay_raw = None
    if args.overlay:
        overlay_raw = read_text(Path(args.overlay), "scoring overlay")
        if overlay_raw is None:
            return 1

    try:
        if args.fixtures:
            if overlay_raw is None:
                sibling = framework_path.resolve().parent / "scoring-overlay.json"
                if sibling.is_file():
                    overlay_raw = read_text(sibling, "scoring overlay")
            if args.no_schema:
                print("✗ validate: the fixture harness does not run with --no-schema", file=sys.stderr)
                return 1
            return run_fixture_harness(framework_raw, overlay_raw, Path(args.fixtures), schema_dir, True)

        scopes = ["framework"]
        try:
            results, ctx, _data = check_framework(framework_raw, schema_dir, True, run_schema)
        except (ValueError, RecursionError) as exc:
            print(f"✗ validate: framework.json is not valid JSON ({exc})", file=sys.stderr)
            return 1

        if overlay_raw is not None:
            scopes.append("overlay")
            overlay = None
            if not ctx.usable:
                results.fail("V41", "overlay", "not checked: the vocabulary is too broken to check the overlay against")
            else:
                try:
                    overlay = check_overlay(results, overlay_raw, ctx, schema_dir, True, run_schema)
                except (ValueError, RecursionError) as exc:
                    results.fail("V41", "overlay", f"overlay is not valid JSON ({exc})")
                _derive, source = load_confidence_rule()
                results.notes.append(f"axis_confidence rule source: {source}")
            if args.records:
                scopes.append("records")
                if not isinstance(overlay, dict):
                    results.fail("V48", args.records, "not checked: the overlay is not usable")
                else:
                    count = check_records_dir(results, Path(args.records), ctx, overlay, schema_dir, True, run_schema)
                    results.notes.append(f"scored case records checked: {count}")

        if args.coverage:
            scopes.append("coverage")
            coverage_raw = read_text(Path(args.coverage), "coverage document")
            if coverage_raw is None:
                return 1
            try:
                document, duplicates, nonfinite = load_document(coverage_raw)
            except (ValueError, RecursionError) as exc:
                results.fail("V49", args.coverage, f"not valid JSON ({exc})")
            else:
                for key in duplicates:
                    results.fail("V49", args.coverage, f"JSON object key '{key}' appears more than once")
                for token in nonfinite:
                    results.fail("V49", args.coverage, f"bare token {token} is not JSON")
                if not ctx.usable:
                    results.fail("V49", args.coverage, "not checked: the vocabulary is too broken to check against")
                else:
                    check_coverage(results, Path(args.coverage).name, document, ctx, schema_dir, True, run_schema)

        return 0 if print_report(results, scopes) else 1
    except Exception as exc:  # fail closed, with one readable line
        print(f"✗ validate FAILED: internal error {exc.__class__.__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
