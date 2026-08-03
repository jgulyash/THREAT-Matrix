# Instance Record Worksheet

One page. Fill this to condition a type-level indicator score for a specific case. The framework ships no case data; this worksheet and `instance-record-template.json` are the affordance for a consumer that holds its own.

**The rule that governs everything below: instance conditioning may only RAISE a case's priority above the indicator's type band. It may never lower it.** A mild-looking type with a screaming instance is the deadliest miss; a low-credibility or all-unknown instance holds at the type band, it does not demote.

---

## The indicator

- **Indicator ID:** `IND-____-__`  (the type-level indicator you are conditioning)
- **Type severity band:** ☐ low ☐ medium ☐ high ☐ critical  (this is the FLOOR; conditioned priority is never below it)

## The six factors (check one per factor)

**1. Target focus** — how resolved is the target?
☐ diffuse ☐ narrowing ☐ specific_target ☐ unknown

**2. Pathway stage** — this actor's position on the pathway to violence (NTAC vocabulary):
☐ grievance ☐ ideation ☐ research_planning ☐ preparation ☐ breach_or_probing ☐ attack ☐ aftermath ☐ unknown

**3. Means in hand** — does THIS actor have the capability/means now?
☐ assessed_absent ☐ partial ☐ assessed_present ☐ confirmed_present ☐ unknown
*(unknown is the safe default and does NOT lower priority — absence of evidence is not evidence of absence. Boundary: `partial` = some but not all of the means assembled; `assessed_present` = the actor is judged to have the means though it is not directly observed; `confirmed_present` = the means is directly observed in hand.)*

**4. Tempo trajectory** — direction and rate of movement across observations:
☐ accelerating ☐ steady ☐ stalling ☐ unknown

**5. Proximity / access** — the actor's access state relative to the target (a STATE, not a stage — an insider has access without ever breaching):
☐ no_known_access ☐ seeking_access ☐ has_access ☐ at_or_near_target ☐ unknown
*(unknown-safe, same doctrine as means in hand.)*

**6. Source credibility** — reliability of the reporting behind this record:
☐ high ☐ moderate ☐ low ☐ unknown
*(a brake on raising, never a scaler down: a low-credibility screaming instance cannot be dismissed and cannot stampede the queue — the raise waits for corroboration.)*

## The result

- **Conditioned priority:** ☐ low ☐ medium ☐ high ☐ critical  (>= type band, always)
- **Held or raised?** Not a field you set — it is read by comparison: the case was *raised* if conditioned priority is above the type band, *held* if equal to it. (The record stores only the priority; there is no separate effect flag to keep in sync, and no way to record a lowering.)
- **Next action:** ____________________________________________

---

## Raise guidance (advisory patterns — for inter-analyst consistency, NOT a formula)

| Pattern | Consider |
|---|---|
| specific_target + means_in_hand assessed/confirmed present | raise at least one band |
| the above + tempo accelerating | consider critical |
| proximity_access has_access or at_or_near_target + specific_target | strong raise signal |
| pathway_stage at/beyond preparation + target_focus narrowing | consider a raise |
| source_credibility low | hold pending corroboration (band still floors at type) |

## What is deliberately absent

**Protective factors and inhibitors** (stabilizers, stake in conformity) have no box here. Under escalate-only they have no mechanical role — they only argue a case down, and they are the field's most misjudged, most gameable variable. Readers from SPJ traditions (WAVR-21, HCR-20) should read this record as deliberately asymmetric, not incomplete. Inhibitors inform case management, outside the score.

## The Q1 doctrine (why there is no lower path)

The conditioned priority is an escalation detector, not a queue-ranking model; de-prioritization is a case-management decision that must never be written back into the score. At scale, cases leave the queue by disposition (closure, monitoring tiers), never by score demotion — a demotion path becomes a laundering machine for capability discounts.
