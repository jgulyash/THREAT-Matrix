# Person-matrix scope investigation — findings

**Date:** 2026-05-22. **Question (Jay):** is the THREAT Matrix built so the person matrix covers a threat to *one or more* people (including mass-casualty events at a home/car/public area), or are multi-victim attacks meant to fall under the facility/organization/infrastructure matrices?

## What the framework actually says (evidence)

The matrices carry **no description fields** in `framework.json`. The canonical matrix definition is the framework's own published diagram, `docs/images/matrix-overview.svg`, titled **"TARGET MATRICES"**. Verbatim:

| Matrix | SVG definition | SVG examples |
|---|---|---|
| **Person** | **"Target: Specific Individual"** | Fixated individuals · Assassination · Kidnapping · Stalking |
| **Facility** | "Target: Physical Location" | **Active shooter · IED/VBIED · Venue/campus attack** |
| **Organization** | "Target: The Enterprise (trusted-access adversary)" | Insider threat · Corporate espionage · Organizational sabotage |
| **Infrastructure** | "Target: Critical Infrastructure" | Power · Water · Comms · ICS/OT |

README confirms: "four **target** matrices," "154 total tactics across four target **domains**." The taxonomy sorts by **what the adversary aims at**.

All 34 person-matrix tactics are framed around a single "targeted subject." `crowd`/`bystander` language appears (TM0306 Bystander Management, TM0208/0209 crowd-cover) but only as *context around a targeted attack on an individual* — never as the attack objective. No person-matrix tactic is mass-casualty-framed.

## Direct answer

**As currently built: NO.** The person matrix is scoped **"Target: Specific Individual."** Mass-casualty / multi-victim attacks on people are currently routed to the **facility** matrix — the SVG lists "Active shooter · IED/VBIED · Venue/campus attack" as facility examples. This is the framework's deliberate, documented, published design — not an accident.

**Correction owed:** in the F1 discussion I called the "single-subject" assumption a "handoff calibration shorthand / mis-scoping." That was wrong. Single-subject is the framework's actual documented scope; the Session 23/24 handoffs faithfully reflected it. I apologize for that mischaracterization.

## The conflict, and the genuine gap Jay identified

Jay's stated intent (person = one or more people, incl. mass-casualty) **conflicts with the framework as built.** That is a foundational scoping decision only Jay can make.

And Jay has identified a **real gap** in the current 4-matrix taxonomy. It cleanly handles:
- a specific named individual → person (incl. that individual attacked at home or in a car — the location is just the setting; target = the person)
- an enterprise → organization
- critical infrastructure → infrastructure
- a defined venue/campus → facility

But it has a **seam**: an attack on **multiple private people who are not an enterprise** — a family at home, one-or-more people in a car, a crowd in a public area where the *people* are the target. That is not a "Specific Individual," and a home/car/public-square is not an enterprise "Physical Location" in the venue/campus sense. The framework's current answer ("active shooter → facility") files a *people-targeting* attack under a *location* matrix — which is exactly the awkwardness Jay is sensing. A mass shooting at a school: is the target the school (facility) or the people (person)? The framework currently says facility; the actor taxonomy meanwhile explicitly lists "mass-casualty actors" (Ideological category).

## This GATES the F1 fix — F1 is not straightforwardly a bug

The F1 observation (`critical` severity_band unreachable in the person matrix) is factually true. **Whether it is a bug depends entirely on the scope decision:**

- **If person matrix stays "Specific Individual"** — then blast genuinely is ~2.5–3.0 across the whole matrix, `critical`-unreachable may be *intentional and coherent* (critical-weight reserved for mass-casualty, which lives in facility; the person matrix tops at `high`). F1 then becomes "document the intentional ceiling," not "change the formula." Chunk-1's blast values are correct as authored.
- **If person matrix broadens to "one or more people incl. mass-casualty"** — then blast genuinely varies 2.5–10 across the matrix, `critical` becomes reachable naturally for mass-casualty pathways, the geometric-mean formula is fine, and **F1 dissolves**. Instead, chunk-1's blast values need a recalibration pass: mass-casualty-capable indicators (TM0104 weapons-in-quantity, IED-precursor research; TM0102 public-venue targeting) were authored too narrow under the single-subject assumption.

**My last-turn recommendation to "fix F1 via Option B / thresholds" was premature** — it assumed the scope without questioning it. The scope must be settled first.

## Options for Jay (his architectural call)

1. **Keep the taxonomy as built** (person = specific individual; mass-casualty → facility). F1 → document the person-matrix `high` ceiling as intentional. Chunk 1 unaffected. *Still must resolve the home/car/public-area multi-victim seam with an explicit routing rule.*
2. **Broaden the person matrix** to "Target: one or more people" incl. mass-casualty. Re-scopes the matrix (SVG, README, framing). person vs facility then re-distinguishes as: person = the objective is harming people; facility = the objective is the location/asset itself. F1 dissolves; chunk-1 blast values get a recalibration pass.
3. **Restructure** — e.g., split person into "targeted-individual" vs "mass-casualty-against-people," or add an explicit cross-matrix routing rule for the seam. Most work; cleanest taxonomy.

## Recommendation

Do not touch F1 or commit chunk 1 until the scope is decided. This is a framework-identity decision and it is Jay's. Whichever option, the home/car/public-area multi-victim **seam is a genuine gap that needs an explicit answer under any option** — Jay surfaced a real flaw.
