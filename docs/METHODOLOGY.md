# THREAT Matrix Methodology

This document says what the THREAT Matrix is and is not, how its content is written, what its relations mean and how complete they are, how changes are checked, and what has and has not been tested. It is written for threat assessment and security professionals deciding whether and how to use it.

## Limitations and intended use

**What this is.** The THREAT Matrix is an open behavioral vocabulary and evidence index for threat assessment and protective work. It gives named, identified descriptions of observable behavior, grouped into tactics and matrices, with the public sources each description draws on.

**Intended uses.**

- A shared vocabulary, so that different people and teams use the same term for the same behavior.
- A training and case-discussion reference.
- A tagging and interchange layer between tools and between organizations.
- A structure for documenting what was observed, when, and where the information came from.

**What it is not.**

- It is not a risk assessment instrument.
- It is not predictive. Nothing in it estimates whether a person will act.
- It has not been validated against outcomes.
- It is not a score of any person.
- It is not grounds, by itself, for adverse action against anyone.
- It is not a substitute for individualized assessment by qualified professionals.
- It is not legal advice.

**What an entry is.** Each entry is an authored description of a class of behavior, with public sources cited. An entry is not a finding about a person, and matching a person's conduct to an entry establishes nothing by itself. The same observable conduct often has an ordinary explanation; each tactic's `assessment_guidance.false_positive_context` exists for that reason and should be read with the entry.

**Source support varies.** Every tactic, indicator, countermeasure, and response protocol cites at least one public source. A citation shows where the behavior is discussed. It does not show that the source confirms every detail of the entry. 425 of the 828 indicators cite a single source. 8 of the 120 bibliography entries have neither a URL nor a DOI.

**Scoring overlay.** The vocabulary file carries no scores. A separate file, `docs/data/scoring-overlay.json`, holds an experimental scoring overlay. It is experimental, non-normative, unvalidated, and opt-in. It is not part of the vocabulary contract. It is described only in the fenced section [Experimental scoring overlay](#experimental-scoring-overlay) near the end of this document.

**Maturity of the matrices.** People and Facilities are the core matrices. Organizations and Infrastructure are drafts: thinner, less well sourced, and likely to change. Some Organizations entries describe conduct that can be lawful, protected activity, including protest, boycott, litigation, regulatory complaint, shareholder action, union organizing, journalism, and public criticism. Such an entry must never be treated as an indicator of threat without independent evidence of unlawful or violent intent.

**Bias and privacy.** A behavior label attached to a person in a record can follow that person and can be disclosed. Use the same threshold for everyone. Do not treat a protected characteristic, a belief, a diagnosis, or protected activity as an indicator. Record the source of every observation. Collect, share, and keep only what the law and your organization's policy allow. Some countermeasures in the vocabulary describe monitoring; whether a given form of monitoring is lawful where you operate is a question for counsel, not for this document. Only 67 of the 323 response protocols, all in the People matrix, carry an explicit statement that their legal notes are not legal advice; that statement applies to all 323.

**Reliability.** No reliability study has been run. A study of whether independent practitioners agree on which People and Facilities indicators are present in written case narratives is planned. Its protocol is a draft and nothing has been collected. See [docs/study/README.md](study/README.md).

## 1. Scope and maintenance

The vocabulary describes observable behavior against four target matrices: People, Facilities, Organizations, and Infrastructure. Each matrix runs across four lifecycle phases: Target Development, Mobilization, Execution, and Aftermath. The phases describe common patterns, not a required sequence.

| Matrix | Maturity | Tactics | Indicators | Countermeasures | Response protocols |
|---|---|---:|---:|---:|---:|
| People | core | 34 | 191 | 137 | 69 |
| Facilities | core | 40 | 200 | 160 | 80 |
| Organizations | draft | 49 | 244 | 196 | 98 |
| Infrastructure | draft | 38 | 193 | 152 | 76 |
| Total | | 161 | 828 | 645 | 323 |

There are 32 active actor profiles and 2 reserved actor-profile identifiers (`AP022`, `AP027`), and 120 bibliography entries.

Each tactic sits in exactly one matrix, set by what the threat actor's primary objective targets. Motivation lives in actor profiles, not in matrix placement. An incident can touch several matrices. The full placement rule is `matrices.boundary_rule` in the data, and each matrix's scope sentence is `matrices.<name>.scope`.

**Out of scope.** The vocabulary does not contain exploit code, weapon construction, step-by-step attack tradecraft, or targeting information about specific persons or organizations. It ships no case data. Case records and coverage records are held by the organization that makes them.

**Maintenance.** The project is maintained by one person, cites public sources only, and is released under the MIT license. Roles, decision rules, and succession are in [GOVERNANCE.md](../GOVERNANCE.md). Version rules are in [VERSIONING.md](VERSIONING.md); identifier rules are in [IDENTIFIERS.md](IDENTIFIERS.md); lifecycle rules are in [DEPRECATION.md](DEPRECATION.md).

## 2. How the vocabulary is written

Every indicator is a type-level description of a class of behavior. It is never a case. The fields below describe the class as written.

**Required on every indicator:** `id`, `behavior`, `category`, `detection_sources`, `phase_relevance`, `source_refs`, `modality`, `human_social`, `temporal_signature`. All 828 indicators also carry `informs_axes` and `conditioning_guidance`.

**Modality.** `modality` follows the behavior's instrument, never its effect, its target's importance, or the channel it travels through:

- `physical`: matter, force, or presence is the instrument.
- `cyber`: the instrument acts on a computing system's technical properties, including reading exposed data.
- `cyber_physical`: the behavior itself crosses between the two, and the indicator must name a `crossing_mechanism`.
- `human_social`: the mechanism lies in the human, social, or institutional domain, including persuasion, coercion, legal or financial pressure, and warning behaviors.

`human_social` is also a separate true or false flag. It is true whenever the behavior's essence is influencing, recruiting, coercing, deceiving, or negotiating with people, whatever the modality. An indicator whose modality is `human_social` must carry the flag as true.

**Temporal signature.** `temporal_signature` is a categorical value for how close to action the behavior typically appears: `horizon`, `advancing`, `imminent`, `staging`, `in_progress`, or `aftermath`, with optional early and late refinements on four of the six. It describes timing for the class of behavior. It is not a measure of seriousness and says nothing about any case.

**informs_axes.** Each indicator records what observing it reveals on six axes. Three concern the threat actor: capability, intent, and opportunity. Three concern the postulated event: timing, target, and method. Each axis takes `none`, `weak`, `moderate`, or `strong`. The scale is resolution, not seriousness: `weak` resolves only the coarsest fact on that axis, `moderate` adds one narrowing, and `strong` pins a specific value. Intent is read as general intent to act, never specific motive. The values are authored and categorical.

**Conditioning guidance.** `conditioning_guidance` names the case facts worth collecting when the behavior is observed. It has two parts: `probe_factors`, a list drawn from six factor names (target focus, pathway stage, means in hand, tempo and trajectory, proximity and access, source credibility), and `guidance`, a directive of at most 420 characters. It is a collection prompt. It does not produce a rating, and response actions live in the tactic's response protocols.

**Target fields.** People indicators may record `target_identity`. Facilities indicators may record `facility_target_scope` and `within_site_focus`. All three use the revealed reading: a value is recorded only when observing the behavior actually reveals it, and an empty or absent value means the behavior reveals nothing on that point.

**Tactic-level text.** Each tactic carries `notes`, `field_notes`, `observed_contexts` (generic context types, never named cases or people), `evidence_basis`, and `assessment_guidance`. Assessment guidance has six parts: criteria and anchors for credibility, capability, intent, and opportunity; `false_positive_context`; and `threshold_guidance`. These are prompts for structured professional judgment. They are not a scoring scheme.

**Writing rules.** Vocabulary text follows [VOICE.md](VOICE.md). In vocabulary text the class of actor is called "threat actor". In a case record about a person who has not been assessed as posing a threat, that label is rendered "person of concern" (section 6).

## 3. Relations between objects

Four relations link objects by identifier. Their coverage today is uneven, and one of them is untyped. The figures below are from the 2.0.0 data.

| Relation | Lives on | Meaning | Coverage today |
|---|---|---|---|
| `correlates_with` | Indicator, pointing to indicators | The two behaviors tend to occur together, in any phase or matrix. Stored in both directions. | 1,586 entries (360 cross a matrix boundary). 142 of 828 indicators have no entry: 68 Organizations, 37 People, 37 Infrastructure. On 107 of them the field is absent and on 35 it is an empty list; the two mean the same. |
| `mitigates` | Countermeasure, pointing to indicators | The countermeasure acts on that behavior. Each edge is `{"indicator": "<id>", "function": "<value>"}`. | 483 edges on 287 countermeasures (Organizations 341, Facilities 135, Infrastructure 7, People 0). Every edge points to an indicator in the countermeasure's own tactic. 478 of 828 indicators have no edge: all 191 People indicators, 189 Infrastructure, 98 Facilities. |
| `compensates_for` | Countermeasure, pointing to countermeasures | This countermeasure covers for the absence or failure of the other. Countermeasure identifiers only. | 362 entries on 247 of 645 countermeasures. |
| `coordinates_with` | Response protocol, pointing to response protocols | The two protocols are activated together or in a set order. Directed: an entry on A naming B does not require an entry on B naming A. | 512 entries on 269 of 323 response protocols. 340 of the 512 have no matching entry in the other direction. |

**The `mitigates` relation is untyped today.** The schema allows a `function` of `prevent`, `detect`, `deny`, or `unreviewed`. Every one of the 483 edges in the data has the function `unreviewed`. The relation therefore records that a link was drawn and nothing about how the countermeasure acts. Do not read it as a statement that a control prevents or detects anything. The absence of an edge is also not information: the People matrix has no `mitigates` edges at all, because none has been authored, not because no countermeasure applies.

**`compensates_for` does not hold indicators.** Before schema 3.0.0 this field mixed countermeasure and indicator identifiers. Indicator targets now live only in `mitigates`. An indicator identifier in `compensates_for` is rejected.

**What a correlation link claims.** A cross-matrix `correlates_with` link is meant to be drawn only when the two behaviors are the same act, share one literal resource, or form one signal about the whole actor. This is an authoring rule. No field records which test a link meets and no gate checks it (section 5).

**Direction.** `correlates_with` is undirected and stored both ways; the gates reject a one-way entry. `coordinates_with` is directed, and one-way entries are permitted: a protocol may name another that it gates, precedes, or runs alongside without the second naming the first. No field records which of those three the author meant. `mitigates` and `compensates_for` run one way by definition.

**The data's own summary of the links is incomplete.** `detection_mesh.schema_links` in the vocabulary names `correlates_with`, `compensates_for`, and `coordinates_with`. It does not name `mitigates`.

**What a missing link means.** Nothing. A missing or empty `correlates_with`, `mitigates`, or `coordinates_with` means no link has been authored. `coordinates_with` is absent on 6 response protocols and empty on 48.

## 4. Evidence basis

Every tactic declares an `evidence_basis` value. It states how the tactic was written. It is the author's declaration of method: no record of practitioner input is published, so the value is not evidence in itself.

- `practice_led`: tactic structure and indicators were written from practitioner experience, with public sources cited that discuss the pattern.
- `practice_and_literature`: written from practice and published literature together.
- `literature_led`: derived mainly from published literature with practitioner review.
- `literature_only`: derived from published literature. No practitioner origin is claimed.

| Value | Tactics | By matrix |
|---|---:|---|
| `practice_led` | 10 | Facilities 9, People 1 |
| `practice_and_literature` | 111 | Organizations 47, People 33, Facilities 31 |
| `literature_led` | 1 | Infrastructure 1 |
| `literature_only` | 39 | Infrastructure 37, Organizations 2 |

Whatever the value, every tactic, indicator, countermeasure, and response protocol cites public sources only. The bibliography holds no private, unpublished, or attested-experience entry, and the schema no longer allows the entry types that described such sources. Each `source_refs` entry must be a key in the bibliography, and every bibliography entry must be cited at least once; both are checked.

The 120 bibliography entries by type: government report 56, practitioner guide 18, academic paper 12, standard 12, court document 8, incident database 5, book 4, news investigation 4, after-action review 1.

## 5. Review process and gates

A change is checked by a set of gate commands. This section says exactly what runs where, what the gates check, and what they do not.

### The gate commands

```
python3 scripts/lint/validate.py docs/data/framework.json
python3 scripts/lint/validate.py docs/data/framework.json --overlay docs/data/scoring-overlay.json
python3 scripts/lint/validate.py docs/data/framework.json --fixtures scripts/lint/fixtures
python3 scripts/lint/validate.py docs/data/framework.json --overlay docs/data/scoring-overlay.json --records examples/experimental-scoring/worked-cases
python3 scripts/lint/field-parity.py docs/data/framework.json
python3 scripts/lint/mesh-refs.py docs/data/framework.json
python3 scripts/lint/id-manifest.py --check docs/data/framework.json docs/data/id-manifest.json
python3 scripts/lint/consumer-smoke.py
```

### Local hook

`scripts/git-hooks/pre-commit` is opt-in: enable it once with `git config core.hooksPath scripts/git-hooks`. It acts when a staged path is under `docs/data/`, `src/`, `scripts/`, `examples/`, `docs/assets/`, or `.github/workflows/`, or is `index.html`, `docs/index.html`, `package.json`, `bun.lock`, `vite.config.ts`, or a `tsconfig` file. It exports the staged content to a temporary directory and checks that copy, never the working tree. It requires the `jsonschema` package and stops with a message if it is not installed; nothing is skipped for lack of it. It runs: `validate.py` on the framework, on the framework with the overlay, and on the scored worked cases; `field-parity.py`; `mesh-refs.py`; `id-manifest.py --check` with two baselines, the committed published baseline `docs/data/baselines/id-manifest-1.7.0.json` and the manifest in the previous commit; `derive-axis-confidence.py --check`; and `consumer-smoke.py`. It runs the `validate.py` fixture harness only when a file under `scripts/lint/` or a `docs/data/*.schema.json` file is staged. If a viewer build input is staged (anything under `src/`, `index.html`, `package.json`, `bun.lock`, `vite.config.ts`, a `tsconfig` file, or a `docs/data` file the viewer imports), it requires a rebuilt bundle to be staged as well (a new or changed file under `docs/assets/` and `docs/index.html`). On every commit it checks, it confirms that the staged `docs/index.html` references exactly the files in the staged `docs/assets/`. It does not run the viewer build, and for a change to a workflow file it runs the data gates but cannot judge the workflow itself. It can be bypassed with `git commit --no-verify`.

### Continuous integration

Three workflows run on every push and every pull request for `main`, `v1-build`, and `v3-design`, with a read-only token, actions pinned to commit SHAs, Python 3.14, and `jsonschema` 4.26.0. *Framework Validator* runs, in order: `validate.py docs/data/framework.json`; the same with `--overlay docs/data/scoring-overlay.json`; the fixture harness (`--fixtures scripts/lint/fixtures`); the scored worked cases (`--overlay ... --records examples/experimental-scoring/worked-cases`); `field-parity.py`; `mesh-refs.py`; `id-manifest.py --check docs/data/framework.json docs/data/id-manifest.json --baseline docs/data/baselines/id-manifest-1.7.0.json`; a second manifest comparison against the previous manifest (the base branch's on a pull request, the previous commit's on a push; skipped with a message when there is none to fetch, for example on a new branch or after a force push); `consumer-smoke.py`; and `derive-axis-confidence.py --check`. JSON Schema validation is part of `validate.py` and is required; a missing `jsonschema` package fails the run. *Mesh Refs* runs `mesh-refs.py` alone. *Bundle Freshness* checks that `docs/index.html` references exactly the files in `docs/assets/`, then deletes `docs/assets/`, rebuilds with bun 1.3.9, and fails unless `docs/index.html` and every file under `docs/assets/` are byte-identical to the committed ones and the build produced no uncommitted file. Nothing is deployed from CI.

### What the gates check

| Gate | Checks |
|---|---|
| `validate.py` on the vocabulary | 36 numbered checks: unique identifiers in every namespace; every reference resolves to an object of the right kind; identifier grammar, exact to the last character; a tactic's identifier agrees with its matrix and phase; a child's identifier agrees with its parent; the lifecycle contract; the modality and conditioning-guidance rules; bibliography keys, URLs (http and https only), DOIs, and dates; every bibliography entry is cited; no score field anywhere in the vocabulary; no empty or padded string; an actor profile's category and label agree, and matrix-specific fields appear only in their matrix; and the vocabulary against its JSON Schema, together with a pinned digest of that schema's constraints, so that a loosened schema fails too. |
| `validate.py --overlay` | 11 more checks on the overlay (47 in total). Described in the overlay section. |
| `validate.py --records` | 3 more checks on scored case records (50 in total). Described in the overlay section. |
| `validate.py --coverage FILE` | 1 check on an organization's coverage document. It brings the validator's total to 51 checks. It is not one of the gate commands, because the repository ships no coverage document. |
| `validate.py --fixtures` | 199 fixtures (190 negative, 9 positive). Each negative fixture applies a named defect to a fresh copy of the data and must be rejected by the check it targets; each positive fixture must pass cleanly. The harness fails if the unmodified data does not pass, if a fixture's change does not apply, or if any of the 51 checks lacks a negative fixture. |
| `field-parity.py` | A field fully populated in one matrix is not missing from another; every matrix has indicator links of its own; no scoring field is present in the vocabulary. |
| `mesh-refs.py` | Every `correlates_with`, `mitigates`, `compensates_for`, and `coordinates_with` reference resolves to the right kind of object; none refers to itself or repeats; `correlates_with` is symmetric. |
| `id-manifest.py --check` | The committed ID manifest lists exactly the identifiers in the vocabulary, and no identifier is in two places. With `--baseline`, which the hook and continuous integration always pass, no identifier in the baseline is missing from the vocabulary without a removal record, and no reserved or removed identifier is live again. The baselines used are the committed manifest of the published 1.7.0 release and the previous manifest. Run by hand without `--baseline`, the check cannot see an identifier that was dropped together with a regenerated manifest. |
| `consumer-smoke.py` | The vocabulary, the overlay, the five score-free worked cases, the three scored worked cases, and both templates validate against their schemas; the reference consumer prints no score unless asked and prints the overlay notice before any score when asked. |
| Bundle Freshness (CI only) | The committed viewer equals a fresh build of the committed sources. |

Check identifiers, their scope, and the fixture that covers each are listed in [scripts/lint/fixtures/README.md](../scripts/lint/fixtures/README.md).

**Schema validation is required.** `validate.py` runs the JSON Schemas as part of its checks and fails if the `jsonschema` package is missing. `--no-schema` skips them and says in its summary that the run is not a release gate. The validator also holds a digest of each schema's constraints (`SCHEMA_PINS` in `scripts/lint/validate.py`). If a required list, enum, pattern, or closed object in a schema file changes, the schema check fails until the digest is updated in the same change, so a schema cannot be loosened unnoticed.

**A note on trailing newlines.** Python's regular-expression engine lets a closing `$` match before a final newline, so a plain anchored pattern would accept an identifier with a newline appended. The rule that an identifier, key, or version has no trailing whitespace is enforced twice: each anchored pattern in the schemas is paired with a second pattern that rejects whitespace, and `validate.py` applies an exact full match of its own. Both reject such a value when run from Python.

### What the gates do not check

These rules are stated in this project's documents. No gate checks them. They are obligations on the author and the reviewer, not guarantees from the validator.

- **Whether the content is right.** No gate reads a behavior description for accuracy, checks that a cited source supports the entry that cites it, or checks that a URL still resolves.
- **The actor label.** That vocabulary text uses "threat actor" as its only label for the class of actor is a writing rule in VOICE.md. No gate reads prose for it.
- **Correlation link validity.** That a cross-matrix `correlates_with` link meets one of the three tests in section 3. The gates check that a link resolves and is symmetric, not that it is justified.
- **The `mitigates` function.** No gate requires an edge to be typed. All are `unreviewed`.
- **The sunset rule.** That an item stays deprecated for at least one MINOR release before its content is removed. This cannot be seen from one document.
- **Overlay content.** In the overlay, that every indicator describing direct force against a person carries the floor. The gates check the arithmetic, the labels, and that the floored entries are exactly the 43 the rubric lists. They do not check whether the authored values or that list are right. The overlay itself names three known inconsistencies in the floored set.
- **Workflow files.** No gate checks that a workflow file is correct.
- **Case records about real people.** The repository holds none and checks none.

### Review by people

Today every change is reviewed by the maintainer alone. No outside reviewer has been recruited and no outside review of any content has been recorded. [GOVERNANCE.md](../GOVERNANCE.md) section 3 sets the process: public sources required, all gates pass, and, while reviewer seats are vacant, a pull request stays open at least seven days for public comment and the merge note says no outside review was obtained.

## 6. The score-free case record

`docs/data/case-record.schema.json` (record version 1.0.0) defines the default way to document a case with this vocabulary. Templates and five fictional worked cases are in [examples/](../examples/README.md).

A record holds: the vocabulary version it was written against; an organization-assigned case reference; the date; the assessor's role; a list of observations, each naming an indicator, when it was observed, the source, and whether it is corroborated; six instance factors with a free-text basis; protective factors (required, and may be an empty list); a free-text assessment summary; dated reassessments, each marked raised, lowered, or unchanged; a disposition; and an acknowledgment of the limitations above.

Three rules matter most:

1. **No score.** The record has no band, weight, priority, or score field, and its schema is closed, so one cannot be added.
2. **Person of concern.** The record's `subject_term` is fixed to `person_of_concern`. The vocabulary calls the class of actor "threat actor" because it describes behavior classes. A record about a real person who has not been assessed as posing a threat must not carry that label, so in a case record it is rendered "person of concern".
3. **Concern can go down.** Reassessments run in either direction, protective factors are always recorded, and the dispositions include `no_threat_identified` and `transient_no_further_action`.

The six instance factors are prompts for what to find out about the case: target focus, pathway stage, means in hand, tempo and trajectory, proximity and access, and source credibility. Means in hand refers to means actually possessed or acquired. Lawful ability to acquire something is not means in hand.

The repository ships no real case data and has no place to enter any. Keep records in your own case system, under your own retention and access rules.

## 7. Reliability

No reliability study has been run, so no claim is made about how consistently different people apply this vocabulary.

A presence-coding study is planned for the People and Facilities matrices: independent, credentialed practitioners would each mark which indicators are present in written narratives of public, adjudicated cases, and agreement would be reported against thresholds fixed in advance. The protocol, coding manual, record schema, candidate case list, and analysis script are drafts in [docs/study/](study/README.md). The protocol is not registered, no one has been recruited, no case has been selected, and there is no data.

If it runs, a passing result would support one statement: that trained people agreed on presence at a stated level in that sample. It would say nothing about prediction, about risk, or about the scoring overlay.

## 8. Document history

This file replaces the former `docs/methodology` folder. Rules from that folder that still apply are in the sections named below. Dated records and historical designs were retired from the working tree and remain in the repository history. In version 2.0.0 the scoring material moved out of the main sections into the fenced overlay section, and the limitations section was added at the top.

| Former file | Now |
|---|---|
| README.md | Replaced by this document |
| conditioning-guidance-authoring-rubric.md | Section 2 |
| conditioning-guidance-field.md | Section 2 |
| informs-axes-boundary-rubric.md | Section 2 |
| modality-authoring-rubric.md | Section 2 |
| people-target-identity-revealed-guide.md | Section 2 |
| target-dimension-rubric-LOCKED.md | Section 2 |
| mesh-link-rubric-v2.md | Section 3 |
| coverage-derivation.md | Appendix A |
| aftermath-seam-reconciliation.md | Experimental scoring overlay section |
| bottom-cut-recalibration.md | Experimental scoring overlay section |
| instance-conditioning-contract-completion.md | Section 6 and the overlay section |
| severity-floor-clarifications.md | Experimental scoring overlay section |
| v1-6-1-contract-clarifications.md | Sections 1 and 5, and the overlay section |
| Five dated working records | Retired |
| Nine historical design documents | Retired |

---

## Experimental scoring overlay

> **Notice, as carried in the overlay file.** Experimental and non-normative. These values are authored, type-level estimates for classes of behavior. They have not been validated against outcomes or by independent human reviewers. They do not predict violence, they are not a score of any person, and they must not be used as grounds for adverse action. The vocabulary in framework.json is complete without this file.

Everything in this section describes `docs/data/scoring-overlay.json` (overlay version 0.1.0, applies to vocabulary 2.0.0) and its schema `docs/data/scoring-overlay.schema.json`. None of it is part of the vocabulary contract. The overlay is versioned separately and is outside the stability promise in [VERSIONING.md](VERSIONING.md). The file declares its own status in machine-readable fields: `status: experimental`, `normative: false`, `validation_status: unvalidated`, `scope: type_level`, `not_a_risk_score: true`.

This section explains how the numbers are produced so they can be inspected. It is not a recommendation to use them.

### What the overlay holds

- `indicator_scores`: one entry for each of the 828 indicators, keyed by indicator identifier. The key set must equal the vocabulary's indicator identifiers exactly.
- `tactic_priorities`: one label for each of the 161 tactics (`Urgent`, `Immediate`, `Priority`, or `Routine`). The validator requires exactly one entry per tactic.
- `rubric`: the text of the scoring rules, the thresholds, and the floor rule.
- `instance_conditioning`: the text of the experimental case-level rules.

### Axes

Each entry has four authored values from 0.0 to 10.0, stored to one decimal place, under `axes`:

- `impact_potential`: the harm the class of behavior directly produces or imminently enables.
- `blast_radius_potential`: the scope affected.
- `recoverability_inverse`: how hard the harm is to undo. Higher means harder.
- `detectability`: how observable the behavior is to trained people or telemetry.

These are one author's estimates for a class of behavior.

### Weight

```
type_weight = round((impact_potential * blast_radius_potential * recoverability_inverse * (10 - detectability)) ** 0.25, 2)
```

The weight is the geometric mean of the three harm axes and inverted detectability, stored to two decimal places. One low axis pulls the whole weight down. Because detectability is inverted, a behavior that is hard to observe gets a higher weight than an otherwise identical behavior that is easy to observe. A higher weight therefore does not mean a more harmful behavior, and the weight is not an expectation of harm in any statistical sense. The validator recomputes the weight and rejects a stored value more than 0.005 from the result.

### Band

The `type_band` is read from the **stored, rounded** weight at the thresholds in `rubric.type_band_thresholds`, then raised to the floor if the entry has one.

| Band | Stored weight from |
|---|---|
| `low` | 0.0 |
| `medium` | 3.0 |
| `high` | 5.0 |
| `critical` | 6.5 |

The current population is 14 low, 435 medium, 291 high, and 88 critical. The thresholds were set against the distribution of the authored values, as the overlay's own `rubric.calibration_guidance` records. They were not calibrated to outcomes.

### Floor

An entry may carry `type_band_floor`. Where present, the band is at least the floor; the weight is unchanged. In the current file the only floor value used is `critical`, on 43 indicators: 11 People, 24 Facilities, 8 Infrastructure. Organizations has none.

`rubric.type_band_floor_rule` documents the rule, and its `floored_indicators` list names every floored indicator. The validator fails if the entries that carry a floor differ from that list in either direction, so a floor cannot be added or removed without changing the published list.

- People, direct physical force against a person: 11 indicators.
- Facilities, direct physical force: 7 indicators.
- Facilities, secondary strike against responders or evacuees during an active incident: 4 indicators.
- Facilities, harm to occupants through the structure or its systems: 13 indicators.
- Infrastructure, execution behaviors where casualties are the direct mechanism: 8 indicators.

The same text lists three known, unresolved inconsistencies, where an indicator is not floored although a closely similar one is (`IND-F0302-05`, `IND-I0306-02`, `IND-0304-04`). They are published so the set can be reproduced exactly, not because the set is settled.

### Axis confidence

Each axis value carries a label under `axis_confidence`: `established`, `inferred`, or `thin`. The label is derived by rule from the value, by `scripts/analysis/derive-axis-confidence.py`, and the gate fails if a stored label differs from the rule. Of the 3,312 axis values, 2,348 are `inferred`, 917 are `established`, and 47 are `thin`. The overlay defines `inferred` as a reasoned assignment without a documented anchor. Impact and recoverability are `inferred` on every indicator.

### The experimental scored record

`scoring-overlay.schema.json` defines a scored case record (`$defs.scored_case_record`): one `indicator_id`, the `type_band` quoted from the overlay, an `instance` block with the six instance factors, a `conditioned_priority`, and optional `framework_version`, `overlay_version`, `primary_objective_evidence_tier`, and `disposition`.

Its rule is escalate-only: the priority may be above the band and may never be below it. With `--records`, the validator checks three things: the indicator exists and the quoted band equals the overlay's band for that indicator; the priority is not below the quoted band or the overlay's band; and the record has the required shape.

The limits of this record are the reason it is not the default:

- It can only move one way. A case in which concern was lowered still shows the type band.
- It holds one indicator. A real case usually involves several, and there is no rule for combining records.
- It has no place for protective factors.
- Its floor is an authored estimate, so it inherits that estimate's uncertainty.

Do not place a scored record in a case file or use one to decide anything about a person. Use the score-free record in section 6. Three fictional scored records, kept so the format can be checked, are in [examples/experimental-scoring/](../examples/experimental-scoring/README.md).

### Gates on the overlay

With `--overlay`, `validate.py` adds eleven checks: band against stored weight and floor; weight against the axes; floor values; the floored set against the rubric's list; axis-confidence labels against the rule; the header constants and version match; the key set against the vocabulary; exactly one valid priority per tactic; decimal places; threshold ordering and the six factor names; and the overlay against its JSON Schema and that schema's pinned digest. These confirm that the file is internally consistent. They do not, and cannot, confirm that any value is right.

---

## Appendix A. Coverage derivation rule

This appendix defines how an organization can derive, for one protected target and one indicator, whether it has deployed countermeasures that act on that behavior. The vocabulary defines the record shapes (`docs/data/coverage.schema.json`) and this rule. Each organization holds its own records; none is published here. The rule is normative for the derivation, with the limits stated first.

### Limits in the current data

- **Every edge is `unreviewed`.** The rule distinguishes `prevent`, `detect`, and `deny` edges. All 483 `mitigates` edges in version 2.0.0 have the function `unreviewed`, and an unreviewed edge caps the band at `partial`. Run on the published data alone, the rule can therefore never return `covered`.
- **`not_assessable` cannot be derived.** The coverage schema allows the band `not_assessable` for a behavior that no organizationally deployable control addresses. The vocabulary has no field that marks an indicator this way. 478 of 828 indicators have no `mitigates` edge, including every People indicator, and the data does not say whether an edge is absent by design or simply not yet authored. Until such a marker exists, an organization that records `not_assessable` is recording its own judgment and should say so in the record.
- **"Most serious indicators" is the organization's call.** Critical path dominance, below, depends on which indicators in play the organization treats as most serious. The vocabulary ranks nothing. That designation is a documented judgment by the organization.

### Inputs

1. The vocabulary's `mitigates` relation: countermeasure to indicator edges, each with a function (`prevent`, `detect`, `deny`, or `unreviewed`). An edge asserts that the countermeasure acts on that behavior. Edges may cross tactics.
2. The organization's `cm_deployment_record` for the protected target: which countermeasures are deployed, where they apply, and when they were last verified operational.
3. The indicators in scope: a live case's indicator set, or a what-if set.

### The derivation, per target and indicator

1. Collect the mitigating countermeasures for the indicator from the `mitigates` relation.
2. If the indicator has no `mitigates` edge, the published data gives no basis for a band. Record `not_assessable` only on the organization's own documented judgment that no deployable control exists for the behavior (see the limits above). A `not_assessable` band is excluded from `covered` and never drives a posture step up.
3. Intersect the mitigating countermeasures with the target's deployments. Exclude before banding:
   - deployments whose `applies_to` scope does not reach the assessed target;
   - deployments with status `planned` or `not_deployed`;
   - deployments that are unverified, or whose `verified` date is older than the staleness window (default twelve months) at derivation time; these contribute at most `partial`;
   - countermeasures the assessed threat actor's position defeats, such as access controls whose credentials the actor holds.
4. Band the result:
   - `covered`: every relevant mitigating countermeasure class is deployed, verified, and in scope, and at least one contributing edge has function `prevent` or `deny`. Detection alone does not fully cover a behavior; a detect-only edge set caps the band at `partial`. An edge with function `unreviewed` also caps at `partial`.
   - `partial`: some mitigation is deployed, or contributing deployments are unverified, stale, out of scope in part, detect-only, or reached only through unreviewed edges.
   - `exposed`: no relevant mitigating countermeasure is deployed, or critical path dominance applies.
5. Critical path dominance: if the countermeasures mitigating the indicators the organization has designated most serious among those in play are absent, the band is `exposed` regardless of other deployments. The absent countermeasures are recorded as the gap list.

### How coverage enters an organization's posture

This rule assumes the organization keeps its own protective posture levels. The vocabulary does not publish a posture scale. Coverage adjusts the organization's posture upward only:

- `exposed` raises the posture one step, or, where the organization is already at its higher levels, marks the gap as the first priority within that level.
- `covered` never lowers a posture automatically. An organization may record a signed deviation downward on the strength of verified coverage.
- `partial` holds the posture; the gap detail goes in the documented rationale.

### Statelessness

The derivation is a function of the current records, recomputed each time. When remediation closes a gap and a new derivation returns the posture to its default, that return is not a deviation and needs no signature.

### The audit line

Every derivation records: the target, the indicator, the band, the derivation date, the vocabulary version whose `mitigates` relation it ran against, and the age of the oldest input consumed.

### The disposition discipline

An `exposed` band must carry a disposition: `funded`, `accepted_with_rationale`, `transferred`, or `compensating_interim`, with a review date. Deployment records and derivations are held by the organization and never published. Organizations with live litigation exposure should structure record generation under counsel.
