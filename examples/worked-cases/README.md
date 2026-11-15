# Worked Cases (fictional, score-free)

Five filled-in case records that follow `docs/data/case-record.schema.json`. **Every case is fictional.** No real person, organization, or venue is described, and each record says FICTIONAL at the start of its summary. The records hold no score, band, weight, or priority.

These cases show how to write a record. They do not show what any behavior "means". The vocabulary does not predict violence, a record is not grounds for adverse action by itself, and each person is assessed on the facts of their own case. The individual is called the person of concern throughout.

| File | What it shows | Disposition |
|---|---|---|
| `case-1-no-threat-identified.json` | A report that is checked and fully explained | `no_threat_identified` |
| `case-2-transient.json` | An angry remark with no sustained intent | `transient_no_further_action` |
| `case-3-lowered-on-reassessment.json` | Concern lowered twice as a benign explanation and protective factors are confirmed | `closed_benign` |
| `case-4-raised-over-time.json` | Concern raised twice as corroborated observations build up | `heightened_monitoring` |
| `case-5-disrupted-by-interdiction.json` | Concern raised, an interdiction, then concern lowered afterwards | `disrupted_by_interdiction` |

## How to read a record

- **Observations** list each reported behavior with the indicator whose wording fits, the date, the source, and whether it was corroborated. Most cases have several.
- **Instance factors** describe the case at the latest entry. They are not added up. `unknown` is a normal answer.
- **Protective factors** are always filled in, even if only to say the team looked and found none.
- **Reassessments** are dated and can go up, down, or stay the same. When the picture changes, the factor values are updated and the earlier picture is kept in the basis and rationale text.
- **Disposition** is the current case-management outcome.

---

## Case 1: no threat identified

**What was reported.** A front desk supervisor logged a call from an unfamiliar person asking which days a named executive is in the building and how visitors reach the executive floor.

**Observation.** IND-0103-05 (an inquiry to staff about access procedures, schedules, or a person's routine). One identified source, so `single_source`.

**What the team did.** Called the number back, spoke with the internal events team, and confirmed with a contracted events vendor that the caller is a new coordinator arranging a scheduled appearance.

**Factors.** Nothing places the caller on the pathway to violence, so target focus, pathway stage, tempo, and means are all `unknown`. Access is `no_known_access` apart from a visitor pass on the day. Source credibility is `high` because the call was logged and the caller's identity was confirmed.

**Protective factors.** A confirmed legitimate purpose, confirmation from two parties, and a caller who gave a name and answered a call back.

**Reassessment and disposition.** Lowered the next day once identity and purpose were confirmed. Disposition `no_threat_identified`. The front desk was thanked for reporting.

**Why it is here.** The record shows that a behavior can match an indicator's wording and still be ordinary, and that the outcome can be written down plainly.

## Case 2: transient

**What was reported.** Straight after a difficult performance review, an employee told a coworker that the supervisor "will pay for this". The coworker told human resources the same day.

**Observations.** IND-0101-01 (a grievance tied to a named individual) and IND-0101-04 (a statement about that individual to a third party). The second is `corroborated` because the person confirmed the words in interview.

**What the team did.** Interviewed the person the next morning. The person confirmed the remark, described it as anger in the moment, apologized without being asked, and asked how to appeal the review.

**Factors.** Target focus `specific_target` (one supervisor). Pathway stage `grievance`. Tempo `stalling` (one remark, nothing since). Access `has_access`, which only describes the fact that both work on the same floor. Source credibility `high`. **Means in hand is `unknown`:** the team has no information that the person possesses or has acquired any means, and did not go looking on the strength of one remark. That an adult could lawfully acquire something is not means in hand and is not recorded.

**Protective factors.** An explanation and apology, eleven years with no similar concerns, use of the formal appeal, and a coworker who called the remark out of character.

**Reassessment and disposition.** Lowered after the interview. Unchanged at a routine two-week check. Disposition `transient_no_further_action`.

**Why it is here.** It shows the difference between a transient expression of anger and a substantive threat, and an `unchanged` reassessment entry.

## Case 3: lowered on reassessment

**What was reported.** Human resources and two coworkers reported that an employee had voiced a grievance about a named manager several times over two weeks, more often as time went on, and had asked the team administrator which days that manager works on site.

**Observations.** IND-0101-01 (grievance tied to a named individual), IND-0101-03 (returning to it with increasing frequency), and IND-0103-05 (asking staff about a person's routine).

**First review.** The team could not yet explain the schedule questions, so it opened the case for routine monitoring and set out to learn more. It did not treat the questions as planning on the strength of one inquiry.

**What the team found.** The employee relations adviser confirmed that the person had been advised to raise the matter with the manager in person and was trying to find a day when both were on site. The grievance moved into the formal process, with a representative.

**Factors at the latest entry.** Target focus `specific_target`. Pathway stage `grievance`. Tempo `stalling`. Access `has_access` (same site). Source credibility `high`. **Means in hand is `unknown`.** The team has no information that the person possesses or has acquired any means. It did not ask about, and does not record, lawful ability to acquire anything, because that is not means in hand.

**Protective factors.** A confirmed benign explanation, use of the formal process, long tenure with no prior concerns, steady support at home and work, and no statement about harming or confronting anyone.

**Reassessments and disposition.** Lowered on 2026-05-12 when the explanation was confirmed. Lowered again on 2026-06-09 after four weeks with no new reports. Disposition `closed_benign`.

**Why it is here.** It shows concern going down, in the record, with reasons, as protective factors and a benign explanation emerge.

## Case 4: raised over time

**What was reported.** A former contractor whose engagement had been ended by a named executive showed a former coworker a folder holding the executive's home address, family members' names, and daily routine, built from online research.

**Observations, in order.** IND-0101-02 (sustained online research into a specific individual) and IND-0102-01 (compiling personal information), both from one source. Three weeks later IND-0103-01 (appearing at a location associated with the individual on more than one occasion with no apparent reason), corroborated by residential camera footage. Two weeks after that IND-0107-02 (moving from general statements to naming a method and timing), corroborated by two matching accounts.

**Factors at the latest entry.** Target focus `specific_target`. Pathway stage `research_planning`. Tempo `accelerating` (weeks between observations, then days). Access `at_or_near_target` (camera footage at the residence). Source credibility `moderate`: the footage is a record, but the statements rest on two former coworkers. **Means in hand is `assessed_present`, and the basis is possession:** a former coworker reports being shown a handgun and told it had just been bought. No one on the team has seen it, so the value is not `confirmed_present`.

**Protective factors.** A cooperating sibling in regular contact, stable housing, and contact with a former supervisor. The team also records that it looked for a benign explanation for the visits to the residence and found none.

**Reassessments and disposition.** Raised on 2026-03-04 after the camera footage. Raised again on 2026-03-18 after the matching accounts. Disposition `heightened_monitoring`, with protective measures in place and law enforcement notified under the organization's policy.

**Why it is here.** It shows several observations in one record, each with its own source and corroboration, and concern rising step by step on corroborated facts. The summary says what the team sees and why. It does not say what the person will do.

## Case 5: disrupted by interdiction

**What was reported.** Over three weeks an employee voiced a grievance about one named colleague with growing frequency. Law enforcement then told the team that, within ten days, the person had acquired weapons and ammunition in quantities inconsistent with hobbyist or sporting use.

**Observations.** IND-0101-01, IND-0101-03, and IND-0104-01, all corroborated.

**What happened.** Threat management and law enforcement coordinated an interdiction before any approach to the colleague. The items were recovered and workplace access was revoked.

**Factors at the latest entry (after the interdiction).** Target focus `specific_target`. Pathway stage `preparation`, the furthest stage reached. Means in hand `assessed_absent` (items recovered; before the interdiction it was `confirmed_present`, because the items were directly observed and recovered). Tempo `stalling` (before: `accelerating`). Access `no_known_access` (before: `has_access`). Source credibility `high`. The basis text keeps the earlier values so the reasons for the intervention stay on the record.

**Protective factors.** Before the interdiction the team looked and found none, and says so. Afterwards: means removed, access ended, and the person engaging through counsel with a cooperating relative.

**Reassessments and disposition.** Raised on 2026-06-08. Unchanged on 2026-06-10, the day of the interdiction, while the team confirmed what was recovered. Lowered on 2026-07-08 after four weeks with no new behavior. Disposition `disrupted_by_interdiction`. Monitoring continues under policy.

**Why it is here.** It shows all three reassessment directions in one record, and that lowering concern after an intervention does not erase the earlier assessment: the dated entries keep it.

---

## Notes that apply to every case

- **Means in hand means possession.** In no case here is lawful ability to acquire something recorded as means in hand. Where the team has no information about possession, the value is `unknown`.
- **Access is a state.** `has_access` in Cases 2 and 3 describes people who work in the same place. It is not a behavior and is not treated as one.
- **`unknown` is a normal answer.** The pathway stage list has no "not on the pathway" value, so Case 1 records `unknown` and says why in the basis.
- **Pick indicators by wording.** Each indicator ID was chosen because its behavior text fits what was reported. The indicator text in the data uses the label "threat actor" for the class of behavior; the records use "person of concern" for the individual.
- **Scored versions.** Cases 3, 4, and 5 also appear in `../experimental-scoring/worked-cases/` as records for the experimental scoring overlay. Those are an experiment and are not needed to use the records here.

## Check the files yourself

From the repository root:

```bash
pip install jsonschema
python3 scripts/lint/consumer-smoke.py
```
