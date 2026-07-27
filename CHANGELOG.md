# CHANGELOG

All notable changes to THREAT Matrix are documented here, per [VERSIONING.md](docs/VERSIONING.md).

This project adheres to [Semantic Versioning](https://semver.org). Framework
content and JSON Schema are versioned independently; the framework content
and JSON Schema are versioned independently (latest — content: `1.5.0`, schema: `1.4.0`).

## [Unreleased]

### Added

- **Organizations escalation-axis re-derivation documented (Ruling 1, Option A).**
  `docs/methodology/DESIGN-b5-org-escalation-scoring.md` — the written re-derivation the
  escalation_rubric's "other matrices re-derive" note requires, authored post-hoc for the
  Organizations matrix (scored at V1.5 without a preserved written convention).
  Elects stakeholder/population scope of institutional harm as the matrix's
  `blast_radius_potential` semantics, re-anchors all four axes to the institutional harm
  model, records the no-severity_floor rule, and validates the anchors against the shipped
  240-indicator population. Framework data unchanged; the Phase-4 trace-behavior seam is
  explicitly routed to the pending aftermath blast reconciliation rather than ratified.

## [1.5.0] — 2026-07-24

Minor release. Adds the **Organizations matrix** (the fourth and final target matrix)
and completes the cross-domain Detection Mesh across all four matrices. Framework content
only; JSON Schema unchanged at `1.4.0` (all new content uses existing schema fields).

### Added

- **Organizations matrix — 48 tactics, live.** Full behavioral taxonomy for attacks on an
  institution's function, legitimacy, governance, and what it does or represents (distinct
  from its people, facilities, or systems). 48 tactics across the four-phase Threat Lifecycle
  (Target Development 9, Mobilization 11, Execution 15, Aftermath 13), each with 5 behavioral
  indicators (240 total), 4 countermeasures (192), 2 response protocols (96), per-tactic
  assessment guidance, and matrix-wide escalation scoring. Promoted from stub to live; the
  browser now renders `#/organization`.
- **B6 `informs_axes` on all 240 Organizations indicators.** Six-axis resolution ratings
  (actor capability/intent/opportunity, threat timing/target/method) from a sealed-blind
  two-rater inter-rater reliability pass, reconciled against the rubric. Every indicator in
  the framework now carries `informs_axes` and `temporal_signature`.
- **Organizations cross-domain Detection Mesh — 64 indicator edges** (Organization↔People 21,
  ↔Facility 25, ↔Infrastructure 18), authored via the sealed-blind IRR (`correlates_with`).
- **Cross-domain countermeasure and stakeholder mesh — framework-wide.** 291 cross-matrix
  `compensates_for` links (a countermeasure closing a gap another domain's countermeasure
  leaves) and 182 cross-matrix `coordinates_with` links (stakeholder co-activation with
  parallel/gates/precedes/deconflicts relations), grounded on the validated indicator edges.
  Completes the Detection Mesh doctrine: all five mesh axes now deliver.

### Changed

- **Corpus-wide voice normalization.** Actor-word normalization to the canonical "threat
  actor" (117 replacements, carve-outs preserved); em/en-dash purge across framework content;
  VOICE.md Rule 5 carve-outs enumerated.
- **Header stat is now computed** from the live matrices (was hardcoded): 159 tactics ·
  815 indicators · 27 profiles.

## [1.4.1] — 2026-07-19

Patch release. Fixes two rendering bugs exposed when the Infrastructure matrix went live
in 1.4.0. Framework content only (schema unchanged at 1.4.0).

### Fixed

- **Heat map column misalignment.** The header rendered all four matrix columns
  (`MATRICES`) while the body rendered live cells then stub cells (`LIVE_MATRICES` then
  `STUB_MATRICES`). Because Organizations (stub) sits between Facilities and Infrastructure
  in the column order, Infrastructure's live cells rendered under the **Organizations**
  header and the Infrastructure column showed the Organizations stub. The body now renders
  in `MATRICES` order, branching live-vs-stub per column, so header and body always align.
  (Latent since the two-stub layout; surfaced by the 1.4.0 go-live.)
- **Empty Aftermath "Evade" wing for Infrastructure.** All eight Infrastructure aftermath
  tactics were missing the `phase_4_track` field, so they defaulted to the Claim wing and
  the Evade (evasion) wing showed zero. Added `phase_4_track`: TI0401–TI0406 = `evasion`
  (Withdrawal, Access Persistence, Evidence/Log Manipulation, Attribution Obfuscation,
  Network Protection, After-Action Assessment); TI0407–TI0408 = `attribution` (Attribution
  Declaration, Coercive Demand) — the 6/2 split the stub plan already anticipated.

## [1.4.0] — 2026-07-19

Feature release. Completes the **Infrastructure matrix** (37 tactics across all four
phases — critical-infrastructure and OT attack behaviors: grid, water, pipeline, rail,
telecom) and lands the **cross-domain Detection Mesh** — the first cross-matrix edges in
the framework, weaving People, Facilities, and Infrastructure into one operation-scoped
graph. Infrastructure is promoted from stub to full browser rendering. Schema additions
are additive except a deliberate root-level closed-world tightening (below); existing
content validates unchanged.

### Added

- **Infrastructure matrix — complete.** 37 tactics · 185 indicators · 148 countermeasures
  (4/tactic) · 74 response protocols (2/tactic) · per-tactic `assessment_guidance`
  (four-factor) · per-indicator escalation scoring (`escalation_axes`, computed
  `escalation_weight`, `severity_band`, `severity_floor`) · per-indicator `informs_axes`.
- **Facet modality for cyber-physical behaviors.** Each infrastructure indicator carries
  `crossing` {physical | cyber | cyber_physical}, `crossing_mechanism`
  {digital | electromagnetic | physical_implant} on cyber_physical behaviors, and an
  independent `human_social` boolean — the substrate for computed Cyber-Physical-Nexus (CPN).
- **Cross-domain Detection Mesh.** 89 new cross-matrix `correlates_with` edges
  (63 Facility↔Infrastructure, 26 People↔Infrastructure) authored under a same-operation
  participation predicate and validated by a sealed-blind two-rater inter-rater process
  (Cohen κ = 1.000 on both pairs). Cross-matrix edges total 112.
- **OT vocabulary extensions** (additive enums): indicator `detection_sources`
  (+`ot_telemetry`, `network_monitoring`, `vendor_reporting`); countermeasure `domain`
  (+`network_segmentation`, `system_hardening`, `safety_system_integrity`,
  `supply_chain_assurance`); response-protocol `stakeholders` (+`operations_control`,
  `engineering`, `ot_security`, `regulatory_agency`).
- **`CALHOUN-WESTON-2003`** added to the bibliography (Calhoun & Weston, *Contemporary
  Threat Management*), resolving the previously unresolved reference at TM0103.

### Changed

- **Schema is closed-world at the root.** Added `additionalProperties: false` at the top
  level and declared `instance_conditioning` as a typed property; unknown/typo'd top-level
  keys now fail validation (previously silently accepted). Object-level closed-world
  discipline and a referential-integrity CI validator are scoped for a later
  conformance-hardening release.
- **Infrastructure promoted to live rendering** (SPA): `version` flipped from stub to null;
  routing, heat map, and detail views render the matrix and its mesh. Organizations remains
  a stub (V1.5).
- Roadmap corrected: Infrastructure is V1.4 (this release); Organizations is V1.5.

### Fixed

- Reference Python consumer no longer crashes on `matrices.boundary_rule` (guards non-matrix
  siblings before validation).
- Schema `$id` resolves (dropped the nonexistent `/docs` path segment).
- Three stored `escalation_weight` values reconciled to the geometric-mean formula
  (facility `IND-F0208-01`, `IND-F0308-03`, `IND-F0402-03`).
- `escalation_weight` precision prose corrected (one-decimal → two-decimal) to match data and UI.
- Version drift reconciled (`package.json`, README, framework/schema all at 1.4.0); README
  tactic counts, consumer framing, and family count corrected; the retired `techniques` layer
  documented; CI now also triggers on direct pushes to `main`; compiled `.pyc` untracked.

## [1.3.0] — 2026-07-12

Feature release. Completes the **Facilities matrix** (40 tactics across all four
phases — the first non-person attack-surface matrix authored end-to-end), brings
**escalation scoring to the full People matrix** (190 indicators, up from the
23-indicator pilot), and lands **`assessment_guidance` on every tactic in both
matrices** (People 34/34, Facilities 40/40) — the per-tactic four-factor analytic
layer that is the V1.3 hard release gate. `target_identity` is populated
matrix-wide, the identifier contract is extended to non-person matrices, and a
verified 46-entry bibliography (29 new facility sources) is tagged by matrix and
topic. Schema additions are additive; existing content validates unchanged.

### Changed

- **Recoverability reading-seam reconciled (B-10) — `recoverability_inverse` is now
  a clean own-harm axis matrix-wide.** Phase-1/2 preparatory behaviors previously
  carried a presaged-harm R (weapon rehearsal 7.5, acquisition 8.5) inconsistent
  with the own-harm reading elected in rubric v1.2.0 and already used by phase-3
  support behaviors. 39 phase-1/2 person indicators were re-scored: harm-nothing
  preparation (acquisition, cover, OPSEC, financial, rehearsal, logistics) to
  own-harm R ≈ 4.0, and breach/penetration/access-elevation to R ≈ 5.5. Because
  the elected reading would otherwise drop breach severity, `blast_radius_potential`
  for those intrusion behaviors was re-authored off the stale single-victim floor
  (3.0) to the occupied-environment collateral tier (perimeter 5.0, zone-penetration
  5.5, access-elevation 5.0) — a defeated control exposes the population behind it —
  which holds them at high on the weight math, no severity floor required. Net: 8
  band flips (3 weapon-acquisition critical→high, others high↔medium), person
  distribution 91/80/19 → 94/80/16 (medium/high/critical). Detection-catch timing
  and lone-vs-group actor structure logged as instance-conditioning (B-03) leans.
  No double-count: the enabled-harm signal lives in `impact_potential`.

- **People `target_identity` re-authored to the revealed reading (190/190).** The
  field previously carried a *compatibility* reading — 179 of 190 indicators
  tagged with all four values ("which classes the behavior COULD serve"), which
  told an analyst nothing. It now carries a *revealed* reading: tag only the
  victim identity-class the behavior actually resolves. 124 indicators are now
  empty (capability, breach/access mechanics, OPSEC/tradecraft, financing,
  evidence management, most aftermath — these reveal nothing about who), 54 are
  `named_individual` (subject profiling, surveillance/positioning/approach
  against the target's person or coupled site, force/seizure/captivity/leverage),
  and 12 span group/crowd/selection classes. `named_individual` is clarified as
  plural-capable — a specific target-associated site couples to the specific
  known person(s), one or more, who are the target. Reproducibility validated by
  a sealed-blind spot-IRR (per-value Cohen κ 0.80, 20-indicator stratified
  sample). The schema description is updated to the revealed reading; the enum is
  unchanged.

### Added

- **Facility target dimension (facility_target_scope + within_site_focus).** The
  Facility matrix gains the target sub-dimension People's target_identity
  provides but that facility lacked. facility_target_scope captures the breadth
  of site selection an indicator reveals — specific_site / site_class
  (functional type) / symbolic_category (ideological/symbolic category) /
  indiscriminate — answering "which/how many sites" (the Nairobi embassy vs
  any US embassy vs any government building). within_site_focus captures the
  facility-native "what inside bears the harm" — structure / occupants /
  systems / whole_site. Both use a REVEALED reading (tag only what the behavior
  indicates, empty when it reveals nothing) under a target-coupling rule
  (capability/method/recon-of-dimensions stay empty), authored across all 200
  facility indicators. Reproducibility validated by a sealed-blind spot-IRR
  (scope κ=0.94, focus κ=0.88; the site_class/symbolic_category split held).
  Rendered in the indicator detail as **Target Scope** and **Within-Site
  Focus**, mirroring the People target_identity presentation (populated-only).

- **`informs_axes` completed matrix-wide on the Facilities matrix (200/200).**
  The six-axis type-level threat-picture metadata carried on the People matrix
  now covers all 200 facility indicators, extended via the same sealed-blind
  two-rater IRR (κ≥0.60 gate, boundary rubric + phase-locked definitional calls,
  per-chunk adjudication). All eight chunks passed. Weighted κ: F1A 0.75,
  F1B 0.82, F2A 0.89, F2B 0.86, F3A 0.88, F3B 0.85 (raw 0.57 → 0.85 after a new
  locked call), F4A 0.90, F4B 0.76 (Gwet AC2 0.77–0.98). Consensus adjudication
  resolved the soft threat_timing/threat_method axes toward the stricter
  access-vs-method reading and actor_opportunity toward the realized-action bar;
  >1-step target-scope splits settled to the candidate-set middle. Two new
  locked calls were surfaced and recorded: (1) **terminal-act method** —
  execution-phase tactics that ARE the attack modality (occupation, blockade,
  hostage, vandalism, contamination) pin threat_method=strong, while
  support/suppression behaviors stay none/weak; (2) **aftermath intent +
  postulated-event axes** — aftermath intent is strong for declaration/ownership
  behaviors (attribution, amplification, symbolic messaging, coercive demand)
  and moderate for evasion, while the postulated-event axes stay none for
  retrospective behaviors and go live only for forward-looking re-attack
  (TF0408) and coercion (TF0412).

- **Assessment Guidance rendered in the tactic detail.** The per-tactic
  `assessment_guidance` layer — the V1.3 hard-gate content, authored on all 74
  tactics but previously imported in types and rendered nowhere — now displays
  in the detail panel: an escalation-priority badge, the four analytic factors
  (credibility / capability / intent / opportunity) each with their criteria and
  collapsible raise/lower signal anchors, a false-positive-context block, and
  threshold guidance. Faithful to the existing detail-section pattern; renders
  identically for People and Facilities (the voice difference lives in the data).

- **Instance-conditioning layer (Layer 2) contract — B-03 / B-04.** The
  framework's type/instance split (CVSS Base-vs-Environmental) gains its second
  layer as a schema contract: `$defs.instance_assessment` (a required, structured
  per-case record — target_focus, pathway_stage, means_in_hand, tempo_trajectory,
  source_credibility) and `$defs.conditioned_assessment` (the binding object).
  The framework DEFINES the layer and ships NO instances — it stays a type-level
  artifact; consumers instantiate per case. Two safety invariants are encoded in
  the schema, not just documented: the binding requires BOTH a type-score
  reference and an instance record (a bare number cannot be emitted as a
  conditioned assessment — B-04), and conditioning is escalate-only
  (`conditioning_effect` has no `lowered` value; `conditioned_priority` is floored
  at the type band) so instance evidence can catch the false-LOW (F12) but never
  silently discount capability (F13). Indicators gain an optional type-level
  `instance_conditioning_hints` slot, seeded from the V1.3 sealed-blind IRR leans
  (chunk-2B pilot, 23 indicators; full population a follow-on). A top-level
  `instance_conditioning` block documents the layer, the escalate-only rule, and
  the display-binding contract. The consumer/UI instance-entry surface is
  deferred to a later cycle.

- **Facilities matrix — complete (40 tactics, all four phases).** The first
  non-person attack surface, authored end-to-end: Target Development (TF0101–
  TF0110), Mobilization (TF0201–TF0209), Execution (TF0301–TF0309), and Aftermath
  (TF0401–TF0412). Each tactic carries ~5 escalation-scored indicators, ~4
  countermeasures, ~2 response protocols, a full `assessment_guidance` block,
  `field_notes`, `observed_contexts`, `actor_associations`, and a CPN marker.
  Facility escalation is calibrated to the built environment: a blast floor of
  ~4.0 (facilities admit mass-casualty by default), method base rates for
  incendiary/explosive/structural/vehicle-ram/contamination execution, the
  casualty floor on force-on-person execution behaviors, and property-only
  tactics (vandalism) held to medium/high. Facility tactics carry no
  `target_identity` (the place is the objective); voice is "Threat actor" /
  "the targeted facility."

- **Non-person identifier contract.** Schema patterns now accept facility
  identifiers — `TF####` tactics and `IND-F####-##` / `CM-F####-##` /
  `RP-F####-##` compound IDs (with an optional `[FOI]` prefix) — alongside the
  unchanged Person `TM####` scheme, extending the framework to additional matrices.

- **Verified facility bibliography with matrix/topic tagging.** 29 new verified
  facility sources (46 entries total), every entry tagged `matrices[]` and
  `topics[]` so the reference set can be grouped by matrix without partitioning
  the flat key space. No fabricated citations — facility content cites only
  verified keys.

- **Facility matrix rendered in the browser.** The matrix browser now renders
  the Facilities matrix end-to-end, mirroring the People rendering: a live
  teal heat-map column (10/9/9 tactics across phases 1–3 plus the Aftermath
  Evade/Claim split), phase panels, full tactic detail (description,
  cyber-physical nexus, actor associations, indicators, countermeasures,
  response protocols), and indicator detail with the escalation profile.
  Navigation is matrix-aware throughout — routes take `/facility/...` paths
  parallel to `/person/...`, and cross-links (related indicators, actor-detail
  tactic lists, bibliography citations) resolve each tactic's own matrix.
  Organizations and Infrastructure remain planned stubs.

- **Facility Aftermath tracks (`phase_4_track`).** The facility phase-4
  tactics now carry the framework-level Evade/Claim sub-track the People
  matrix established: `evasion` on TF0401–TF0408 (withdrawal, evidence
  management, cover reestablishment, network protection, financial
  disposition, after-action assessment, counter-forensics, re-attack
  positioning) and `attribution` on TF0409–TF0412 (declaration,
  amplification, symbolic messaging, coercive demand). The schema now
  formalizes `phase_4_track` (previously an undocumented data field).

- **Bibliography grouped by matrix.** The References view groups the 46
  sources into sections by their `matrices[]` tag (a multi-matrix source
  appears under each matrix it informs), and the cited-by reverse map now
  includes Facility tactics, so facility sources list their citing TF####
  tactics.

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

- **`assessment_guidance` on every tactic in both matrices (34/34 People,
  40/40 Facilities).** Each tactic now carries the four-factor analytic block —
  `credibility`, `capability`, `intent`, and `opportunity` (each with a criteria
  statement plus high- and low-signal anchors), a `false_positive_context`, a
  `threshold_guidance` paragraph (tier logic, multi-indicator composition rule,
  and known-threat-actor clause), and an `escalation_priority`. This is the V1.3
  hard release gate; it clears the previous 4/34 People coverage. Anchors are
  tactic-specific and phase-calibrated (Target Development / Aftermath at
  Priority, Mobilization at Immediate, Execution at Urgent/Immediate), in the
  matrix's own voice — "the target" for People, "the targeted facility" for
  Facilities.

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

- **Detail-panel section hierarchy clarified.** Major section headers
  (Description, Cyber-Physical Nexus, Actor Associations, Assessment Guidance,
  Indicators, Countermeasures, Response Protocols, Sources) now share one
  treatment — a consistent amber label with a left accent bar and more space
  between sections — so each reads as a distinct section start. The
  actor-category sub-labels (Lone Actor, Insider, …), previously amber and the
  same weight as section headers, are muted to match the indicator-category
  sub-labels, so sub-groups sit clearly below their section rather than blending
  into the next one.

- **Assessment Guidance is now a compact accordion that introduces the indicators.**
  The four factors, the false-positive block, and threshold guidance each
  collapse to a single row with a fixed one-line descriptor and expand on click;
  the escalation-priority badge stays visible in the section header at all times,
  and threshold guidance renders its authored paragraphs. The section sits
  directly before the Indicators list with the subtitle "How to weigh observed
  findings of this tactic" — the guidance is tactic-level advice for weighing
  the tactic's findings, so it frames the indicators rather than reading as an
  assessment of the tactic description.

- **Assessment-guidance threshold text broken into paragraphs.** Each tactic's
  `threshold_guidance` (previously a single ~2,000-character block) is now
  authored with paragraph breaks at its natural seams — framing, the
  tier-determination factors, each tier rung on its own line, the
  correlation-escalation and composition rules, and the tier-triggered actions
  (5–10 paragraphs per tactic). Breaks live in the data (agents and
  downstream systems read the structure), inserted by a seam rule keyed on the
  consistent tier skeleton and verified word-for-word unchanged. A V1.4 item is
  logged to promote this into a structured tier-ladder object.

- **Severity thresholds recalibrated against the realized scored population
  (escalation_rubric v1.2.0).** With both matrices fully scored (390 indicators),
  the equal-quartile `critical` cut of 7.5 left the critical band floor-driven:
  24 of 41 critical indicators reached the band only via the casualty severity
  floor, because the geometric mean rarely computes past 7.5. The `critical`
  threshold moves to **6.5** (medium 2.5 and high 5.0 are unchanged), giving the
  band a genuine weight-driven population while preserving the medium/high
  split: 24 indicators move high → critical (People 13 → 19, Facilities 28 → 46).
  `calibration_guidance` (framework + schema) now documents the recalibrated
  default, and `computed_critical_requires_both` is updated for the new cut —
  at 6.5, a behavior combining mass blast_radius with substantial (not
  mass-lethal) impact_potential can compute critical at the margin. The
  consumer-side posture knob (shift thresholds to your environment) is
  unchanged. Per-phase category scoring defaults (phases 2–4, n≥8 cells only)
  are published alongside the recalibrated phase-1 defaults in the authoring
  workspace. No `escalation_weight`, axis value, or floor assignment changed.

- **Indicator behavior texts hardened to observable-only criteria (13
  classes).** Thirteen phase-1/2 behavior descriptions carried clauses that
  presupposed observer knowledge of the actor's plan ("the planned attack
  method", "attack-relevant items", "the intended attack window") — matching
  them required already knowing the plan, baking method/intent signal into
  the definition instead of the observation. Each is reworded to an
  observable criterion that preserves the class's scope (e.g., "items whose
  most coherent use is harmful", "consistent times concentrated on one
  recurring window", "the same route to or past the target"). During- and
  post-attack behaviors that reference "the operation" are unchanged — there
  the attack is observed reality, not presupposed knowledge. No escalation
  or informs_axes value changed with the wording; the affected People-matrix
  informs_axes ratings get a sealed-blind spot re-check.

- **`informs_axes` axis semantics formalized in the schema (V1.3 refinements
  #1–#4).** The six axes now carry description text encoding the locked
  boundary rubric the matrix-wide authoring was rated against: the universal
  none/weak/moderate/strong resolution scale (resolution, not severity),
  `actor_intent` = general intent-to-act only (#1), `actor_opportunity`
  tiered informational-moderate / realized-action-strong (#2),
  `threat_method` = attack-method-only within the framework's all-physical
  scope (#3), and the locked phase-boundary wording on `threat_timing`. The
  top-level field description sheds its V1.2 EXPERIMENTAL/pilot framing —
  coverage is authored matrix-wide (190/190) through the sealed-blind
  inter-rater process — and the cross-matrix extension remains an explicit
  deferred decision (B-09).

- **Three capability constructs distinguished in schema text.**
  `impact_potential` (presumes the class's capability ceiling; now also
  documents the V1.3 directly-produces-or-imminently-enables gradient),
  `informs_axes.actor_capability` (what observing the class reveals about
  skill), and `assessment_guidance.capability` (how to read a specific
  actor's capability from evidence) each name the distinction and point to
  the instance-conditioning layer as the per-case judgment's home.

- **Detectability-flip documented (`escalation_rubric.detectability_guidance`).**
  The (10 − detectability) inversion is documented as deliberate: the
  composite reads as expected residual harm (stealth removes the
  interdiction window, matching CVSS/insider-threat convention), with an
  explicit guard against misreading stealth as severity and a caveat that
  detectability is a self-censoring axis (the stealthiest classes rest on
  the thinnest observational base). No formula change.

- **`recoverability_inverse` reading elected (schema axis text).** The axis
  scores the harm a behavior class directly produces — it does not inherit the
  permanence of the harm a behavior presages or enables (contrast
  `impact_potential`, which counts both). The election resolves the apparent
  phase-3 "dip": execution force behaviors score 9.0–9.5 as the axis demands,
  while in-execution support behaviors honestly score their own transient
  harm. A known seam — phase-1/2 preparatory indicators authored under the
  earlier presaged-harm reading — is logged for a future gated scoring pass
  rather than silently re-scored.

- **Collateral-reveal blast policy documented and reconciled.** The blast_radius
  authoring rule — raise blast above the single-victim floor only where the
  behavior itself observably reveals a group/population target or a public/crowd
  venue (the parallel to method-revealed) — is now a first-class, reusable rule
  in `escalation_rubric.blast_radius_guidance.collateral_reveal_guidance`, with
  graduated tiers and an explicit deferral of unrevealed-venue collateral to the
  instance layer. One consistency fix (`IND-0206-01` line-of-sight to a
  gathering: blast 3.5 → 4.5 to match its sibling). The policy adds no criticals
  by design under the equal-quartile 7.5 cut it was authored against: critical
  required both mass-lethal impact and mass blast, so a positioning/timing/
  bystander behavior with high blast but moderate impact read high, not
  critical. (The severity-threshold recalibration entry above moves the
  critical cut to 6.5, which admits a handful of those behaviors at the margin.)

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

- **`informs_axes` completed matrix-wide — no longer a pilot (B-01 closed).** The
  type-level annotation layer now covers **all 190 People-matrix indicators (34/34
  tactics)**, up from the 23-indicator V1.2 pilot. Coverage was authored via the
  established sealed-blind inter-rater process — an independent AI rater and Jay
  each code every indicator's six axes from the locked boundary rubric, then
  weighted Cohen κ + Gwet AC2 gate each chunk at κ≥0.60 before values ship. Seven
  chunks, all passing after adjudication (κ 0.75 / 0.65 / 0.75 / 0.77 / 0.88 / 0.93
  / 0.74). The process surfaced and locked several cross-phase definitional calls
  (`threat_method` = attack-method only; mobilization rehearsal/probing = strong
  `threat_timing`; `threat_target` = strong when target-associated; during-execution
  support inherits realized `actor_opportunity`; aftermath retrospective behaviors
  score the postulated-event axes at `none` with the recurrence residual deferred to
  the instance layer). The four-bucket scale and per-indicator "leans" (the
  situational directionality) are retained as seed data for the future
  instance-conditioning layer (B-03).

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
