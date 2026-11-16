#!/usr/bin/env python3
"""Migrate a schema 2.1.0 framework document to schema 3.0.0.

Input: one framework document in the PUBLISHED 2.1.0 shape (the shape of
docs/data/framework.json on the main branch at content version 1.7.0).
Output: two documents.

  1. A 3.0.0 vocabulary document. It carries no scores.
  2. An experimental scoring overlay holding every score that the input
     carried, in the overlay shape (see docs/data/scoring-overlay.schema.json).

This migrates SHAPE, not CONTENT. It renames, moves, splits, and drops
fields exactly as the 3.0.0 contract requires. It does not review, add, or
correct any behavioral content, citation, or score, and it does not make
the scores any more valid: the overlay it writes is labelled experimental,
non-normative, and unvalidated.

Changes performed (every breaking change between 2.1.0 and 3.0.0):

  A. schema_version is set to 3.0.0.
  B. evidence_basis values are renamed:
       operational_primary -> practice_led
       hybrid              -> practice_and_literature
       literature_primary  -> literature_led
  C. The root `operations` array is dropped. If it is not empty, its
     content is saved in the report so nothing is lost silently.
  D. countermeasure.compensates_for is split. Countermeasure IDs stay.
     Indicator IDs become edges in countermeasure.mitigates, each
     {"indicator": <id>, "function": "unreviewed"}. Any other value is
     removed and listed in the report for a manual decision.
  E. Scores leave the vocabulary. From every indicator: escalation_axes,
     escalation_weight, severity_band, severity_floor, axis_confidence.
     From every tactic: assessment_guidance.escalation_priority. From the
     root: escalation_rubric and instance_conditioning. All of it moves
     into the overlay with these renames:
       escalation_axes     -> indicator_scores[id].axes
       escalation_weight   -> indicator_scores[id].type_weight
       severity_band       -> indicator_scores[id].type_band
       severity_floor      -> indicator_scores[id].type_band_floor
       axis_confidence     -> indicator_scores[id].axis_confidence
       escalation_priority -> tactic_priorities[tactic_id]
       escalation_rubric   -> rubric (severity_thresholds ->
                              type_band_thresholds, severity_floor_rule ->
                              type_band_floor_rule; the rule also gains
                              floored_indicators, the sorted list of the
                              indicators that carried severity_floor)
       instance_conditioning -> instance_conditioning
  F. matrices.<name>.maturity is added where absent: "core" for person and
     facility, "draft" for every other matrix.

Left alone on purpose: actor_profile.v2_tactic_associations, the content
`version` (use --content-version to set it), and all prose. Prose that
mentions an old field name is listed in the report for manual editing.

What it cannot do automatically is reported as a list, never as a crash:
bibliography keys or source_refs that the tightened key grammar rejects,
bibliography URLs that are not http or https, compensates_for values that
are neither countermeasure nor indicator IDs, indicators with an
incomplete score, tactics with no escalation_priority (the overlay needs
one tactic_priorities entry per tactic and the tool never invents one),
and (when the jsonschema package, the 3.0.0 schemas, and
scripts/lint/validate.py are available) every remaining schema error and
every failing validator check, grouped. Those remaining items are content
problems in the input, which 3.0.0 checks and 2.1.0 did not.

Exit codes: 0 migrated with nothing left for manual work; 1 migrated, but
the report lists items that need manual remediation (outputs are still
written unless --dry-run); 2 the input could not be read or is not a
2.1.0 document.

Usage:
  python3 scripts/migrate/2.1-to-3.0.py INPUT.json --dry-run
  python3 scripts/migrate/2.1-to-3.0.py INPUT.json \\
      --out-framework out/framework.json --out-overlay out/scoring-overlay.json \\
      [--report out/migration-report.json] [--content-version 2.0.0]
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter, OrderedDict
from pathlib import Path

NAME = "migrate-2.1-to-3.0"
REPO = Path(__file__).resolve().parents[2]
TARGET_SCHEMA_VERSION = "3.0.0"

EVIDENCE_BASIS_RENAMES = {
    "operational_primary": "practice_led",
    "hybrid": "practice_and_literature",
    "literature_primary": "literature_led",
}
INDICATOR_SCORE_RENAMES = OrderedDict([
    ("escalation_axes", "axes"),
    ("escalation_weight", "type_weight"),
    ("severity_band", "type_band"),
    ("severity_floor", "type_band_floor"),
    ("axis_confidence", "axis_confidence"),
])
REQUIRED_SCORE_PARTS = ("axes", "type_weight", "type_band", "axis_confidence")
RUBRIC_RENAMES = {
    "severity_thresholds": "type_band_thresholds",
    "severity_floor_rule": "type_band_floor_rule",
}
MATURITY = {"person": "core", "facility": "core"}
DEFAULT_MATURITY = "draft"
OLD_FIELD_NAMES = (
    "escalation_axes", "escalation_weight", "severity_band", "severity_floor",
    "type_severity_band", "escalation_priority", "escalation_rubric",
    "severity_thresholds", "severity_floor_rule",
)

IND_ID = re.compile(r"^IND-[FOI]?[0-9]{4}-[0-9]{2}\Z")
CM_ID = re.compile(r"^CM-[FOI]?[0-9]{4}-[0-9]{2}\Z")
BIB_KEY = re.compile(r"^(?!(IND|CM|RP)-[FOI]?[0-9]{4}-[0-9]{2}\Z)[A-Z][A-Z0-9]*(-[A-Z0-9]+)+\Z")
HTTP_URL = re.compile(r"^https?://\S+\Z")

OVERLAY_NOTICE = (
    "Experimental and non-normative. These values are authored, type-level "
    "estimates for classes of behavior. They have not been validated against "
    "outcomes or by independent human reviewers. They do not predict violence, "
    "they are not a score of any person, and they must not be used as grounds "
    "for adverse action. The vocabulary in framework.json is complete without "
    "this file."
)


class InputError(Exception):
    """The input could not be read or is not a 2.1.0 framework document."""


def load_json(path, label: str):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle, object_pairs_hook=OrderedDict)
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


def insert_after(mapping: OrderedDict, after_key: str, key: str, value) -> OrderedDict:
    """Return a copy of mapping with key placed right after after_key."""
    out = OrderedDict()
    placed = False
    for existing_key, existing_value in mapping.items():
        if existing_key == key:
            continue
        out[existing_key] = existing_value
        if existing_key == after_key:
            out[key] = value
            placed = True
    if not placed:
        out[key] = value
    return out


class Migration:
    def __init__(self, document, content_version: str | None):
        if not isinstance(document, dict):
            raise InputError("the input top level is not a JSON object")
        schema_version = document.get("schema_version")
        if isinstance(schema_version, str) and schema_version.startswith("3."):
            raise InputError(
                f"the input already declares schema_version {schema_version}; "
                f"this tool migrates 2.1.0 documents only"
            )
        if not isinstance(schema_version, str) or not schema_version.startswith("2."):
            raise InputError(
                f"the input declares schema_version {schema_version!r}; expected a 2.x document "
                f"(the published shape is 2.1.0)"
            )
        if not isinstance(document.get("matrices"), dict):
            raise InputError("the input has no 'matrices' object")
        self.doc = copy.deepcopy(document)
        self.source_schema_version = schema_version
        self.content_version = content_version
        self.counts: Counter = Counter()
        self.manual: list[dict] = []
        self.saved: dict = {}
        self.overlay: OrderedDict = OrderedDict()

    # -- helpers -------------------------------------------------------------

    def note(self, kind: str, where: str, detail: str, remediation: str) -> None:
        self.manual.append(OrderedDict(
            kind=kind, where=where, detail=detail, remediation=remediation,
        ))

    def matrices(self):
        for key, value in self.doc["matrices"].items():
            if isinstance(value, dict):
                yield key, value

    def tactics(self):
        for matrix_key, matrix in self.matrices():
            tactics = matrix.get("tactics")
            if not isinstance(tactics, list):
                self.note("shape", f"matrices.{matrix_key}.tactics", "missing or not an array",
                          "Restore the tactics array, then run the migration again.")
                continue
            for tactic in tactics:
                if isinstance(tactic, dict):
                    yield matrix_key, tactic
                else:
                    self.note("shape", f"matrices.{matrix_key}.tactics", "an entry is not an object",
                              "Remove or repair the entry.")

    # -- changes -------------------------------------------------------------

    def change_a_schema_version(self) -> None:
        self.doc["schema_version"] = TARGET_SCHEMA_VERSION
        self.counts["A. schema_version set to 3.0.0"] += 1
        if self.content_version:
            self.doc["version"] = self.content_version
            self.counts["content version set by --content-version"] += 1

    def change_b_evidence_basis(self) -> None:
        self._rename_evidence_basis(self.doc)

    def _rename_evidence_basis(self, node) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "evidence_basis" and isinstance(value, str) and value in EVIDENCE_BASIS_RENAMES:
                    node[key] = EVIDENCE_BASIS_RENAMES[value]
                    self.counts[f"B. evidence_basis {value} -> {EVIDENCE_BASIS_RENAMES[value]}"] += 1
                else:
                    self._rename_evidence_basis(value)
        elif isinstance(node, list):
            for item in node:
                self._rename_evidence_basis(item)

    def change_c_operations(self) -> None:
        if "operations" not in self.doc:
            return
        operations = self.doc.pop("operations")
        self.counts["C. root operations dropped"] += 1
        if operations:
            self.saved["operations"] = operations
            self.note(
                "dropped-content", "operations",
                f"the root operations value was not empty ({type(operations).__name__}, "
                f"{len(operations) if hasattr(operations, '__len__') else 1} item(s)); it has no place in 3.0.0",
                "The dropped value is saved under saved.operations in the report. Keep it outside "
                "the framework document.",
            )

    def change_d_compensates_for(self) -> None:
        for matrix_key, tactic in self.tactics():
            countermeasures = tactic.get("countermeasures")
            if not isinstance(countermeasures, list):
                continue
            for index, cm in enumerate(countermeasures):
                if not isinstance(cm, dict) or "compensates_for" not in cm:
                    continue
                cm_id = cm.get("id", "?")
                refs = cm["compensates_for"]
                if not isinstance(refs, list):
                    self.note("compensates_for", str(cm_id), "compensates_for is not an array",
                              "Replace it with an array of countermeasure IDs.")
                    continue
                keep, edges = [], []
                existing = cm.get("mitigates") if isinstance(cm.get("mitigates"), list) else []
                seen = {
                    edge.get("indicator") for edge in existing if isinstance(edge, dict)
                }
                for ref in refs:
                    if isinstance(ref, str) and CM_ID.match(ref):
                        if ref not in keep:
                            keep.append(ref)
                        self.counts["D. compensates_for countermeasure IDs kept"] += 1
                    elif isinstance(ref, str) and IND_ID.match(ref):
                        if ref not in seen:
                            edges.append(OrderedDict(indicator=ref, function="unreviewed"))
                            seen.add(ref)
                        self.counts["D. compensates_for indicator IDs moved to mitigates (function unreviewed)"] += 1
                    else:
                        self.counts["D. compensates_for values removed (neither CM nor IND)"] += 1
                        self.note(
                            "compensates_for", str(cm_id),
                            f"value {ref!r} is neither a countermeasure ID nor an indicator ID; removed",
                            "Decide what the value meant and re-add it as a countermeasure ID in "
                            "compensates_for or as a mitigates edge.",
                        )
                cm["compensates_for"] = keep
                if edges or existing:
                    cm = insert_after(cm, "compensates_for", "mitigates", list(existing) + edges)
                    countermeasures[index] = cm
                    self.counts["D. countermeasures that gained mitigates edges"] += 1 if edges else 0

    def change_e_scores(self) -> None:
        indicator_scores: OrderedDict = OrderedDict()
        tactic_priorities: OrderedDict = OrderedDict()
        for matrix_key, tactic in self.tactics():
            tactic_id = tactic.get("id", "?")
            guidance = tactic.get("assessment_guidance")
            if isinstance(guidance, dict) and "escalation_priority" in guidance:
                tactic_priorities[str(tactic_id)] = guidance.pop("escalation_priority")
                self.counts["E. assessment_guidance.escalation_priority moved to tactic_priorities"] += 1
            else:
                # Never invented: the overlay needs one entry per tactic, and
                # choosing a priority is a content decision.
                self.note(
                    "tactic-priority", str(tactic_id),
                    "the tactic has no assessment_guidance.escalation_priority, so the overlay has no "
                    "tactic_priorities entry for it (the overlay requires exactly one per tactic)",
                    "Add tactic_priorities[<tactic id>] to the overlay with one of Urgent, Immediate, "
                    "Priority, Routine. This tool does not choose a value.",
                )
            for indicator in tactic.get("indicators") or []:
                if not isinstance(indicator, dict):
                    continue
                ind_id = indicator.get("id")
                entry: OrderedDict = OrderedDict()
                for old, new in INDICATOR_SCORE_RENAMES.items():
                    if old in indicator:
                        entry[new] = indicator.pop(old)
                        self.counts[f"E. indicator {old} moved to overlay {new}"] += 1
                if not entry:
                    self.note("score", str(ind_id), "the indicator carried no score fields",
                              "The overlay needs one entry per indicator. Author a score for it in "
                              "the overlay, or do not publish an overlay.")
                    continue
                if not isinstance(ind_id, str):
                    self.note("score", f"{tactic_id}", "an indicator with scores has no string id; scores dropped",
                              "Give the indicator an id and re-enter its scores in the overlay.")
                    continue
                missing = [part for part in REQUIRED_SCORE_PARTS if part not in entry]
                if missing:
                    self.note("score", ind_id, f"incomplete score: missing {', '.join(missing)}",
                              "Complete the overlay entry by hand; a partial score is invalid.")
                # Overlay key order: axes, type_weight, type_band, type_band_floor, axis_confidence.
                indicator_scores[ind_id] = entry
        self.counts["E. overlay indicator_scores entries"] = len(indicator_scores)

        rubric = self.doc.pop("escalation_rubric", None)
        if rubric is None:
            self.note("rubric", "escalation_rubric", "the input has no escalation_rubric",
                      "Supply the overlay's rubric by hand; it is required by the overlay schema.")
            rubric = OrderedDict()
        else:
            self.counts["E. root escalation_rubric moved to overlay rubric"] += 1
        if isinstance(rubric, dict):
            renamed = OrderedDict()
            for key, value in rubric.items():
                new_key = RUBRIC_RENAMES.get(key, key)
                if new_key != key:
                    self.counts[f"E. rubric {key} -> {new_key}"] += 1
                renamed[new_key] = value
            rubric = renamed
            # 3.0.0 publishes the complete list of floored indicators inside
            # the floor rule. It is derived, not authored: exactly the
            # indicators that carried severity_floor.
            floored = sorted(
                ind_id for ind_id, entry in indicator_scores.items() if "type_band_floor" in entry
            )
            floor_rule = rubric.get("type_band_floor_rule")
            if isinstance(floor_rule, dict):
                floor_rule["floored_indicators"] = floored
                self.counts["E. rubric.type_band_floor_rule.floored_indicators written (derived list)"] = len(floored)
            else:
                self.note(
                    "rubric", "rubric.type_band_floor_rule",
                    "the floor rule is missing or is not an object, so floored_indicators could not be written",
                    "Write rubric.type_band_floor_rule by hand (definition, applies_to, added, "
                    f"floored_indicators). The derived floored_indicators list has {len(floored)} ID(s): "
                    "every indicator_scores entry that has a type_band_floor, sorted.",
                )

        conditioning = self.doc.pop("instance_conditioning", None)
        if conditioning is None:
            self.note("instance_conditioning", "instance_conditioning", "the input has no instance_conditioning",
                      "Supply the overlay's instance_conditioning by hand; it is required by the overlay schema.")
            conditioning = OrderedDict()
        else:
            self.counts["E. root instance_conditioning moved to overlay"] += 1

        self.overlay = OrderedDict([
            ("name", "THREAT Matrix experimental scoring overlay"),
            ("overlay_version", "0.1.0"),
            ("applies_to_framework_version", self.doc.get("version")),
            ("status", "experimental"),
            ("normative", False),
            ("validation_status", "unvalidated"),
            ("scope", "type_level"),
            ("not_a_risk_score", True),
            ("notice", OVERLAY_NOTICE),
            ("rubric", rubric),
            ("instance_conditioning", conditioning),
            ("tactic_priorities", tactic_priorities),
            ("indicator_scores", indicator_scores),
        ])

    def change_f_maturity(self) -> None:
        for matrix_key, matrix in list(self.matrices()):
            if "maturity" in matrix:
                continue
            value = MATURITY.get(matrix_key, DEFAULT_MATURITY)
            anchor = "scope" if "scope" in matrix else next(reversed(matrix), "")
            self.doc["matrices"][matrix_key] = insert_after(matrix, anchor, "maturity", value)
            self.counts[f"F. matrices.{matrix_key}.maturity added ({value})"] += 1
            if matrix_key not in ("person", "facility", "organization", "infrastructure"):
                self.note("matrix", f"matrices.{matrix_key}",
                          "this matrix key is not one of the four the 3.0.0 schema allows",
                          "Remove the matrix or keep it in a separate document.")

    # -- things the tool cannot fix -----------------------------------------

    def report_unmigratable(self) -> None:
        bibliography = self.doc.get("bibliography")
        bad_keys: set[str] = set()
        if isinstance(bibliography, dict):
            for key, entry in bibliography.items():
                if not BIB_KEY.match(key):
                    bad_keys.add(key)
                    self.note(
                        "bibliography-key", f"bibliography.{key}",
                        "the key does not match the 3.0.0 key grammar (uppercase letters and digits in "
                        "hyphen-separated segments, starting with a letter, at least two segments, and "
                        "not in the shape of an IND-, CM-, or RP- ID)",
                        "Rename the key and update every source_refs entry that cites it.",
                    )
                url = entry.get("url") if isinstance(entry, dict) else None
                if url is not None and not (isinstance(url, str) and HTTP_URL.match(url)):
                    self.note(
                        "bibliography-url", f"bibliography.{key}.url",
                        f"value {url!r} is not an http or https URL without whitespace",
                        "Replace it with an http(s) URL, or set it to null.",
                    )
        else:
            self.note("shape", "bibliography", "missing or not an object", "Restore the bibliography object.")
            bibliography = {}

        def walk(node, where: str) -> None:
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == "source_refs" and isinstance(value, list):
                        for ref in value:
                            if not isinstance(ref, str) or not BIB_KEY.match(ref):
                                self.note("source-ref", f"{where}.source_refs",
                                          f"entry {ref!r} does not match the 3.0.0 key grammar",
                                          "Fix the entry to cite a valid bibliography key.")
                            elif ref not in bibliography:
                                self.note("source-ref", f"{where}.source_refs",
                                          f"entry {ref!r} cites no bibliography key",
                                          "Add the bibliography entry or correct the reference.")
                    else:
                        label = node.get("id") if isinstance(node.get("id"), str) else None
                        walk(value, label or f"{where}.{key}")
            elif isinstance(node, list):
                for item in node:
                    walk(item, where)

        walk(self.doc.get("matrices"), "matrices")
        walk(self.doc.get("actor_profiles"), "actor_profiles")

        # Prose that still names an old field: the tool does not edit prose.
        mentions: Counter = Counter()

        def scan(node) -> None:
            if isinstance(node, str):
                for name in OLD_FIELD_NAMES:
                    if name in node:
                        mentions[name] += 1
            elif isinstance(node, dict):
                for value in node.values():
                    scan(value)
            elif isinstance(node, list):
                for item in node:
                    scan(item)

        scan(self.doc)
        scan(self.overlay)
        for name, count in sorted(mentions.items()):
            self.note(
                "prose", "(text values in the framework and overlay)",
                f"{count} text value(s) still mention the old field name '{name}'",
                "Edit the wording by hand to use the 3.0.0 names. This tool does not edit prose.",
            )

    def run(self) -> None:
        self.change_a_schema_version()
        self.change_b_evidence_basis()
        self.change_c_operations()
        self.change_d_compensates_for()
        self.change_e_scores()
        self.change_f_maturity()
        self.report_unmigratable()


def schema_residue(framework, overlay, schema_dir: Path) -> tuple[list[dict], str]:
    """Validate the outputs against the 3.0.0 schemas. Returns (items, status)."""
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry
    except ImportError:
        return [], "skipped (the jsonschema package is not installed)"
    items: list[dict] = []
    ran = []
    for label, document, filename in (
        ("framework", framework, "framework.schema.json"),
        ("overlay", overlay, "scoring-overlay.schema.json"),
    ):
        path = schema_dir / filename
        if not path.exists():
            ran.append(f"{label}: schema not found at {path}")
            continue
        try:
            schema = load_json(path, filename)
            validator = Draft202012Validator(
                schema, format_checker=Draft202012Validator.FORMAT_CHECKER, registry=Registry()
            )
            errors = list(validator.iter_errors(json.loads(json.dumps(document))))
        except Exception as exc:
            ran.append(f"{label}: validation could not run ({exc.__class__.__name__})")
            continue
        ran.append(f"{label}: {len(errors)} schema error(s)")
        groups: dict[tuple, list] = {}
        for error in errors:
            generic_path = "/".join("*" if isinstance(part, int) else str(part) for part in error.absolute_path)
            # One group per missing or unexpected property; other rules group by location.
            variant = error.message if error.validator in ("required", "additionalProperties") else ""
            groups.setdefault((error.validator, generic_path, variant), []).append(error)
        for (keyword, generic_path, _variant), members in sorted(groups.items(), key=lambda kv: str(kv[0])):
            first = members[0]
            location = "/".join(str(part) for part in first.absolute_path) or "(root)"
            items.append(OrderedDict(
                kind=f"schema-{label}",
                where=generic_path or "(root)",
                detail=f"{len(members)} error(s) of rule '{keyword}'; first at {location}: {first.message[:160]}",
                remediation="Not a shape change this tool performs. Correct the value(s) by hand so the "
                            f"document validates against {filename}.",
            ))
    return items, "; ".join(ran)


VALIDATOR_HINTS = {
    "V43": "The overlay needs exactly one tactic_priorities entry per tactic. Add the missing entries "
           "(listed above under tactic-priority) with one of Urgent, Immediate, Priority, Routine.",
    "V35": "Content rule added in 3.0.0. Add the parent tactic's phase to each listed object's "
           "phase_relevance, or move the object to the tactic whose phase it describes.",
    "V20": "The published axis_confidence labels disagree with their own derivation rule for these "
           "indicators. In the overlay, set each listed label to the value the rule derives "
           "(python3 scripts/analysis/derive-axis-confidence.py --print-derived --framework F --overlay O).",
}
VALIDATOR_LINE = re.compile(r"^\S+ \[(V[0-9]+)\] (.*) \(([0-9]+) failure\(s\)\)\s*$")
VALIDATOR_DETAIL = re.compile(r"^\s+\S+ \[(V[0-9]+)\] (.*)$")


def validator_residue(framework, overlay, schema_dir: Path) -> tuple[list[dict], str]:
    """Run the project validator on the outputs; group what still fails."""
    validator = REPO / "scripts" / "lint" / "validate.py"
    if not validator.exists():
        return [], "skipped (scripts/lint/validate.py not found)"
    items: list[dict] = []
    with tempfile.TemporaryDirectory() as tmp:
        framework_path = Path(tmp) / "framework.json"
        overlay_path = Path(tmp) / "scoring-overlay.json"
        framework_path.write_text(json.dumps(framework), encoding="utf-8")
        overlay_path.write_text(json.dumps(overlay), encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(validator), str(framework_path), "--overlay", str(overlay_path),
                 "--schema-dir", str(schema_dir)],
                capture_output=True, text=True, encoding="utf-8", errors="backslashreplace", timeout=600,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return [], f"skipped (validate.py could not run: {exc.__class__.__name__})"
    lines = (result.stdout + "\n" + result.stderr).splitlines()
    first_detail: dict[str, str] = {}
    for line in lines:
        match = VALIDATOR_DETAIL.match(line)
        if match and match.group(1) not in first_detail:
            first_detail[match.group(1)] = match.group(2)
    failed = 0
    for line in lines:
        match = VALIDATOR_LINE.match(line)
        if not match:
            continue
        failed += 1
        check, title, count = match.groups()
        if "JSON Schema" in title:
            continue  # itemized by the schema check above
        items.append(OrderedDict(
            kind=f"validator-{check}",
            where=f"validate.py check {check}: {title}",
            detail=f"{count} failure(s); first: {first_detail.get(check, '(no detail line)')[:200]}",
            remediation=VALIDATOR_HINTS.get(
                check,
                "A content rule, not a shape change. Run scripts/lint/validate.py on the output to list "
                "every failure and correct each by hand.",
            ),
        ))
    if result.returncode not in (0, 1):
        return items, f"validate.py exited {result.returncode} (it could not complete)"
    return items, f"validate.py exit {result.returncode}, {failed} check(s) failing"


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="backslashreplace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(
        description="Migrate a schema 2.1.0 framework document to a 3.0.0 vocabulary document "
                    "plus an experimental scoring overlay. Migrates shape, not content."
    )
    parser.add_argument("input", help="the 2.1.0 framework document")
    parser.add_argument("--out-framework", help="where to write the 3.0.0 vocabulary document")
    parser.add_argument("--out-overlay", help="where to write the scoring overlay")
    parser.add_argument("--report", help="where to write the JSON migration report")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the per-change counts and the manual-work list; write nothing")
    parser.add_argument("--content-version",
                        help="set the content `version` of the output (default: leave it unchanged)")
    parser.add_argument("--schema-dir", default=str(REPO / "docs" / "data"),
                        help="directory holding framework.schema.json and scoring-overlay.schema.json, "
                             "used to list remaining schema errors")
    parser.add_argument("--no-schema-check", action="store_true",
                        help="do not check the outputs against the 3.0.0 schemas and validate.py")
    args = parser.parse_args()

    if not args.dry_run and not (args.out_framework and args.out_overlay):
        print(f"error: {NAME}: give --out-framework and --out-overlay, or use --dry-run", file=sys.stderr)
        return 2
    if args.content_version and not re.match(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z", args.content_version):
        print(f"error: {NAME}: --content-version {args.content_version!r} is not MAJOR.MINOR.PATCH", file=sys.stderr)
        return 2

    try:
        source = load_json(args.input, "input document")
        migration = Migration(source, args.content_version)
        migration.run()
    except InputError as exc:
        print(f"error: {NAME}: {exc}", file=sys.stderr)
        return 2

    schema_status = validator_status = "skipped (--no-schema-check)"
    if not args.no_schema_check:
        try:
            residue, schema_status = schema_residue(migration.doc, migration.overlay, Path(args.schema_dir))
        except InputError as exc:
            residue, schema_status = [], f"skipped ({exc})"
        migration.manual.extend(residue)
        try:
            residue, validator_status = validator_residue(migration.doc, migration.overlay, Path(args.schema_dir))
        except InputError as exc:
            residue, validator_status = [], f"skipped ({exc})"
        migration.manual.extend(residue)

    report = OrderedDict([
        ("tool", NAME),
        ("input", str(args.input)),
        ("source_schema_version", migration.source_schema_version),
        ("target_schema_version", TARGET_SCHEMA_VERSION),
        ("content_version", migration.doc.get("version")),
        ("dry_run", bool(args.dry_run)),
        ("changes", OrderedDict(sorted(migration.counts.items()))),
        ("schema_check", schema_status),
        ("validator_check", validator_status),
        ("manual_remediation", migration.manual),
        ("saved", migration.saved),
        ("scope", "Shape only. No behavioral content, citation, or score was reviewed or changed. "
                  "The overlay is experimental, non-normative, and unvalidated."),
    ])

    print(f"{NAME}: {args.input} (schema {migration.source_schema_version} -> {TARGET_SCHEMA_VERSION})")
    print("Changes:")
    for label, count in sorted(migration.counts.items()):
        print(f"  {count:6d}  {label}")
    print(f"Schema check: {schema_status}")
    print(f"Validator check: {validator_status}")
    if migration.manual:
        by_kind = Counter(item["kind"] for item in migration.manual)
        print(f"Manual remediation needed: {len(migration.manual)} item(s) "
              f"({', '.join(f'{kind} {count}' for kind, count in sorted(by_kind.items()))})")
        for item in migration.manual[:40]:
            print(f"  [{item['kind']}] {item['where']}: {item['detail']}")
            print(f"      fix: {item['remediation']}")
        if len(migration.manual) > 40:
            print(f"  ...and {len(migration.manual) - 40} more (see the report file)")
    else:
        print("Manual remediation needed: none")

    if args.dry_run:
        print("Dry run: nothing was written.")
    else:
        try:
            for path, document in (
                (args.out_framework, migration.doc),
                (args.out_overlay, migration.overlay),
                (args.report, report),
            ):
                if not path:
                    continue
                target = Path(path)
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("w", encoding="utf-8") as handle:
                    json.dump(document, handle, indent=2, ensure_ascii=False)
                    handle.write("\n")
                print(f"wrote {target}")
        except OSError as exc:
            print(f"error: {NAME}: could not write output ({exc.__class__.__name__}: {exc})", file=sys.stderr)
            return 2
    return 1 if migration.manual else 0


if __name__ == "__main__":
    sys.exit(main())
