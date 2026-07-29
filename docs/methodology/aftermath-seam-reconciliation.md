# Aftermath Seam Reconciliation (Phase-4 blast and impact)

Status: APPLIED (rulings 3, 2-B, 4-A, 5-A, 6-A — Jay, 2026-07-28 session).
Procedural precedent: the V1.3 B-10 recoverability reading-seam reconciliation
(elect the reading, re-score the nonconforming population, document the seam).

## The seam
Phase-4 (aftermath) indicators had been authored with `blast_radius_potential`
and, in places, `impact_potential` that echoed the *completed* attack's scope
rather than the scope the aftermath behavior itself presages or enables going
forward. That over-scored trace behaviors (withdrawal, cleanup, attribution,
after-action) and, on the Facility matrix, propped them up further through the
~4.0 mass-casualty blast floor. This pass elects the forward-looking reading and
re-scores the nonconforming population.

## The rules applied
- **Ruling 3 (the rule):** an aftermath behavior's `blast_radius_potential`
  encodes only the victim/stakeholder scope it presages or enables going forward.
  The completed attack's scope belongs to the execution-phase indicators.
- **Ruling 6-A (impact audit):** the same forward-looking test governs aftermath
  `impact_potential`. Carve-out: impunity-enablement (evidence destruction,
  witness silencing to preserve freedom to operate) is not impact — that value
  lives in recoverability/persistence, and encoding it in impact double-counts.
- **Ruling 2-B (facility floor scope):** the Facility ~4.0 blast floor governs
  Phases 1-3 and forward-looking Phase 4 only, not aftermath pure trace.
  TF0401-TF0407 re-author to the cross-matrix trace floor (~2.5); TF0408
  (secondary device / re-attack) and TF0412 (coercive demand) are untouched.
  Edge case IND-F0402-04 (returns to site / dispatches proxy) kept elevated for
  genuine venue proximity.
- **Ruling 4-A (copycat boundary, narrow):** only explicitly instructional or
  celebratory copycat-enablement content earns a discounted forward scope (one
  tier above the trace floor). Generic amplification and plain attribution take
  the trace floor. The Organizations continuing-harm classes are exempt from
  down-scoring under Ruling 1-A (see DESIGN-b5-org-escalation-scoring.md).
- **Ruling 5-A (continuation threats):** a claim of responsibility that includes
  a threat of continuation gets no blast uplift; the continuation content is
  carried by the coercive-demand class via `correlates_with` (edges added, not
  score inflation).

## Anti-harmonization
After this pass, same-named messaging/amplification classes are deliberately
scored differently across matrices: Organizations keeps them elevated
(continuing institutional harm, Ruling 1-A); Person, Facility, and
Infrastructure take the trace floor (Ruling 4-A narrow). This asymmetry is the
harm-model difference working as designed and is recorded in
`escalation_rubric.blast_radius_guidance.aftermath_rule`. Future authoring passes
must not harmonize these classes.

## Population moved (2026-07-28)
- 215 Phase-4 indicators classified; 165 RE-AUTHOR, 50 KEEP (forward-looking /
  continuing-harm). 66 indicators moved high -> medium; none crossed into
  critical or low. Framework band distribution 381/348/86 -> 447/282/86.
- Two `correlates_with` edges added under Ruling 5-A (IND-0407-04 -> IND-0409-01;
  IND-O0410-03 -> IND-O0412-01). These are ruling-authored edges, editorial
  provenance, distinct from the sealed-blind IRR mesh.
- The reshaped bottom of the scale (sub-3.5 population) feeds the bottom-cut
  recalibration (Ruling 7), run as a separate pass against this distribution.
- `rubric_version` 1.2.0 -> 1.3.0.
