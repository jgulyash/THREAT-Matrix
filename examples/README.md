# Examples

Minimum viable consumers for the THREAT Matrix open standard. Use these as starting points; build your own.

## Files

| File | What it does |
|---|---|
| `python_consumer.py` | Reference consumer in Python. Loads `framework.json`, validates against `framework.schema.json`, demonstrates phase and actor-profile filters, prints a structured summary. |
| `instance-record-template.json` | A schema-valid, fillable `conditioned_assessment` record (all six instance factors defaulted to `unknown`, held at type). Copy it, fill it per the worksheet. |
| `instance-record-worksheet.md` | One-page printable analyst worksheet: the six factors as questions with the enum options as checkboxes, the escalate-only rule, the raise-guidance patterns, and the Q1 demotion doctrine. |
| `worked-cases/` | Three fictional end-to-end walk-throughs (held at type, raised one band, raised to critical) showing the instance-conditioning contract in use. |

## Instance conditioning: the framework ships no case data

The framework defines the instance-conditioning contract (`$defs.instance_assessment`, `$defs.conditioned_assessment`) but ships **zero instances** — it is a type-level artifact. A type score is not a case assessment until it is joined to an instance record.

The reference SPA (the public site) displays only type-level taxonomy and **must never invite real case data**: it is a static public site with no place to hold it safely. The interactive instance-entry surface is therefore deferred to V2, where it ships with the SDKs, which have a legitimate consumer-side home for case data. In the meantime the zero-liability affordance is the pair above — `instance-record-template.json` and `instance-record-worksheet.md` — plus the worked cases. They let an analyst condition a score by hand, on their own system, without the framework or its public site ever holding a case record.

## Running the reference consumer

From the repository root:

```bash
pip install jsonschema
python3 examples/python_consumer.py
```

Common flags:

```bash
# Show all Phase 1 (Target Development) tactics
python3 examples/python_consumer.py --phase 1

# Show all tactics associated with actor profile AP005
python3 examples/python_consumer.py --actor AP005

# Validate a custom framework.json against the schema
python3 examples/python_consumer.py --framework /path/to/your/framework.json

# Skip schema validation (useful if you're iterating on draft content)
python3 examples/python_consumer.py --no-validate
```

## What this example demonstrates

1. **The contract works end-to-end.** The reference consumer loads the canonical artifact, validates it against the published schema, and produces useful output. If this consumer runs cleanly, your own consumer can rely on the same contract.
2. **Filters are minimal but representative.** Phase filtering (Threat Lifecycle stage) and actor-profile filtering are the two most common access patterns. Other filters — by matrix, by Behavioral Mode (indicator `modality`), by tactic family, by indicator category, by countermeasure domain — follow the same shape.
3. **No framework-specific helper library is required.** The consumer uses only the standard library plus `jsonschema`. THREAT Matrix consumers do not need a SDK; the JSON shape and the published schema are the SDK.

## Build your own consumer

A consumer is anything that loads `framework.json`, optionally validates against `framework.schema.json`, and does something useful. The contract guarantees that:

- Identifiers are stable across releases (see [IDENTIFIERS.md](../docs/IDENTIFIERS.md))
- The schema versions independently from the content (see [VERSIONING.md](../docs/VERSIONING.md))
- Deprecated and superseded items are surfaced via `lifecycle_state` (see [DEPRECATION.md](../docs/DEPRECATION.md))

Common consumer shapes:

- **Detection rule generators.** Walk indicators and emit Sigma, YARA, KQL, or SIEM-native rules.
- **Vector indexers.** Embed tactic and indicator descriptions for retrieval-augmented generation. Index by stable identifier; re-index when the description text changes (see CHANGELOG).
- **Mapping bridges.** Use `phase_mappings` to translate between THREAT Matrix and MITRE ATT&CK / D3FEND / ATLAS / NTAC pathway / Calhoun-Weston / CERT insider stages.
- **Operational composers.** Filter by phase, actor profile, and detection source to assemble situational playbooks. The V2 platform release will ship one of these as a reference.
- **Case management integrations.** Enrich existing case records with the framework's response-protocol scaffolding via `RP-####-##` lookups.

## Submit your consumer

Open a pull request that adds your consumer to the [Consumers section in README.md](../README.md#consumers). Include: name, language, link, one-sentence description, and the framework version your consumer has been tested against.
