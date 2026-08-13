# Contract Stress Tests (Workstream C)

Adversarial edge cases aimed at the v1.6.0 contract itself: escalate-only violations, severity-floor interactions, malformed instance records, referential-integrity attacks, and ambiguous matrix placement. Eleven fixtures in `manifest.json` each declare which validator layer **must** reject them (`C1` schema / `C2` cross-ref / `C3` escalate-only ordering; `[]` = must be accepted); `../validate_cases.py` passes a fixture only when the fired set exactly matches the declaration. All eleven currently match.

Run: `python3 examples/test-cases/validate_cases.py`

## Fixture results

| Fixture | Attack | Schema (C1) | Caught by | Verdict |
|---|---|---|---|---|
| st-01 | Capability-discount demotion (type high → priority low) | **ACCEPTS** | C3 only | schema gap — see ST-F1 |
| st-02 | Below-floor demotion of a floored direct-force indicator (critical → high) | **ACCEPTS** | C3 only | schema gap — see ST-F1 |
| st-03 | Floor laundering: misquote IND-I0302-01's floored-critical band as "high", priority "high" | **ACCEPTS** | C2 only | out of schema reach — see ST-F2 |
| st-04 | Invalid enum (`tempo_trajectory: "rapid"`) | rejects | C1 | closure holds |
| st-05 | Missing `proximity_access` (the Q3a sixth factor) | rejects | C1 | closure holds |
| st-06 | `inhibitors` field on the instance record | rejects | C1 | Q3b exclusion holds mechanically |
| st-07 | Stored top-level `effect: "raised"` flag | rejects | C1 | derived-state doctrine holds mechanically |
| st-08 | Pattern-valid but nonexistent `IND-9999-99` | **ACCEPTS** | C2 only | out of schema reach — see ST-F3 |
| st-09 | Invalid matrix letter `IND-X0301-01` | rejects | C1 | pattern holds |
| st-10 | `primary_objective_evidence_tier` written on the incident record | rejects | C1 | rejection is the *wrong* outcome — see ST-F5 / RG-1 |
| st-11 | Valid all-unknown control record | accepts | — | control passes |

## Findings

**ST-F1 — The escalate-only invariant is documented as schema-encoded, but it is not.**
`framework.json → instance_conditioning.escalate_only_rule` states the rule is *"Encoded in the schema by conditioned_priority being floored at type_severity_band."* The schema's own `conditioned_priority` description says the opposite: *"JSON Schema cannot compare the two enums directly, so consumers MUST NOT emit conditioned_priority below type_severity_band."* Fixtures st-01 and st-02 settle it empirically: both demotion records validate cleanly against `$defs/conditioned_assessment`. The deadliest-error path the contract exists to forbid is, at the schema layer, representable — including below a `severity_floor: critical` direct-force indicator (st-02).
*Remedy (either closes the finding):* (a) actually encode it — draft 2020-12 expresses this with three `if/then` branches (`type_severity_band: medium` ⇒ `conditioned_priority ∈ {medium, high, critical}`, etc.; `low` needs no branch); or (b) correct the `escalate_only_rule` prose to say the floor is a consumer obligation enforced by validation tooling, and ship a reference check. `validate_cases.py` layer C3 is that reference check; note that the repo's own `scripts/lint/validate.py` V18 walks only the *canonical artifact* for lowering, so consumer-side records have no first-party guard today.

**ST-F2 — Floor laundering by misquoting the type band is invisible to both the schema and the ordering rule.**
st-03 demotes a floored-critical indicator without ever writing a priority below its *claimed* band: it misquotes `type_severity_band` as "high" and conditions to "high". Internally consistent — C3 passes — and the schema has no knowledge of authored bands. Only a cross-reference against `framework.json` (C2) catches the misquote. This is the strongest argument that the binding contract needs a stated third obligation: a conditioned assessment is valid only if its `type_severity_band` **equals the authored `severity_band`** of `indicator_id` at a stated framework version. *Remedy:* add that sentence to `instance_conditioning.binding_contract` (and the worksheet), and recommend consumers pin `version` alongside records.

**ST-F3 — Referential integrity is out of schema reach.**
st-08's `IND-9999-99` matches the ID pattern and validates. Expected JSON Schema behavior, but worth stating in the contract docs: shape validation is not existence validation; consumers must resolve `indicator_id` against the artifact. (Positive census: all 815 shipped indicator IDs conform to `^IND-[FOI]?[0-9]{4}-[0-9]{2}$` — the pattern and the data agree.)

**ST-F4 — Where V1.6 closure exists, the doctrine holds mechanically.**
The four doctrine-bearing rejections all fire at the schema layer: unknown enum values (st-04), a missing sixth factor (st-05), the SPJ-tradition `inhibitors` field (st-06 — the Q3b exclusion is not just prose, `additionalProperties: false` enforces it), and a stored held/raised effect flag (st-07 — the derive-don't-store rule likewise). This is the V1.6 "contract hardening" promise working as shipped.

**ST-F5 — The one rejection that is a bug, not a defense.**
st-10 writes `primary_objective_evidence_tier: "weakly_inferred"` on a conditioned assessment for an Oldsmar-like incident — exactly where `matrices.boundary_rule` prose says the annotation belongs ("annotated separately via primary_objective_evidence_tier"). The schema rejects it: the enum is defined only on the type-level `indicator` object (where zero of 815 shipped indicators carry it) and the incident-facing objects reject unknown fields. The fixture *expects* rejection because that is current behavior — the finding is that rejection is the wrong outcome. Mechanical confirmation of retrospective-mapping finding **RG-1**; remedy there.

## Ambiguous matrix placement (analytic stress test)

`matrices.boundary_rule` is prose, so it is stress-tested analytically rather than by fixture. Two fictional probes plus one real-world confirmation:

**Probe 1 — co-terminal objectives, tie-break path.** A coerced insider disables a campus data center's backup power plant (infrastructure tactic) to force an evacuation that flushes a named executive to a predictable assembly point, where the actor attempts an assault (person tactic). Terminal objective: harm to the person — **person matrix**, no tie-break needed; the infrastructure action is a subordinate enabler. Now delete the assault from the fact pattern (interdiction at the assembly point): the *achieved* terminal objective is now arguably the outage. A consumer reading "achieved" strictly flips the primary call to **infrastructure** even though the plan was person-terminal — the rule's word "achieved" makes primary placement path-dependent on how far the plot ran before disruption. This interacts directly with RG-3 (disrupted plots): for interdicted cases the rule needs one clarifying sentence — whether "achieved" falls back to *intended* terminal objective when execution was prevented, and at what evidence threshold.

**Probe 2 — uncertain objective, consequence default.** Overnight arson destroys a shared office building housing a controversial nonprofit and four uninvolved tenants; no claim, no attribution. Objective (intimidate the organization? destroy the venue?) is unresolvable, so the uncertainty branch fires: most observable consequence → structure destroyed → **facility matrix**, annotated `weakly_inferred`. The branch resolves deterministically — but the annotation it mandates has nowhere to live (ST-F5/RG-1), and if later evidence resolves the objective to organization-intimidation, the primary call migrates facility → organization. Nothing in the contract states whether re-placement is expected, versioned, or frozen at first call.

**Real-world confirmation.** Workstream B's YouTube HQ analysis ran the rule against a genuine three-matrix incident (organization grievance, facility site, person victims): terminal-objective and precedence tie-break independently resolve to **person** — the rule passes. The residual weakness for multi-matrix incidents is not placement but *walkability*: the rule delegates cross-matrix coverage to `correlates_with`, and the verified mesh census (RG-6) shows zero person→infrastructure, zero facility→outbound, zero organization→inbound edges — so for several matrix pairs, the mesh the rule points to has no edge to walk in the direction real cases develop.

## Severity-floor interaction summary

Fixtures st-02/st-03 cover the demotion side; the positive suites cover the other two edges: FS-2 (fictional) shows a floored-critical type correctly *holding at the ceiling* under a maximal instance, and incident-3 (Whitmer) shows the same hold reading identically to a bare-minimum critical in the enum fields — the observation behind RG-3's secondary note. Net: the floor is sound in the data (verified: all 43 floored indicators band at critical; lint V15/V18 guard the canonical artifact) — every failure mode found lives on the *consumer record* side, which is exactly where V2 platform tooling (SDKs, MCP server) will sit.
