# THREAT Matrix Voice Guidelines

**Date:** 2026-04-30
**Amended:** 2026-07-20 (V1.5 review) — Rule 4 literature register clarified (no first-person disclaimer); Rule 5 third-party "adversary" carve-out added.
**Status:** LOCKED for V1.1+ content authoring
**Audience:** Maintainers and contributors authoring tactic content (`field_notes`, indicators, countermeasures, response protocols)

THREAT Matrix is practitioner-first by design and by schema. The framework's evidence model (`evidence_basis` enum), source typing (Tier 1 includes attested operational experience), and mandatory `field_notes` field all enforce this structurally. These voice rules govern the prose that fills the schema.

The six rules below apply to all V1.1+ content authoring. They are not editorial preferences. They are quality discipline.

---

## Rule 1 — Rewrite clinical-anchor framings

**Citations are structural, not prose.**

Every tactic, indicator, countermeasure, and response protocol has a `source_refs` array for citations. The bibliography links live there. Prose must not duplicate citations rhetorically.

**Wrong (clinical anchor in prose):**
> "Psychologically-driven actor with obsessive focus on a specific target. Clinical anchor: WAVR-21, PATH model, Threat Assessment in Schools."

**Right (citations live in source_refs; prose stays practitioner):**
> "Psychologically-driven actor with obsessive focus on a specific named target. The fixation is the defining characteristic — this actor's threat is organized entirely around one person."
>
> `source_refs: ["WHITE-MELOY-WAVR21-2016", "CALHOUN-WESTON-2003", "VOSSEKUIL-FEIN-REDDY-2002"]`

The reader who wants the academic backing finds it in source_refs. The reader who wants to know what the tactic looks like reads the prose without an academic detour.

---

## Rule 2 — Latinate to observable action

**Keep Latinate terms as formal labels (field names, phase names, tactic names) but rewrite descriptions in observable-action vocabulary.**

Latinate descriptors signal academic distance. Observable-action descriptors signal practitioner literacy. Both can describe the same behavior; only the second connects to what a reviewer in the field actually encounters.

**Latinate (academic):** "Subject demonstrates escalating ideation, mobilization toward operational preparation, and increasing fixation on target."

**Observable-action (practitioner):** "Subject is showing up where the target is more often. Started buying things they don't normally buy. Talks about the target without prompting in conversations."

Use Latinate terms where they ARE the label (the phase is named "Mobilization"). In descriptions, render the label in observable-action language.

---

## Rule 3 — Encounter-first structure

**What the practitioner encounters first, then what it means taxonomically, then citation last.**

Bad practitioner content tells you the taxonomy and assumes you'll connect it to encounter. Good practitioner content describes the encounter and lets the taxonomy follow.

**Wrong (taxonomy-first):**
> "Pathway behavior in Phase 1 (Target Development) involves research, planning, preparation, or implementation of an attack as documented by Meloy & Gill (2016)."

**Right (encounter-first):**
> "The first thing you usually notice is the research artifact — a saved address, a downloaded blueprint, a printed schedule. Sometimes a peer brings it to you because it didn't sit right. Taxonomically this is pathway behavior in early-phase Target Development; the source literature on this construct is in Meloy & Gill (2016)."

Encounter-first prose teaches a reader to recognize the pattern. Taxonomy-first prose teaches a reader to look it up.

---

## Rule 4 — Voice follows evidence

**The `evidence_basis` enum declares the grounding; the prose follows the declaration.**

Practitioner register is the default when `evidence_basis` is `operational_primary` or `hybrid`. Academic register is appropriate when `evidence_basis` is `literature_primary` or `literature_only` — but even literature-grounded content should describe observable behaviors in encounter-first language.

The framework supports BOTH registers. The schema declares which is which. The prose must follow the declaration.

**For `operational_primary` content** — practitioner voice throughout. `field_notes` describes what the maintainer or contributor has actually seen. `observed_contexts` lists generic context archetypes from practice.

**For `literature_only` content** — the `field_notes` signal the documented grounding through an ANALYTIC register attributed to the sources, not a first-person disclaimer. The framework is not personal narration about any individual maintainer, so do not write "I haven't worked a case involving this directly." Instead attribute the pattern to the documented record. Example pattern: *"The documented pattern is that a threat actor... The literature describes... The analytic marker is..."* Honesty is first-class, carried by the documented-register attribution rather than a personal confession. The `observed_contexts` may be tagged `[literature: <source-id>]` so the reader sees the provenance.

*(Amendment 2026-07-20: the prior example used a first-person "I haven't worked this directly" disclaimer. That was retired because the framework's voice is analyst-general, not personal memoir; the honesty signal is the documented-register attribution.)*

**For `hybrid` content** — practitioner voice frames the observable detail; academic citation supports. The schema and prose work together.

---

## Rule 5 — Canonical actor naming

**The framework names two roles consistently across all behavior, indicator, countermeasure, and response-protocol prose. Notes and cpn_notes are exempt; metadata stays general.**

| Concept | Canonical term | Pre-canonical wording (do not use) |
|---|---|---|
| The adversary performing the observable behavior | **Threat actor** | "Subject" (capitalized) |
| The person being targeted or protected | **targeted subject** *(primary)* / `the target` *(possessive carve-out)* / `named individual` *(variety)* | "target" (alone, when meaning the person, except in carve-out below) |
| Actor-target compound | "the threat actor / targeted subject pair" | "subject-target pair" |

**Possessive-compound carve-out.** In possessive compounds where the noun, not the person, carries the meaning, `target's <noun>` is acceptable: `the target's calendar`, `the target's residence`, `the target's vehicle`. Reading `the targeted subject's calendar` repeatedly produces the fatigue Rule 6 is designed to avoid. Use judgment: when the protectee is the foreground, write `targeted subject`; when the noun is the foreground, `target's <noun>` is acceptable.

**Variety carve-out.** When the protectee has just been referenced as `targeted subject` and the next reference would create local redundancy, `named individual` or `individual` is an acceptable alternative — particularly in extended prose like `field_notes`. Do not introduce new alternatives (`subject`, `victim`, `mark`, etc.); the rotation is `targeted subject` / `the target's <noun>` / `named individual` / `individual`.

**Latinate label carve-out.** Tactic names, phase names, and field names that are Latinate labels stay as-is — `Subject Profiling` (the tactic), `Target Selection` (the tactic), `Subject Description` (the field). Body prose still uses `Threat actor` and `targeted subject`.

**Third-party "adversary" carve-out (Amendment 2026-07-20).** "Adversary" is banned only as a label for the threat actor; the canonical term for the actor is "threat actor." When "adversary" refers to a THIRD PARTY, for example a rival institution the threat actor frames in an attribution-obfuscation tactic ("the trail terminates at a convenient adversary"), "adversary" is acceptable and is often stronger than "rival." Do NOT blanket grep-ban "adversary" in voice audits; surface it for judgment and keep it only where it means a party other than the threat actor. The hard bans (em and en dashes, smart quotes, "attacker", "practitioner" in body prose) are unaffected.

**Right (canonical):**
> "Threat actor appears at locations associated with the targeted subject on multiple occasions with no apparent legitimate reason."
> "Multiple correlated indicators detected for the same threat actor / targeted subject pair."
> "Implement protective measures for the targeted subject."

**Wrong (pre-canonical):**
> "Subject articulates specific grievance tied to a named individual..."
> "...for the same subject-target pair."
> "Implement protective measures for the identified target."

This rule is enforced retroactively. Any pre-canonical wording surfaced during authoring is rewritten in the same commit that touches the tactic.

---

## Rule 6 — Voice variety palette (anti pattern-collapse)

**The framework will scale to 150+ tactics. If 30% of tactics use the same opener phrase, the corpus reads as Mad-Libs and the voice fails — irrespective of whether each individual paragraph is well-written. Variety is enforced at three levels: opener phrase, mid-paragraph pivot phrase, and diction.**

**Pattern usage is unconstrained — phrase variety is the actual enforcement.** The six opener patterns below are tools, not quotas. Pick the pattern that best fits the tactic. The same pattern may be used for many tactics in a row as long as no opener PHRASE repeats more than three times across the corpus.

### Six opener patterns (pick the best fit)

Each pattern is voice-compliant under Rules 1–4. Pick the pattern that best fits the tactic — pattern frequency is descriptive, not prescriptive. The phrase-level cap (no opener PHRASE repeats more than three times across the full framework) is the variety enforcement.

| # | Pattern | Example | Best for |
|---|---|---|---|
| 1 | **Behavioral-observation** | "The first signal you usually catch is repetition where there shouldn't be any." | Tactics where the entry signal is unambiguous |
| 2 | **Functional-definitional** | "Subject Profiling is the tactic that turns 'a name' into 'a target file'." | Tactics where the *function* is the most useful frame |
| 3 | **Decision-point** | "Target Selection is the point where a vague or specific grievance lands on a named person." | Tactics that pivot on a binary or threshold |
| 4 | **Literature-anchored** | "Pathway Indicators are the observable behaviors that mark a threat actor's progression toward an attack..." | `evidence_basis: hybrid` or `literature_primary` |
| 5 | **Counter-intuitive / tension** | "The thing about Cover Construction is that it doesn't usually fail at the cover — it fails at the second-order detail nobody scripted." | Tactics where common intuition is wrong |
| 6 | **Mechanism / typology** | "Capability Acquisition resolves into three pathways: legitimate purchase, theft or diversion, and proxy procurement." | Tactics with distinct sub-types |

A 7th may be used when warranted: **temporal anchor** ("By the time Network Development is observable, the threat actor has decided they need help.") — useful for late-phase or threshold-driven tactics.

### Mid-paragraph pivot variety

The pivot is the sentence that moves the paragraph from definition to behavior. **No mid-pivot phrase may appear in more than two tactics.** Rotate among:

- "Operationally, this resolves into..." / "Operationally, this can resolve into..."
- "What separates this tactic from [adjacent] is..."
- "Past this point, the work has shifted from..."
- "Where this tends to surface is..."
- "In casework, the entry point is usually..."
- "The detection vector is..."
- "Two distinct streams produce this: A and B..."

Avoid as default openers: "The signal you usually catch is..." (echoes Rule 1's exemplar). Avoid as defaults: "The threat actor is no longer just..." beyond two tactics.

### Closing texture variety

Avoid using `"X is heaviest in [phase] but compresses sharply just before [phase]"` more than twice. Rotate among:

- "Most of X sits in [phase], with a tail into [phase]."
- "X is front-loaded in [phase]; residual signal in [phase] is mostly attributable to [reason]."
- "The window where this is most catchable is..."
- "After [event], X is essentially closed unless [condition]."

### Rhetorical-stance caps

The audience perceives stance more strongly than content. Stance variety is the single biggest defense against pattern-collapse.

| Stance | Example | Cap (across the 150+ tactic corpus) |
|---|---|---|
| **You-address** | "The first thing you catch is..." | ≤ 15% |
| **Role-narrator** ("an analyst", "an investigator", "the threat management team", "the threat assessment team") | "An analyst usually surfaces this through..." / "The threat management team escalates when..." | ~30–35% |
| **Case-pattern** | "In observed cases, the entry point is usually..." | ~25–30% |
| **Mechanism-narrator** | "X surfaces in two ways..." | ~15–20% |
| **Other / mixed** | situational | balance |

You-address is high-impact in small doses and corrosive at scale. Cap it tight.

### Diction (analyst / investigator, not practitioner)

The word **`practitioner`** is too clinical for body prose. In tactic content (`field_notes`, `observed_contexts`, indicator behaviors, countermeasure measures, response-protocol actions and triggers), use rotation:

- **analyst** — threat assessment analyst, security analyst, intelligence analyst
- **investigator** — threat assessment investigator, security investigator
- **threat management team** — collective noun for the assessment body (no hyphen)
- **threat assessment team** — collective noun for the assessment body
- **security professional** — generalist role descriptor
- **reception**, **security personnel**, **threat reporters** — domain-specific roles

Excluded from the rotation: `practitioner` (clinical), `protective intelligence analyst` (over-specific compound that reads as a job title rather than a role), and unilateral substitutes like `expert` or `professional` without a domain anchor.

`practitioner` may appear in meta-documents (this VOICE.md, README.md, CLAUDE.md) describing the audience — but not in the framework's tactic content itself.

**Deployment rule:** across the corpus, no single role term should account for more than ~30% of role-references in tactic `field_notes`. The voice-audit pass at session start should grep tactic field_notes for role-term distribution and surface any term running hot.

### Three-rule discipline (the standard)

1. **No identical opener PHRASE** appears more than 3 times across the full corpus. (Pattern usage itself is unconstrained — best fit wins.)
2. **No mid-paragraph pivot phrase** appears more than 2 times.
3. **You-address stance** ≤ 15% of tactic `field_notes`.

A periodic voice-audit pass (corpus-wide grep of common openers, pivots, and stance markers) is the operational enforcement.

---

## Application Checklist

Before submitting any tactic, indicator, countermeasure, or response protocol for V1.1, verify:

- [ ] No "clinical anchor" or similar citation-in-prose framings (Rule 1)
- [ ] Descriptions use observable-action vocabulary (Rule 2)
- [ ] Encounter precedes taxonomy and citation (Rule 3)
- [ ] Prose register matches the declared `evidence_basis` (Rule 4)
- [ ] Canonical actor naming applied: "Threat actor" / "targeted subject"; possessive-compound carve-out and variety carve-out (`named individual`/`individual`) used where appropriate (Rule 5)
- [ ] Opener pattern selected from the six-pattern palette and rotated against recent commits (Rule 6)
- [ ] No `practitioner` and no `protective intelligence analyst` in tactic content; analyst / investigator / threat management team / threat assessment team rotation used (Rule 6)
- [ ] You-address stance not over-used (Rule 6 cap: ≤ 15%)
- [ ] No single role term > ~30% of role-references in field_notes (Rule 6)
- [ ] `field_notes` written in 3–6 sentences, voice-led, encounter-first
- [ ] `observed_contexts` lists pattern archetypes only (no case names, no PII)
- [ ] `source_refs` includes at least one Tier 1 source

---

## What this is not

These voice rules do not require the maintainer or contributors to be unable to write academic prose. The framework cites peer-reviewed literature throughout. What the rules require is that the prose carry practitioner literacy as the default and use academic register only where the evidence is academic.

The reader who matters most is the practitioner who picks up the framework and recognizes their own work in it. Build for that reader.