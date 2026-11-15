# Versioning Policy

Four artifacts in this repository carry their own version numbers. All follow [Semantic Versioning 2.0.0](https://semver.org).

| Artifact | Recorded in | On this branch | Published on `main` |
|---|---|---|---|
| Vocabulary content | `version` in `docs/data/framework.json` | `2.0.0` | `1.7.0` |
| Vocabulary schema | `schema_version` in `docs/data/framework.json`, and `x-schema-version` in `docs/data/framework.schema.json` | `3.0.0` | `2.1.0` |
| Score-free case record | `record_version` in each record (`docs/data/case-record.schema.json`) | `1.0.0` | not yet published |
| Experimental scoring overlay | `overlay_version` in `docs/data/scoring-overlay.json` | `0.1.0` | not yet published |

Content 2.0.0 and schema 3.0.0 are not released. They become the published versions only when the release is announced and tagged under the rules below. Until then the published contract is content 1.7.0 with schema 2.1.0.

The vocabulary content and its schema move independently: a content release can ship without a schema change, and a schema change can ship without new content.

**The overlay and the case record are versioned separately from the vocabulary.** The case record has its own schema and its own version. The scoring overlay has its own version and names the vocabulary version it applies to in `applies_to_framework_version`.

**The scoring overlay is outside the stability promise.** It is experimental and non-normative. Its fields, values, and rules may change or be withdrawn in any overlay release, and no vocabulary release depends on it. Its version is below 1.0.0 for that reason.

**The schema `$id` carries no version.** `https://jgulyash.github.io/THREAT-Matrix/data/framework.schema.json` names the location of the latest published schema, so what it serves changes at each release. To pin a schema version, take the schema file from a release tag.

## What triggers each level

### Vocabulary content (`framework.json`)

- **MAJOR**: a change that consumers must adapt to.
  - Renaming a top-level matrix key
  - Removing a tactic, actor profile, indicator, countermeasure, or response protocol, or changing what an identifier means
  - Restructuring the lifecycle phases
  - Removing or moving a documented field
- **MINOR**: an additive change.
  - New tactics, actor profiles, indicators, countermeasures, or response protocols
  - New optional fields
  - A change of lifecycle state (deprecated or superseded)
  - New `phase_mappings`
- **PATCH**: a correction that does not change meaning.
  - Typo fixes, bibliography corrections, wording that preserves meaning, reordering where order carries no meaning

### Vocabulary schema (`framework.schema.json`)

- **MAJOR**: a previously valid document can now fail.
  - A previously optional field becomes required
  - A field is removed from a closed object, or its type changes
  - An enum value is removed or renamed
  - A pattern or other constraint is tightened
- **MINOR**: additive.
  - New optional fields, new enum values, loosened constraints
- **PATCH**: no effect on validation outcomes.
  - `description` text, reordering of `properties`

**Any change to the schema file changes the schema version.** At the least a PATCH. Two different schema files never carry the same version number. See the record of departures below for why this is stated as a rule.

### Case record schema and overlay

The case record schema follows the same three levels as the vocabulary schema. The overlay follows SemVer for its own number, with the caveat above: while it is below 1.0.0, any release may break.

## Stability promise

A version is published when its commit is on `main` and a release tag exists. A published version is frozen. Any later edit is a new release with a CHANGELOG entry, including a correction to a defect. A tag is never moved.

This promise covers the vocabulary content, the vocabulary schema, the case record schema, and identifiers. It does not cover the experimental scoring overlay, the viewer, the scripts, or the draft study and crosswalk material.

## Identifier stability

Identifiers are never reused, and the guarantee is checked against a committed manifest. See [IDENTIFIERS.md](./IDENTIFIERS.md).

## Deprecation

An object is deprecated or superseded for at least one MINOR release before its content may be removed, and its identifier is never assigned again. See [DEPRECATION.md](./DEPRECATION.md).

## Branches

| Branch | Purpose |
|---|---|
| `main` | Latest published release |
| `v1-build` | Earlier 1.x development |
| `v3-design` | Work toward schema 3.0.0 and content 2.0.0 |

Continuous integration runs every gate on pushes and pull requests for all three.

## Release rules

The project has one maintainer and releases when work is ready, not on a calendar.

- **PATCH** ships as needed.
- **MINOR** ships when a coherent unit of work is complete.
- **MAJOR** is announced at least 30 days before the release tag, with a migration guide. The guide is written against the latest published release and tested on it: the test command and its result are part of the guide. The 30-day clock starts when the announcement is public and the guide passes its test, not before. This matches [GOVERNANCE.md](../GOVERNANCE.md) section 4.

## Major version record

| Artifact | Version | Status | What it contains | Migration guide |
|---|---|---|---|---|
| Vocabulary schema | 3.0.0 | Drafted on `v3-design`. Not announced. The 30-day clock has not started. | Scores removed from the vocabulary: the five indicator score fields, `assessment_guidance.escalation_priority`, and the root `escalation_rubric` and `instance_conditioning` blocks are no longer allowed. `compensates_for` narrowed to countermeasure identifiers, with indicator targets moved to a new `mitigates` relation. `evidence_basis` values renamed. Root `operations` removed. `matrices.<name>.maturity` required. Lifecycle contract added, with `reserved` allowed on actor profiles only. Identifier, key, version, URL, DOI, and date patterns tightened; enums added on actor-profile fields and `phase_name`; four bibliography `type` values removed; `license` fixed to `MIT`; empty or padded text rejected. Indicator field `primary_objective_evidence_tier` removed. The case-record definitions `instance_assessment` and `conditioned_assessment` moved out to the overlay schema. | [migration/2.1-to-3.0.md](./migration/2.1-to-3.0.md) |
| Vocabulary content | 2.0.0 | Drafted on `v3-design`. Ships with schema 3.0.0. | The content changes that schema 3.0.0 requires (scores moved out to the overlay file, the relation split, the renames, `maturity`), two reserved actor-profile stubs, and corrections to sources, `phase_relevance`, and two tactics' guidance. It is a MAJOR because documented fields were removed and moved. | Same guide |

Earlier schema majors: 2.0.0 shipped with content 1.6.0 on 2026-08-08 and closed every object in the schema.

## Record of departures from this policy

These are stated so that a reader comparing the history with the policy does not have to find them.

1. **A schema change without a version change, between 1.7.0 and this branch.** After content 1.7.0 was published, development branches narrowed `compensates_for` to countermeasure identifiers and added the `mitigates` relation while the schema file still declared 2.1.0. That changed schema was never published on `main`, but for a time two different schema files carried the label 2.1.0, and an earlier draft of the 3.0.0 migration guide was measured against the unpublished one. The relation split is now recorded as a breaking change of 3.0.0, the migration guide is written and tested against the published 2.1.0 document, and the rule above (any schema change changes the schema version) exists to prevent a repeat.
2. **Schema 2.1.0 tightened validation as a MINOR.** Schema 2.1.0 (content 1.6.1) added a rule that rejects a case record whose priority is below its band. By the rule above that is a MAJOR. It shipped as a MINOR by a stated exception recorded in the CHANGELOG entry for 1.6.1.
3. **Content label 1.7.1 on development branches.** The label 1.7.1 was used on two development branches for different documents and was never released from `main`. The next published content version after 1.7.0 is 2.0.0.

## Changelog template

Every release adds an entry to `CHANGELOG.md` with this structure. A section is omitted when empty.

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New tactics, actor profiles, indicators, countermeasures, or response protocols
- New schema fields, enum values, or mappings

### Changed
- Changes that are not breaking

### Deprecated
- Objects marked deprecated or superseded in this release, each with its reason
  and the earliest release at which removal would be considered

### Removed
- Content removed after its sunset (the identifier is recorded in the ID manifest)

### Fixed
- Corrections that do not change meaning

### Security
- Any change relevant to the security or privacy of the project or its users
```

A release that changes more than one artifact uses one entry that names each version changed.

## Migration guidance

Every MAJOR release ships a guide under `docs/migration/`. It lists every breaking change with what changed, why, the remediation, and a before and after example, and it reports a test of the remediation on the latest published document. For a MINOR release that adds commonly used fields, the CHANGELOG entry carries a short note.

## Versioning of consumers

The reference consumer, the viewer, and outside consumers are not versioned by this policy. Each consumer states the vocabulary content and schema versions it was tested against.
