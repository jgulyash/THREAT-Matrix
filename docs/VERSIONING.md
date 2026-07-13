# Versioning Policy

THREAT Matrix is a published open standard. Two artifacts in this repository are versioned independently:

| Artifact | Versioned at | Current |
|---|---|---|
| **Framework content** | `version` in `docs/data/framework.json` | `1.3.0` |
| **JSON Schema** | `schema_version` in `docs/data/framework.json` and the `$id` of `docs/data/framework.schema.json` | `1.3.0` |

Both follow [Semantic Versioning 2.0.0](https://semver.org). They move independently — a content release can ship without a schema bump, and vice versa.

## What triggers each level

### Framework content (`framework.json`)

- **MAJOR** — breaking changes to the taxonomy that downstream consumers must adapt to:
  - Renaming a top-level matrix key
  - Renaming or removing a tactic, actor profile, indicator, countermeasure, or response protocol identifier
  - Restructuring the Threat Lifecycle phases (count, ordering, semantics)
  - Removing a documented field that consumers may have depended on
  - Changing the meaning of an existing identifier
- **MINOR** — additive changes that do not break existing consumers:
  - New tactics, actor profiles, indicators, countermeasures, or response protocols
  - New optional fields with documented defaults
  - New entries in an `enum` field (consumers should ignore unknown values)
  - New cross-framework `phase_mappings`
  - Authoring of previously empty mandatory fields on existing identifiers
- **PATCH** — corrections that do not change semantics:
  - Typo fixes
  - Bibliography metadata corrections
  - Description tightening that preserves meaning
  - Re-ordering of array elements where order is not semantic

### JSON Schema (`framework.schema.json`)

- **MAJOR** — the JSON shape changes in a way that breaks validation of previously valid documents:
  - A previously optional field becomes required
  - A field's allowed type changes (e.g., string → array)
  - A previously valid enum value is removed
- **MINOR** — additive shape changes:
  - New optional fields
  - New enum values
  - Loosened constraints (e.g., a regex becomes more permissive)
- **PATCH** — clarifications that do not affect validation outcomes:
  - `description` text updates
  - Re-ordering of `properties` (when the document model is unaffected)

A content MAJOR bump implies a schema MAJOR bump if and only if the breaking content change requires a corresponding shape change. Content MAJOR bumps that only rename identifiers within an existing field structure do not require a schema bump.

## Stability promise

Once a version is published — meaning the commit is pushed to `main` and a release tag exists — the artifacts at that version are **frozen**. Subsequent edits create a new release. This includes patch releases: a `1.1.0` document does not silently become a different `1.1.0` document.

If a published release contains a defect that requires correction, the correction ships as a new patch release with a CHANGELOG entry describing what was wrong.

## Identifier stability

See [IDENTIFIERS.md](./IDENTIFIERS.md). Summary: identifiers are never reused. A removed or retired identifier remains reserved.

## Deprecation discipline

See [DEPRECATION.md](./DEPRECATION.md). Summary: items are deprecated for at least one MINOR release before any consideration of content removal, and the identifier itself is preserved indefinitely.

## Branches

| Branch | Purpose |
|---|---|
| `main` | Latest published release |
| `v1-build` | V1.x in-progress work |
| `vN-design` | Pre-major-bump design work for future major version `N` |

Major-version development happens on a dedicated branch so that minor and patch releases on the current major can ship without contamination. This mirrors the OpenAPI 4.x ("Moonwalk") pattern.

## Release cadence

THREAT Matrix is solo-maintained and releases when content is ready, not on a fixed calendar. The discipline:

- **PATCH** ships as needed
- **MINOR** ships when a coherent unit of work (a matrix slice, a contract addition) is complete
- **MAJOR** is pre-announced at least 30 days before the release tag, with a migration guide and a side-by-side example available

## Changelog template

Every release adds an entry to `CHANGELOG.md` (created at first release after V1.1) using this fixed structure:

```markdown
## [X.Y.Z] — YYYY-MM-DD

### Added
- New tactics / actor profiles / indicators / countermeasures / response protocols
- New schema fields, enum values, or mappings

### Changed
- Behavioral changes that are not breaking

### Deprecated
- Items marked `lifecycle_state: deprecated` or `superseded` this release
- Pointer to DEPRECATION.md for sunset rules

### Removed
- Content removed after the deprecation window expired (the identifier
  remains reserved)

### Fixed
- Typo / metadata / clarity corrections that do not change meaning

### Security
- Any change relevant to security posture of the framework or its consumers
```

Each section is omitted when empty. The same structure is used for both content and schema releases; a release that bumps only one artifact still uses one CHANGELOG entry covering the version bumped.

## Migration guidance

For MAJOR releases, a `docs/migration/X.Y-to-X+1.0.md` document ships with the release. It enumerates every breaking change, the remediation, and a worked example. For MINOR releases that change defaults or add commonly relied-upon fields, the CHANGELOG entry includes a brief migration note inline.

## Versioning of consumers

The reference consumer (`examples/python_consumer.py`), the SPA, and any community consumers are not versioned by this policy. Each consumer pins the framework content and schema versions it has been tested against, and is responsible for its own release cadence.
