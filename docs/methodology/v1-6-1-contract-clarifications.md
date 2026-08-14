# v1.6.1 Contract Clarifications

**Status:** shipped in content 1.6.1 / schema 2.1.0 (2026-08-13).
**Provenance:** an adversarial test-case exercise against v1.6.0 (six fictional scenarios spanning all four matrices and phases 2 to 4, four retrospective real-incident mappings, eleven contract stress fixtures). The exercise found that several contract obligations were documented as stronger than the artifact enforced, and that two incident-level annotations had no schema-valid home. This note records the clarifications. No indicator content changed; all 815 indicators are byte-identical to 1.6.0.

## 1. The escalate-only floor is two invariants, not one

Escalate-only decomposes into two separate obligations, and naming which layer owns each is the correction:

- **I1, the floor: `conditioned_priority >= type_severity_band`.** This is now enforced structurally by conditional subschemas on `$defs.conditioned_assessment` (an `allOf` of three `if/then` branches keyed on the stated `type_severity_band`). A below-floor demotion, including of a `severity_floor: critical` direct-force indicator, fails validation. Before 1.6.1 the rule text claimed this was "encoded in the schema"; it was not, and a below-floor record validated clean. It is now true.
- **I2, band fidelity: the stated `type_severity_band` equals the authored `severity_band` of `indicator_id`.** JSON Schema cannot perform this lookup against `framework.json`, so it is owned by the reference validator and the consumer SDK, and it is stated as a `binding_contract` obligation. Without it, a consumer can launder a floor by misquoting the band (writing a critical indicator's band as high, then demoting to high), producing an internally consistent record that only a cross-reference catches.

Together I1 and I2 enforce escalate-only. The schema catches the floor at the earliest layer; the tooling closes the misquote. Enforcement of the full invariant is therefore a tooling guarantee, not a schema guarantee, and the docs now say so.

**Why not store a raise-delta.** A tempting alternative makes demotion unrepresentable by storing a raise amount (held / raised one band / raised two) instead of an absolute priority. It is rejected: a stored raise amount is a stored effect flag, which violates the framework's derive-don't-store doctrine (the held-vs-raised distinction is derived by comparison, never stored). The `if/then` floor keeps `conditioned_priority` as the stored absolute value and is the doctrine-consistent choice.

## 2. Legitimate-context carve-out override rule

Many indicator texts carve out legitimate context so an ordinary act is not flagged in isolation (a lawful single-firearm purchase, licensed range practice, routine maintenance access). The retrospective mapping of a real attack showed every pre-attack behavior returning "partial" because each carve-out fired in isolation, excluding the attacker's entire preparation surface.

**Rule (mapping guidance, no indicator text changes):** a legitimate-context carve-out is a baseline assumption about a behavior seen alone. It is overridden when the same actor already carries active grievance or pathway indicators. Co-occurrence with active same-actor indicators puts the carved-out behavior back in scope for mapping and conditioning. The carve-out prevents false positives on isolated acts; it does not immunize an act that co-occurs with a developing pathway.

## 3. Interdicted-case placement

`boundary_rule` keys primary-matrix placement on the tactic that achieved the threat actor's terminal objective. For an interdicted case, nothing was achieved, so placement was path-dependent on how far the plot ran before disruption. Clarification: for an interdicted case, placement follows the INTENDED terminal objective at a stated evidence tier, not the furthest tactic reached. Disruption does not move the matrix call, and the confidence of the intended-objective inference is recorded in `primary_objective_evidence_tier`.

## 4. Homes for two incident-level annotations

- **`primary_objective_evidence_tier`** is an incident-level annotation the `boundary_rule` refers to, but it was defined only on the type-level indicator object (carried by zero of 815 indicators, and rejected on the incident-facing objects under `additionalProperties: false`). Its canonical home is now `$defs.conditioned_assessment.primary_objective_evidence_tier`. It gains a `contested` value for the case where the existence of a hostile actor is itself disputed, which `unknown` (no basis for inference) overstated. The dormant type-level field is retained for compatibility and redirected.
- **`disposition`** makes case outcomes machine-readable: `active_monitoring`, `heightened_monitoring`, `disrupted_by_interdiction`, `closed_benign`, `closed_resolved`, `referred_out`. It is recorded alongside the score, never in it, consistent with the demotion doctrine (a disrupted plot or benign reassessment exits by disposition, not by a score rewrite). Before 1.6.1 a disrupted plot and a benign reassessment were unrepresentable, and hostile-attribution confidence had to be crammed into `source_credibility`, which measures reporting reliability instead.

## 5. Deferred (not in 1.6.1)

- **Detection Mesh directional gaps** (verified: zero person to infrastructure `correlates_with` edges though the reverse has 26; zero facility outbound cross-matrix edges; zero organization inbound). This is data work through the IRR process, a separate content release.
- **Taxonomy additions** surfaced by the historical record (an attack-window timing tactic in infrastructure, distinct from the existing timing-signal tactic TI0308; a transportation-structure asset class; physical operational-signaling and counter-forensics homes). Normal taxonomy growth through the contribution pipeline.
