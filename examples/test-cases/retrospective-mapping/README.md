# Retrospective Mapping — Workstream B

Retrospective coverage test of the THREAT Matrix (v1.6.0, `docs/data/framework.json`) against four well-documented, historical, public incidents. The goal is defensive framework validation: does the taxonomy have an indicator class for each behavior the public record documents, does the `matrices.boundary_rule` produce a sensible primary-matrix call, and can the instance-conditioning contract (`$defs/conditioned_assessment`) carry the record an analyst holding the real evidence at the time would have written?

**Scope and ethics.** Behavior-level mapping only: each row names what the actor did and which indicator class it matches, with no operational detail beyond what identifies the behavior class. All facts are from open public reporting (court records, regulatory dockets, official statements, established press accounts). All four cases are completed or adjudicated. This is the framework's explicitly acceptable "case mapping" use.

## Method

Per incident:

1. **Timeline** — 5–12 rows of public-record behavior.
2. **Mapping** — best-fit tactic + indicator ID found by searching `framework.json` (no ID invented; every band quoted is the indicator's real `severity_band`). Confidence per row:
   - **strong** — the indicator's behavior text covers the observed behavior;
   - **partial** — an indicator sort-of covers it; the miss is stated in the row;
   - **GAP** — no adequate indicator exists (feeds the numbered gap findings).
3. **Boundary-rule analysis** — primary-matrix placement per `matrices.boundary_rule`, showing the terminal-objective call, the People > Facilities > Organizations > Infrastructure tie-break where invoked, and (for Oldsmar) the `primary_objective_evidence_tier` annotation under attribution uncertainty.
4. **Retrospective conditioned assessment** — one schema-shaped `conditioned_assessment` JSON per incident (`incident-N-*.json`) for the pivotal pre-execution indicator, written as-of a stated moment, using only evidence the record shows was available then. `type_severity_band` equals the indicator's real band; `conditioned_priority` respects the escalate-only floor.
5. **Gap findings** — consolidated at the end as RG-1…RG-9.

Files:

| File | Incident | Pivotal indicator | Type band → conditioned |
|---|---|---|---|
| `incident-1-metcalf.json` | Metcalf substation attack (2013) | IND-I0204-05 | high → critical (raised) |
| `incident-2-oldsmar.json` | Oldsmar water plant event (2021) | IND-I0205-05 | medium → high (raised) |
| `incident-3-whitmer.json` | Whitmer kidnapping plot (2020) | IND-0107-03 | critical → critical (held at ceiling) |
| `incident-4-youtube-hq.json` | YouTube HQ shooting (2018) | IND-0101-01 | medium → high (raised) |

---

## Incident 1 — Metcalf substation sniper attack (April 2013, California)

**Matrix under test: infrastructure.** In the early morning of 16 April 2013, one or more unidentified actors severed telecom fiber in two underground vaults near PG&E's Metcalf transmission substation, then fired rifles for roughly 19 minutes at the substation's transformer bank from positions outside the fence, disabling 17 transformers through coolant loss, and departed minutes before police arrived. No arrest or attribution ever followed. Source basis: FERC-docket accounts, congressional testimony, and extensive 2014 press reporting.

### Timeline and mapping

| # | When (public record) | Behavior | Mapped tactic / indicator | Type band | Confidence |
|---|---|---|---|---|---|
| 1 | Weeks–months prior (inferred post hoc) | Site survey of the substation approach; firing positions pre-selected and pre-marked (small rock piles found at the standoff positions) | TI0103 Physical Site Reconnaissance / IND-I0103-01; position pre-staging nearest IND-I0210-04 | medium / medium | **partial** — reconnaissance is only inferable from artifacts; the specific behavior "pre-marking standoff firing positions" has no indicator (IND-I0210-04 is a staged *cache of tools*, not a marked position). Feeds RG-4. |
| 2 | 16 Apr, ~00:58 | Manhole cover lifted; entry into an AT&T underground fiber vault | TI0204 Physical Perimeter Breach / IND-I0204-05 ("pries open a vault cover to enter the buried conduit protecting … fiber and control lines") | high | **strong** |
| 3 | ~00:58–01:07 | Fiber trunks severed, knocking out 911, landline, and some cell service in the surrounding area ahead of the attack | TI0309 Response & Recovery Suppression / IND-I0309-05 | high | **partial** — the behavior class (severing links so the incident goes unannounced and response is delayed) matches, but the indicator text names redundant *power feeds to alarm systems*, not area telecom trunks serving 911. Feeds RG-5. |
| 4 | ~01:07 | Second vault (different carrier) cables cut | Same as row 3 | high | **partial** (same miss) |
| 5 | ~01:31 | Flashlight signal observed on camera, initiating the firing sequence; a second signal later ends it | — | — | **GAP** — no infrastructure-matrix indicator for team operational signaling/communication. Person matrix has TM0308 Operational Communication, but no mesh edge reaches it (person→infrastructure `correlates_with` edges are zero; see RG-6). Feeds RG-4. |
| 6 | 01:31–~01:50 | Sustained rifle fire (100+ rounds) into transformer radiators from outside the fence; 17 transformers disabled by oil/coolant loss | TI0304 Physical Sabotage / IND-I0304-01 ("destroys a distribution transformer by directing rifle fire at it to induce catastrophic oil loss") | medium | **strong** — near-verbatim behavior match; minor wording note: Metcalf hit *transmission-level* transformer banks, the indicator says "distribution transformer." See RG-9 on the medium band. |
| 7 | ~01:50 | Firing ends on signal; egress completed before police arrival at ~01:51 | TI0401 Withdrawal / IND-I0401-03 (retreat along rehearsed egress route) | low | **partial** — the clean, pre-response egress class fits; the "rehearsed route / discarded tools" specifics are unestablished (no tools or vehicle were ever identified). |
| 8 | Aftermath | Expended casings recovered free of latent prints — disciplined physical evidence handling | Infrastructure TI0403 Evidence & Log Manipulation (nearest home) | — | **GAP in the infrastructure matrix** — TI0403's five indicators are all digital (control-system logs, CMMS, CCTV, historian, falsified reports). The behavior is squarely covered by *facility* IND-F0407-02 (scene notable for absence of expected latent-print evidence), but that is a cross-matrix reach for an infrastructure-primary incident. Feeds RG-8. |

Not mapped as a row: the absence of any claim of responsibility. Attribution silence is an absence of behavior, not a behavior; TI0404 Attribution Obfuscation correctly covers only *active* misdirection. No gap.

**Row tally: 2 strong, 4 partial, 2 GAP.**

### Boundary-rule analysis

The terminal objective achieved was the disabling of a grid asset — TI0304 Physical Sabotage, an infrastructure tactic. The telecom cuts were a subordinate enabler (also infrastructure). No other matrix's tactic achieved the terminal objective, so no precedence tie-break is needed: **primary matrix = infrastructure**. The actor's *motive* was never established (the incident drove CIP-014 precisely because intent could not be bounded), but the boundary rule correctly keeps motive out of placement: the primary objective is read from what the attack observably targeted. Under the rule's uncertainty branch, an annotation of the inference confidence belongs in `primary_objective_evidence_tier` — for Metcalf `strongly_inferred` fits (operational evidence overwhelming, motive unbounded) — but the field is defined only on the type-level `indicator` schema object, which is not where an incident-level annotation can live (RG-1).

### Retrospective conditioned assessment — `incident-1-metcalf.json`

Pivotal pre-execution indicator: **IND-I0204-05** (vault entry), type band **high**, the last observable behavior before fire began. As-of ~01:10, an analyst holding the two coordinated vault breaches would have had: specific_target, breach_or_probing, means confirmed_present, tempo accelerating, at_or_near_target, source high → **conditioned critical** (raise per `raise_guidance`: specific target + confirmed means + accelerating). The sobering test result: the real window between this evidence and execution was about 20 minutes — the record is writable, but only a mesh that treats a regional 911 fiber cut as an infrastructure-attack precursor would ever open it in time.

---

## Incident 2 — Oldsmar water treatment plant event (February 2021, Florida)

**Test: cyber-initiated-physical mapping plus attribution-uncertainty handling.** On 5 February 2021 an operator at the Oldsmar, Florida water treatment plant reported watching a remote-desktop session raise the sodium hydroxide dosing setpoint from 100 ppm to 11,100 ppm; he reversed it immediately. The event was publicly announced as an intrusion, driving national advisories about shared-credential remote-access tools on internet-connected control workstations. **2023 reassessment:** a former Oldsmar city official publicly stated the event was probably an employee's error rather than an intrusion, reporting that the FBI found no evidence of outside compromise; no charges were ever filed. Both accounts are in the public record; neither is adjudicated. This incident therefore stress-tests the framework's handling of *uncertain actor existence*, not just uncertain objective.

### Timeline and mapping

| # | When (public record) | Behavior / event | Mapped tactic / indicator | Type band | Confidence |
|---|---|---|---|---|---|
| 1 | Pre-incident | Plant operated a shared-credential commercial remote-access tool on internet-connected, end-of-life OS workstations (per advisories) | — | — | n/a — defender posture/precondition, not actor behavior; correctly out of scope for an actor-behavior taxonomy |
| 2 | 5 Feb, ~08:00 | First remote session observed moving the HMI cursor; dismissed as a supervisor checking in | TI0205 Remote Access Acquisition / IND-I0205-05 | medium | **partial** — the class (authentication to an exposed remote-desktop path using weak shared credentials) matches; the text says "reused vendor default passwords" where Oldsmar had a shared operator password; and whether a threat actor existed at all was later disputed |
| 3 | ~13:30 | Second session takes control of the operator's screen and opens treatment control functions | TI0206 Control-System Access / IND-I0206-04 ("hijacks an active HMI operator session to view and drive the process control screens") | medium | **strong** *as reported in 2021*; attribution disputed 2023 |
| 4 | ~13:30 | Sodium hydroxide dosing setpoint raised 100 → 11,100 ppm | TI0306 Contamination / Adulteration / IND-I0306-01 ("raises the sodium hydroxide dosing setpoint on the treatment SCADA to push finished water out of safe range") | critical | **strong** — near-verbatim behavior match; same attribution caveat. Notably, the indicator's own `conditioning_guidance` says "Confirm the setpoint change is hostile rather than a fault" — the framework anticipated exactly this ambiguity at the tasking level |
| 5 | ~13:33 | Session ends; no persistence, log tampering, or view falsification observed then or since | — | — | n/a — absence of aftermath behavior; consistent with both the intruder-who-left and the no-intruder accounts |
| 6 | Immediately after | Operator reverses the setpoint; plant notes downstream safeguards (pH monitoring, 24–36 h treatment transit) would have caught the change | — | — | n/a — defender action (framework models this on the countermeasure side, not as indicators) |
| 7 | 2023 | Former city official: probable operator error, "non-event"; FBI reportedly found no evidence of intrusion; no charges | — | — | **GAP (representation)** — the reassessment is not an actor behavior, but the framework has no vocabulary to carry "indicator observed; hostile actor existence later contested" on the incident record. Feeds RG-1 and RG-2 |

**Row tally (actor-behavior rows): 2 strong, 1 partial, 1 representation GAP.**

### Boundary-rule analysis, with `primary_objective_evidence_tier`

Under the 2021 account, the terminal objective was contamination of a water system — TI0306, infrastructure; no tie-break needed. Under the 2023 account there was no threat actor and no objective at all. This is precisely the boundary rule's uncertainty branch: *"Where the threat actor's primary objective is uncertain or unknown, primary-matrix placement defaults to the matrix containing the tactic that produced the most observable consequence; the incident-level confidence of this inference is annotated separately via `primary_objective_evidence_tier`."* The most observable consequence — the out-of-range setpoint on the treatment SCADA — sits in the infrastructure matrix, so **primary matrix = infrastructure**, with the evidence tier at its floor: the *existence* of a hostile objective is contested, which is a deeper uncertainty than the branch contemplates (it presumes an actor whose objective is unclear). Writing that annotation exposes RG-1: the schema does define a `primary_objective_evidence_tier` enum (`stated`/`strongly_inferred`/`weakly_inferred`/`unknown`) — but on the type-level `indicator` object, where no incident can write it; none of its four values expresses "hostile actor existence contested" (`unknown` means *no basis for inference*, which overstates what is known here); and the incident-facing objects (`conditioned_assessment`, `instance_assessment`) reject the field under `additionalProperties: false`.

### Retrospective conditioned assessment — `incident-2-oldsmar.json`

Pivotal pre-execution indicator: **IND-I0205-05** (shared-credential remote-desktop access), type band **medium**, as-of the ~08:00 first session — the moment the real operator dismissed. Instance: specific_target, breach_or_probing, means assessed_present (an interactive HMI session *is* dosing capability), proximity has_access, tempo unknown, source **moderate** — the observation was reliable but hostile attribution was unresolved, and the framework offers no better slot for that distinction than source credibility (RG-2). Conditioned **high** (has_access + specific_target is a strong raise signal). The contract behaves correctly on the 2023 reversal: escalate-only means the record was right to raise *given what was held*, and a later benign finding exits by disposition, not by rewriting the score — exactly the `demotion_doctrine`. What is missing is any documented place to record that disposition (RG-2).

---

## Incident 3 — Plot against the Governor of Michigan (2020)

**Test: person matrix, cross-matrix reach, and pre-execution disruption.** Through 2020, a group of men led by Adam Fox, associated with the "Wolverine Watchmen," progressed from anti-government grievance over COVID-19 orders to a concrete plan to abduct Governor Gretchen Whitmer from her vacation home, including surveillance of the home, nighttime reconnaissance, attempted IED construction, and inspection of a nearby highway bridge for demolition to slow law-enforcement response. The FBI had human sources and undercover employees inside the group throughout; arrests on 7–8 October 2020 disrupted the plot pre-execution. Source basis: federal and state trial records and court filings.

### Timeline and mapping

| # | When (public record) | Behavior | Mapped tactic / indicator | Type band | Confidence |
|---|---|---|---|---|---|
| 1 | Spring–summer 2020 | Specific grievance articulated against the named governor over emergency orders, in chats and recorded meetings | TM0101 / IND-0101-01 | medium | **strong** |
| 2 | 6 Jun 2020 (Dublin, OH meeting) | Coordination with co-ideologues in a forum openly endorsing violent action against state governments | TM0105 / IND-0105-03 | high | **strong** |
| 3 | Summer 2020 | Recruitment and vetting of members to provide capability; compartmentalized encrypted-app communications with rotating channels | TM0105 / IND-0105-04; TM0202 / IND-0202-02 | high; medium | **strong** |
| 4 | Jun–Oct 2020 | Repeated field training exercises: combat drills, breach practice | TM0201 / IND-0201-04 (capability rehearsal outside any legitimate context) | high | **strong** |
| 5 | Jul–Sep 2020 | Attempted construction and test detonation of improvised explosive devices at training exercises | TM0104 / IND-0104-05 (researches/attempts improvised construction of attack capability, incl. IED) | critical | **strong** |
| 6 | Late Aug 2020 | Daytime surveillance of the vacation home area, including observation from the water | TM0103 / IND-0103-01 and IND-0103-03 | medium | **strong** |
| 7a | 12–13 Sep 2020 | Nighttime vehicle reconnaissance of the vacation home; approach, observation, withdrawal | TM0209 / IND-0209-01, IND-0209-02 | high | **strong** |
| 7b | Same night | Inspection of the underside of a nearby highway bridge to assess explosive placement for delaying police response | Intent class: TM0305 Response Suppression; nearest text IND-0305-05 (positions obstacles near response staging) or cross-matrix TI0304 | high / medium | **GAP** — no indicator anywhere covers *demolition of a transportation structure to deny a response route*: IND-0305-05 is obstacle-positioning, not structure destruction; infrastructure TI0304's five indicators cover transformers, transmission towers, pump stations, substations, pipelines — no bridges/roads (RG-5); and no person→infrastructure mesh edge exists to walk to it anyway (RG-6) |
| 8 | Sep–Oct 2020 | Surveillance results and target detail shared across the cell; abduction plan converges (method, route, disposition of the target); operational funds pooled | TM0105 / IND-0105-05; TM0107 / IND-0107-02, IND-0107-03 | high; high; critical | **strong** |
| 9 | 7 Oct 2020 | Travel to a rendezvous to pay for explosives — a purchase channel controlled by an undercover employee | TM0104 / IND-0104-01 | high | **partial** — the indicator reads "acquires weapons…"; here the acquisition was *attempted* through a sting-controlled channel and could never complete. The behavior class (capability acquisition in motion) is right; attempted/interdicted acquisition is not distinguished |
| 10 | 7–8 Oct 2020 | Arrests; plot disrupted during Mobilization, pre-execution | — | — | **GAP (representation)** — interdiction is a case outcome, not an actor behavior, but nothing in `pathway_stage` (…preparation, breach_or_probing, attack, aftermath), `temporal_signature`, or documented disposition vocabulary can state that a case *terminated by law-enforcement action before execution*. Feeds RG-3 |

**Row tally: 8 strong (rows 1–6, 7a, 8), 1 partial (row 9), 2 GAP (rows 7b, 10).**

### Boundary-rule analysis

The terminal objective was the abduction of a named person — Execution-phase tactics TM0303/TM0304, person matrix. The facility-flavored behaviors (residence surveillance) and infrastructure-flavored behaviors (bridge demolition planning) were subordinate enablers of the person-directed objective. Even treating the bridge attack as an independent infrastructure tactic invoked simultaneously, the tie-break precedence **People > Facilities > Organizations > Infrastructure** resolves the single primary-matrix call to **person**. This is the boundary rule working as designed; what does *not* work as designed is the Detection Mesh's promise that "cross-matrix coverage is expressed through … `correlates_with` references" — for this incident the person-matrix indicators would need edges into the infrastructure matrix, and there are currently **zero** person→infrastructure edges in the framework (the reverse direction has many; RG-6). The disruption itself (informant penetration, pre-execution arrest) also has no representation (RG-3) — notable because this is the *success case* the framework exists to produce.

### Retrospective conditioned assessment — `incident-3-whitmer.json`

Pivotal pre-execution indicator: **IND-0107-03** (preparation behavior converging on a specific time, place, or person), type band **critical** — the band ceiling. As-of mid-September 2020, post-reconnaissance, every instance factor corroborates: specific_target, preparation, means partial (IEDs failed testing; purchase incomplete), tempo accelerating, at_or_near_target, source high (multiple informants, recordings). Conditioned **critical — held at the ceiling**: the escalate-only contract has no headroom above critical, so a maximally converging instance is recorded as "held," indistinguishable in the score from a bare-minimum critical. The record's value is carried entirely by the basis text (RG-3 note: a "held-at-ceiling with full corroboration" case reads identically to a weakly-evidenced critical in the two enum fields).

---

## Incident 4 — YouTube headquarters shooting (April 2018)

**Test: boundary-rule stress — grievance against an organization, expressed by attacking people at its facility.** Nasim Aghdam, aggrieved for months over the platform's demonetization and filtering of her videos, drove from San Diego to the Bay Area, was found by police sleeping in her car ~25 miles from the company's San Bruno headquarters the night before the attack (welfare check after a family missing-person report; released), practiced at a licensed gun range that morning, entered the campus through an open parking garage, wounded three employees, and died of a self-inflicted wound. Source basis: police statements, family accounts, and contemporaneous press reporting.

### Timeline and mapping

| # | When (public record) | Behavior | Mapped tactic / indicator | Type band | Confidence |
|---|---|---|---|---|---|
| 1 | 2017–early 2018 | Public videos and website posts fixating with rising hostility on one named company as the object of grievance | TO0101 / IND-O0101-02 (fixation shifts from sector-wide to one named organization, rising hostile framing) | medium | **strong** |
| 2 | Same period | Grievance narrative frames the company as a persecutor punishing her ("suppressed"/"discriminated against" her content) | TO0109 / IND-O0109-01 | medium | **strong** |
| 3 | Jan 2018 | Legal purchase of a handgun | TM0104 / IND-0104-01 | high | **partial** — a single lawful purchase is expressly outside the indicator's "quantities or configurations inconsistent with hobbyist or sporting use." The pathway-relevant fact (capability acquisition by an actor already deep in grievance) is real but only becomes indicator-visible in combination |
| 4 | Late Mar 2018 | Departure from home without notice; ~500-mile drive toward the target's region; family files missing-person report and warns police she was angry at the company and might go to its headquarters | TM0107 / IND-0107-07 (sudden visible increase in goal-directed movement) | high | **partial** — the movement was goal-directed in hindsight; contemporaneously the *family's warning*, not her statement, supplied the target link (she never communicated intent, so IND-0101-04/IND-O0109-02 do not fire) |
| 5 | 3 Apr, ~01:40 | Found sleeping in her car ~25 miles from the headquarters; calm during welfare contact; released | TM0107 / IND-0107-03 (logistical arrangements converging on a specific place) | critical | **partial** — overnight staging in the target's area is convergence, but no indicator names *near-target staging below the target-site threshold*; person-matrix recon/approach indicators (TM0103, TM0209) all require presence at target-associated locations |
| 6 | 3 Apr, morning | Practice session at a licensed gun range hours before the attack | TM0201 / IND-0201-04 | high | **partial** — the behavior (weapon function practice on the day of an attack) matches the indicator's core, but the text carves out "licensed range use" as a legitimate context, which excludes this real pre-attack instance. Feeds RG-7 |
| 7 | ~12:46 | Entry to the campus courtyard through an open parking garage — no control defeated | TM0204 Zone Penetration (nearest) | high | **partial** — every TM0204 indicator assumes a defeated or manipulated control (badge, tailgate, lock bypass); open-perimeter entry has no hook. Minor; the following row dominates within seconds |
| 8 | 12:46–12:48 | Discharges firearm at employees in the courtyard, wounding three; then self-inflicted fatal wound | TM0301 / IND-0301-01 | critical | **strong** |

**Row tally: 3 strong, 5 partial, 0 GAP** (the partials feed RG-7; none rises to a missing indicator *class*).

### Boundary-rule analysis

Three matrices are simultaneously invoked: the grievance object is an **organization**, the attack site is a **facility**, and the victims are **persons**. The boundary rule resolves this cleanly in two independent ways:

1. **Terminal objective.** The tactic that achieved the terminal objective was TM0301 Force Application against people — person matrix. The organization was the *motivational* target, and "motivation lives in actor profiles, not in matrix placement."
2. **Precedence tie-break.** Even for a consumer who reads the terminal objective as "punish the organization" (making the org and person tactics co-terminal), the tie-break **People > Facilities > Organizations** > Infrastructure still resolves to **person**.

**Primary matrix = person**, with organization-matrix indicators (IND-O0101-02, IND-O0109-01) as the earliest detectable surface — which is exactly the cross-matrix pattern the Detection Mesh is built for, and here the mesh has real edges (organization→person edges exist, e.g. IND-O0109-04 → IND-0107-05, IND-O0109-05 → IND-0107-07). The rule passes this stress test; the incident's lesson is instead about carve-outs (RG-7) and the pre-attack contact (see the JSON).

### Retrospective conditioned assessment — `incident-4-youtube-hq.json`

Pivotal pre-execution indicator: **IND-0101-01** (specific grievance tied to an identifiable target), type band **medium** — deliberately the *mildest-looking* of the incident's indicators, because the real decision point was the ~02:00 welfare contact, where the only firm evidence was grievance + family warning + proximity. Instance: specific_target, preparation, means **unknown** (unknown-safe: not checked at the contact, does not demote), tempo accelerating, seeking_access, source high. Conditioned **high** — a one-band raise on a medium type. This is the textbook false-LOW: the historical contact ended in release with no notification to the company, and the attack followed within roughly eleven hours; the escalate-only contract exists precisely so that this record, written at 02:00, could not have been scored down.

---

## Gap Findings

Consolidated from the four mappings. Each: what is missing, the incident evidence, and a suggested remedy.

**RG-1 — `primary_objective_evidence_tier` is defined at the wrong level and unusable where it is needed.**
The `matrices.boundary_rule` prose calls it an *incident-level* annotation, and the schema does define it — enum `stated` / `strongly_inferred` / `weakly_inferred` / `unknown`, optional, on the **type-level `indicator` object** (`$defs/indicator`; also typed and rendered in the SPA). But (a) zero of the 815 shipped indicators carry it, (b) an indicator class is not an incident, so the one place it may legally appear is a place an incident-level fact cannot meaningfully live, and (c) the incident-facing objects — `conditioned_assessment` and `instance_assessment` — reject it under `additionalProperties: false`, so a consumer mapping a real incident (both Metcalf and Oldsmar need it) has no schema-valid location to write the annotation. The enum also lacks a value for Oldsmar's situation, where hostile-actor *existence* is contested (`unknown` = "no basis for inference" overstates the uncertainty asymmetry). *Remedy:* move (or duplicate) the field into an incident-record `$def` — or document that it lives in consumer-side incident records — and consider a `contested` value; remove or populate the dormant indicator-level definition.

**RG-2 — Hostile-attribution confidence has no slot distinct from `source_credibility`.**
`source_credibility` measures reliability of *reporting*; Oldsmar's core uncertainty was whether a *hostile actor existed at all* (intrusion vs. operator error) even though the reporting (direct operator observation) was reliable. The two constructs got conflated into one enum in `incident-2-oldsmar.json` because there is nowhere else to put the second. The escalate-only contract handles the 2023 benign reassessment correctly in principle (exit by disposition, never score demotion — `demotion_doctrine`), and IND-I0306-01's own `conditioning_guidance` even anticipates the fault-vs-hostile question, but no documented disposition vocabulary exists to record "reassessed benign / no threat actor." *Evidence:* Oldsmar 2021 report vs. 2023 reassessment. *Remedy:* doc clarification in `instance_conditioning` (worksheet + worked-cases): distinguish reporting reliability from hostile-attribution confidence, and name the disposition states a consumer should use for benign-cause closure. No change to the escalate-only invariant.

**RG-3 — Pre-execution disruption (the framework's success case) is unrepresentable.**
`pathway_stage` runs grievance→aftermath with no interdicted/disrupted terminal value; `temporal_signature` likewise; no disposition vocabulary is documented. A plot stopped by arrest at Mobilization simply stops appearing. Secondary effect: a case held at the critical ceiling with total corroboration (Whitmer) is indistinguishable in the two enum fields from a minimally-evidenced critical. *Evidence:* Whitmer rows 9–10 (sting-controlled acquisition attempt; 7–8 Oct arrests). *Remedy:* doc clarification preferred over enum change — state that disruption is a case-management *disposition* (consistent with `demotion_doctrine`) and enumerate disposition states (`disrupted_by_interdiction`, `closed_benign`, …) in the worksheet; optionally note in `instance_conditioning` how attempted-but-interdicted acquisition should be recorded (as the attempt class, not the completed class).

**RG-4 — Infrastructure matrix under-covers physical standoff-attack team tradecraft.**
The infrastructure Mobilization/Execution phases are OT/cyber-weighted. Missing classes evidenced at Metcalf: (a) pre-marking of standoff firing positions (IND-I0210-04 covers only a staged tool cache); (b) team operational signaling to initiate/terminate an attack (no infra analogue of person TM0308); (c) no timing-exploitation tactic at all (person TM0208 and facility TF0207 exist; infrastructure has none — Metcalf's attack window ended on signal one minute before police arrival). *Remedy:* new indicators — a standoff-position-preparation indicator under TI0210 or TI0201, an operational-signaling indicator, and consider a TI-timing-exploitation tactic mirroring TF0207.

**RG-5 — Transportation infrastructure and area-communications denial are missing asset classes.**
TI0304 Physical Sabotage enumerates transformers, transmission towers, pump stations, substation relays, pipelines — no bridges, roads, or rail structures; TI0309-05 names power feeds to alarm systems, not area telecom trunks. *Evidence:* Whitmer bridge-demolition planning (row 7b — mapped GAP) and Metcalf's 911-denying fiber cuts (rows 3–4 — only partial). Both incidents' *response-route/response-communications denial* behavior lands between indicators. *Remedy:* new indicators — a transportation-structure sabotage indicator in TI0304 (or recon analogue in TI0103), and a broadened or additional TI0309 indicator for severing third-party communications serving the target area.

**RG-6 — Detection Mesh asymmetry: zero person→infrastructure `correlates_with` edges.**
Programmatic check of v1.6.0: infrastructure→person edges exist (10+, e.g. IND-I0110-01 → IND-0107-02), organization→all-three exist, person→facility exist — but person→infrastructure edges number exactly zero. A person-matrix case that grows an infrastructure component (Whitmer: bridge; also the boundary rule's own "tactics from multiple matrices simultaneously" clause) cannot walk the mesh in the direction the case actually develops. *Evidence:* Whitmer row 7b; Metcalf row 5 (person TM0308 unreachable from an infrastructure case is the mirror image, though that direction has other edges). *Remedy:* author person→infrastructure edges where the correlation is real (candidates: IND-0305-05 ↔ TI0304-class, IND-0104-05 ↔ IND-I0106-*, IND-0107-03 ↔ IND-I0110-04).

*Verified full cross-matrix edge census (v1.6.0, outbound `correlates_with` by source→target matrix):* facility→facility 314 (facility emits **zero** outbound cross-matrix edges); infrastructure→facility 63, →person 26, →infrastructure 126; organization→facility 25, →infrastructure 18, →person 21, →organization 124; person→facility 23, →person 171, **→infrastructure 0**, →organization 0. Two structural asymmetries beyond the one this incident exposed: the facility matrix never points outward, and the organization matrix receives no inbound edges from any other matrix. The mesh's cross-domain promise currently flows mostly *out of* organization and infrastructure and *into* facility and person.

**RG-7 — Legitimate-context carve-outs can exclude real pre-attack behavior.**
IND-0201-04 excludes "licensed range use" from capability rehearsal; Aghdam's rehearsal *was* licensed range use, hours before the attack; her single lawful handgun purchase likewise falls outside IND-0104-01's "quantities or configurations inconsistent with sporting use." Both carve-outs are correct base-rate hygiene for the indicator class in isolation, but the framework nowhere states that a carved-out behavior re-enters scope when it co-occurs with active indicators from the same actor. *Evidence:* YouTube HQ rows 3 and 6 — five partials, no strong, across the entire pre-attack preparation surface. *Remedy:* doc clarification (no indicator text change needed): in `instance_conditioning` or the worksheet, state that legitimate-context exclusions are baseline assumptions that a conditioned case overrides — for an actor already carrying grievance/pathway indicators, the same behavior is mapped and conditioned rather than excluded.

**RG-8 — Physical counter-forensics has no home in the infrastructure matrix.**
TI0403 Evidence & Log Manipulation is entirely digital (logs, CMMS, CCTV, historian, falsified reports). Print-free casings at Metcalf map cleanly only to *facility* IND-F0407-02 — an awkward cross-matrix reach for an infrastructure-primary incident, and TF0407↔TI0403 have no connecting edge. *Evidence:* Metcalf row 8. *Remedy:* either add one physical evidence-discipline indicator to TI0403, or add a TI0403↔TF0407 mesh edge plus a doc note that physical counter-forensics is deliberately homed in the facility matrix.

**RG-9 — IND-I0304-01's medium type band is correct; no change needed (calibration check).**
The Metcalf firing behavior maps to a *medium*-band indicator even though the incident reshaped national grid-security policy (CIP-014). This is the type/instance split working, not a mis-band: the class (rifle fire at a transformer) is medium at type level, and the instance layer is what carries a specific coordinated, multi-position, comms-suppressed case to critical — as `incident-1-metcalf.json` demonstrates one indicator upstream. Minor wording note only: the indicator says "distribution transformer"; Metcalf's targets were transmission-level banks; consider "distribution or transmission transformer." *Remedy:* no band change; optional two-word text edit.

---

*All indicator IDs, tactic IDs, severity bands, and temporal signatures cited above were verified against `docs/data/framework.json` (v1.6.0) by script; the four JSON records validate against `$defs/conditioned_assessment` shape, band-floor ordering, and exact type-band match.*
