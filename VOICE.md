# THREAT Matrix Voice Guidelines

**Date:** 2026-04-27
**Status:** LOCKED for V1.1+ content authoring
**Audience:** Maintainers and contributors authoring tactic content (`field_notes`, indicators, countermeasures, response protocols)

THREAT Matrix is practitioner-first by design and by schema. The framework's evidence model (`evidence_basis` enum), source typing (Tier 1 includes attested operational experience), and mandatory `field_notes` field all enforce this structurally. These voice rules govern the prose that fills the schema.

The four rules below apply to all V1.1+ content authoring. They are not editorial preferences. They are quality discipline.

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

**For `literature_only` content** — `field_notes` explicitly says so. Example pattern: *"I haven't worked a case involving this tactic directly. The pattern documented in NTAC-MASS-2021 and FEIN-VOSSEKUIL-HOLDEN-1995 is that the actor..."* Honesty is first-class. The `observed_contexts` are tagged `[literature: <source-id>]` so the reader sees the provenance.

**For `hybrid` content** — practitioner voice frames the observable detail; academic citation supports. The schema and prose work together.

---

## Application Checklist

Before submitting any tactic, indicator, countermeasure, or response protocol for V1.1, verify:

- [ ] No "clinical anchor" or similar citation-in-prose framings (Rule 1)
- [ ] Descriptions use observable-action vocabulary (Rule 2)
- [ ] Encounter precedes taxonomy and citation (Rule 3)
- [ ] Prose register matches the declared `evidence_basis` (Rule 4)
- [ ] `field_notes` written in 1-3 sentences minimum, practitioner-voice
- [ ] `observed_contexts` lists pattern archetypes only (no case names, no PII)
- [ ] `source_refs` includes at least one Tier 1 source

---

## What this is not

These voice rules do not require the maintainer or contributors to be unable to write academic prose. The framework cites peer-reviewed literature throughout. What the rules require is that the prose carry practitioner literacy as the default and use academic register only where the evidence is academic.

The reader who matters most is the practitioner who picks up the framework and recognizes their own work in it. Build for that reader.