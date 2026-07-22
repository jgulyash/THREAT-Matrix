# informs_axes — weak / moderate / strong / none boundary rubric (Step 7)

**Status:** Step-7 working-notes authoring aid. Authored 2026-05-20 (Session 25).
**Scope:** see "Scope and what this is NOT" at the end — this is **not** a schema or docs change.

## Purpose

`informs_axes` is EXPERIMENTAL V1.2 **type-level metadata** on an indicator: for the indicator *class* as written, which axes of the larger threat picture does observing it typically inform, and how strongly. Six axes in two triads:

- **Actor:** `actor_capability`, `actor_intent`, `actor_opportunity`
- **Postulated event:** `threat_timing`, `threat_target`, `threat_method`

Each axis takes one categorical value: **`none` / `weak` / `moderate` / `strong`**.

This rubric exists so two annotators (human + AI) coding `informs_axes` independently apply the *same* level definitions. The post-chunk-1 IRR re-check measures whether two raters apply these definitions **consistently** — it does not measure whether the definitions are *correct* (that was settled in the Step 6 reconciliation and the 5 Step-7 calibration questions). The definitions must therefore be locked *before* chunk-1 authoring; this document locks them.

## Three framing rules (apply to every axis)

1. **Resolution, not severity.** The question is *"how finely does observing this indicator class narrow what you know on this axis?"* — not *"how bad is it?"* Severity lives in `escalation_axes` / `escalation_weight` / `severity_band`. A low-severity indicator can still be `strong` on an axis (it resolves that axis sharply), and a high-severity indicator can be `weak` on an axis (it tells you little there).
2. **Type-level, not case-level.** Rate the indicator *class* as written in `behavior`. Do not rate a vivid hypothetical instance. Case-level specifics (this particular actor's exact motive, this particular victim) must not bake into the value. (Step 6 reconciliation #5, #7.)
3. **Categorical only.** The value is one of {none, weak, moderate, strong}. The mapping `strong=0.9, moderate=0.6, weak=0.3, none=0.0` is a **downstream-consumer convention only** — never a framework-level score. Do not author numbers.

## The universal level scale

Every axis has a **grain hierarchy** — coarsest knowledge to finest. The level says how far down that hierarchy observing the indicator class takes you:

| Level | General definition | Grain reached |
|---|---|---|
| **none** | Observing this indicator class tells you nothing on this axis — zero informational signal. | — |
| **weak** | Resolves the axis only at its **coarsest grain**: the axis-relevant fact *exists*, but no finer detail. | coarsest |
| **moderate** | Resolves **one grain finer**: the coarse fact **plus a narrowing** below it. | one finer |
| **strong** | Resolves to a **specific value** on the axis — a clear, specific signal. | specific |

**Locked weak/moderate boundary (verbatim, Step 6 reconciliation Group C, 2026-05-12):**
> `moderate` = "phase + something narrower (signal resolves below phase-level)"; `weak` = "phase-only information without finer resolution."

That wording is the **timing-axis instance** of the general principle above ("phase" = the coarsest grain *for `threat_timing`*). Each per-axis section below states that axis's own coarsest grain so the boundary is concrete for every axis, not only timing.

The hardest call is always weak vs moderate. The decisive question: **does the indicator resolve anything *below* the coarse "it exists" level?** If no → `weak`. If it adds exactly one narrowing → `moderate`. If it pins a specific value → `strong`.

---

## Axis 1 — `actor_capability`

**Signal:** the actor's skill, tradecraft, and operational sophistication.
**Coarsest grain:** "the behavior involved some deliberate action." **Finer:** "demonstrates a real competence." **Specific:** "demonstrates advanced / specialized tradecraft."

| Level | Definition | Anchor |
|---|---|---|
| none | Behavior demonstrates no capability signal at all — purely passive/ambient, achievable with zero skill *and* zero deliberate effort. Rare. | *(no TM0103 anchor — calibration-watch)* |
| weak | Demonstrates only that the actor took a deliberate action; no tradecraft visible. Basic OSINT, showing up at a location. | IND-0103-01 (physical presence), IND-0103-02 (digital recon) |
| moderate | Demonstrates a real competence: pretext durability, multi-modal coordination, concealed-imaging tradecraft, counter-surveillance behavior. | IND-0103-03 (photography), IND-0103-05 (insider elicitation) |
| strong | Demonstrates advanced / specialized tradecraft: acquiring **and productively analyzing** restricted operational artifacts (per Step 6 reconciliation #7). Credential fabrication, manufacturing, and regulatory-control defeat also land here (per `phase1-defaults.md` access & acquisition deviation guidance). | IND-0103-04 (blueprints/diagrams) |

Phase-1 category default: `access` = **moderate** (Q3 — phase-1 access indicators are all exploit-class; signal spans moderate-to-strong).

---

## Axis 2 — `actor_intent`

**Signal:** the actor's intent to act — read at **type level as *general* intent-to-act**, NOT specific motive class. Whether the actor wants to blackmail vs kidnap vs kill is a *case-level* property and is excluded (Step 6 reconciliation #5).
**Coarsest grain:** "some adverse interest exists." **Finer:** "purposive, directed attention toward the subject." **Specific:** "clear general intent-to-act."

| Level | Definition | Anchor |
|---|---|---|
| none | Behavior carries no intent signal. | *(no TM0103 anchor — calibration-watch)* |
| weak | Signals only diffuse / ambient adverse interest — could be idle, not yet directed. | *(no TM0103 anchor — calibration-watch)* |
| moderate | Signals purposive, directed attention toward the subject, but not yet clear commitment — exploratory. | IND-0103-01, IND-0103-02 |
| strong | Signals clear general intent-to-act: behavioral progression broad-to-narrow, operational specificity, retention of acquired materials, grievance paired with recon. | IND-0103-03, IND-0103-04, IND-0103-05 |

**Guardrail:** do not raise to `strong` because you can *imagine* a specific lethal motive — that is case-level reasoning. Rate general intent-to-act only.

**Calibration-watch (highest residual IRR risk on any axis).** The `weak` level has no TM0103 anchor, and the weak/moderate line — "diffuse / ambient adverse interest" vs "purposive, directed attention" — is the softest boundary in this rubric. The first time `weak` is coded on this axis during Step 7, run an IRR spot-check on that indicator before relying on the value.

---

## Axis 3 — `actor_opportunity`

**Signal:** the actor's opportunity — read for Step 7 as **action-opportunity** (the conditions that let the threat actually land). Informational opportunity (pattern-of-life mastery, security-gap knowledge) is a *moderate-tier contributor*, not strong (Q4 resolution; Step 6 reconciliation #8).
**Coarsest grain:** "actor has generic reach toward the subject's world." **Finer:** "actor has resolved a specific exploitable condition." **Specific:** "actor has realized action-opportunity."

| Level | Definition | Anchor |
|---|---|---|
| none | Behavior says nothing about opportunity (e.g., a pure grievance statement). | *(no TM0103 anchor — calibration-watch)* |
| weak | Signals only generic / ambient reach; no resolved exploitable condition. | IND-0103-02 (digital recon) |
| moderate | Signals a **resolved exploitable condition** — the *informational-opportunity* tier: pattern-of-life knowledge or security-gap awareness. (Generic, unresolved positional reach is `weak`, not here.) | IND-0103-01 (physical presence — repeat presence builds pattern-of-life knowledge), IND-0103-04 (blueprints — security-camera-diagram = security-gap knowledge) |
| strong | Signals **realized action-opportunity**: an exploited insider relationship, direct unsupervised access, demonstrated ability to reach the subject in an exploitable window. | IND-0103-03 (photography of interiors → achieved proximity), IND-0103-05 (insider elicitation → exploited relationship) |

Phase-1 category defaults: `planning` = **weak** (Q4 — artifacts prove only opportunity-to-acquire-the-artifact; pattern-of-life / security-gap planning variants deviate up to moderate). `communication` = **moderate** (Q5 — strong reserved for insider-elicitation / recruitment variants).

**V1.3 #2 tension (flagged, not fixed):** `actor_opportunity` currently bundles information-opportunity and action-opportunity. Step 7's working reading: `moderate` = the indicator resolves informational opportunity; `strong` = realized action-opportunity. This supersedes any "average the two sub-meanings" framing. V1.3 may split the axis.

---

## Axis 4 — `threat_timing`

**Signal:** proximity-to-action — when the threat will materialize.
**Coarsest grain:** "places the threat in a broad pathway phase." **Finer:** "phase + a narrower window." **Specific:** "pins a specific action window."

| Level | Definition | Anchor |
|---|---|---|
| none | No timing signal. | *(no TM0103 anchor — calibration-watch)* |
| weak | **Phase-only** — places the threat in a pathway phase (e.g., target_development) with no finer resolution. | IND-0103-01, IND-0103-02 |
| moderate | **Phase + something narrower** — phase plus a narrowing toward a window: schedule-aligned behavior, operational-tempo cues. | IND-0103-03, IND-0103-04, IND-0103-05 |
| strong | Pins a specific action window — imminent, dated, or event-aligned timing. | *(no TM0103 anchor — calibration-watch; phase-1 target_development indicators rarely pin timing)* |

This axis is the verbatim source of the locked weak/moderate boundary — "phase" here is literal.

---

## Axis 5 — `threat_target`

**Signal:** which specific target / asset is in view.
**Coarsest grain:** "a target / target-class exists." **Finer:** "narrows to a candidate set." **Specific:** "pins the specific named subject or subject-specific assets."

| Level | Definition | Anchor |
|---|---|---|
| none | No target signal — e.g., generic capability research implicating no subject. | *(no TM0103 anchor — calibration-watch)* |
| weak | Signals only that targeting is occurring at a target-*class* level; no specific subject. | *(no TM0103 anchor — calibration-watch)* |
| moderate | Narrows to a candidate set or subject-associated locations, but not the specific subject alone. | *(no TM0103 anchor — calibration-watch)* |
| strong | Pins the specific named subject, or subject-specific assets / locations. | IND-0103-01 — IND-0103-05 (all five) |

**Heavily skewed anchor set — calibration-watch.** All 5 TM0103 indicators are `strong` because Environmental Survey is intrinsically subject-specific. Other phase-1 tactics will produce the unanchored levels: e.g., a TM0104 indicator like "researches improvised weapon construction" implicates no subject → likely `none`; a TM0101 Target Selection indicator surveying a candidate pool → `weak` or `moderate`. Watch these closely; consider an IRR spot-check the first time `weak`/`moderate`/`none` is coded on this axis.

---

## Axis 6 — `threat_method`

**Signal:** how the attack will be conducted. **All methods in THREAT Matrix scope are physical** — the framework has no digital / remote execution. There is no "physical vs digital" narrowing to make (Step 6 reconciliation Group B).
**Coarsest grain:** "method-agnostic — all physical methods in play." **Finer:** "narrowed to a few candidate physical methods." **Specific:** "a specific physical method."

| Level | Definition (locked verbatim, Step 6 reconciliation Group B) | Anchor |
|---|---|---|
| none | Method-agnostic — all physical methods remain in play. | *(no TM0103 anchor — calibration-watch)* |
| weak | Barely narrows within the physical-methods space. | IND-0103-01, IND-0103-02 (location study doesn't narrow physical method) |
| moderate | Narrows to **2–3 candidate physical methods** (e.g., blueprints hint cameras→covert approach, exits→containment, interior layout→entry-and-clear). | IND-0103-03, IND-0103-04, IND-0103-05 |
| strong | Pins a **specific physical method** — e.g., VBIED, hostage scenario, targeted assassination. | *(no TM0103 anchor — calibration-watch; phase-1 target_development rarely pins method)* |

This axis's "2–3 candidates" is a count-based specialization of the universal one-grain-finer principle — `moderate` = narrowed-but-not-pinned.

**Guardrail (the #1 AI-annotator failure mode — Step 6 reconciliation Group B):** never treat "physical vs digital/remote execution" as a narrowing. There is no digital execution in framework scope. Digital *reconnaissance* (an indicator) still describes a *physical* attack downstream.

---

## Two AI-annotator failure modes to guard against (Step 6 reconciliation Pattern 3)

1. **Out-of-scope baseline.** Do not apply a broader-universe interpretation that does not exist in framework scope. The framework is the **person matrix, physical execution**. threat_method: all execution is physical (above). Rate every axis against the framework's actual scope, not a generic threat universe.
2. **Conflating sub-meanings within an axis.** Two axes bundle two sub-meanings:
   - `actor_opportunity` = information-opportunity + action-opportunity → Step 7 reading: `moderate` = informational tier, `strong` = realized action tier.
   - `actor_intent` = general intent-to-act + specific motive class → Step 7 reading: general intent-to-act only; specific motive is case-level and excluded.
   When an indicator is strong on one sub-meaning and weak on the other, do not silently average to a false-precise middle — apply the Step-7 reading explicitly.

## TM0103 worked-anchor matrix (30 shipped consensus judgments)

| Indicator (class) | actor_capability | actor_intent | actor_opportunity | threat_timing | threat_target | threat_method |
|---|---|---|---|---|---|---|
| IND-0103-01 physical presence | weak | moderate | moderate | weak | strong | weak |
| IND-0103-02 digital recon | weak | moderate | weak | weak | strong | weak |
| IND-0103-03 photography | moderate | strong | strong | moderate | strong | moderate |
| IND-0103-04 blueprints/diagrams | strong | strong | moderate | moderate | strong | moderate |
| IND-0103-05 insider elicitation | moderate | strong | strong | moderate | strong | moderate |

These 30 are the reconciled SHIPPED values (IRR κ_w = 0.70, AC2 = 0.86, all 9 disagreements 1-step). Every level definition above is consistent with this matrix. When a Step-7 coding feels uncertain, find the closest TM0103 row and reason by analogy from its shipped value.

## Scope and what this is NOT

This rubric is a **Step-7 working-notes authoring aid**. It transcribes already-locked doctrine — the Step 6 reconciliation thresholds, the universal scale semantics from the Session 24 handoff, and the 5 Step-7 calibration-question resolutions — into one IRR-usable reference.

It is **NOT**:
- a change to `framework.schema.json` (the per-axis informs_axes properties remain description-less by design);
- a change to `framework.json`;
- the implementation of V1.3 refinement #4. V1.3 #4's deliverable is formal *schema/docs axis-description text*. This rubric is the **input** to that future formalization, not the formalization itself.

**V1.3 tensions flagged here — ✅ FORMALIZED 2026-07-09 (Session 30): refinements #1–#4 shipped as schema axis-description text on informs_axes (per-axis level semantics + elected readings), alongside the three-capability-construct distinction. This rubric remains the authoring-depth reference; the schema text is the consumer-facing contract.**

**Original deferred list (as flagged in Step 7):**
- #1 `actor_intent` — formally tighten to "general intent-to-act" or split general/specific.
- #2 `actor_opportunity` — formally split or align information-opportunity vs action-opportunity.
- #3 `threat_method` — promote the framework-physical-scope scale into schema axis-text.
- #4 boundary anchors — promote this rubric's level definitions into schema/docs axis-description text.
