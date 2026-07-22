# Architect: `target_identity` Sub-Dimension + Schema Additive Patch

Structural design and draft JSON Schema fragments for Jay's enriched-Option-2 framing. Read-only on `framework.json` and `framework.schema.json`; this document delivers the patch as draft fragments for committer review.

Schema baseline read: `docs/data/framework.schema.json` (schema_version 1.2.1). Key relevant facts for the patch:
- `matrices` uses `patternProperties` on `^(person|facility|organization|system)$`, no `additionalProperties: false` anywhere — additive properties are non-breaking.
- `indicators[*].correlates_with` is already an unrestricted `array of strings` — cross-matrix IND references are already structurally supported (no schema work needed for the Detection Mesh cross-matrix path).
- The four escalation axes are `impact_potential`, `blast_radius_potential`, `recoverability_inverse`, `detectability` — names matter for A.5.

---

## A) `target_identity` Sub-Dimension Design

### A.1 — Field name and value names

Pin: **field name `target_identity`**, values **`named_individual` / `role_or_identity_category` / `affinity_group` / `indiscriminate`**.

I am keeping Jay's candidate names with one refinement: `role_category` → `role_or_identity_category`. The reason is that "role" alone reads as occupational (cop, judge, journalist) and quietly drops the non-occupational identity-categories that belong here (clinic patient, transit rider). "Role or identity category" preserves the cop-by-uniform case while making room for the broader pattern of "targeted because of what they are, not who." The other three names are already distinct, self-explanatory, and mutually exclusive in the common case, and `indiscriminate` is the conventional term-of-art in the literature for what's meant here.

### A.2 — Boundary rule between `affinity_group` and `indiscriminate`

**Tie-breaker rule (analyst-facing):** Ask whether the adversary's targeting was constrained by a group property — demographic, religious, ethnic, occupational, ideological, or locational-affinity (e.g., "patrons of this clinic"). If the targeting filter is *any* such property (even one applied loosely, like "anyone visibly Jewish in this neighborhood"), it is `affinity_group`. If the targeting filter is purely proximity or presence with no group property selecting the location either (e.g., random crowd, generic public space chosen for foot traffic alone), it is `indiscriminate`.

Applied to Jay's examples: "Anyone at this mall" → if the mall was selected for foot traffic with no demographic filter, `indiscriminate`; if the mall was selected because of its patron demographic (a community-specific mall, an LGBTQ-frequented venue), `affinity_group`. "Jews at this synagogue" → `affinity_group` (the location was selected *because of* its affinity property). The rule reduces to a single field-deployable question: *did a group property select either the people or the location?* Yes → affinity. No → indiscriminate.

### A.3 — Attachment location in the schema

**Attach `target_identity` at the indicator level, not the tactic level.**

The reason is that the same person-matrix tactic routinely spans multiple identity categories. "Hostile surveillance" can be conducted against a named protectee (named_individual), against a class of personnel (role_or_identity_category), against a religious community (affinity_group), or against generic crowd flow (indiscriminate) — and the indicator pattern shifts meaningfully across those cases (surveillance of a named target has different temporal and detectability signatures than crowd surveillance). Forcing one `target_identity` per tactic would either over-constrain authors or push them to duplicate tactics by identity category, which is the splitting the sub-dimension was designed to avoid. Per-indicator granularity lets a single tactic cleanly cover all four identity cases through its indicator catalog.

### A.4 — Backward-compat for the 34 already-authored person-matrix tactics

**Make `target_identity` optional in the schema; do not gate chunk-1 commit on retroactive tagging.** The 34 existing tactics and their indicators ship untagged, and the field begins populating from chunk-2 forward as new and revisited indicators are authored. This is the lighter-weight backward-compat path: untagged existing content remains schema-valid because the field is optional, the renderer treats missing `target_identity` as "unspecified" (no badge, no filter contribution), and the field becomes a coverage-growth metric rather than a coverage-blocking gate.

A complementary optional convention — strongly recommend but not require — is that any indicator newly authored or revised after V1.2.2 ships *should* carry `target_identity`. That gives the field a forward-only adoption curve without a flag-day backfill. A coverage report (% of person-matrix indicators with `target_identity` populated) becomes the natural progress metric for chunk-3 / chunk-4 work.

### A.5 — Interaction with existing `escalation_axes`

There is **no automatic coupling** between `target_identity` and `escalation_axes`; the axes remain independently authored per-indicator. But there is a **typical correlation worth documenting** in the rubric guidance: `indiscriminate` indicators tend to score higher on `blast_radius_potential` than `named_individual` indicators within the same tactic, because the type-level harm scope is broader when targeting is unconstrained. Similarly, `affinity_group` indicators often carry elevated `impact_potential` relative to `named_individual` for the same tactic when the group's collective harm exposure is structurally larger.

The rule is: `target_identity` is a *descriptor* of who the indicator class targets; `escalation_axes` are *consequences* the framework scores independently. Authors should not derive axes from identity, but reviewers should treat axis values that contradict the typical correlation (e.g., `indiscriminate` indicator with low `blast_radius_potential`) as a review prompt — usually either the axis is mis-scored or the indicator is genuinely an exception worth a `field_notes` line. This keeps the two fields orthogonal in the schema while giving reviewers a usable consistency heuristic.

---

## B) Schema Additive Patch Draft

All three fragments below are **purely additive** (new optional properties). Recommended bump: **schema_version 1.2.2** — additive patches following the established Session 24 / V1.2.1 convention. A 1.3.0 bump would be appropriate only if these patches landed alongside a minor-version content release; on their own they are SemVer-PATCH.

### B.1 — `matrices.{matrix}.scope` field

```json
// PATCH SITE: properties.matrices.patternProperties["^(person|facility|organization|system)$"].properties
// Adds an optional "scope" string holding the canonical scope sentence for each matrix.
// Backward-compat: optional. Existing matrices without scope remain schema-valid.

"scope": {
  "type": "string",
  "description": "Canonical scope sentence for this matrix, expressed in WHAT/WHY/WHERE terms. Defines the primary adversary objective that places a tactic in this matrix at authoring time. Type-level field; not case-specific. See matrices.boundary_rule for the framework-vs-operational distinction."
}
```

**Scope sentence text for all four matrices** (consistent with Jay's WHAT/WHY/WHERE principle — matrix is set by WHAT, motivation lives in actor profiles, setting is WHERE for non-People matrices):

- **person.scope:** *"Tactics centered on one or more human beings as the primary target. The adversary's primary objective is harm, control, coercion, or surveillance directed at people. Setting and motivation are separate dimensions and do not change matrix placement."*
- **facility.scope:** *"Tactics centered on a physical venue, structure, or built environment as the primary target. The adversary's primary objective is damage, destruction, denial, or symbolic action against the place itself. Incidental human harm in an unoccupied facility does not move the tactic to People."*
- **organization.scope:** *"Tactics centered on an institution, mission, brand, or operational continuity as the primary target. The adversary's primary objective is disruption, delegitimization, infiltration, or coercion of what the organization does or represents, distinct from its facilities or its individuals."*
- **system.scope:** *"Tactics centered on infrastructure or technical systems as the primary target. The adversary's primary objective is disruption, degradation, or compromise of the system's function — physical infrastructure, cyber-physical systems, or critical service delivery. Cyber-Physical Nexus tactics are tagged via the `cpn` field on tactic."*

Recommend: **optional** in the schema; **mandatory by editorial convention** for V1.2.2 release (all four matrices populated at the same time, since the four sentences ship together as a single conceptual unit).

### B.2 — `matrices.boundary_rule` field at the container level

```json
// PATCH SITE: properties.matrices.properties (new sibling alongside patternProperties)
// Adds an optional "boundary_rule" string on the matrices container itself
// holding the framework-vs-operational principle.
// Backward-compat: optional. Existing framework.json without boundary_rule remains schema-valid.

"boundary_rule": {
  "type": "string",
  "description": "Framework-vs-operational boundary principle governing matrix placement. Authoring-time: one matrix per tactic, set by the adversary's primary objective. Operational-time: real incidents may invoke tactics from multiple matrices via Detection Mesh cross-references (correlates_with at the indicator level). Type-level statement of the framework's organizing principle."
}
```

**Boundary-rule text:**

*"Each tactic in this catalog is placed in exactly one matrix, determined by the adversary's primary objective at authoring time. Motivation and setting are separate dimensions and live in actor profiles and field notes, not in matrix placement. Real-world incidents may legitimately invoke tactics from multiple matrices simultaneously; cross-matrix coverage is expressed through the Detection Mesh via indicator `correlates_with` references rather than by re-classifying tactics."*

Recommend: **optional** in the schema; **mandatory by editorial convention** for V1.2.2 release.

**Schema-shape note:** Because `matrices` currently uses `patternProperties` without an explicit `properties` block, adding a non-pattern key requires either adding a sibling `properties: { boundary_rule: {...} }` *and* keeping `patternProperties` (JSON Schema supports both — `properties` checked first, then `patternProperties`), or modeling `boundary_rule` as a fifth pattern alternative (rejected — it isn't a matrix). The `properties` + `patternProperties` co-existence path is the clean one and is what the fragment above assumes.

### B.3 — `target_identity` field at the indicator level

```json
// PATCH SITE: $defs.indicator.properties
// Adds an optional "target_identity" enum on each indicator.
// Backward-compat: optional. Per A.4, the 34 existing person-matrix tactics
// and their indicators ship untagged; the field begins populating from
// chunk-2 forward.

"target_identity": {
  "type": "string",
  "enum": [
    "named_individual",
    "role_or_identity_category",
    "affinity_group",
    "indiscriminate"
  ],
  "description": "Type-level sub-dimension within the People matrix describing the identity-class the indicator targets. Optional; primarily meaningful for person-matrix indicators. named_individual = specific known person (assassination, stalking, kidnapping of a known target). role_or_identity_category = targeted because of what they are, not who (cops by uniform, journalists, clinic staff). affinity_group = group property selects the people or location (demographic, religious, ethnic, locational-affinity). indiscriminate = no group property filter (random crowd, generic public space). Boundary rule between affinity_group and indiscriminate: did a group property select either the people or the location? See architect design A.2."
}
```

**Where it attaches:** `$defs.indicator.properties` only (per A.3 — per-indicator granularity, not per-tactic).

**Required vs optional:** **optional** in the schema (per A.4); editorially encouraged for all newly-authored person-matrix indicators from chunk-2 forward.

**Schema_version bump:** **1.2.2** for all three patches together. They are additive, non-breaking, and follow the V1.2.1 Session 24 four-additive-patch precedent.

---

## C) Backward-Compat Sanity Check

All three patches are purely additive: new optional properties only, no enum tightenings, no `required` additions, no removed fields, no changes to existing field types. The 34 already-authored person-matrix tactics and all their indicators remain schema-valid without any rewriting — `scope` and `boundary_rule` populate at the framework level (one-time authoring), and `target_identity` is per-indicator-optional with forward-only adoption from chunk-2. The chunk-1 commit is unblocked: it ships the schema patch (1.2.2) plus the four `matrices.{name}.scope` sentences plus `matrices.boundary_rule`, with zero changes to existing tactic or indicator content. The Detection Mesh cross-matrix mechanism needs **no additional schema work**: `$defs.indicator.properties.correlates_with` is already `array of strings` with no pattern constraint on the referenced IDs, so cross-matrix IND-XXXX-YY references are already structurally supported. The only adjacent work this surfaces is editorial: the `detection_mesh.principle` and `detection_mesh.axes[name=cross_matrix].description` prose strings should be reviewed for consistency with the new `matrices.boundary_rule` text in the same release, but those are content edits not schema changes.
