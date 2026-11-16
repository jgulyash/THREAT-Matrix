# THREAT Matrix Roadmap

This document says where the project is, what the next twelve months are for, how the decision to continue or stop will be made, and what is deliberately not planned. It gives no dates for future work.

## Where the project is

The THREAT Matrix is an open behavioral vocabulary and evidence index for threat assessment and protective work. It was previously described as a scored open standard. That description has been withdrawn: the scores were unvalidated, and the project has one maintainer, no outside reviewer, and no known outside adopter.

| | Published on `main` | On branch `v3-design`, not released |
|---|---|---|
| Vocabulary content | 1.7.0 | 2.0.0 |
| Vocabulary schema | 2.1.0 | 3.0.0 |
| Score-free case record | none | 1.0.0 |
| Experimental scoring overlay | none (scores are inside the vocabulary file) | 0.1.0, separate and opt-in |

Content 2.0.0 holds 161 tactics, 828 indicators, 645 countermeasures, 323 response protocols, 32 active actor profiles, and 120 public sources. The People and Facilities matrices are the core. The Organizations and Infrastructure matrices are labelled draft.

The 3.0.0 release has not been announced. Under [docs/VERSIONING.md](docs/VERSIONING.md), a MAJOR release needs at least 30 days of public notice with a tested migration guide, and that clock has not started.

## What has shipped

The record of each release is [CHANGELOG.md](CHANGELOG.md). In brief:

| Release | Date | What it added |
|---|---|---|
| 1.0 | before 1.1.0 | People matrix: tactics across four lifecycle phases, and actor profiles |
| 1.1.0 | 2026-05-02 | JSON Schema, versioning and identifier policies, a reference consumer; indicators, countermeasures, and response protocols for the People matrix; the bibliography |
| 1.2.2 | 2026-07-04 | People scope widened to one or more people; indicator links across phases; per-tactic assessment guidance |
| 1.3.0 | 2026-07-12 | Facilities matrix |
| 1.4.0 | 2026-07-19 | Infrastructure matrix; links between matrices |
| 1.5.0 | 2026-07-24 | Organizations matrix; `informs_axes` on every indicator |
| 1.6.0 | 2026-08-08 | Schema 2.0.0, closing every object; per-indicator `modality`; `conditioning_guidance` |
| 1.6.1 | 2026-08-13 | Schema 2.1.0; clarifications |
| 1.7.0 | 2026-08-15 | Transportation brought into Infrastructure; symmetric `correlates_with`; 161 tactics and 828 indicators |

From 1.2 to 1.7 each release also carried authored scoring fields inside the vocabulary. Those fields are history: in content 2.0.0 they are removed from the vocabulary and kept only in the experimental overlay. Version 1.7.1 was a development label and was not released.

## The next twelve months

Four steps, in this order. Each depends on the one before.

### Step 1. Enforce the contract

**Status: done on this branch. Not released.**

- The schema is closed and tightened (3.0.0): identifier grammar, bibliography keys, URLs limited to http and https, required structures, lifecycle rules.
- The validator runs 51 checks across the vocabulary, the overlay, scored records, and coverage documents. It runs the JSON Schemas themselves, requires them, and pins their constraints. 199 fixtures prove that each check rejects the defect it is for.
- The lifecycle contract is gated: required fields per state, supersession targets must be active with no cycles, and only actor profiles may be reserved.
- A committed ID manifest makes the no-reuse rule checkable. On every commit through the hook, and on every push and pull request, it is compared with a committed baseline of the published 1.7.0 identifiers and with the previous manifest.
- The local hook checks staged content and requires schema validation. Continuous integration runs every gate on `main`, `v1-build`, and `v3-design`.
- The migration guide is written against the published 2.1.0 document and tested on it, with a migration tool and a flat export.

Still to do: announce and tag the release under the 30-day rule.

Known limits, stated in [docs/METHODOLOGY.md](docs/METHODOLOGY.md#what-the-gates-do-not-check): no gate checks that content is accurate or that a citation supports its entry; every `mitigates` edge is untyped; 478 indicators have no `mitigates` edge and 142 have no `correlates_with` link.

### Step 2. Clean up the legal surface

**Status: done on this branch for documents, records, and the viewer. Open for content.**

Done:

- A limitations and intended-use statement opens the README and the methodology, and the viewer's landing view carries the short form.
- Scores are out of the vocabulary, out of the viewer's default view, and out of the case record. The overlay is a separate, opt-in, experimental file.
- A score-free case record is the default: it uses "person of concern", requires protective factors, records reassessment in either direction, and includes dispositions for no threat identified and transient concern.
- The self-description "standard" is withdrawn.
- Organizations and Infrastructure are labelled draft in the data, the viewer, and the documents.
- A private reporting route (SECURITY.md) and issue-template warnings against posting real case data.
- The schema no longer allows non-public source types.

Open, each needing a decision or work by the maintainer:

- **Organizations entries that describe protected activity.** They are labelled draft and carry a caution. Whether to quarantine or remove specific tactics has not been decided.
- **Response-protocol action lines that tell staff to detain a person** (four People protocols). They have not been reworded.
- **Citation repair.** Three dead links were replaced. Locators, and citations that do not cover the behavior they are attached to, have not been addressed.
- **Vocabulary text still uses "threat actor" and "targeted subject".** The case-record rendering rule covers records. The vocabulary text itself has not been reworded.
- **No legal review has been done.**

### Step 3. Build one adoption hook

**Status: protocol drafted. Study not run.**

The hook is a presence-coding reliability study on the People and Facilities matrices, published with its coded case set: a test of whether independent, credentialed practitioners agree on which indicators are present in written narratives of public, adjudicated cases. The draft protocol, coding manual, record schema, candidate case list, and analysis script are in [docs/study/](docs/study/README.md).

What is needed before it can start, none of which has happened:

1. A coordinator who is not the maintainer and does not code cases.
2. Four to six independent, credentialed practitioners, with signed conflict-of-interest declarations.
3. A decision on ethics review and on the dataset license.
4. Selected cases, written and checked narratives, and a completed pilot.
5. The protocol lodged with a public registry.

Also drafted and unreviewed: two concept-level crosswalks, People to published warning-behavior and pathway concepts and Facilities to PACT ([docs/crosswalks/](docs/crosswalks/README.md)). Also done: a flat per-object export.

No organization other than the maintainer is known to use the vocabulary.

### Step 4. Governance

**Status: drafted. All seats other than the maintainer are vacant.**

[GOVERNANCE.md](GOVERNANCE.md) and [MAINTAINERS.md](MAINTAINERS.md) set out roles, the decision process, the release and immutability rules, succession, funding disclosure, and the decision gate below. Today there is no second maintainer, no reviewer, no review board, no continuity contact, and no funder. Private vulnerability reporting has to be enabled in the repository settings for SECURITY.md to work as written.

A neutral steward is considered only after outside adoption exists. None exists.

## The decision gate

Twelve months after the first release under the current scope, the maintainer, with the review board if one exists, publishes a written decision to continue, change course, or stop. The conditions are those in [GOVERNANCE.md](GOVERNANCE.md) section 10, which is the authority if the two documents ever differ.

**Continue requires all of:**

- at least one outside reviewer, second maintainer, or pilot adopter recruited within six months of that release;
- the presence-coding study staffed with independent practitioners, and either completed with a result that meets its own continue condition or under way under a registered protocol;
- a patron, grant, or sponsoring organization secured, or a second maintainer or seated review board sharing the curation work, by month twelve;
- the blocking technical findings from the most recent audit closed within 90 days of that release;
- no legal review has concluded that the People matrix cannot be used in an employment setting even without scores.

**Stop, and archive under GOVERNANCE.md section 7, if any of:**

- no external reviewer, second maintainer, or pilot adopter has been recruited within six months of that release;
- the presence-coding study shows agreement below its stated threshold after its one permitted rework, or cannot be staffed with independent practitioners;
- by month twelve there is no patron, grant, or sponsoring organization and curation still rests on one person;
- an incumbent has occupied the position first: an established open physical-security matrix has extended into behavioral indicators, a platform vendor has published its own open behavior vocabulary, or a revised professional standard specifies one;
- a legal review concludes the People matrix cannot be used in an employment setting even without scores;
- the blocking technical findings remain open at 90 days.

**What would reopen the questions of scoring and the word "standard"** (all of): a published reliability study by independent, credentialed practitioners covering band assignment and not only presence, meeting a threshold fixed in advance; a standalone scoring specification with a normative formula, rounding rule, and test vectors; a written legal review of the People matrix; and at least one outside organization depending on a pinned release, with a second maintainer able to cut a release. Until then the overlay stays experimental and non-normative.

Status today: none of the conditions is met, none has failed, and the clock has not started.

## Not planned now

- **No new matrices.**
- **No new scoring layers.** The consequence layer once planned as V1.8 is withdrawn. No scoring work is planned beyond keeping the experimental overlay internally consistent.
- **No further schema major** until 3.0.0 is released.
- **No platform work.** An MCP server, SDKs, embeddings, a case library, and a change feed appeared in earlier roadmaps. None is scheduled.
- **No steward application** until there is outside adoption.

## Later work, not scheduled

If the gate is passed, the likely next items are: typing the `mitigates` edges and authoring them for the People matrix; filling the `correlates_with` gaps; citation locators; exercising deprecation and supersession on a real object; and bringing the draft matrices to core or removing what cannot be supported.
