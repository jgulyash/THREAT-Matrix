# CHANGELOG

All notable changes to THREAT Matrix are documented here, per [VERSIONING.md](docs/VERSIONING.md).

This project adheres to [Semantic Versioning](https://semver.org). Framework
content and JSON Schema are versioned independently; the framework content
and JSON Schema are both at `1.2.2` as of the latest release.

## [Unreleased]

### Added

- **Actor-profile filter in the matrix browser.** The FilterBar's Actor
  control is now live: a category-grouped dropdown that filters the heat
  map and phase panels to tactics associated with a selected actor
  profile, composing with the CPN filter. Completes the filter set the
  V1.1 matrix browser described.

- **Full escalation scoring across the People matrix (B-05).** All 190
  indicator classes across all four phases now carry a `temporal_signature`,
  four `escalation_axes`, a computed `escalation_weight`, and a `severity_band`
  (up from the 23-indicator phase-1 pilot). Blast is authored to method-revealed
  collateral ceilings per escalation_rubric v1.1.0: it rises to a method's
  mass-casualty ceiling only where a behavior reveals or presages that method,
  so recon and profiling keep moderate blast while capability acquisition and
  force application escalate. The severity band, previously degenerate
  (20 high / 3 medium / 0 critical on the pilot), now spans **56 medium /
  128 high / 6 critical**. The six criticals are the mass-casualty Force
  Application behaviors (explosive 8.68, vehicle-ramming 8.18, weapon discharge
  8.00) and the method-revealing capability acquisitions (IED-construction
  research 8.48, straw purchase 7.82, weapons-in-quantity 8.00). Aftermath
  behaviors top out at high (impunity, recurrence, ongoing coercive leverage);
  no aftermath behavior is critical, since the mass-casualty event is past.

### Added

- **`target_identity` populated matrix-wide.** The per-indicator People-matrix
  identity-class field now covers all 190 indicators (up from the 23-indicator
  chunk-1 pilot), and every tactic carries a `target_identity_scope` (34/34).
  Authoring convention: a behavior carries `indiscriminate` unless it inherently
  requires a specific known subject — so only target-selection and subject-
  profiling behaviors are narrowed (named/role/affinity, no indiscriminate);
  every other behavior carries all four sub-classes. This is a reproducible
  compatibility reading rather than a subjective "characteristic target" call.
  Two pre-existing tactic scopes corrected: TM0303 (Objective Seizure) and
  TM0304 (Captive Control) gain `role_or_identity_category` — role-based
  kidnapping (a judge, a diplomat, an executive taken for their position) is
  real, so seizure and captivity span all four identity-classes.

### Changed

- **Collateral-reveal blast policy documented and reconciled.** The blast_radius
  authoring rule — raise blast above the single-victim floor only where the
  behavior itself observably reveals a group/population target or a public/crowd
  venue (the parallel to method-revealed) — is now a first-class, reusable rule
  in `escalation_rubric.blast_radius_guidance.collateral_reveal_guidance`, with
  graduated tiers and an explicit deferral of unrevealed-venue collateral to the
  instance layer. One consistency fix (`IND-0206-01` line-of-sight to a
  gathering: blast 3.5 → 4.5 to match its sibling). The policy adds no criticals
  by design: critical requires both mass-lethal impact and mass blast, so a
  positioning/timing/bystander behavior with high blast but moderate impact
  reads high, not critical.

- **Casualty severity floor.** Behaviors that apply direct physical force to a
  person (weapon discharge, ramming, detonation, physical assault, overpowering
  personnel, taking/restraining a person, injuring a captive) carry a
  `severity_floor` of `critical` — `severity_band` is the greater of the computed
  band and that floor. A casualty is critical at any scale: the severity math
  gates the top band on `blast_radius` (population scope), which would leave a
  single-victim killing at high and reserve critical for mass-casualty events,
  but for triage any application of force to a person is top-priority. Seven such
  behaviors move to critical (three were already critical by weight), taking the
  People-matrix criticals to 13. `escalation_weight` is left unchanged, so the
  severity gradient between a single assault (~4.6) and a mass bombing (~8.7) is
  preserved even though both band as critical. Documented triage rule
  (`escalation_rubric.severity_floor_rule`), not a formula change.

- **impact_potential re-spread as a pathway severity gradient.** impact was
  clustered at 7.0–8.0 because every behavior presages a lethal attack, forcing
  ~67% of the matrix into `high`. It now measures the harm a behavior directly
  produces or imminently enables: recon/tradecraft 4.0–5.5, planning/access
  6.0–6.5, force/seizure/acquisition 7.5–9.5. Band distribution moved 56 medium /
  128 high / 6 critical → 91 / 93 / 6, and reads sensibly per phase (Target
  Development mostly medium, Mobilization skews high, Aftermath skews medium).

- **People-matrix column label.** The matrix-overview grid header, nav tabs,
  and stub landing pages now read People / Facilities / Organizations /
  Infrastructure (plural, via a shared `MATRIX_LABELS` map) to match the
  V1.2.2 scope prose. The `matrices.person` data key, routes, and schema enum
  are unchanged for consumer stability.

- **`informs_axes` is now the sole remaining escalation pilot (B-01).** With
  escalation scoring complete, the README pilot caveat applies only to the
  `informs_axes` annotation layer (23 indicators, TM0101–TM0104), which awaits
  the sealed-blind inter-rater reliability pass on the rest of the matrix.

## [1.2.2] — 2026-07-04

Feature release. Broadens the People matrix scope from a single specific
individual to one or more human beings as the primary target, adds the
Detection Mesh cross-referencing layer with an interactive indicator detail
page, and introduces two experimental type-level annotation surfaces —
`informs_axes` and the escalation-scoring fields — as pilots on the
phase-1 chunk (TM0101–TM0104). Framework content advances to `1.2.2` to
align with the JSON Schema and release; the schema additions are all
additive (existing `1.1.0` content validates unchanged).

### Added

- **People-matrix scope broadening.** The matrix now covers one or more
  human beings as the primary target, spanning four target-identity
  sub-classes: `named_individual`, `role_or_identity_category`,
  `affinity_group`, and `indiscriminate`. New per-indicator
  `target_identity` (multi-select) and per-tactic `target_identity_scope`
  fields, a canonical `matrices.{X}.scope` sentence per matrix, and a
  `matrices.boundary_rule` describing framework-vs-operational placement.
- **Detection Mesh.** Per-indicator `correlates_with` cross-references,
  an inline "Related" surface, and a new `/person/indicator/:id` detail
  page with click-through navigation. Reference-resolution lint
  (`scripts/lint/mesh-refs.py`) and CI (`.github/workflows/mesh-refs.yml`).
- **`informs_axes` (EXPERIMENTAL — pilot).** Type-level categorical
  metadata (six axes, `strong`/`moderate`/`weak`/`none`) describing which
  axes of the threat picture an indicator class informs. Populated on the
  23 phase-1 chunk indicators (TM0101–TM0104) via a sealed-blind
  inter-rater exercise (weighted Cohen κ 0.66 / Gwet AC2 0.78, substantial
  agreement). Not yet populated on the remaining 167 indicators; treat as
  a pilot, not full coverage.
- **Escalation scoring (EXPERIMENTAL — pilot).** Type-level
  `escalation_axes`, `escalation_weight`, `severity_band`, and
  `temporal_signature`, with an `escalation_rubric` documenting the
  recommended composite and severity thresholds. Populated on the same 23
  phase-1 indicators. Consumers should calibrate `severity_band`
  thresholds to their environment and treat the current coverage as a
  pilot.

### Changed

- **34-tactic scope-prose audit.** People-matrix tactic notes and
  indicator behavior text extended so that behaviors whose logic
  generalizes are no longer worded to a single named individual: location
  and target references broadened to admit venues, crowds, and cohesive
  groups; force, seizure, captive-control, attribution, and coercive-
  leverage indicators extended to multiple or group targets. Subject
  Profiling remains individual-and-cohesive-group by design (a genuinely
  indiscriminate target has no shared pattern to profile and is addressed
  through Environmental Survey).
- Plural display labels (People / Facilities / Organizations) across the
  SVG overview and README; `system` → `infrastructure` rename aligned with
  the V1.1 data-side rename.
- SPA TypeScript types extended to cover all V1.2 fields.

## [1.1.1] — 2026-05-04

Patch release correcting a build-artifact defect in the `1.1.0` viewer
bundle. The `framework.json` and `framework.schema.json` artifacts at
`1.1.0` were correct (downstream consumers fetching either file directly
were unaffected); the SPA bundle that GitHub Pages served to the viewer
was a stale Session 20-era build that did not include the V1.1 content
authored after 2026-04-29.

The `framework.json` content version remains `1.1.0`. The
`framework.schema.json` schema version remains `1.1.0`. Only the SPA
build artifact and `package.json` were updated.

### Fixed

- SPA bundle (`docs/assets/index-*.js`) rebuilt from current source. The
  previously-shipped `1.1.0` bundle was built before the Session 21
  V1.1 content authoring and contained framework data with only TA0101,
  TA0103, and TA0305 populated and 15 bibliography entries. The
  rebuilt bundle includes all 34 Person tactics with full V1.1 mandatory
  fields, indicators, countermeasures, response protocols, and Detection
  Mesh cross-links; both new bibliography entries
  (`KIM-JONGNAM-KUL-2017`, `CHAINALYSIS-CCR-2024`); the schema enum
  extensions (`rf_detection`, `anti_drone_systems`, `weeks_to_months`);
  and the `GULYASH-FIELD-OPS-2004-2026` source attribution across the
  corpus.
- `package.json` version bumped from `1.1.0` to `1.1.1` to reflect the
  build artifact change.

### Notes

Root cause: `src/App.tsx` imports `framework.json` at build time (Vite
bundles JSON imports), so framework content commits do not reach the
viewer until the SPA bundle is rebuilt. The release ritual for `1.1.0`
did not include a pre-tag bundle rebuild step. A pre-release build
verification check should be added to the release process to prevent
recurrence.

## [1.1.0] — 2026-05-02

The first release under the V1.1 standard contract. Promotes THREAT Matrix
from a framework to an open standard with a published versioning policy,
identifier contract, deprecation discipline, and reference consumer.
Person matrix Detection & Response is complete across all 34 tactics.

### Added

**Standard contract**
- `VERSIONING.md` — independent SemVer for content and schema, frozen-published rule, fixed-section CHANGELOG template
- `IDENTIFIERS.md` — five operational namespaces (TA####, AP###, IND-*, CM-*, RP-*), compound-ID anatomy, never-reused guarantee
- `DEPRECATION.md` — four-state lifecycle (active / deprecated / superseded / reserved), required fields per state, sunset window
- `NOTICES.md` — MIT License, bibliographic sources, related work, attribution format
- `VOICE.md` — six locked authoring rules (Rules 1–4 in pre-V1.1; Rules 5 + 6 added this release: canonical actor naming and voice variety palette)
- `examples/python_consumer.py` — minimum viable reference consumer (stdlib + jsonschema), demonstrating phase + actor filters
- `examples/README.md` — starting-point guide for five common consumer shapes

**Architecture**
- `schema_version` field in `framework.json` (independent from content `version`)
- Top-level `phase_mappings` cross-walk to NTAC, Calhoun & Weston, CERT, Cyber Kill Chain, MITRE ATT&CK, and MITRE ATLAS
- Top-level `detection_mesh` with five axes (cross_phase, cross_matrix, cross_domain, cross_countermeasure, cross_stakeholder)
- Mandatory tactic fields: `field_notes`, `observed_contexts`, `evidence_basis`, `source_refs`
- Formal JSON Schema published at `docs/data/framework.schema.json` (Draft 2020-12)

**Person Detection & Response**
- All 34 Person tactics (TA0101–TA0108, TA0201–TA0209, TA0301–TA0308, TA0401–TA0409) authored to V1.1 quality with full mandatory fields, indicators, countermeasures, response protocols, and Detection Mesh cross-links (`correlates_with`, `compensates_for`, `coordinates_with`) populated across all four phases
- `GULYASH-FIELD-OPS-2004-2026` source attribution applied across the corpus where framework content is observed in operational casework

**Schema enum extensions**
- `indicator.detection_sources`: added `rf_detection` (RF spectrum monitoring) and `anti_drone_systems` (acoustic / radar / RF triangulation)
- `countermeasure.time_to_implement`: added `weeks_to_months` (resolves TA0103 CM-0103-04 enum violation)

**Bibliography**
- `KIM-JONGNAM-KUL-2017` — Lowy Institute (The Interpreter) coverage of the 13 Feb 2017 Kim Jong-nam assassination, sourcing the unwitting-bystander media-production deception archetype in TA0306
- `CHAINALYSIS-CCR-2024` — Chainalysis Crypto Crime Report, sourcing the comparative blockchain-forensics tracing-speed claim in TA0405

**SPA + assets**
- Vite / React 18 / TypeScript single-page application; bundle prebuilt at `docs/assets/` so GitHub Pages serves without a build step
- 18 components (HeatMapGrid, TopNav, FilterBar, SplitView, PhasePanel, TacticDetail, ActorDetailView, ActorProfilesView, BibliographyView, StubLanding) plus detection-response subcomponents
- `docs/images/threat-lifecycle-diagram.svg` (light-mode SPA tokens, four-phase lifecycle with phase-accent color bars)
- `docs/images/matrix-overview.svg` (light-mode tokens, matrix accent color top strips, V1.1 LIVE / V1.3–V1.5 IN PROGRESS pill aesthetic)
- Sources dropdown UI across IndicatorSection / CountermeasureSection / ResponseProtocolSection

### Changed

- **Top-level matrix key:** `system` → `infrastructure` (and 9 actor-profile `primary_matrices` arrays updated accordingly)
- **SPA matrix version labels:** `V2` / `V3` / `V4` → `V1.3` / `V1.4` / `V1.5`
- **Bibliography ID:** `GULYASH-FIELD-OPS-2010-2025` → `GULYASH-FIELD-OPS-2004-2026`
- **Phase 4 actor track:** `FLIGHT` → `EVADE` (in SVG and SPA labels)
- **Countermeasure subcategory display label:** `Detective` → `Detection` (schema enum value `detective` retained — display-only)
- **WARDEN positioning** removed from README / ROADMAP consumer claims; `framework.json.warden_integration` retained as `status: reserved` per DEPRECATION.md "reserved" lifecycle state
- **Authoring voice canonicalization** (Rule 5): pre-canonical wording (`Subject` / `subject-target pair`) replaced with `Threat actor` / `threat actor — targeted subject pair` across all populated tactics; clinical diction (`incongruity`, `practitioner`) replaced with palette alternatives in tactic content

### Removed

- Legacy single-file React-via-Babel SPA in `docs/index.html` (replaced by Vite build)
- `docs/images/kill-chain-diagram.svg` (replaced by `threat-lifecycle-diagram.svg`)

### Fixed

- TA0103 IND-0103-03 typo: `targeted sujbect` → `targeted subject`
- TA0103 CM-0103-04 pre-existing `time_to_implement: weeks_to_months` enum violation (resolved via schema enum extension)
- `threat-lifecycle-diagram.svg` XML parse error (illegal `--` in comment)
- `matrix-overview.svg` IN PROGRESS pill sizing (text overflow at 108px → widened to 132px → narrowed to 120px for visual balance)
- `ROADMAP.md` line 19 extra columns and line 51 double-hash
- Broken `V1.1-Schema-Spec.md` link from README

### Security

- None specific to V1.1.0.

---

**Validation state at release:** 0 schema errors against `framework.json` (validated by `examples/python_consumer.py` + `jsonschema` Draft 2020-12).
