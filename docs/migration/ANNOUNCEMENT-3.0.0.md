# Announcement: THREAT Matrix schema 3.0.0

Announced: ANNOUNCED_ON. Earliest release tag: EARLIEST_TAG.

Schema 3.0.0 is a MAJOR release. Documents that validate against schema 2.1 may fail against 3.0. Per our versioning policy, the release tag will not be cut before EARLIEST_TAG, 30 days after this announcement. Schema 2.1 remains the published version on `main` until then.

The release carries four breaking changes:

1. **evidence_basis values renamed.** `operational_primary` becomes `practice_led`, `hybrid` becomes `practice_and_literature`, `literature_primary` becomes `literature_led`, and `literature_only` is unchanged. The field name stays the same. For authoring method, see METHODOLOGY.md.
2. **Lifecycle contract.** Tactics, actor profiles, indicators, countermeasures, and response protocols gain optional `lifecycle_state`, `deprecated_in`, `superseded_by`, and `reserved_reason` fields. A per-release ID manifest format is added.
3. **Tightening.** Patterns on bibliography keys, `source_refs`, `related_tactics`, `version`, and `schema_version`; enums on seven actor-profile fields; consistency rules for severity floors and crossing mechanisms.
4. **Unused stubs.** The root `operations` key is removed. `v2_tactic_associations` becomes optional with typed items.

No identifiers change. For the canonical document the data changes are mechanical.

The migration guide lists every change with remediation steps, before and after examples, validation results, and a consumer checklist: [docs/migration/2.1-to-3.0.md](./2.1-to-3.0.md).

Questions and objections are welcome during the 30-day window.
