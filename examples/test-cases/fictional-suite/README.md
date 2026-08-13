# Fictional Test Suite (Workstream A)

Six end-to-end fictional scenarios, each run through the full v1.6.0 pipeline: observed behavior → indicator-class mapping → type severity band → six-factor instance record → conditioned priority. **Every case is fictional** — no real person, organization, venue, or system. Each `.json` is a schema-valid `conditioned_assessment` (schema `$defs/conditioned_assessment`, schema 2.0.0).

The three shipped worked cases (`examples/worked-cases/`) all sit in Phase 1 (Target Development), in the Person and Organization matrices, and exercise only single-band moves. This suite deliberately covers the ground they leave untested:

| Case | Matrix | Phase | Modality | Indicator | Type band | Conditioned | Contract behavior exercised |
|---|---|---|---|---|---|---|---|
| FS-1 | Facility | 2 Mobilization | cyber_physical | IND-F0208-04 | high | **critical** | Raise on attained insider access (`has_access` + `specific_target`) |
| FS-2 | Infrastructure | 3 Execution | cyber_physical | IND-I0302-01 | critical | **critical** | **Ceiling hold**: floored critical type; screaming instance has no band above |
| FS-3 | Organization | 2 Mobilization | human_social | IND-O0202-01 | high | **high** | Hold: moderate credibility, pitch not yet taken hold, means unknown |
| FS-4 | Infrastructure | 4 Aftermath | human_social | IND-I0407-01 | low | **medium** | **Trace-layer raise**: type-low aftermath indicator conditioned upward |
| FS-5 | Person | 3 Execution | physical (UAS) | IND-0307-04 | medium | **critical** | **Two-band raise** (medium → critical, skipping high) |
| FS-6 | Person | 2 Mobilization | cyber | IND-0208-05 | high | **high** | **Credibility brake**: low-credibility screaming instance holds at type |

Coverage check: all four matrices; phases 2, 3, 4; all four modalities; all four type bands (low, medium, high, critical); held and raised outcomes; a floored indicator; single-band, two-band, and zero-band moves.

---

## FS-1 — Facility, raised high → critical (`fs-1-facility-bas-reach.json`)

**Scenario.** A badged HVAC subcontractor's remote account is observed traversing from the corporate IT segment onto the building-automation VLAN of one named campus, issuing after-hours commands to door-control test points.

- **Indicator class:** IND-F0208-04, Utility & Systems Access — reaching the facility's BAS/ICS network to command physical systems. **Type band: high** (`staging`).
- **Why it raises.** The indicator's own `conditioning_guidance` probes `proximity_access` and `means_in_hand`: "confirm the access reaches live control systems." Here both resolve at the top — control-system reach directly observed (`means_in_hand: confirmed_present`), standing insider access (`proximity_access: has_access`), one resolved facility (`specific_target`), instrumented-source reporting (`source_credibility: high`). Raise-guidance pattern: *attained access + specific_target = strong raise signal*.
- **Why not held.** The only soft factor is tempo (`steady`). Tempo modulates *how far* the raise goes, not whether attained control-system access on a resolved target raises at all.
- **Next action:** immediate access revocation coordination, OT/physical-security joint response, insider-threat referral.

## FS-2 — Infrastructure, held at critical ceiling (`fs-2-infrastructure-sis-defeat.json`)

**Scenario.** Plant OT monitoring at a chemical processing site confirms unauthorized logic changes to the safety instrumented system controller — verified against change management, so not a maintenance change — while a process excursion develops with the last-resort trip disabled.

- **Indicator class:** IND-I0302-01, Protection & Safety-System Defeat. **Type band: critical, with `severity_floor: critical`** (`in_progress`).
- **The edge this tests.** Every instance factor converges at the top of its scale — and the conditioned priority still reads **critical**, because the contract has no band above it. The escalate-only invariant (`conditioned_priority >= type_severity_band`) is trivially satisfied at the ceiling; *held-vs-raised* reads as **held**, which is the correct, slightly counter-intuitive reading: a maximal instance on a maximal type has nowhere to go. Urgency beyond the band (site emergency response, safe-state forcing) is carried by case management and response protocols, not by the score — exactly the division of labor the demotion doctrine describes in the other direction.
- **Next action:** emergency OT isolation and safe-state procedures per RP links; this is response-protocol territory, not queue territory.

## FS-3 — Organization, held at high (`fs-3-organization-insider-pitch.json`)

**Scenario.** One employee reports a sympathetic direct-message approach referencing their public grievance posts about the firm, followed by an offer of paid "consulting." No corroboration yet.

- **Indicator class:** IND-O0202-01, Insider Recruitment & Cultivation — targeted contact opening with sympathy and money. **Type band: high** (`advancing_late`).
- **Why it holds.** The `conditioning_guidance` names the drivers: "a recruitment pitch is only as dangerous as the cooperation it wins and the access it reaches." Neither is established — the approach has not visibly taken hold, means are `unknown` (which must not lower priority, but supplies no raise either), the recruiter is still `seeking_access`, target set merely `narrowing`, and the single-source report is `moderate` credibility. No raise pattern fires; the type-high band already prices the behavior class.
- **What would flip it:** corroboration plus evidence the pitched employee accepted or holds sensitive access → escalating-request pattern (IND-O0202-02) and a raise.
- **Next action:** protect the reporting employee, quiet corroboration, map what access the pitched employee holds.

## FS-4 — Infrastructure aftermath, raised low → medium (`fs-4-infrastructure-aftermath-claim.json`)

**Scenario.** After a confirmed sabotage incident at a regional utility site, a claim of responsibility appears on an extremist channel. Provenance analysis ties the account to pre-incident reconnaissance chatter — the claimant is assessed to be the actual actor — and the claim names a second, specific substation as "next," with posting cadence compressing.

- **Indicator class:** IND-I0407-01, Attribution Declaration. **Type band: low** — the trace/attributional layer (`aftermath`).
- **The edge this tests.** The low band exists for investigative-trace behaviors whose *direct residual* harm is trace-level. But `conditioning_guidance` asks precisely the question this instance answers: "verify whether the claimant is the actual actor or an opportunist." Actual actor + demonstrated means (`assessed_present` — they already executed once) + a resolved next target (`specific_target`) + compressing cadence (`accelerating`) is the pattern *pathway restart observed from inside the aftermath phase*. The type score prices the claim; the instance prices the claimant.
- **Result:** conditioned priority **medium** — a deliberate one-band raise, not a leap to high: proximity to the named next target is `unknown` and the pathway position is still `aftermath` of attack one, not `preparation` of attack two. Re-condition against Phase-1 target-selection indicators for the named substation as evidence develops.
- **Next action:** open an active case on the claimant; notify the named substation's operator; joint referral with law enforcement.

## FS-5 — Person, raised medium → critical, two bands (`fs-5-person-drone-overwatch.json`)

**Scenario.** A protective detail observes a small UAS repeatedly holding overwatch above the protectee's residence and motorcade staging area, maneuvering against the detail's counter-surveillance runs. Flight windows compress from weekly to daily and align with the protectee's movement schedule; a correlated ground vehicle is logged at consecutive movement sites.

- **Indicator class:** IND-0307-04, Counter-Surveillance — drone overwatch extending observation during execution. **Type band: medium** (`in_progress`).
- **The edge this tests: a multi-band raise.** The contract's only invariant is `conditioned_priority >= type_severity_band` — nothing requires raising one band at a time. The type band is medium because *as a class*, drone overwatch is an observation behavior whose direct harm is low. But `conditioning_guidance` says to determine "what ground action the aerial overwatch is guiding" — and here the answer is: a present, correlated, accelerating ground element at or near one named protectee, with the platform directly observed. The raise-guidance patterns converge exactly as in worked case 3 (`specific_target` + `confirmed_present` + `accelerating` → consider critical; `at_or_near_target` + `specific_target` → strong raise). An intermediate stop at high would understate an in-progress, capable, converging operation.
- **Next action:** immediate protective escalation — movement changes, counter-UAS measures per policy, law-enforcement coordination.

## FS-6 — Person, held at high on the credibility brake (`fs-6-person-location-feed-tip.json`)

**Scenario.** An anonymous web-form tip claims a former associate is "watching every move" of a named executive via live event feeds and social check-ins and "knows exactly when to catch him alone." Nothing beyond the tip is established.

- **Indicator class:** IND-0208-05, Timing Exploitation — using real-time location feeds against a subject. **Type band: high.**
- **The edge this tests.** The mirror image of worked case 1 (all-unknown, low-credibility, type-*low*): here the *content* screams — specific target, alarming intent language — but the *source* is low-credibility and every capability factor is unknown or absent (`means_in_hand: unknown`, `proximity_access: no_known_access`, `tempo: unknown`). Source credibility works exactly as the Q4 ruling defines: **a brake on raising, never a scaler down.** The case cannot be dismissed — the type-high band floors it, so it enters the queue at high regardless — and it cannot stampede the queue to critical on an anonymous say-so. The raise waits for corroboration.
- **What would flip it:** any independent corroboration of monitoring behavior → `source_credibility` moves, and `specific_target` + resolved means would fire the raise patterns immediately.
- **Next action:** corroborate (does the claimed monitoring surface actually exist? does the named associate exist?), review the executive's location-exposure surface, no protectee alarm yet.

---

## The through-line

Two invariants carry every case: the type band floors, and only converging positive evidence raises. What this suite adds to the worked cases is the contract's *outer* behavior: the floor still binds at the top of the scale (FS-2), the raise is unbounded above the floor (FS-5), the trace layer is conditionable like any other (FS-4), and the brake holds against alarming-but-unverified content exactly as hard as the floor holds under it (FS-6).

Validation: `python3 examples/test-cases/validate_cases.py` schema-validates every record in this directory and cross-checks indicator existence, type-band fidelity against `framework.json`, and the escalate-only ordering.
