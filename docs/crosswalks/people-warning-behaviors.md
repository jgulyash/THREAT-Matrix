# Crosswalk: People matrix to published warning-behavior and pathway concepts

**Status: DRAFT. Concept-level. Unreviewed. Not endorsed by any author or organization cited.**

Crosswalk version 0.1.0-draft. Machine-readable copy: `people-warning-behaviors.json` (generated from the same table). Checked against `docs/data/framework.json` on 2026-11-15.

## What this is

A concept-level map from the 34 People tactics to three sets of published concepts, by concept name only:

1. the eight warning behaviors (Meloy, Hoffmann, Guldimann, and James 2012);
2. the six pathway-to-violence stages (Calhoun and Weston 2003);
3. the thirteen investigative themes in the US Secret Service NTAC operational guide (2018).

It lets a reader who knows those concepts find the tactics that describe related observable behavior, and shows where the People matrix has nothing to say.

## What this is not

- It is not a mapping to any licensed assessment instrument. No instrument's items, coding criteria, scoring, or wording is reproduced, and none was consulted to build this table. Several licensed instruments use some of the same concept names; anyone using such an instrument must use it under its own license and training requirements.
- It does not say the vocabulary measures these concepts, or that a tactic is a valid indicator of one.
- It has not been reviewed by any author of the cited works or by any outside practitioner.
- The one-line glosses below are this project's paraphrase, written for orientation. The cited sources govern.

## Sources

| Key | Citation | Link | Link status | Used for |
|---|---|---|---|---|
| MELOY-2012 | Meloy, J. R., Hoffmann, J., Guldimann, A., and James, D. (2012). The role of warning behaviors in threat assessment: An exploration and suggested typology. Behavioral Sciences and the Law, 30(3), 256 to 279. | https://doi.org/10.1002/bsl.999 | blocked to scripts (403), check in browser | Names of the eight warning behaviors. |
| CALHOUN-WESTON-2003 | Calhoun, F. S., and Weston, S. W. (2003). Contemporary Threat Management: A Practical Guide for Identifying, Assessing, and Managing Individuals of Violent Intent. Specialized Training Services. | none | book, no public link; edition and page references to be confirmed | Names of the six pathway stages. |
| FEIN-VOSSEKUIL-1998 | Fein, R. A., and Vossekuil, B. (1998). Protective Intelligence and Threat Assessment Investigations: A Guide for State and Local Law Enforcement Officials. National Institute of Justice. | https://www.ojp.gov/pdffiles1/nij/179981.pdf | verified (200) | Public-domain statement of attack as the end of a discernible process of thinking and behavior. |
| NTAC-2018 | U.S. Secret Service National Threat Assessment Center (2018). Enhancing School Safety Using a Threat Assessment Model: An Operational Guide for Preventing Targeted School Violence. | https://www.secretservice.gov/sites/default/files/reports/2020-10/USSS_NTAC_Enhancing_School_Safety_Guide_7.11.18.pdf | verified (200); theme names read from the document | Names of the thirteen investigative themes. |

The NTAC guide's theme names were read from the document itself. The warning-behavior and pathway-stage names are standard in the literature; the journal article and the book were not re-read for this draft, and page references are to be confirmed at review.

## Concepts

| ID | Group | Name | Gloss (this project's paraphrase) |
|---|---|---|---|
| `wb.pathway` | Warning behaviors | Pathway | Research, planning, preparation, or implementation of an attack |
| `wb.fixation` | Warning behaviors | Fixation | Increasingly pathological preoccupation with a person or a cause |
| `wb.identification` | Warning behaviors | Identification | Taking on a warrior or attacker identity, or close association with weapons or prior attackers |
| `wb.novel_aggression` | Warning behaviors | Novel aggression | A first act of violence that appears unrelated to the planned attack, testing ability to act |
| `wb.energy_burst` | Warning behaviors | Energy burst | A rise in the frequency or variety of activity related to the target shortly before an attack |
| `wb.leakage` | Warning behaviors | Leakage | Communicating to a third party an intent to do harm to a target |
| `wb.last_resort` | Warning behaviors | Last resort | Words or acts showing a felt time limit or a belief that no alternative to violence remains |
| `wb.directly_communicated_threat` | Warning behaviors | Directly communicated threat | A threat conveyed to the target or to law enforcement before an attack |
| `pv.grievance` | Pathway stages | Grievance | A sense of injury or injustice attributed to a person or institution |
| `pv.ideation` | Pathway stages | Ideation | Coming to see violence as an answer to the grievance |
| `pv.research_and_planning` | Pathway stages | Research and planning | Gathering information on the target and working out how to act |
| `pv.preparation` | Pathway stages | Preparation | Acquiring means and making arrangements |
| `pv.breach` | Pathway stages | Breach | Getting past the security or distance that separates the subject from the target |
| `pv.attack` | Pathway stages | Attack | The act itself |
| `ntac.motives` | NTAC themes | Motives | see source |
| `ntac.communications` | NTAC themes | Communications | see source |
| `ntac.inappropriate_interests` | NTAC themes | Inappropriate interests | see source |
| `ntac.weapons_access` | NTAC themes | Weapons access | see source |
| `ntac.stressors` | NTAC themes | Stressors | see source |
| `ntac.emotional_and_developmental_issues` | NTAC themes | Emotional and developmental issues | see source |
| `ntac.desperation_or_despair` | NTAC themes | Desperation or despair | see source |
| `ntac.violence_as_an_option` | NTAC themes | Violence as an option | see source |
| `ntac.concerned_others` | NTAC themes | Concerned others | see source |
| `ntac.capacity_to_carry_out_an_attack` | NTAC themes | Capacity to carry out an attack | see source |
| `ntac.planning` | NTAC themes | Planning | see source |
| `ntac.consistency` | NTAC themes | Consistency | see source |
| `ntac.protective_factors` | NTAC themes | Protective factors | see source |

## Confidence values

- **direct**: the tactic, or one of its indicators, describes the same behavior the concept names.
- **partial**: related, but narrower, broader, or at a different point in time.
- **none**: no concept in these three sets corresponds.

Confidence is assigned to the tactic as a whole. Where a link rests on particular indicators they are listed.

## Tactic mappings

| Tactic | Name | Mapped concepts | Confidence | Reason |
|---|---|---|---|---|
| TM0101 | Target Selection | Grievance; Research and planning; Pathway; Fixation; Leakage; Identification; Motives; Communications; Inappropriate interests; Planning | direct | Indicators state a grievance tied to a target, repeated return to it, intent voiced to third parties, and target research, which are the grievance stage, fixation, leakage, and pathway research by name. |
| TM0102 | Subject Profiling | Pathway; Research and planning; Planning | direct | Compiling a profile of the target's life is target research in the research and planning stage. |
| TM0103 | Environmental Survey | Pathway; Research and planning; Planning | direct | Visiting, photographing, and studying target locations is site research in the research and planning stage. |
| TM0104 | Capability Acquisition | Pathway; Preparation; Weapons access; Capacity to carry out an attack; Planning | direct | Acquiring weapons, tools, and credentials is the preparation stage and bears on weapons access and capacity. |
| TM0105 | Network Development | Preparation; Leakage; Communications | partial | Recruiting helpers is preparation, and sharing the grievance narrative resembles leakage, but the published concepts describe a lone subject and have no network concept. |
| TM0106 | Cover Construction | Pathway; Preparation; Planning | partial | Building a pretext or false identity is a preparation act; the published concepts do not name cover or deception. |
| TM0107 | Pathway Indicators | Pathway; Identification; Energy burst; Last resort; Novel aggression; Ideation; Research and planning; Preparation; Violence as an option; Inappropriate interests; Desperation or despair; Planning | direct | This tactic gathers the pathway and warning-behavior signals; five of its indicators correspond one to one with a named concept. |
| TM0108 | Surveillance Detection Countermeasures | Pathway; Research and planning | partial | Checking for surveillance is planning tradecraft; no published concept names it, so the link is to pathway behavior in general. |
| TM0201 | Operational Rehearsal | Pathway; Preparation; Planning; Capacity to carry out an attack | direct | Dry runs and timing checks are preparation and are named as planning behavior in the public guides. |
| TM0202 | Concealment | Preparation; Consistency | partial | Hiding activity is not a named concept; the indicator on mismatch between stated and actual activity touches the consistency theme. |
| TM0203 | Perimeter Breach | Pathway; Breach | direct | Getting through the outer security layer is the breach stage. |
| TM0204 | Zone Penetration | Pathway; Breach | direct | Moving through inner security layers continues the breach stage. |
| TM0205 | Access Elevation | Pathway; Breach | direct | Gaining access by deception is breach by another means. |
| TM0206 | Position Establishment | Pathway; Breach | partial | Taking up position sits between breach and attack; the stage model does not separate it. |
| TM0207 | Operational Pause | Pathway | partial | A deliberate stand-down has no named counterpart; the literature notes movement along the pathway is not always forward, which is the nearest idea. |
| TM0208 | Timing Exploitation | Pathway; Research and planning; Planning | partial | Choosing a time window is a planning act; no published concept names timing. |
| TM0209 | Partial Approach Rehearsal | Pathway; Breach | partial | An approach that stops short is implementation behavior near the breach stage; the published concepts do not name aborted approaches. |
| TM0301 | Force Application | Attack; Directly communicated threat | direct | Use of force is the attack stage; one indicator includes a declaration of intent at the scene, which only partly matches a directly communicated threat. |
| TM0302 | Barrier Defeat | Breach; Attack | direct | Forcing a barrier is breach carried out at the moment of attack. |
| TM0303 | Objective Seizure | Attack | partial | Seizing a person or asset is an attack-stage act; the published concepts were framed around assault, not seizure. |
| TM0304 | Captive Control | Attack | partial | Controlling captives is conduct during an attack; no published concept covers it. |
| TM0305 | Response Suppression | Pathway; Research and planning; Preparation | partial | Its indicators are research into and acquisition of means to delay response, which are planning and preparation acts. |
| TM0306 | Bystander Management | Attack | partial | Managing bystanders is conduct during an attack; no published concept covers it. |
| TM0307 | Counter-Surveillance | Attack | partial | Watching for responders is conduct during an attack; no published concept covers it. |
| TM0308 | Operational Communication | none | none | Coordination among several actors during execution has no counterpart in concepts framed around one subject. |
| TM0401 | Withdrawal | Last resort | partial | The pathway model ends at the attack. One indicator, making no attempt to leave, relates to last resort thinking. |
| TM0402 | Evidence Management | none | none | Post-attack evidence handling is outside the pathway model, which ends at the attack. |
| TM0403 | Cover Reestablishment | none | none | Post-attack return to routine is outside the pathway model. |
| TM0404 | Network Protection | none | none | Post-attack protection of accomplices is outside the pathway model. |
| TM0405 | Financial Disposition | none | none | Handling of proceeds is outside the pathway model. |
| TM0406 | After-Action Assessment | none | none | Review of a completed operation is outside the pathway model. |
| TM0407 | Attribution Declaration | Leakage; Communications | partial | Claims after the fact are not leakage as published, which is communication before an attack; material prepared in advance for later release is the nearest link. |
| TM0408 | Audience Amplification | none | none | Spreading a claim after an attack has no counterpart. |
| TM0409 | Coercive Leverage | Directly communicated threat | partial | Threats and demands sent to families or decision-makers are direct threats, but they follow a seizure rather than precede an attack. |

## Indicator-level links

Only links that are clear from the indicator sentence are listed. Absence from this table means no indicator-level link is claimed.

| Indicator | Concepts |
|---|---|
| IND-0101-01 | Grievance; Motives |
| IND-0101-02 | Pathway; Research and planning; Planning |
| IND-0101-03 | Fixation |
| IND-0101-04 | Leakage; Communications |
| IND-0101-05 | Identification; Inappropriate interests |
| IND-0104-01 | Preparation; Weapons access |
| IND-0107-01 | Ideation; Violence as an option |
| IND-0107-02 | Research and planning; Planning |
| IND-0107-03 | Preparation; Pathway |
| IND-0107-04 | Last resort; Desperation or despair |
| IND-0107-05 | Identification; Inappropriate interests |
| IND-0107-06 | Novel aggression |
| IND-0107-07 | Energy burst |
| IND-0202-05 | Consistency |
| IND-0301-05 | Directly communicated threat |
| IND-0401-03 | Last resort |
| IND-0407-03 | Leakage |
| IND-0409-04 | Directly communicated threat |

## Coverage summary

- Tactics mapped **direct**: 11 (TM0101, TM0102, TM0103, TM0104, TM0107, TM0201, TM0203, TM0204, TM0205, TM0301, TM0302).
- Tactics mapped **partial**: 16 (TM0105, TM0106, TM0108, TM0202, TM0206, TM0207, TM0208, TM0209, TM0303, TM0304, TM0305, TM0306, TM0307, TM0401, TM0407, TM0409).
- Tactics that map to **nothing**: 7 (TM0308, TM0402, TM0403, TM0404, TM0405, TM0406, TM0408). All but one are aftermath tactics; the published concepts stop at the attack.
- Concepts with **no tactic**: Stressors (NTAC themes), Emotional and developmental issues (NTAC themes), Concerned others (NTAC themes), Protective factors (NTAC themes).
- Concepts linked only through **partial** tactics: Consistency.
- Concepts whose only indicator-level links are **loose** (the indicator is related but does not describe the concept as published), whatever the tactic's overall confidence: Novel aggression, Directly communicated threat, Consistency.
- Concepts carried by **a single indicator**: Fixation (IND-0101-03), Novel aggression (IND-0107-06), Energy burst (IND-0107-07).

What the summary shows, stated plainly:

- The People matrix is organised around operational steps toward and after an attack. It aligns well with the Pathway warning behavior and with the research, preparation, breach, and attack stages.
- It is thinner on the other seven warning behaviors. Leakage, identification, and last resort each have a clear indicator. Fixation, novel aggression, and energy burst each rest on one indicator, and the novel aggression link is loose. Directly communicated threat has no indicator that describes a threat sent to a target before an attack.
- It has nothing on the contextual NTAC themes: stressors, emotional and developmental issues, concerned others, and protective factors. These describe the person's circumstances and the people around them, not operational behavior. A user who needs them must look elsewhere; the score-free case record has a protective-factors field for that reason.
- Aftermath tactics have no counterpart in these concept sets. That is a difference of scope, not a defect on either side.

## Known limits of this draft

- One reader's judgment, unreviewed. Expect corrections.
- Tactic-level confidence hides variation among indicators.
- The pathway stage names are used as commonly cited; the original text was not re-read.
- Other public frameworks (for example the FBI's published concerning-behavior categories) are not yet mapped.

Corrections: see `README.md` in this directory.
