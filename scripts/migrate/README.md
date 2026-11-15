# Migration: schema 2.1.0 to schema 3.0.0

`2.1-to-3.0.py` converts one framework document in the published 2.1.0 shape into the two documents that schema 3.0.0 uses:

1. a 3.0.0 vocabulary document, which carries no scores, and
2. an experimental scoring overlay, which holds every score the input carried.

It is for anyone who holds a copy or fork of the 2.1.0 `framework.json` (content version 1.7.0 or earlier on the `main` branch) and wants a document that validates against the 3.0.0 schema. If you only read the published file, you do not need this tool: download the 3.0.0 files instead.

**It migrates shape, not content.** It renames, moves, splits, and drops fields. It does not review, correct, or add any behavioral content, citation, or score. The overlay it writes is labelled experimental, non-normative, and unvalidated, because moving a score to a new file does not validate it.

## Run it

Standard library only. If the `jsonschema` package is installed, the tool also validates its output against the 3.0.0 schemas in `docs/data/`, runs `scripts/lint/validate.py` on it, and lists whatever still fails.

See what would change, writing nothing:

```
python3 scripts/migrate/2.1-to-3.0.py path/to/framework-2.1.json --dry-run
```

Migrate:

```
python3 scripts/migrate/2.1-to-3.0.py path/to/framework-2.1.json \
    --out-framework out/framework.json \
    --out-overlay out/scoring-overlay.json \
    --report out/migration-report.json
```

Then check the result with the project gates:

```
python3 scripts/lint/validate.py out/framework.json --schema-dir docs/data
python3 scripts/lint/validate.py out/framework.json --overlay out/scoring-overlay.json --schema-dir docs/data
python3 scripts/lint/mesh-refs.py out/framework.json
python3 scripts/lint/field-parity.py out/framework.json
```

Options:

| Option | Effect |
|---|---|
| `--dry-run` | Print the count of each change and the manual-work list. Write nothing. |
| `--out-framework PATH` | Where to write the 3.0.0 vocabulary document. |
| `--out-overlay PATH` | Where to write the scoring overlay. |
| `--report PATH` | Where to write the JSON report (counts, manual-work list, anything dropped). |
| `--content-version X.Y.Z` | Set the content `version` of the output. By default it is left unchanged. The overlay's `applies_to_framework_version` always equals the output's `version`. |
| `--schema-dir DIR` | Where to find `framework.schema.json` and `scoring-overlay.schema.json` for the output check. Default: `docs/data`. |
| `--no-schema-check` | Skip the output checks (schemas and `validate.py`). |

Exit codes: `0` migrated and nothing is left for manual work; `1` migrated, and the report lists items that need manual work (the outputs are still written); `2` the input could not be read or is not a 2.x document.

## What it does

Every breaking change between 2.1.0 and 3.0.0:

| | Change | Detail |
|---|---|---|
| A | `schema_version` | Set to `3.0.0`. |
| B | `evidence_basis` values renamed | `operational_primary` to `practice_led`; `hybrid` to `practice_and_literature`; `literature_primary` to `literature_led`. `literature_only` is unchanged. |
| C | Root `operations` dropped | 3.0.0 has no root `operations`. If the array is not empty, its content is saved in the report under `saved.operations`. |
| D | `compensates_for` split | Countermeasure IDs (`CM-...`) stay in `compensates_for`. Indicator IDs (`IND-...`) become edges in a new `mitigates` array on the same countermeasure, each `{"indicator": "<id>", "function": "unreviewed"}`. `compensates_for` is kept even when it ends up empty. |
| E | Scores moved to the overlay | See the table below. |
| F | `matrices.<name>.maturity` added | `core` for `person` and `facility`; `draft` for `organization` and `infrastructure`. An existing value is kept. |

Score moves (change E):

| 2.1.0 location | Overlay location |
|---|---|
| indicator `escalation_axes` | `indicator_scores[<indicator id>].axes` |
| indicator `escalation_weight` | `indicator_scores[<indicator id>].type_weight` |
| indicator `severity_band` | `indicator_scores[<indicator id>].type_band` |
| indicator `severity_floor` | `indicator_scores[<indicator id>].type_band_floor` |
| indicator `axis_confidence` | `indicator_scores[<indicator id>].axis_confidence` |
| tactic `assessment_guidance.escalation_priority` | `tactic_priorities[<tactic id>]` |
| root `escalation_rubric` | `rubric`, with `severity_thresholds` renamed `type_band_thresholds` and `severity_floor_rule` renamed `type_band_floor_rule` |
| root `instance_conditioning` | `instance_conditioning` |

The overlay header is written with `status: experimental`, `normative: false`, `validation_status: unvalidated`, `scope: type_level`, `not_a_risk_score: true`, and the standard notice.

Key order and all other content are preserved. `mitigates` is placed directly after `compensates_for`; `maturity` directly after `scope`.

## What it does not do

- **It does not change content.** No behavior text, guidance, citation, relationship, or score value is reviewed or edited.
- **It does not edit prose.** Text values that mention an old field name (for example "severity_band" inside the rubric wording) are left as they are and listed in the report under `prose`.
- **It does not assign a `function` to migrated `mitigates` edges.** Every migrated edge is `unreviewed`. Choosing `prevent`, `detect`, or `deny` is a review decision.
- **It does not touch `actor_profile.v2_tactic_associations`.**
- **It does not set the content `version`** unless you pass `--content-version`.
- **It does not add reserved actor-profile stubs** for gaps in the `AP` numbering, and it does not write an ID manifest. Use `scripts/lint/id-manifest.py` for that.
- **It does not migrate case records.** A 2.1.0 `conditioned_assessment` record is a scored record; in 3.0.0 its field `type_severity_band` is named `type_band` and the record validates against `scoring-overlay.schema.json`. The default 3.0.0 case record is score-free (`docs/data/case-record.schema.json`) and has to be written, not converted.
- **It does not fix what the tightened 3.0.0 schema rejects for content reasons.** Those are listed, each with a suggested fix:
  - a bibliography key or `source_refs` entry that does not match the key grammar;
  - a bibliography `url` that is not an `http` or `https` URL;
  - a bibliography `type` or any other enumerated value that 3.0.0 no longer allows;
  - a required field that the input never had;
  - a `compensates_for` value that is neither a countermeasure ID nor an indicator ID (removed and listed);
  - an indicator with no score or an incomplete score (a partial overlay entry is invalid).

The list is printed, and written in full to the `--report` file under `manual_remediation`. Each item has a `kind`, a `where`, a `detail`, and a `remediation`.

## Result on the published 2.1.0 document

Run against `docs/data/framework.json` from the `main` branch (content 1.7.0, schema 2.1.0), the tool performs these changes: 1 `schema_version`; 122 `evidence_basis` renames (111, 10, and 1); 1 root `operations` dropped; 476 indicator references moved from `compensates_for` into `mitigates` edges on 283 countermeasures, with 360 countermeasure references kept; scores moved for 828 indicators (43 with a floor) and 159 tactic priorities; the rubric and the instance-conditioning block moved; 4 `maturity` values added.

Against the 3.0.0 schema the published document has 1,596 errors before migration. After migration, 5 schema errors and 2 failing validator checks remain. All of them are content problems in the published document that 3.0.0 checks and 2.1.0 did not, and each is listed by the tool with a suggested fix:

| Remaining item | Count | Manual fix |
|---|---|---|
| A bibliography entry has a `type` that 3.0.0 no longer allows | 1 | Give the entry an allowed `type`, or remove the entry and the references to it. |
| Two tactics (one organization, one infrastructure) lack `assessment_guidance.false_positive_context` and `threshold_guidance` | 4 | Write the two missing guidance fields for each tactic. |
| `phase_relevance` on an indicator or countermeasure omits its parent tactic's phase (validator check V35) | 72 | Add the parent tactic's phase to `phase_relevance`, or move the object. |
| `axis_confidence` labels in the overlay disagree with their derivation rule (validator check V20) | 12 | Set each label to the value `scripts/analysis/derive-axis-confidence.py --print-derived` gives. |
| Text values that still mention an old field name | 7 groups | Edit the wording. Not a validation failure. |

With those corrected by hand, the migrated pair passes `validate.py` with and without the overlay, `mesh-refs.py`, and `field-parity.py`. The tool never makes these corrections itself, because each is a content decision.

Reproduce the list with:

```
git show origin/main:docs/data/framework.json > /tmp/framework-2.1.json
python3 scripts/migrate/2.1-to-3.0.py /tmp/framework-2.1.json --dry-run
```
