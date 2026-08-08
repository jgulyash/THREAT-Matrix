# conditioning_guidance — authoring rubric (ratified 2026-08-06)

The standard every `conditioning_guidance` entry is authored and reviewed against. Ratified via a 24-entry validation batch spanning the hard classes (acts underway, aftermath, organizational non-physical harm, thin-reveal reconnaissance, technical-fact scoping), reviewed and accepted without changes; the batch entries and five earlier owner corrections are the canonical anchors. Contributors extending the framework author to this rubric.

## What the field is (unchanged)

Per-indicator, type-level, assessment-scoped investigative tasking: **which instance factors are the hidden drivers of danger for this behavior class, and what should the analyst go collect.** Machine tags (`probe_factors`, the six instance-factor enum names) + one prose directive (`guidance`, max 420 chars). A framework-provided default consumers may follow, extend, or override; intended for composition across observed-indicator combinations, not single-indicator reading. It does not affect the score.

## The consumer (owner ruling, 2026-08-07)

The entry addresses the analyst, investigator, or threat manager working the case, never the on-scene responder. It tasks only collection reachable from analyst sources: case records, communications, prior indicators, telemetry, logs, platform analytics, report streams, and post-event review. Scene-observable facts on a response timescale (how far a fire reaches, who stands in a vehicle's path, how near a cut member is to failure) are incident-command work and are never tasked here. For an act underway, the analyst's lane is the pathway behind the act (what mobilization preceded it that collection can now surface), the case connection (whether the actor ties to a known subject, grievance, or open case), and the act after this one (follow-on, secondary, re-attack). Scope questions stay only where the answer comes from analyst-accessible data (how far a wipe spread across relays, how widely a narrative traveled), not from eyes on the scene.

## Scope boundary

**conditioning_guidance carries NO response tasking.** Alerting, notification, mitigation, evacuation, takedown, and coordination live in the tactic's `response_protocols` (a first-class framework object, 2 per tactic). For behaviors that are a harmful act underway, the cg entry stays assessment-scoped: verify the reporting is real, gauge scope and trajectory, and hold open the actor questions the act does not settle (one actor or many, whole attack or cover for a second act, continuation).

## Making the boundary discoverable (so no practitioner reads cg as "not far enough")

The deferral must be visible at the moment the instinct fires, on four layers:

1. **SPA (primary):** a standing caption under the Conditioning Guidance heading on EVERY indicator detail: "Assessment tasking only. Immediate response actions live in this tactic's Response Protocols" with a link that jumps to the tactic's RP section. This catches the reader exactly where the "doesn't go far enough" reaction happens, on all 815 entries, without bloating the prose.
2. **Schema:** one sentence in the field's `description` (the contract consumers build against): assessment-scoped; response actions are carried by the tactic's response_protocols.
3. **Methodology doc:** the scope-boundary section in conditioning-guidance-field.md, with the F0301-01 example of why.
4. There is deliberately NO per-entry deferral clause: with layers 1-3 in place, a clause repeated across every acts-underway entry would go stale and pad the prose. (Decided at ratification.)

## Voice rules

1. **Imperative opener** naming the collection or assessment action: Assess, Establish, Confirm, Determine, Identify, Verify, Weigh, Assemble, Track, Build out. Not colloquial.
2. **Hedge every inferential claim, in both directions.** What the behavior reveals: "can narrow", "may show", "can signal", "could reveal". What it conceals: "may not show", "may show little of", "could still be masked", "may or may not surface". Banned as flat meaning-claims: marks, confirms, proves, resolves, fixes, hides, shows nothing, leaves nothing/little, will not show/tell, cannot tell you, "but not the X" contrast frames, "names ... plainly", "makes plain". The observable act may be described factually; what it MEANS is always an inference and always hedged. Near-certain technical scoping uses precise modal phrasing ("cannot by itself establish"), never blanket assertion.
3. **Never claim the act settles the actor picture.** One actor or many, whole attack or diversion, continuation, sophistication: open questions, name them where useful.
4. **Target hedging:** "target candidates" / "may be converging on"; an apparent target can be misdirection. The target is not always a person (place, asset, institution).
5. **Alternative explanations** where the behavior admits them: an innocent anomaly, a lost contractor, an opportunist's shortcut, a cutout, or other less nefarious goals.
6. **Concrete consequences,** not intensifiers: "how close an attack may be", "whether the actor is able to carry it out, and how soon", "how much is at stake". Never "turns serious", "the lever", "drives escalation".
7. **Name the actor and the culminating act** (an attack; the matrix equivalent: an attack on the site / acting against the institution / an attack on the system or process). Never a bare "it"/"this".
8. **Frames:** Aftermath (p4): task continuation, attribution, follow-on, rebrand, not proximity to a first attack. Acts underway: verify-and-gauge plus open actor questions plus response deferral (scope boundary above). Execution-support acts: standard investigative frame.
9. **Plain hedges** (can/could/may), no ICD-203 estimative lexicon ("likely", "probably", "we assess", confidence levels).
10. **Definite article for the observed; indefinite/hedged for the inferred** ("the pretext" vs "a working timeline").
11. **No em/en dashes.** Max 420 chars; use length only when the tasking needs it; do not pad. Vary openers and sentence shapes so 800 entries do not read machine-stamped.
12. **Tags and prose agree.** target_focus = the target/targeting; pathway_stage = where they are on the pathway; means_in_hand = capability/the means; tempo_trajectory = tempo/pace/trajectory; proximity_access = opportunity/access/reach; source_credibility = how solid the reporting is. No tagged factor the prose never addresses; no addressed factor left untagged.

## Confirmation targeting (owner ruling, 2026-08-07)

A Confirm/Verify/Establish opener must name the actual uncertainty; it never re-asks whether the indicator fired (the indicator having fired IS the observation). Three legitimate targets, and only three:

1. **Classification** when a benign twin produces the same observable: a deliberate ram vs. an accident or medical event at the wheel; a hostile setpoint vs. a controller fault; sabotage cutting vs. permitted structural work; arson vs. accidental fire. The classification call is the hinge that changes everything downstream.
2. **Report reality** when the source chain is indirect (peer report, intercept, single sensor) and first reports are characteristically unreliable: name what is unconfirmed ("how solid the first reports are", "whether occupants are actually held rather than sheltering").
3. **Suspicion resolution** when the behavior itself is stated as suspected: a suspected device's viability is genuinely the question ("can be a working charge or a hoax").

If none applies, there is no confirmation opener: the entry opens with its assessment move. Generic forms ("Confirm the report", "confirm X is real") are banned. A verification lead is further reserved for discriminations that are themselves behavior-specific analyst collection (a telemetry twin names what to check; a suspected device names viability); generic report-solidity belongs to the instance record's source_credibility factor and rides, at most, as a subordinate clause.

## probe_factors selection (judgment, not mechanics)

Read the behavior and its informs_axes; weak/none axes suggest hidden factors but are never a formula (mechanical inversion was tried and disproven at ~5% match). Ask: for a real case built on this behavior, what would a threat manager most need to collect next to judge danger? source_credibility surfaces where "is this report even real?" is the live question.

## Canonical anchors

The ratified validation batch (24 entries, in the shipped data) plus five earlier owner corrections (IND-0107-06, IND-0105-04, IND-0105-05, IND-0209-03, IND-0204-04). The pre-ratification 18-example set is superseded.
