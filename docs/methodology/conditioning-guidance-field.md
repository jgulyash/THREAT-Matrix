# conditioning_guidance — per-indicator investigative tasking (V1.6)

Every indicator carries a `conditioning_guidance` object: `probe_factors` (a machine-filterable array of instance-factor enum names) and `guidance` (a natural-language practitioner directive, max 420 characters). The field answers one question for each behavior class: **which instance factors are the hidden drivers of danger — the things the behavior does not surface but that decide how dangerous the case is — and what should the analyst go collect?**

It is the third member of a deliberately distinct trio:

| Field | Question it answers |
|---|---|
| `informs_axes` | What does observing this behavior *reveal* about the actor and the postulated event? |
| `assessment_guidance` (tactic-level) | How should an analyst *read* evidence for this tactic class? |
| `conditioning_guidance` | What does this behavior *hide* that decides case danger, and what should the analyst collect next? |

## Provenance: why this field is authored, not derived

The field replaces a pilot (`instance_conditioning_hints`, 23 People indicators) that tagged which `informs_axes` tend to lift at instance time. A derivation experiment (S37, stage-1) tested whether those hints could be computed mechanically from `informs_axes`: the pilot's real signal matched a mechanical inversion of `informs_axes` on only ~5% of values. The judgment "which hidden factor decides danger for this behavior" is not a function of what the behavior reveals; it is practitioner knowledge about the *class of case* the behavior opens. The pilot was therefore retired, and the field was reconceived as first-class authored content, written to a locked 11-rule voice (professional imperatives, named actor and culminating act, concrete consequences, analytic humility, aftermath and active-execution frame variants, no estimative lexicon) and validated against an 18-example hand-authored gold set before the 815-indicator authoring pass.

## The openness contract

`conditioning_guidance` is a **framework-provided default starting point, not a prescriptive or complete instruction** — the same posture as `escalation_rubric`, which consumers "may follow or override with documented rationale."

- **Intended consumption is composition, not single-indicator reading.** A real playbook triggers on combinations of observed indicators (see `detection_mesh` / `correlates_with`); the framework supplies per-indicator seeds and the consumer's tooling composes them. `probe_factors` is machine-readable precisely so consumers can compose and filter across combinations ("show every indicator where proximity_access is the hidden driver").
- **The default is not the full extent of practitioner action.** It is useful to a human reading one indicator; its larger value is as an extensible, composable base a consumer wires into their own procedures, assets, and thresholds.
- **Openness raises the quality bar; it does not lower it.** A seed everyone inherits propagates its quality. These defaults are authored to be trustworthy enough that a consumer would rather extend them than rewrite them.

## The scope boundary: assessment, never response

`conditioning_guidance` carries **no response tasking**. Alerting, notification, evacuation, mitigation, takedown, and coordination are the province of the tactic's `response_protocols` — a first-class framework object, two per tactic. The boundary was settled on a hard case: for an active incendiary attack on an occupied structure, the practitioner's first moves are response moves, and an early draft of that entry absorbed them ("alert site security and first responders... support mitigation"). That draft was rejected: a per-indicator assessment seed that duplicates response doctrine drifts from the RPs it shadows and bloats the field beyond its design. The ruling: **an act underway is a response moment; this field stays assessment-scoped and the response protocols carry the response.** For a harmful act in progress, an entry does exactly three things: verify the reporting is real, gauge scope and trajectory, and hold open the actor questions the act does not settle (one actor or many, whole attack or cover for a second act, continuation). The deferral is surfaced where practitioners read: a standing caption on every indicator's Conditioning Guidance section in the reference SPA (linking to the tactic's Response Protocols), this document, and the schema field description.

## Reading rules

- The field is **type-level** and does not affect the score. It points at the instance factors (`$defs.instance_assessment`) whose values decide the conditioned case priority.
- Every inferential claim is hedged in both directions — what the behavior may reveal and what it may conceal — because a threat actor may telegraph everything or nothing. No entry claims the act settles the actor picture.
- Phase 4 (Aftermath) entries task **continuation, attribution, and follow-on** rather than proximity to a first attack: the culminating act is past, and the live question is whether it is over.
- Acts underway follow the three-move assessment frame above; execution-phase support acts (staging, positioning, comms) keep the standard investigative frame.
- No behavior reveals everything. Even the highest-reveal behaviors carry a directive, because deeper questions always remain: sophistication, number of actors, continuation, diversion, whether this is the whole picture.
