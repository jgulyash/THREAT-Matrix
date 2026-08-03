# Worked Cases (fictional)

Three end-to-end walk-throughs of the instance-conditioning contract, one per edge of its behavior: a case held at type, a case raised one band, and a case raised to critical. **Every case is fictional** — no real person, organization, or venue. Each `.json` is a schema-valid `conditioned_assessment`; the walk-through below shows how an analyst would arrive at it. The framework ships no instance data; these exist to show the contract in use.

---

## Case 1 — held at type (`case-1-held-at-type.json`)

**Observed behavior.** An anonymous web-form tip reports that "someone has been asking around about" a named nonprofit's office hours and staff. No named subject, no corroboration.

- **Indicator class:** IND-O0101-04, Organization Target Selection — basic identifying-detail collection. **Type band: low** (ambient pre-operational recon).
- **Instance record:** target_focus unknown, pathway_stage unknown, means_in_hand unknown, tempo unknown, proximity_access unknown, source_credibility **low**.
- **Raise guidance:** low source credibility → hold pending corroboration. Nothing resolves a target, a capability, or a trajectory.
- **Result:** conditioned_priority **low**, equal to the type band — read as **held** (priority not above band). The all-unknown, low-credibility instance does not demote and does not raise.
- **What the analyst does next:** open a monitoring record; seek corroboration; do not escalate. If a named target or a capability later resolves, re-condition.

## Case 2 — raised one band (`case-2-raised-one-band.json`)

**Observed behavior.** HR and two coworkers independently report that an employee has repeatedly voiced a specific grievance against a named manager and has begun asking which days that manager works on-site.

- **Indicator class:** IND-0101-01, Target Selection — articulating a specific grievance tied to a specific individual. **Type band: medium.**
- **Instance record:** target_focus **specific_target**, pathway_stage research_planning, means_in_hand **assessed_present** (lawfully able to acquire the means), tempo steady, proximity_access seeking_access, source_credibility **high**.
- **Raise guidance:** specific_target + means assessed_present → raise at least one band. Tempo is not accelerating, so not critical.
- **Result:** conditioned_priority **high**, one band above the medium type — read as **raised**.
- **What the analyst does next:** active case management; interview/collateral steps; watch tempo. Acceleration would push toward critical.

## Case 3 — raised to critical (`case-3-raised-to-critical.json`)

**Observed behavior.** Multi-source reporting: an individual has been conducting sustained research on one named person, the means was directly observed in the individual's possession, the individual has been seen moving toward the target's location, and the timeline across recent observations is compressing.

- **Indicator class:** IND-0101-02, Target Selection — sustained online research on a specific individual. **Type band: high.**
- **Instance record:** target_focus **specific_target**, pathway_stage preparation, means_in_hand **confirmed_present**, tempo **accelerating**, proximity_access **at_or_near_target**, source_credibility high.
- **Raise guidance:** specific_target + confirmed means + accelerating → consider critical; attained access + specific_target is a strong raise signal. All converge.
- **Result:** conditioned_priority **critical**, one band above the high type — read as **raised**.
- **What the analyst does next:** immediate escalation to threat management and, per policy, protective and law-enforcement channels. This is the false-LOW the contract exists to catch: a type-high indicator that a specific, capable, accelerating, proximate instance pushes to critical.

---

## The through-line

The type band is the floor in all three. Nothing here lowers it — the all-unknown Case 1 holds, and only converging positive evidence raises. The difference between a monitoring record and an immediate escalation is carried entirely by the instance layer, joined to the type score, never by the type score alone.
