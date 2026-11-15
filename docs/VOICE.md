# THREAT Matrix Writing Rules

**First issued:** 2026-04-30. **Amended:** 2026-07-20 and 2026-07-23 (Rules 4 and 5). **Amended:** 2026-11-15 (case-record rendering rule added to Rule 5; source wording aligned with public-sources-only).
**Audience:** anyone writing or reviewing vocabulary text: `notes`, `field_notes`, `observed_contexts`, indicator `behavior`, countermeasure `measure`, and response-protocol `action` and `trigger`.

These rules govern the prose inside the vocabulary. They exist so that an entry reads as a description of something observable, cites its sources in the right place, and uses the same words for the same things throughout.

**How the rules are enforced.** By review. No gate reads prose for these rules. The only mechanical checks on prose are that no text is empty or padded with whitespace, and that `conditioning_guidance` is at most 420 characters with no em or en dash. Everything else here is an obligation on the author and the reviewer.

**Sources.** Every entry cites public sources only, in `source_refs`. Unpublished experience is not a source. See [METHODOLOGY.md](./METHODOLOGY.md#4-evidence-basis).

---

## Rule 1: Citations live in source_refs, not in prose

Every tactic, indicator, countermeasure, and response protocol has a `source_refs` array. Citations go there. Prose does not repeat them as a list of authorities.

**Wrong (authorities named in prose):**
> "Psychologically driven actor with obsessive focus on a specific target. Clinical anchor: WAVR-21, PATH model, Threat Assessment in Schools."

**Right (prose describes; citations sit in source_refs):**
> "Psychologically driven actor with obsessive focus on a specific named target. The fixation is the defining characteristic: the behavior is organized around one person."
>
> `source_refs: ["WHITE-MELOY-WAVR21-2016", "CALHOUN-WESTON-2003", "VOSSEKUIL-FEIN-REDDY-2002"]`

The reader who wants the source finds it in `source_refs`. The reader who wants to know what the behavior looks like reads the prose.

---

## Rule 2: Describe observable action

Keep formal terms where they are labels (field names, phase names, tactic names). In descriptions, say what can be seen or recorded.

**Abstract:** "Demonstrates escalating ideation, mobilization toward operational preparation, and increasing fixation on target."

**Observable:** "Threat actor appears where the targeted subject is more often, makes purchases outside an established pattern, and raises the targeted subject unprompted in conversation."

Use a formal term where it is the label (the phase is named "Mobilization"). In a description, render it as observable behavior.

---

## Rule 3: Observation first, classification second

Say what is encountered first, then how it is classified. Citations stay in `source_refs`.

**Wrong (classification first):**
> "Pathway behavior in Phase 1 (Target Development) involves research, planning, preparation, or implementation of an attack as documented by Meloy and Gill (2016)."

**Right (observation first):**
> "The first thing usually noticed is a research artifact: a saved address, a downloaded floor plan, a printed schedule. Sometimes a colleague reports it because it did not seem right. This is pathway behavior in early Target Development."

---

## Rule 4: Register follows the declared evidence basis

Each tactic declares an `evidence_basis` value: `practice_led`, `practice_and_literature`, `literature_led`, or `literature_only`. The prose follows the declaration. Whatever the value, every claim rests on the public sources the entry cites.

**For `practice_led` and `practice_and_literature`:** describe the pattern in plain, observable terms. `observed_contexts` lists generic kinds of setting, never named cases or people.

**For `literature_led` and `literature_only`:** attribute the pattern to the documented record. Write "The documented pattern is that a threat actor...", "The literature describes...", "The analytic marker is...". Do not write in the first person, and do not claim or disclaim personal experience: the vocabulary is not a personal account. `observed_contexts` entries may be tagged `[literature: <bibliography key>]` so the reader sees where they come from.

The declared value is the author's statement of how the tactic was written. It is not a claim of evidence, and the prose must not use a practice-led register to imply more support than the cited sources give.

---

## Rule 5: Naming the people in an entry

### In vocabulary text

Vocabulary text names two roles the same way everywhere.

| Role | Term | Do not use |
|---|---|---|
| The class of person carrying out the behavior | **threat actor** | "Subject" (capitalized), "adversary", "attacker", "perpetrator" as the label for this role |
| The person targeted or protected | **targeted subject**; `the target's <noun>` in possessives; `named individual` or `individual` for variety | "target" alone when it means the person; "victim", "mark" |
| The pair | "the threat actor and targeted subject pair" | "subject-target pair" |

"Threat actor" is the label for a **class of behavior as described in the vocabulary**. An entry that says "Threat actor compiles the targeted subject's address and routine" describes what that kind of conduct looks like. It does not say that a person seen doing something similar is a threat actor.

**Possessives.** Where the noun carries the meaning, `the target's calendar`, `the target's residence`, and `the target's vehicle` are acceptable.

**Variety.** Where "targeted subject" has just been used, `named individual` or `individual` may follow. Do not introduce other alternatives.

**Labels stay as they are.** Tactic, phase, and field names that are established labels are not rewritten: `Subject Profiling`, `Target Selection`.

**Five uses of "adversary" and "attacker" that are acceptable,** because they do not label the threat actor carrying out the tactic:

1. "Adversary" for a third party the threat actor blames or frames ("the trail ends at a convenient adversary").
2. "Prior attackers" for a historical class the threat actor studies or imitates.
3. The adjective "adversarial" ("adversarial tone").
4. Terms of art and titles reproduced from a cited source ("adversary sequence" analysis).
5. The compound "attacker-controlled" for hardware, code, or a path.

Do not strip these with a blanket search. Read each one and keep it only in the sense above.

**Right:**
> "Threat actor appears at locations associated with the targeted subject on multiple occasions with no apparent legitimate reason."
> "Implement protective measures for the targeted subject."

**Wrong:**
> "Subject articulates specific grievance tied to a named individual..."
> "Implement protective measures for the identified target."

### In a case record: the rendering rule

A case record is about a real person. A person who has been reported or observed has not been assessed as posing a threat, and most never will be.

- **In a case record about a person who has not been assessed as posing a threat, "threat actor" is rendered "person of concern".** The score-free case record fixes this in its schema: `subject_term` must be `person_of_concern`.
- Do not copy the label "threat actor" from an indicator into a record, a report, a message, or a system field about a person.
- Record what was observed in plain words, with its source. Tag the observation with the indicator identifier. The identifier points to the vocabulary's description of a class of behavior; it is not a description of the person.
- "Targeted subject" is a vocabulary term. In a record, describe the person who may be at risk in the plain terms your organization uses.
- Keep the same neutral wording for everyone. Do not vary it with the person's role, background, or how alarming the report sounded.

The worksheet and worked cases in [examples/](../examples/README.md) follow this rule.

---

## Rule 6: Variety

A corpus of 161 tactics reads as a template if the same phrases recur. Variety is kept at three levels: the opening phrase, the pivot from definition to behavior, and word choice.

### Openers

Pick the pattern that fits the tactic. No opening **phrase** should appear more than three times across the corpus.

| Pattern | Example | Suits |
|---|---|---|
| Observation | "The first signal usually caught is repetition where there should be none." | Tactics with an unambiguous entry signal |
| Function | "Subject Profiling is the tactic that turns a name into a target file." | Tactics best explained by what they accomplish |
| Decision point | "Target Selection is the point where a grievance lands on a named person." | Tactics that turn on a threshold |
| Literature | "Pathway Indicators are the observable behaviors that mark progression toward an attack..." | `practice_and_literature`, `literature_led`, `literature_only` |
| Tension | "Cover Construction does not usually fail at the cover. It fails at a second-order detail nobody scripted." | Tactics where the common assumption is wrong |
| Typology | "Capability Acquisition resolves into three pathways: legitimate purchase, theft or diversion, and proxy procurement." | Tactics with distinct sub-types |
| Timing | "By the time Network Development is observable, the threat actor has decided help is needed." | Late-phase or threshold tactics |

### Pivots

No pivot phrase should appear in more than two tactics. Rotate among forms such as:

- "Operationally, this resolves into..."
- "What separates this tactic from [the adjacent one] is..."
- "Past this point, the work has shifted from..."
- "Where this tends to surface is..."
- "The detection vector is..."
- "Two distinct streams produce this..."

### Closings

Do not reuse one closing formula. Rotate among forms such as:

- "Most of X sits in [phase], with a tail into [phase]."
- "The window where this is most observable is..."
- "After [event], X is essentially closed unless [condition]."

### Stance

| Stance | Example | Share of tactic `field_notes` |
|---|---|---|
| Second person | "The first thing you catch is..." | At most 15 percent |
| Role as narrator | "An analyst usually surfaces this through..." | About 30 to 35 percent |
| Pattern | "In documented cases, the entry point is usually..." | About 25 to 30 percent |
| Mechanism | "X surfaces in two ways..." | About 15 to 20 percent |

### Role words

In vocabulary text, name roles specifically: **analyst**, **investigator**, **threat management team**, **threat assessment team**, **security professional**, and domain roles such as **reception**, **security personnel**, and **threat reporters**. Do not use "practitioner" or "protective intelligence analyst" in vocabulary text, or an unanchored "expert" or "professional". No single role word should make up more than about 30 percent of role references in `field_notes`.

"Practitioner" is fine in documents about the project, such as this one.

### Characters

No em dashes, no en dashes used as dashes, and no typographic quotation marks in vocabulary text.

---

## Checklist

Before proposing a tactic, indicator, countermeasure, or response protocol:

- [ ] Citations are in `source_refs`, not listed in prose (Rule 1)
- [ ] Every `source_refs` key is a public source in the bibliography
- [ ] Descriptions say what can be observed (Rule 2)
- [ ] Observation comes before classification (Rule 3)
- [ ] Register matches the declared `evidence_basis`, with no first person (Rule 4)
- [ ] "Threat actor" and "targeted subject" used as defined, for classes of behavior only (Rule 5)
- [ ] Nothing in the entry names or describes a real, identifiable person (Rule 5)
- [ ] Opening phrase, pivot, and closing are not overused elsewhere (Rule 6)
- [ ] No "practitioner" or "protective intelligence analyst" in vocabulary text (Rule 6)
- [ ] `field_notes` is three to six sentences, observation first
- [ ] `observed_contexts` lists kinds of setting only: no case names, no personal information
- [ ] The tactic's `false_positive_context` says what ordinary conduct looks like this

## What these rules are not

They do not rule out academic prose where the support is academic. They ask that the default be plain description of observable behavior, that the register never imply more support than the cited sources give, and that a label for a class of behavior never be attached to a person.
