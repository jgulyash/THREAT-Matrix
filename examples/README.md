# Examples

Starting points for using the THREAT Matrix open vocabulary: a score-free case record with a worksheet and fictional worked cases, a small reference consumer, and, last and labelled, examples for the experimental scoring overlay.

The framework publishes vocabulary and record formats only. It ships no real case data, and the public site has no place to enter any. Keep real records in your own case system.

## What is here

| Path | What it is |
|---|---|
| `case-record-template.json` | A placeholder score-free case record, valid against `docs/data/case-record.schema.json`. Copy it and replace every `REPLACE` value. |
| `case-record-worksheet.md` | A practitioner worksheet for the same record. Opens with the limitations and intended-use box. |
| `worked-cases/` | Five fictional score-free case records (`case-1` to `case-5`) and a README that walks through each one. |
| `python_consumer.py` | Reference consumer in Python. Loads `framework.json`, validates it against its schema, and prints a summary with simple filters. |
| `experimental-scoring/` | **Experimental, non-normative.** One scored-record template, three fictional scored records, and a README that starts with the overlay notice. Not needed for anything above. |

## The score-free case record

This is the default record. It documents what was observed, where the information came from, the six instance factors, protective factors, the assessor's judgment, dated reassessments in either direction, and a disposition. It holds no score, band, weight, or priority, and its schema is closed so one cannot be added.

Before using it, read the limitations box at the top of `case-record-worksheet.md`. In short: the vocabulary does not predict violence; an indicator describes a kind of behavior, not a person; the record is not grounds for adverse action by itself; each person is assessed individually; protective factors and context are always considered; sources are always documented. The individual is called the person of concern.

The five worked cases cover:

| Case | Shows | Disposition |
|---|---|---|
| 1 | A report checked and fully explained | `no_threat_identified` |
| 2 | An angry remark with no sustained intent | `transient_no_further_action` |
| 3 | Concern lowered as a benign explanation and protective factors emerge | `closed_benign` |
| 4 | Concern raised over time on corroborated observations | `heightened_monitoring` |
| 5 | Concern raised, an interdiction, concern lowered afterwards | `disrupted_by_interdiction` |

## How to validate each file

Run these from the repository root. `pip install jsonschema` first.

**Everything in this folder at once.** The consumer smoke test validates the framework and the overlay against their schemas, every file in `examples/worked-cases` against `case-record.schema.json`, every file in `examples/experimental-scoring/worked-cases` against the scored-record definition, and both templates:

```bash
python3 scripts/lint/consumer-smoke.py
```

**One score-free record of your own:**

```bash
python3 - <<'PY' examples/case-record-template.json
import json, sys
from jsonschema import Draft202012Validator, FormatChecker
schema = json.load(open("docs/data/case-record.schema.json"))
record = json.load(open(sys.argv[1]))
errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record))
for e in errors:
    print("INVALID:", "/".join(map(str, e.path)) or "(record)", "-", e.message)
print("valid" if not errors else f"{len(errors)} error(s)")
sys.exit(1 if errors else 0)
PY
```

The schema checks the form of each indicator ID. To confirm the IDs exist, look them up in `docs/data/framework.json` at the `framework_version` the record states.

**The experimental scored records:**

```bash
python3 scripts/lint/validate.py docs/data/framework.json --overlay docs/data/scoring-overlay.json --records examples/experimental-scoring/worked-cases
```

**The data these examples depend on.** The full set of project gates:

```bash
python3 scripts/lint/validate.py docs/data/framework.json
python3 scripts/lint/validate.py docs/data/framework.json --overlay docs/data/scoring-overlay.json
python3 scripts/lint/validate.py docs/data/framework.json --fixtures scripts/lint/fixtures
python3 scripts/lint/validate.py docs/data/framework.json --overlay docs/data/scoring-overlay.json --records examples/experimental-scoring/worked-cases
python3 scripts/lint/field-parity.py docs/data/framework.json
python3 scripts/lint/mesh-refs.py docs/data/framework.json
python3 scripts/lint/id-manifest.py --check docs/data/framework.json docs/data/id-manifest.json
python3 scripts/lint/consumer-smoke.py
```

## Running the reference consumer

```bash
pip install jsonschema
python3 examples/python_consumer.py
```

Common flags:

```bash
# Show all Phase 1 tactics
python3 examples/python_consumer.py --phase 1

# Show all tactics associated with actor profile AP005
python3 examples/python_consumer.py --actor AP005

# Validate a different framework.json against the schema
python3 examples/python_consumer.py --framework /path/to/your/framework.json

# Skip schema validation while iterating on draft content
python3 examples/python_consumer.py --no-validate
```

The consumer uses only the standard library plus `jsonschema`. No helper library is needed: the JSON shape and the published schemas are the contract.

## Build your own consumer

A consumer is anything that loads `framework.json`, optionally validates it against `framework.schema.json`, and does something useful. You can rely on:

- Identifiers that stay stable across releases (see [IDENTIFIERS.md](../docs/IDENTIFIERS.md)).
- A schema that is versioned separately from the content (see [VERSIONING.md](../docs/VERSIONING.md)).
- Deprecated and superseded items marked with `lifecycle_state` (see [DEPRECATION.md](../docs/DEPRECATION.md)).

Common shapes:

- **Case management integrations.** Store score-free case records in your own system and look up indicator wording, false-positive context, and response protocols by ID.
- **Training and case-discussion references.** Filter tactics and indicators by matrix, phase, or Behavioral Mode (indicator `modality`) for team use.
- **Search and retrieval indexes.** Index tactic and indicator text by stable identifier; re-index when the text changes (see the CHANGELOG).
- **Mapping bridges.** Use `phase_mappings` to line up THREAT Matrix phases with the stage names of other published models. The mappings are stage and tactic names, not external technique identifiers.

The People and Facilities matrices are the core. The Organizations and Infrastructure matrices are labelled draft (`matrices.<name>.maturity`); treat them accordingly.

## Experimental scoring (optional, non-normative)

`experimental-scoring/` holds examples for the scoring overlay. The overlay is experimental, type-level, and unvalidated. It is not a risk score and must not be used as grounds for adverse action. Read `experimental-scoring/README.md` before opening anything in that folder. Nothing else in `examples/` depends on it.

## Submit your consumer

Open a pull request that adds your consumer to the Consumers section of the top-level [README.md](../README.md). Include: name, language, link, one-sentence description, and the framework version it was tested against.
