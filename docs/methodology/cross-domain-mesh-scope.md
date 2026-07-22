# Cross-domain Detection Mesh authoring — scope (S31, 2026-07-13)

**Goal:** make the Detection Mesh actually span domains — author People↔Facility mesh links so the
framework's stated "any matrix can correlate with anywhere else" doctrine is true in the data.
**Status:** V1.4 candidate (alongside org/infra). Scoping only — no data written.

## 1. The linking model

A cross-domain link means: **in one real operation, this People behavior and this Facility behavior
co-occur** — because the target is a person located at / associated with a specific facility, and the
same actor works both surfaces. Observing one should raise the analyst's attention to the other.

- **Field:** indicator `correlates_with` (the mesh's indicator layer). Same field, cross-matrix values.
- **Directionality:** author **bidirectionally** (person→facility AND facility→person) — the SPA renders
  `correlates_with` directly and does NOT compute reverse links, so a one-directional link only shows from
  one side. (See §5 for the better alternative: add reverse computation.)
- **Grain:** indicator↔indicator (that's what the field holds), but derived from a **tactic-correspondence
  grid** (§3) so the links are systematic, not ad hoc.
- **Not** a merge of matrices — People and Facility stay distinct; the link is an *edge*, not a move.

## 2. What makes a link valid (the authoring test)

Link A(person)↔B(facility) when a competent analyst, seeing A, should pull B into the same case file
because they are **the same operation's two faces**. Three qualifying patterns:
- **Shared tradecraft** — the same preparatory act serves both targets (one cover identity, one materiel
  cache, one insider, one counter-surveillance posture).
- **Convergent targeting** — the person target IS reached *through* the facility (breach the building to
  reach the executive; occupy the site to seize the people).
- **Shared actor-level signal** — pathway/escalation and aftermath tradecraft that is actor-level and
  domain-agnostic (final-act markers, withdrawal, laundering).

Reject "same category, unrelated case" pairs — mere thematic similarity is not co-occurrence (the same
error the target_identity compatibility reading made). A link asserts operational correlation, not analogy.

## 3. The tactic-correspondence grid (link families)

| Person tactic | ↔ Facility tactic | Why they co-occur |
|---|---|---|
| TM0102 Subject Profiling | TF0102 Site Profiling | profiling the person + their workplace = one recon effort |
| TM0103 Environmental Survey | TF0103 Physical Reconnaissance | casing the subject's locations IS casing the facility |
| TM0104 Capability Acquisition | TF0106 Capability Acquisition | one materiel/weapon cache serves either target |
| TM0105 Network Development | TF0107 Network Development | one recruited insider gives person-intel AND facility access |
| TM0106 Cover Construction | TF0108 Cover Construction | one fabricated vendor identity gets near the person AND into the site |
| TM0107 Pathway Indicators | TF0109 Pathway/Escalation | final-act / energy-burst markers are actor-level, cross both |
| TM0108 Surveillance Detection | TF0110 Surveillance Detection | one counter-surveillance posture protects both recon streams |
| TM0203/0204 Breach/Zone Pen | TF0203/0204 Perimeter/Interior Pen | reaching the subject = penetrating the facility |
| TM0206 Position Establishment | TF0206 Position Establishment | one overwatch position covers both the person and the site |
| TM0301 Force Application | TF0305 Forced Entry / Vehicle Ram | attacking the person at the site is one act |
| TM0303 Objective Seizure | TF0306 Occupation & Blockade | kidnapping the person = seizing/holding them at the site |
| TM0401–0405 Aftermath (flight/evidence/cover/network/financial) | TF0401–0405 (same) | actor-level aftermath tradecraft is domain-agnostic |

## 4. Proposed FIRST BATCH (pilot — ~12 highest-confidence indicator pairs)

Start with the recon/capability/network/cover convergences (phase 1–2) — the clearest "same operation,
both targets" cases, lowest interpretive risk:

| # | Person indicator | ↔ Facility indicator | link basis |
|---|---|---|---|
| 1 | IND-0102-01 (compile subject's home/routine/associates) | IND-F0102-01 (OSINT on the chosen facility) | dossier of person + their site |
| 2 | IND-0103-01 (appears at subject-associated locations) | IND-F0103-01 (casing visits to the facility) | same casing effort |
| 3 | IND-0103-03 (photographs target locations) | IND-F0103-02 (photographs facility) | same surveillance product |
| 4 | IND-0104-01 (acquires weapons/ammo) | IND-F0106-01 (acquires accelerants/incendiary) | shared materiel prep |
| 5 | IND-0105-04 (recruits insider for target access) | IND-F0107-02 (cultivates facility insider) | one insider, two access paths |
| 6 | IND-0106-02 (fabricated credentials) | IND-F0108-01 (fabricated vendor/contractor identity) | one cover, both surfaces |
| 7 | IND-0107-04 (final-act signature) | IND-F0109-04 (farewell/legacy behaviors) | actor-level pathway convergence |
| 8 | IND-0108-05 (VPN/burner recon) | IND-F0110-03 (maps facility's coverage of the actor) | shared counter-surveillance |
| 9 | IND-0203-02 (tailgates a secured access point) | IND-F0203-02 (defeats perimeter fencing) | reaching the subject via the site |
| 10 | IND-0301-01 (weapon at the targeted subject) | IND-F0305-01 (vehicle/force into people at the site) | convergent execution |
| 11 | IND-0303-01 (takes custody of the subject) | IND-F0306-04 (seizes/confines facility occupants) | seizure = occupation |
| 12 | IND-0401-01 (directed withdrawal from scene) | IND-F0401-01 (directed withdrawal from the site) | shared aftermath egress |

Each is authored on BOTH indicators (bidirectional). ~12 pairs → 24 field edits for the pilot.

## 5. Reliability gate

Cross-domain correlation is a **binary present/absent** judgment (unlike the ordinal informs_axes IRR).
Gate it like the target_identity spot-IRR:
1. **Candidate set** — derive ~30–40 candidate pairs from the §3 grid (a superset of the batch).
2. **Two independent raters** judge each candidate **valid / invalid** ("would a competent analyst pull
   both into one case file?"), blind to each other.
3. **Per-pair Cohen κ** (present/absent) + exact agreement. **Gate κ ≥ 0.60** (the mesh IRR bar).
4. **Adjudicate** disagreements; ship only pairs both raters (post-adjudication) accept.
5. This filters "thematic-similarity" false links — the whole point is that a link asserts *operational
   co-occurrence*, and two SMEs must agree it does.

## 6. Companion code improvement (recommended, do first)

Add **reverse-link computation** to `IndicatorDetail` — a "Referenced by" list computed from all indicators
whose `correlates_with` points at the current one. Benefits: (a) authoring becomes one-directional (halves
the edits — author person→facility only), (b) repairs the existing **202 one-directional** within-matrix
links that currently only display from one side, (c) makes the cross-domain edges visible from either
matrix for free. Small, self-contained SPA change; do it before the authoring pass.

## 7. Effort / sequencing

- Code (reverse-link computation): ~1 focused session, self-contained.
- Candidate grid + 2-rater IRR + adjudication: 1–2 Hermes cycles (like a target_identity spot-IRR).
- Authoring the passed pairs byte-preserving + rebuild + smoke: inline.
- Sequence within V1.4: do the reverse-link code first (halves authoring + fixes existing asymmetry), then
  the IRR-gated cross-domain pass. Can run in parallel with org/infra matrix authoring — different files.
