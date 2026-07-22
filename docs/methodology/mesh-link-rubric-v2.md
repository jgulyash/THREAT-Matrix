# Cross-domain mesh link — VALIDITY RUBRIC v2 (Session 32, round 2)

**Why v2 exists:** round-1 IRR hit raw κ=0.49 (prevalence-deflated) with 5 one-directional
disagreements, all on the "same *type* of behavior vs. same *act*" boundary. That boundary was
never defined precisely. This rubric fixes it with a hard, testable decision rule, then a
balanced candidate set is re-rated blind against it.

---

## The claim a link makes

A link **A (person indicator) ↔ B (facility indicator)** asserts **operational co-occurrence**:
in ONE real operation — where the person target is located at or associated with the facility,
and ONE actor works both surfaces — observing A should make a competent analyst pull B into the
**same case file**, because A and B are **the same act, the same shared resource, or the same
actor-level signal instance** — NOT merely the same category of behavior.

## The decision rule

Mark **VALID** only if the pair satisfies **at least one** of these three identity tests:

- **T1 — Single-act identity.** A and B describe *the same physical or logical act*, seen from
  the person lens and the facility lens. (Occupying the site to hold the person = one occupation.)
- **T2 — Single shared-resource identity.** A and B are served by *one literal shared artifact* —
  one cover identity, one recruited insider, one materiel cache, one counter-surveillance posture,
  one credential set — such that the resource itself is shared, not merely analogous.
- **T3 — Single actor-level signal instance.** The behavior is a *whole-actor state* that by
  definition spans targets in one operation — final-act signature, energy-burst acceleration,
  withdrawal from the one scene, laundering the one operation's proceeds.

## The hard NEGATIVE test (ANY one → INVALID, overrides a weak T-match)

- **Different method / modality**, even within the same tactical family: weapon vs. vehicle;
  tailgating vs. fence-cutting; digital anonymity vs. physical camera-mapping.
- **Different artifact / resource**: a weapons cache vs. an accelerant cache are two procurements,
  not one; two separately fabricated credentials are not "one cover."
- **"Same family" as the only justification**: "both are counter-surveillance / both are force /
  both are recon / both are escalation" with no shared act, artifact, or actor-signal = INVALID.
- **Necessity test**: if you can construct a realistic version of the operation where A happens and
  B does **not** (and vice versa), the pairing is a correlation *of type*, not co-occurrence *of
  act* → INVALID unless it independently passes T2 or T3.

## Worked NEGATIVES (the 8 known-correct INVALIDs this rubric must reproduce)

| pair | why INVALID | rule |
|---|---|---|
| weapons-acquisition ↔ accelerant-acquisition | two different materiel programs | different artifact |
| specific-planning/method ↔ place-tied countdown language | two different escalation expressions | same-family-only |
| VPN/burner digital recon ↔ mapping the site's camera coverage | two different counter-surv modalities | different modality |
| tailgating ↔ cutting/climbing a fence | two different breach methods | different method |
| weapon directed at subject ↔ vehicle ram at the site | two different attack modalities | different modality |
| profiling the subject's vehicle ↔ acquiring/modifying an attack vehicle | "both vehicles" only | same-family-only |
| identification with prior attackers ↔ mapping symbolic facility dates | "both symbolic" only | same-family-only |
| accessing interior security systems ↔ staged-stimulus guard-response test | "both security-probing" only | same-family-only |

## Worked POSITIVES (clear VALIDs)

| pair | why VALID | test |
|---|---|---|
| one fabricated vendor/contractor identity, person-approach ↔ site-access | one literal cover identity | T2 |
| final-act signature (manifesto/farewell) ↔ facility legacy/farewell behavior | one whole-actor endpoint state | T3 |
| directed withdrawal from the scene ↔ directed egress from the site | one egress from one scene | T1 |
| one recruited insider giving person-intel ↔ facility access | one literal insider | T2 |
| taking custody of the subject ↔ seizing/confining occupants at the held site | one seizure act | T1 |

## Rating protocol
- Judge each pair **VALID** or **INVALID** with one sentence naming the test (T1/T2/T3) or the
  negative rule that decided it. Force the binary — no "maybe."
- Two raters, blind to each other: **Rater A = a fresh independent agent** (no knowledge of round
  1); **Rater B = Hermes**. Primary agent (rubric author) is **adjudicator only**, not a rater.
- Gate: **genuine Cohen κ ≥ 0.60** on a prevalence-balanced set (target invalid base rate ≥ 30%,
  so κ is not paradox-deflated). Report κ as the headline; PABAK secondary.
- Ship only pairs both raters accept post-adjudication, authored one-directional (person→facility;
  A1 reverse-link renders the facility side).
