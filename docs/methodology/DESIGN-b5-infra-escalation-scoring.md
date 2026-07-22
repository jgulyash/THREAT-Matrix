# DESIGN — B5 Infrastructure Escalation Scoring (OT axis re-derivation)

Status: PROPOSED (2026-07-18, Session 33). Blocks the 185-indicator authoring fan-out.
The escalation_rubric's base rates are the People matrix and state "other matrices
re-derive." This doc is the Infrastructure re-derivation. Formula, thresholds, and the
detectability flip are UNCHANGED from the rubric; only the axis semantics and the
blast_radius base rates are re-anchored for OT, plus the severity_floor applicability.

## Formula (unchanged)
escalation_weight = (impact_potential × blast_radius_potential × recoverability_inverse
× (10 − detectability))^(1/4), bounded 0.0–10.0.
Bands: low 0.0 / medium 2.5 / high 5.0 / critical 6.5.
Weight and band are COMPUTED at merge, never hand-authored. Agents author only the four
axes (one-decimal), temporal_signature, and the severity_floor flag.

## Axis re-derivation for Infrastructure

### impact_potential — severity of the consequence the behavior produces or presages
Reads the physical/service consequence, not the actor's effort. OT anchors:
- 9.0–10.0: mass-casualty-capable release or destruction (toxic/flammable release,
  dam/floodgate failure, pipeline rupture in a populated area, defeat of a safety
  system guarding such a hazard).
- 7.0–8.5: wide sustained loss of an essential service (regional grid/water/gas outage),
  or irreversible destruction of long-lead hardware.
- 5.0–6.5: localized outage or process upset with real but bounded harm; manipulation
  that degrades safe operation.
- 3.0–4.5: reconnaissance/access that presages the above (inherits a discounted share
  of the consequence it enables, per phase).
- 1.0–2.5: preparatory/organizational behavior with diffuse consequence.

### blast_radius_potential — TOTAL expected affected scope (downstream population + collateral)
Infra base rates (re-derived from the People method table; here "method" = the asset
class and effect scope the behavior embodies or presages):
- cascading_or_bulk_system (transmission node, bulk water, interstate pipeline, core
  telecom): 8.0–9.0
- regional_distribution (distribution substation, regional main, compressor station): 6.0–7.5
- public_release_or_crowd_exposure (toxic/flammable release near population, contamination
  of a consumed product): 7.0–9.0 combined with impact
- local_facility_or_single_feeder: 4.0–5.5
- single_device_or_edge (one meter, one edge controller, one field sensor): 2.5–3.5
Collateral-reveal parallel to People: uplift only where the BEHAVIOR reveals a
bulk/population-serving asset or a public-exposure venue; do not uplift on mere
compatibility. Unrevealed / single-edge keeps the floor. Instance venue/demand
conditioning is deferred to the assessment layer, not the type-level base rate.

### recoverability_inverse — how hard to restore (high = hard)
OT-specific, this axis carries much of infra's severity (long-lead hardware):
- 9.0–10.0: destroyed HV transformer / large rotating machine / specialized long-lead
  component (12–18+ month replacement); physical destruction of unique assets.
- 7.0–8.5: damaged control/safety hardware or field devices needing vendor rebuild;
  contaminated media requiring remediation.
- 5.0–6.5: config/logic corruption needing validated rebuild and re-commissioning.
- 3.0–4.5: recoverable disruption (restart, failover, credential reset).
- 1.0–2.5: transient or self-clearing.

### detectability — observability by trained OT personnel / telemetry (flipped in formula)
Higher = more observable = smaller residual harm. OT anchors:
- 8.0–10.0: loud/physical or strongly alarmed (breaker trip, SIS annunciation, physical breach).
- 5.0–7.0: visible in normal OT telemetry/historian if monitored.
- 2.0–4.0: blends with legitimate engineering activity (valid credentials, vendor access).
- 0.0–2.0: covert by design (view-only recon, falsified HMI, log-clean implants). Apply
  the rubric's self-censoring caveat: very-low values carry wider uncertainty.

## severity_floor applicability — LOCKED: NARROW extension (Jay, 2026-07-18)
Rule: an indicator whose behavior directly applies physical force to a person's body
floors to severity_band critical, escalation_weight unchanged. In person+facility this
tags 34 direct-force indicators.

DECISION (Jay, 2026-07-18): NARROW extension. Apply severity_floor: "critical" ONLY to
infra EXECUTION behaviors whose direct, foreseeable MECHANISM is human casualties:
- contamination/adulteration of a consumed product or supply (TI0306),
- explosive rupture / ignition / release of stored energy or toxic/flammable material,
- defeat/disable of a safety instrumented system that exists to prevent a
  casualty-bearing hazard (TI0302), where the behavior removes the casualty safeguard.
Keep the floor OFF pure service-denial (blackout, DoS, view falsification) whose
lethality is indirect, downstream, and instance-dependent (medical dependency, traffic).
Rationale: the floor's own logic ("a casualty is critical regardless of scale") is
mechanism-agnostic — a chlorine release kills as surely as a bullet — but must gate on
DIRECT mechanism, not consequence-chain speculation, or it collapses toward a blanket
floor. Estimated scope: a subset of the 45 phase-3 execution indicators, likely ~10–16.

Rejected alternatives: (A) NO floor for infra — risks a lethal isolated-site release
computing just under 6.5 and banding 'high'; (B) BROAD floor incl. phase 1–2 presaging —
floor-inflation, the exact failure the v1.2.0 recalibration fixed for People.

Authoring instruction for the floor flag: agents set severity_floor: "critical" on an
indicator ONLY if its behavior's direct, foreseeable mechanism is human casualties per
the three bullets above; otherwise omit the field. Merge validates the flagged set is a
subset of phase-3 execution indicators (plus any TI0302/TI0306 spanning behaviors) and
surfaces the count for review before splice.

## Float-safe splice (resolved)
Continue the B4 infra-only re-dump: modify only matrices.infrastructure.tactics,
json.dumps(indent=2) that array, pad-6 splice. Person/facility bytes are never
rewritten, so their 2-decimal floats are preserved by not-touching (B4 byte-diff proved
person+facility byte-identical). Infra's own floats are computed then round(x,1) for
axes / round(x,2) for weight and stored as float; json canonical shortest form is
schema-valid. Gate adds: recompute-and-compare escalation_weight for all 185 (== stored
to 2dp), severity_band == threshold(weight or floor), severity_floor only on approved set.
