# DESIGN — B5 Organizations Escalation Scoring (institutional-harm axis re-derivation)

Status: RATIFIED POST-HOC (Ruling 1, Option A — Jay, 2026-07-27). The escalation_rubric's
blast base rates are the People matrix and state "other matrices re-derive." Infrastructure
re-derived in advance of its authoring fan-out (DESIGN-b5-infra-escalation-scoring.md);
Organizations did not: the 240 indicators were scored at V1.5 (commit b2c4267, eight
parallel authoring agents) with the convention carried in authoring prompts that were not
preserved. This doc closes that gap. It states the semantics the ruling elects, derives
anchors from the authored population, and validates against all 240 indicators. It is
written after the fact and says so; where the authored values and these semantics disagree,
the disagreement is routed to the aftermath reconciliation pass (see the seam section), not
silently ratified.

Formula, thresholds, and the detectability flip are UNCHANGED from the rubric; only the
axis semantics and the blast_radius base rates are re-anchored for the institutional harm
model, plus the severity_floor applicability.

## Formula (unchanged)
escalation_weight = (impact_potential × blast_radius_potential × recoverability_inverse
× (10 − detectability))^(1/4), bounded 0.0–10.0.
Bands: low 0.0 / medium 2.5 / high 5.0 / critical 6.5.
Weight and band are COMPUTED at merge, never hand-authored.

## The Organizations harm model
The institution is the target; the victims are its stakeholders. Organizational harm is
institutional — operational, financial, reputational, governance — and it lands on people
through the institution: employees and members who depend on it, customers and clients it
serves, donors and funders invested in it, and the publics that rely on its function.
Two consequences follow:

1. **blast_radius_potential is stakeholder scope, not casualty count.** The Organizations
   analog of the People matrix's victim scope is the TOTAL expected affected stakeholder
   population — intended plus collateral (peer institutions, sector trust, the public's
   reliance on institutions of that kind).
2. **No severity_floor applies.** No Organizations behavior's direct mechanism is physical
   force to a person's body; force-mechanism behaviors against people or venues live in the
   Person and Facility matrices, and cross-matrix coverage is expressed through the
   Detection Mesh (`correlates_with`), not by re-classifying tactics. Recorded at the B5
   merge (zero floors in the authored population); ratified here.

## Axis re-derivation for Organizations

### impact_potential — magnitude of institutional harm produced or presaged
Reads the institutional consequence, not the actor's effort:
- 8.5–9.5: capture or destruction of institutional function — a seated captured majority
  redirecting budgets, contracts, or mission; a coordinated bloc taking governance control.
- 6.5–8.0: major operational, financial, or reputational damage — extortion leveraging
  exfiltrated institutional data, funding strangulation, engineered mass defection.
- 5.0–6.0: material but bounded harm; narrative and legitimacy operations staged and
  positioned to strike.
- 3.5–4.5: reconnaissance and probing that presages the above (inherits a discounted
  share of the consequence it enables, per phase — same convention as Infrastructure).
- 2.5–3.0: earliest target selection and identification with diffuse consequence.

### blast_radius_potential — TOTAL expected affected stakeholder scope
Elected by Ruling 1, Option A (2026-07-27): the scope of stakeholders and dependent
population harmed by the institutional damage the behavior embodies or presages. It is
NOT a physical-casualty count, and it is NOT raw audience size (see the misread guard
below). Base rate tiers, derived from and validated against the authored population:
- multi_institution_or_sector: 7.5–8.5 — the behavior reveals scope beyond one
  institution: naming additional institutional targets, a sector-wide pressure campaign,
  governance capture that turns an institution against its own stakeholder base.
- full_stakeholder_base: 6.5–7.5 — whole-institution coercion or ecosystem engagement:
  extortion at peak tempo, an organized boycott of the institution's funders, a front
  entity working the partner and funder ecosystem.
- mass_audience_narrative: 5.5–6.5 — narrative operations built to reach the stakeholder
  public at scale: disinformation infrastructure, inauthentic account networks, front
  organization construction, lookalike domains.
- bounded_segment: 4.0–5.5 — a bounded stakeholder segment or dependency thread: donor
  and funder mapping, regulator identification, member-community seeding, rehearsal
  batches against a subset.
- single_thread: 2.0–3.5 — single-thread reconnaissance on the institution or its
  individual officers: registry queries, roster compilation, basic identifiers.

Collateral-reveal parallel to People and Infrastructure: uplift only where the BEHAVIOR
observably reveals multi-stakeholder or sector scope; mere compatibility with a broader
campaign keeps the tier floor. Instance-level scope conditioning (this institution's
actual stakeholder base, this campaign's actual reach) is deferred to the assessment
layer, not the type-level base rate.

**Audience-vs-victims misread guard.** Reach counts only insofar as the reached
population is the harmed stakeholder population. A narrative operation aimed at an
institution's members, funders, and dependent public carries the scope of the harm it
produces in them; a communication's readership is not by itself stakeholder harm. This
distinction is what separates continuing-harm aftermath behaviors from trace aftermath
behaviors in the seam section below.

### recoverability_inverse — how hard the institutional harm is to undo (high = hard)
Institutional damage recovers on governance, trust, and relationship timescales:
- 8.0–9.0: governance capture effected — bylaws amended, budgets redirected; control must
  be litigated, re-elected, or re-chartered back.
- 6.0–7.5: entrenched reputational or narrative damage; defected members, staff, or
  funders; exfiltrated institutional data (which cannot be un-taken).
- 4.5–5.5: cultivated footholds — insider relationships, seated affiliations, front
  legitimacy — removable once found, costly to find.
- 3.0–4.0: staged-but-unlaunched assets; probing and testing.
- 2.0–2.5: public grievance and attention artifacts; early reconnaissance traces.

### detectability — observability by institutional defenders (flipped in formula)
The trained observer is the institution's own defensive apparatus: corporate security,
communications and brand monitoring, governance and membership administration, counsel:
- 8.0–9.0: public and attributed — a manifesto naming the institution, a direct ultimatum.
- 5.5–7.0: visible to routine vigilance — staff approaches, records-request bursts,
  patterned registry queries.
- 3.5–5.0: visible only to deliberate monitoring — narrative seeding, coordinated
  inauthentic account behavior, front-entity assembly.
- 2.0–3.0: covert by design — breach-dump credential searches, insider cultivation,
  internal-channel enumeration. Apply the rubric's self-censoring caveat: very-low
  values carry wider uncertainty.

## severity_floor applicability — NONE (recorded at B5 merge; ratified 2026-07-27)
The floor rule ("direct physical force to a person's body floors to critical") has no
Organizations application: the matrix's harm mechanisms are institutional. Behaviors that
escalate to force against people or venues cross into the Person or Facility matrices and
are covered there; the mesh, not re-classification, expresses that adjacency. The B5 merge
recorded zero floors across the 240 authored indicators, consistent with this rule.

## Aftermath seam — what this doc settles and what it routes onward
Under stakeholder scope, Phase-4 behaviors that CONTINUE producing institutional harm —
audience amplification, narrative laundering, coercive follow-through, recruitment and
momentum exploitation — legitimately carry elevated blast: the harm production is ongoing,
so a forward-looking reading of "embodies or presages" is satisfied by the behavior
itself. This doc ratifies that class.

This doc does NOT pre-ratify Phase-4 trace behaviors — evidence destruction, financial
disposition, cover reestablishment, network protection, rebranding, after-action
assessment. Whether those carry stakeholder scope or take the trace floor is adjudicated
by the aftermath blast reconciliation (forward-looking rule; the B-10 recoverability
reading-seam reconciliation at V1.3 is the procedural precedent: elect the reading,
re-score the nonconforming population, document the seam). Realized aftermath values mix
both classes; expect the trace class to move in that pass.

## Validation against the authored population (2026-07-27)
- 240 indicators across 48 tactics; weight range 2.69–7.32; bands 105 medium / 123 high /
  12 critical; 0 severity_floor.
- Phase medians (impact / blast / recoverability / detectability): Target Development
  4.0 / 3.5 / 3.5 / 4.0 · Mobilization 5.5 / 5.0 / 4.5 / 4.0 · Execution 6.5 / 5.5 / 5.5 /
  6.0 · Aftermath 6.0 / 5.5 / 6.0 / 4.5 — monotone growth in impact and scope along the
  lifecycle, consistent with the tiers above.
- Tier spot-validation: single-thread recon authors at 2.0–3.0 (registry queries, roster
  compilation); mass-audience staging at 5.5–6.5 (disinformation infrastructure, front
  construction); full-scope coercion at 7.0–7.5 (extortion escalation, governance capture,
  funder boycott); the single 8.0 (naming additional institutional targets in a follow-up
  demand) is multi-institution scope, correctly at the top tier.
- A full per-indicator conformance audit is deliberately folded into the aftermath
  reconciliation pass rather than duplicated here.

## Provenance
- Gap: Organizations was the only matrix scored without a locked written re-derivation;
  the V1.5 B5 commit (b2c4267) records process and gates only.
- Ruling 1 (2026-07-27): Option A — blast_radius_potential in Organizations means
  stakeholder/population scope of institutional harm (elected over Option B, strict
  physical-casualty scope, which would have invalidated the matrix's blast values
  wholesale and contradicts the matrix's harm model).
- This doc is the written re-derivation that ruling requires, authored post-hoc against
  the shipped V1.5 population and validated above.
