DRAFT, not posted

This file is a draft of the release announcement. It has not been posted anywhere, and the 30-day notice period has not started. The two dates below are placeholders, written in capitals between square brackets, and must be filled in before anything is posted. Nothing in this draft is in effect.

---

# Announcement: THREAT Matrix schema 3.0.0 and content 2.0.0

Announced: [PLACEHOLDER: DATE OF ANNOUNCEMENT]. Earliest release tag: [PLACEHOLDER: DATE OF ANNOUNCEMENT PLUS 30 DAYS].

## What is changing, and why

The THREAT Matrix is changing what it says it is.

**It is an open behavioral vocabulary and evidence index for threat assessment and protective work.** It gives named, identified descriptions of observable behavior, organized by target and phase, each tied to public sources. That is what the People and Facilities matrices can support today.

**Scoring is demoted to an experimental overlay.** Until now every indicator in the main file carried authored axis values, a computed weight, and a band, and the project described those as a priority signal. They were one author's estimates. They have not been validated against outcomes or checked by independent reviewers. From this release the main file carries no scores at all. The values move to a separate, opt-in file that is labelled experimental, non-normative, and unvalidated, and is outside the stability promise. The default case record, the worksheet, and the viewer are score-free.

**The word "standard" is withdrawn.** Earlier documents called the project an open standard. It has one maintainer, no outside reviewer, and no known outside adopter. It is an open vocabulary. The question can be reopened only on the conditions in GOVERNANCE.md.

**Two matrices are labelled draft.** People and Facilities are the core. Organizations and Infrastructure are drafts: thinner, less well sourced, and likely to change. Some Organizations entries describe conduct that can be lawful, protected activity, and must never be treated as an indicator of threat without independent evidence of unlawful or violent intent.

**A limitations and intended-use statement now opens the README and the methodology.** In short: this is not a risk assessment instrument, not predictive, not validated against outcomes, not a score of any person, not grounds by itself for adverse action, not a substitute for individualized assessment by qualified professionals, and not legal advice. No reliability study has been run; a protocol for one is drafted.

## What breaks

Schema 3.0.0 is a MAJOR release. A document that validates against schema 2.1.0 does not validate against 3.0.0. The published 1.7.0 document produces 1,596 schema errors against it. The breaking changes:

1. **Scores leave the vocabulary.** The five indicator score fields, the per-tactic priority, the rubric, and the case-level scoring rules move to `docs/data/scoring-overlay.json` under new names.
2. **`compensates_for` is split.** It now holds countermeasure identifiers only. Indicator targets move to a new `mitigates` relation. Every `mitigates` edge is currently untyped (`unreviewed`).
3. **`evidence_basis` values are renamed.** `operational_primary` becomes `practice_led`, `hybrid` becomes `practice_and_literature`, `literature_primary` becomes `literature_led`. `literature_only` is unchanged.
4. **A lifecycle contract is added.** Objects can be deprecated or superseded under gated rules. Two reserved actor-profile identifiers appear as stubs. A committed ID manifest makes the no-reuse rule checkable.
5. **Each matrix must declare its maturity.**
6. **Patterns and enums are tightened.** Identifier grammar, bibliography keys, URLs (http and https only), DOIs, dates, and several enums. Four bibliography source types that described non-public sources are removed.
7. **The case record is split.** The default record is new and score-free. The old scored record continues only as an experimental format beside the overlay, with one field renamed.
8. **Root `operations` is removed,** along with one unused indicator field.

No identifier is renamed, renumbered, or removed.

## What to do

The migration guide lists every change with the reason, the remediation, and a before and after example: [docs/migration/2.1-to-3.0.md](./2.1-to-3.0.md).

A migration tool, `scripts/migrate/2.1-to-3.0.py`, performs the shape changes. It was tested on the published 1.7.0 document. It takes that document from 1,596 schema errors to 5, and lists the remaining work: 89 values that are content defects in the published document, each with a remediation. With those corrected, every gate passes. The tool does not review or validate content, and moving a score into the overlay does not validate it. The test is recorded in [docs/migration/3.0.0-validation-report.md](./3.0.0-validation-report.md).

## Timing

Under the versioning policy, the release tag will not be cut before [PLACEHOLDER: DATE OF ANNOUNCEMENT PLUS 30 DAYS]. Schema 2.1.0 with content 1.7.0 remains the published version on `main` until then.

Questions, corrections, and objections are welcome during the notice period, as issues in the repository. Do not include details of any real case or person. Report privacy or security problems through the private route in SECURITY.md.
