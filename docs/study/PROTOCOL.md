# Indicator presence-coding reliability study: protocol

**Status: DRAFT protocol. Not preregistered. Not yet run. No raters recruited. No data collected. No results exist.**

Protocol version: 0.1.0-draft. Nothing in this file reports a finding. Every number below is a design choice fixed in advance, not an outcome.

This protocol is written in the form of a preregistration so that it can be lodged with a public registry (for example the OSF preregistration service, https://osf.io/prereg/) before any rater sees any case. Until that is done and the registration link is recorded in section 16, the study has not started.

## 1. Purpose

The THREAT Matrix is an open behavioral vocabulary: a set of indicators, each a one-sentence description of an observable behavior, grouped into tactics and matrices. A vocabulary is useful for recording and comparing cases only if different trained people, reading the same account, agree on which indicators are present.

This study measures that agreement for the People and Facilities matrices.

### What the study establishes

- Whether independent, credentialed practitioners, working alone from the same written case narrative, agree on the presence or absence of each indicator.
- Which indicators, tactics, and matrices reach a level of agreement fixed in advance, and which do not.
- A public, versioned dataset of coded cases that others can reuse and check.

### What the study does not establish

- **Not predictive validity.** Agreement that a behavior is present says nothing about whether that behavior predicts violence. Cases are selected for the quality of their public record, not sampled from any population, so no rate, base rate, or likelihood can be drawn from them.
- **Not validity of any scoring.** No weight, band, priority, or score is coded, analysed, or reported. See section 15.
- **Not accuracy against ground truth.** The study measures agreement among raters, not whether the raters are right. A separate consensus step (section 9) produces a reference coding for the dataset but is not used to grade raters.
- **Not field performance.** Raters code a finished written narrative. Live casework has incomplete, arriving, and conflicting information.
- **Not coverage.** The study does not test whether the vocabulary is missing behaviors. Raters may note suspected gaps (section 9) and these are published as notes, not results.

## 2. Research questions

- RQ1. For each of the People and Facilities matrices, what is the chance-corrected agreement among independent raters on indicator presence, pooled over all indicators and cases?
- RQ2. For each tactic (indicator family), what is the pooled agreement, and which tactics fall below the thresholds in section 8?
- RQ3. For each indicator that is evaluable (section 7), what is its agreement, and which indicators should be returned for rewrite or retirement?
- RQ4. How often do raters choose "cannot determine", and for which indicators? A high rate signals an indicator that a written record rarely supports.
- RQ5. Does agreement differ by case class (attack, disrupted, non-attack comparison)? This is descriptive only; the study is not powered to test it.

No hypothesis about the direction of any result is registered. The thresholds in section 8 are decision rules, not predictions.

## 3. Materials

### 3.1 Vocabulary

Indicator wording is taken from one pinned release of `docs/data/framework.json`, identified by content version and file checksum, recorded in section 16 before coding starts. Raters see, for each indicator: its ID, its behavior sentence, and the name and notes of its tactic. Raters do not see any score, weight, band, priority, or the experimental scoring overlay. Indicators with a lifecycle state other than active are excluded.

At the time of drafting the People matrix holds 34 tactics and 191 indicators and the Facilities matrix holds 40 tactics and 200 indicators. The counts at the pinned release govern.

### 3.2 Cases

Case narratives are drawn only from three classes of public document:

1. court documents (opinions, indictments, complaints, plea agreements, sentencing memoranda) in adjudicated matters;
2. government after-action reviews;
3. official commission or inquiry reports.

News reporting, books, social media, leaked material, and unpublished records are not used, including to fill gaps.

A candidate list with verified links is in `candidate-cases.md`. A case is eligible when:

- the matter is adjudicated or officially closed (conviction, plea, final judgment, completed inquiry, or an official finding where the subject is deceased); pending prosecutions are excluded;
- at least one admitted source class describes behavior before the event in enough detail to write a one to two page narrative;
- the document is publicly reachable without payment, and its link and retrieval date can be recorded.

### 3.3 Case mix

Presence must not be assumed. If every case is a completed attack, raters can infer that pathway behaviors "must have" occurred. The sample therefore mixes three classes:

| Class | Definition | Planned share |
|---|---|---|
| attack | An attack was carried out or attempted at the target | about half |
| disrupted | A plot was interrupted before execution began | about one quarter |
| non_attack_comparison | Concerning conduct or communication was examined by a court or official body and no attack or attack preparation was found | about one quarter |

Public non-attack comparison cases are hard to find; `candidate-cases.md` says how they are sourced and what that limits. If fewer than four usable comparison cases per matrix can be assembled, that is recorded as a deviation and the limitation is stated in the report.

### 3.4 Narratives

For each selected case the study coordinator writes a neutral summary of one to two pages:

- chronological, plain statements of what the source says happened, each sentence traceable to a cited page or paragraph;
- no outcome statement, no charges, no verdict, no casualty count, no adjectives of judgment, and no vocabulary terms (the narrative must not use indicator or tactic wording);
- events at and after the point of attack are included only for cases assigned to test execution and aftermath tactics, and are written as a separate final section so the pre-event section can be coded first;
- the subject is referred to as "the subject"; other private persons are referred to by role ("a coworker");
- a source list with title, link, document type, and retrieval date.

A second person who is not a rater checks each narrative against its sources for fidelity and for leakage of outcome or vocabulary terms before release to raters. The narrative text is frozen (checksummed) before the first rater opens it.

### 3.5 Pilot

Three cases outside the main sample are coded first by all raters to test the manual and the tooling. Pilot codes are not analysed for the research questions and are published separately, labelled as pilot. The coding manual may be revised once after the pilot. After that revision the manual is frozen and its checksum recorded.

## 4. Units of coding

The unit is one (case, indicator) pair.

For each unit a rater records exactly one code:

- **present**: the narrative states the behavior, or states facts that amount to it, under the rules in `CODING-MANUAL.md`;
- **absent**: the narrative gives a reasonably full account of the relevant period and does not show the behavior;
- **cannot_determine**: the narrative is silent or too thin on the matter to say either way.

Every "present" code must carry a verbatim evidence passage from the narrative. A "present" without a passage is invalid and is returned to the rater for completion before the file is accepted. Each code also carries the rater's confidence (high, medium, low).

For a case assigned to a matrix, the rater codes every active indicator in that matrix. File format: `coded-case.schema.json`.

## 5. Raters

- **Number.** Four to six.
- **Qualifications.** Each rater holds a current professional credential or documented role in threat assessment, protective intelligence, or security investigation (for example a recognised threat-management certification, or at least five years in a threat assessment or protective intelligence function). The specific credential classes accepted are fixed in the registration.
- **Independence.** No rater has authored, edited, or reviewed any part of the vocabulary, has a financial relationship with the project, or reports to or is supervised by the maintainer. The maintainer is not a rater and does not see individual codes until all coding is complete.
- **Conflict-of-interest declaration.** Each rater signs a declaration before training covering: any role in the vocabulary; any commercial interest in a competing or dependent product; any personal or professional involvement in a candidate case. A rater with involvement in a case does not code that case.
- **Training.** Limited to the published vocabulary and the frozen coding manual, plus one calibration session using the pilot cases. No other guidance, examples, or feedback is given. Questions during coding go to the coordinator in writing; answers that clarify the manual are sent to all raters and logged.
- **Isolation.** Raters work alone and have no access to each other's codes, to the reference coding, or to any discussion of the cases until every rater has submitted every file. Raters agree not to discuss cases with each other during coding.
- **Identification.** Published files carry a pseudonym (R01, R02, ...). The key linking pseudonym to person is held by the coordinator only and is not published. Raters may choose to be named in the acknowledgements; naming is never linked to a pseudonym.
- **Compensation.** Whether raters are paid, and by whom, is disclosed in the report.

If fewer than four eligible raters can be recruited, the study does not run (section 14).

## 6. Design and sample size

### 6.1 Design

- 30 main-sample cases: 15 assigned to the People matrix and 15 to the Facilities matrix, each set split about 8 attack, 4 disrupted, 3 comparison.
- Each case is coded by at least three raters. With five raters each rater codes 18 cases; the allocation is balanced so that every pair of raters shares cases, and is generated from a recorded random seed.
- Case order is randomised separately for each rater.

### 6.2 Reasoning

- **Burden.** A matrix has about 200 indicators. Reading a narrative and coding one matrix is estimated at 60 to 90 minutes. Eighteen cases is about 18 to 27 hours per rater. Full crossing (every rater, every case) would add burden without much gain; Krippendorff's alpha accepts incomplete designs.
- **Matrix level.** 15 cases by about 200 indicators gives about 3,000 units per matrix, each with three or more codes. This is ample for a stable matrix-level estimate.
- **Tactic level.** A tactic has 5 to 7 indicators, so about 75 to 105 units per tactic. This supports a tactic-level estimate with a case-level bootstrap interval, expected to be wide for rarely observed tactics.
- **Indicator level.** 15 units per indicator is too few for a precise coefficient. Indicator-level figures are reported as screening flags, with the evaluability rule in section 7, not as estimates to be relied on individually.

### 6.3 The prevalence problem

Most indicators will be absent in most cases. When nearly all codes fall in one category, chance-corrected coefficients such as alpha become unstable and can be low even when raters agree almost always. This is handled four ways, all fixed in advance:

1. Two coefficients with different chance models are reported side by side (section 7).
2. Prevalence and a prevalence index are reported next to every coefficient.
3. An indicator is **evaluable** only if, across the sample, it has at least 5 units in which at least one rater coded "present" and at least 5 in which at least one rater coded "absent". Indicators that are not evaluable are reported as such and are neither passed nor failed.
4. Case selection aims to cover every tactic with at least three cases whose source record plausibly bears on it. Coverage by tactic is tabulated before coding and published.

## 7. Statistics, fixed in advance

All statistics are computed by `analysis/agreement.py` at the commit recorded in section 16. Its tests (`analysis/test_agreement.py`) use synthetic inputs only.

For each indicator, each tactic, and each matrix:

| Statistic | Definition |
|---|---|
| Percent agreement | Mean over units of the share of rater pairs giving the same code |
| Krippendorff's alpha (nominal) | 1 minus observed over expected disagreement, from the coincidence matrix; any number of raters; missing data allowed (Krippendorff 2011) |
| Gwet's AC1 | Chance-corrected agreement with chance agreement computed as the sum over categories of p(1 minus p), divided by (categories minus 1) (Gwet 2008) |
| Prevalence | Share of usable codes that are "present" |
| Prevalence index | Absolute difference between the share "present" and the share "absent" (after Byrt, Bishop and Carlin 1993) |
| Bias index | Mean over rater pairs of the absolute difference between the two discordant cell counts, divided by the units both coded (after Byrt, Bishop and Carlin 1993) |
| Cannot-determine rate | Share of all codes that are "cannot_determine" |

Fixed analytic choices:

- **Primary coefficient:** Krippendorff's alpha, nominal metric.
- **Primary levels:** matrix (RQ1) and tactic (RQ2). Indicator level (RQ3) is a screening analysis.
- **Pooling:** tactic and matrix coefficients pool all (case, indicator) units belonging to the tactic or matrix.
- **Missing data:** "cannot_determine" is treated as missing in the primary analysis. A sensitivity analysis treats it as a third category (`--cd-as-category`). Both are reported.
- **Intervals:** 95 percent percentile intervals for tactic-level and matrix-level alpha from a bootstrap that resamples cases, 2,000 replicates, seed recorded in section 16.
- **No rater is dropped** after data are seen. Rater-level summaries (each rater's prevalence and bias against the others) are reported under pseudonym.
- **No other coefficient, subgroup, or exclusion** is added after unblinding except as a labelled exploratory analysis in a separate section of the report.

References: Krippendorff, K. (2011), Computing Krippendorff's Alpha-Reliability, https://repository.upenn.edu/asc_papers/43 (200). Gwet, K. L. (2008), Computing inter-rater reliability and its variance in the presence of high agreement, British Journal of Mathematical and Statistical Psychology 61, 29 to 48, https://doi.org/10.1348/000711006X126600 (publisher blocks scripted checks, 403; confirm in a browser). Byrt, T., Bishop, J., and Carlin, J. B. (1993), Bias, prevalence and kappa, Journal of Clinical Epidemiology 46, 423 to 429, https://doi.org/10.1016/0895-4356(93)90018-V (200).

## 8. Acceptance thresholds and consequences

Thresholds are on Krippendorff's alpha and follow Krippendorff's customary guidance (0.80 for reliance, 0.667 as the lowest level for tentative conclusions; Krippendorff, Content Analysis, 2nd ed., 2004; page reference to be confirmed at registration).

| Alpha | Label | Consequence |
|---|---|---|
| at or above 0.80 | acceptable | The indicator, tactic, or matrix may be described as having acceptable presence-coding agreement in this study, with the interval and limits stated |
| at or above 0.67 and below 0.80 | tentative | May be described as tentative. Indicators in this band are reviewed for wording and are re-coded in the next dataset round |
| below 0.67 | below threshold | Returned for rewrite or retirement under the project's lifecycle rules (`docs/DEPRECATION.md`). The existing wording is not described as reliable |
| not computable | not evaluable | No claim either way. Carried to the next round with cases chosen to exercise it |

Rules that apply to the table:

- **Tactic and matrix level** use the point estimate for the label and report the interval. A level is described as "acceptable" only if the lower bound of its interval is at or above 0.67.
- **Indicator level** applies only to evaluable indicators (section 6.3).
- **Prevalence exception.** Where alpha is below 0.67, AC1 is at or above 0.80, and the prevalence index is at or above 0.80, the result is labelled "not evaluable (prevalence)" instead of "below threshold". This exception is reported in its own column so readers can see how often it was used.
- **Rewrites are new indicators for study purposes.** A rewritten indicator carries no agreement claim until it is coded again in a later round. Agreement measured on old wording is never attached to new wording.
- **One rewrite round.** The decision gate in section 14 allows one rewrite-and-recode round before a stop decision.

## 9. Handling disagreement

- Agreement statistics are computed on the independent codes as first submitted. Nothing done after submission changes them.
- After all files are in, raters meet for a consensus session on units where they disagreed. The session produces a **reference coding** for the dataset, recorded with the reason for each resolution. Where consensus is not reached the unit is recorded as unresolved, with the positions stated.
- The reference coding is published as a separate, labelled layer. It is not ground truth and is not used to score raters.
- Recurrent disagreements on an indicator are summarised as rewrite input: which words were read differently and what evidence raters wanted.
- Rater notes about behaviors in a narrative that no indicator covers are collected and published as notes.

## 10. Blinding and leakage controls

- Raters are not told a case's class or outcome. Narratives omit outcomes (section 3.4).
- Well-known cases are recognisable. Before coding each case the rater records whether they recognise it (yes, no, unsure). Agreement is reported separately for recognised and unrecognised codings as a descriptive check. Raters are instructed to code only from the narrative text.
- Raters never see scores, the scoring overlay, the crosswalks, or the reference coding.
- The maintainer and anyone who authored vocabulary content do not see individual codes until all coding is complete, and do not write or edit narratives after rater recruitment begins.
- Narratives, manual, vocabulary release, allocation seed, and analysis script are frozen and checksummed before coding. The registration records the checksums.
- Raters submit through a channel that gives each rater access only to their own files.
- Any breach (a rater sees another's codes, a narrative is edited after freeze, an outcome is disclosed) is logged in section 13 and the affected units are flagged in the dataset.

## 11. Ethics and privacy

- **Public adjudicated cases only.** No new information is collected about any person. No interviews, records requests about individuals, or open-source research on subjects, victims, witnesses, or their families is performed.
- **No more than the source states.** A narrative contains nothing about a living private individual beyond what the cited court or official document published. Victims, witnesses, family members, and minors are referred to by role and never named, even where the source names them.
- **Subjects.** Narratives use "the subject". The dataset identifies the case by its public caption or report title and by a study case ID, because the sources are public and must be citable.
- **Non-attack comparison cases** involve people who were not found to have planned an attack. Their narratives say so in the dataset record (not in the rater copy), and the dataset carries a notice that a coded behavior is not a finding about any person.
- **Raters** are adult professionals taking part voluntarily. They consent in writing to publication of their pseudonymised codes, may withdraw before publication, and are warned that source material describes violence.
- **Review.** Whether the study needs review by an institutional ethics body depends on the institution, if any, that hosts it. Status: to be confirmed before registration. If a host institution requires review, the study does not start without it.
- **Not for adverse action.** The dataset and report carry a notice that they are research material about a vocabulary and must not be used to assess, score, or take action against any individual.
- **Takedown.** A person described in a narrative, or their representative, can ask for correction or removal through the channel in `SECURITY.md`. Requests are logged and answered.

## 12. Data management and release

- The coded dataset is published in this repository under `docs/study/dataset/` as a versioned open dataset: narratives, source lists, every rater's independent codes under pseudonym, the reference coding, the allocation table, the analysis output, and the deviations log.
- Each dataset release has a version, a date, a manifest of file checksums, and a statement of the vocabulary release it was coded against. Published releases are not edited; corrections are issued as a new version with a change note.
- License for the dataset: to be decided at registration (the repository code and vocabulary are MIT; a data license such as CC BY 4.0 is under consideration). Source documents are linked, not copied, unless they are public-domain government works.
- The pseudonym key, signed declarations, and consent forms are held privately by the coordinator, not in the repository, and are destroyed five years after publication.
- Results are published whatever they show, including a result below threshold and including a study that stops early.

## 13. Deviations log

Any departure from this protocol after registration is recorded here with date, what changed, why, and whether it happened before or after any data were seen.

| Date | Deviation | Reason | Before or after data seen |
|---|---|---|---|
| | No entries. The protocol has not been registered or run. | | |

## 14. Timeline and decision gate

Times are relative to registration. No calendar dates are set.

| Step | When |
|---|---|
| Recruit raters and coordinator; confirm ethics position; select and verify cases | before registration |
| Write and check narratives; pilot; freeze manual | before registration of the main study (pilot is registered as such) |
| Register protocol with checksums | week 0 |
| Independent coding | weeks 1 to 8 |
| Analysis on frozen script | weeks 9 to 10 |
| Consensus session and reference coding | weeks 10 to 12 |
| Publish dataset and report | by week 16 |

Decision gate, applied to the primary analysis:

- **Continue** (publish as dataset round 1, plan round 2 with new cases, begin rewrites of flagged indicators) if, for both matrices, matrix-level alpha is at or above 0.67 and at least 70 percent of tactics with a computable alpha are at or above 0.67.
- **Rework, then re-test once** if either matrix is below 0.67, or fewer than 70 percent of computable tactics reach 0.67. Indicators and manual are revised, a new registration is lodged, and a fresh sample of cases is coded by raters who meet the same independence rule.
- **Stop** if the re-test also fails the continue condition; or if four independent eligible raters cannot be recruited within six months of the first recruitment attempt; or if fewer than 20 eligible cases can be assembled. A stop is published with its reasons. Under `GOVERNANCE.md` a stop here is one of the project's stated stop conditions.

## 15. What this study will not license

- It does not validate the experimental scoring overlay or any other weighting, banding, ranking, or prioritisation of indicators. No score is coded or analysed.
- It does not support any statement that an indicator, alone or in combination, predicts violence or measures risk.
- It does not support use of the vocabulary to assess a person without professional judgment.
- It does not cover the Organizations or Infrastructure matrices.
- A result in the acceptable band licenses one sentence: that independent trained raters, coding written public case narratives, agreed on presence at the stated level for the stated indicators, tactics, or matrix, in this sample.

## 16. Registration record

To be completed at registration. Empty until then.

| Item | Value |
|---|---|
| Registry and link | not registered |
| Protocol version registered | none |
| Vocabulary release (content version, checksum) | not fixed |
| Coding manual checksum | not fixed |
| Analysis script commit | not fixed |
| Allocation seed and bootstrap seed | not fixed |
| Accepted credential classes | not fixed |
| Ethics review position | to be confirmed |
| Dataset license | to be decided |
