# Governance

**Status: draft, single maintainer today.**

This document describes how the project is run now and how it intends to be run. Where it describes a role, board, funder, or relationship that does not yet exist, it says so. Nothing here should be read as a claim that any person or organization other than the maintainer has reviewed, adopted, funded, or endorsed the project.

## 1. Scope of the project

The THREAT Matrix is an **open behavioral vocabulary and evidence index for threat assessment**. It publishes named, identified descriptions of observable behaviors (indicators), grouped into tactics and matrices, each tied to public sources, with related countermeasures and response protocols.

- The **People** and **Facilities** matrices are the core. The **Organizations** and **Infrastructure** matrices are labelled draft.
- The **vocabulary** (`docs/data/framework.json` and its schema) carries no scores.
- The **experimental scoring overlay** (`docs/data/scoring-overlay.json`) is a separate, opt-in file. It is **non-normative**: type-level, unvalidated, not predictive, not a risk score, and not for use in any decision about a person. No governance decision treats the overlay as part of the vocabulary, and no release of the vocabulary depends on it.
- The project does not describe itself as a standard.
- The project does not assess, score, or hold data about any person, and does not accept case data about real people through any channel.

Changes to this scope are breaking changes to governance and follow section 4.

## 2. Roles

### 2.1 Maintainer

One today: the repository owner (see `MAINTAINERS.md`). The maintainer merges changes, cuts releases, enforces the lifecycle and versioning rules, answers security and privacy reports, and keeps this document accurate. While there is one maintainer, the maintainer is also the final decision-maker, and that concentration is the project's main structural weakness. Sections 2.3, 7, and 10 are the plan to reduce it.

### 2.2 Reviewers

**Vacant. To be recruited.** A reviewer is an outside practitioner or researcher who reads proposed content changes, crosswalk rows, or study materials and records an opinion in public on the pull request or issue. Reviewers have no merge rights. A reviewer's name is listed in `MAINTAINERS.md` only with their written consent, and listing means "has reviewed", not "endorses".

### 2.3 Review board

**Does not exist. To be recruited: three to five members.**

Purpose: to give content decisions a check that does not rest on one person. Once seated, the board reviews new and rewritten indicators in the core matrices, rules on disputed content changes, approves breaking changes, and takes part in the twelve-month decision gate.

Qualifications sought across the board (not every member needs all):

- current practice in behavioral threat assessment and management, protective intelligence, or security investigation, with a recognised professional credential or equivalent documented experience;
- research experience in violence risk, reliability studies, or measurement;
- legal experience in employment, privacy, or civil-liberties law as it bears on threat assessment;
- experience maintaining a published vocabulary, taxonomy, or data standard used by other parties.

Composition rules:

- no more than one member from any one employer;
- at least one member who works outside the United States, if one can be recruited;
- the maintainer is not a voting member.

Conflict-of-interest rule (applies to board members, reviewers, and the maintainer):

- each discloses in writing, published in `MAINTAINERS.md`, any employer or client that sells threat assessment software, instruments, training, or services; any financial interest in the project; and any authorship of content under review;
- a person does not vote on, or act as the deciding reviewer for, content they authored, content that benefits their employer's product, or a dispute to which they are a party;
- the disclosure is updated when circumstances change.

Until three members are seated, decisions that this document assigns to the board are made by the maintainer and are recorded as "maintainer decision, no board" in the change record.

## 3. Decision process for content changes

Content means tactics, indicators, countermeasures, response protocols, actor profiles, bibliography entries, and crosswalk rows.

1. **Proposal.** An issue or pull request states the change and why. It must not contain details of any real case or person beyond what a cited public source states.
2. **Public sources required.** Every new or changed behavioral claim cites at least one public source that states or shows the behavior, with a locator (page, paragraph, or section). The source goes in the bibliography. Unpublished experience, private casework, and uncited assertion are not accepted as sources.
3. **Checks.** The change passes every gate command the repository documents (schema, validator, fixtures, reference and manifest checks). A change that needs a gate relaxed is a breaking change.
4. **Review.** At least one reviewer other than the author records an opinion in public. While reviewer seats are vacant, the pull request stays open for at least seven days for public comment, and the merge note says no outside review was obtained.
5. **Lifecycle rules.** Identifiers are never reused or renumbered. An object is changed in meaning only by deprecating or superseding it under `docs/DEPRECATION.md`, never by silent edit. Wording changes that do not change meaning are recorded as such.
6. **Decision.** The maintainer merges or declines with reasons. A declined proposer may ask for board review once the board exists.
7. **Record.** The change is entered in `CHANGELOG.md` under the rules in `docs/VERSIONING.md`.

The scoring overlay follows the same steps, but an overlay change never blocks, justifies, or forces a vocabulary change.

## 4. Decision process for breaking changes

A breaking change is any change that can break a consumer pinned to a published release: removing or renaming a field, tightening the schema so previously valid documents fail, changing the meaning of an identifier, or changing a stated guarantee. `docs/VERSIONING.md` governs classification.

1. **Proposal** with a statement of who is affected and what they must do.
2. **Migration guide** written against the latest published release, not against a working branch, and **tested**: the guide's steps are run on the published document and the result must pass the new gates with zero errors. The test command and its output are attached to the proposal.
3. **Notice.** At least 30 days of public notice before the release, posted in the repository (release notes or a pinned issue) with the migration guide. The clock starts when the notice is public and the guide passes its test, not before.
4. **Approval** by the review board; while no board exists, by the maintainer, recorded as such.
5. **Release** under section 6. The previous major remains available.

No further schema major is planned until the current one is frozen and published.

## 5. How an outside author contributes an indicator, end to end

1. Read `CONTRIBUTING.md`, `docs/METHODOLOGY.md`, and `docs/VOICE.md`.
2. Open an issue describing the behavior in one sentence, the matrix and tactic it belongs to, and the public sources. Wait for a reply on fit and on overlap with existing indicators.
3. Draft the indicator: an observable behavior, not a trait, diagnosis, belief, or protected characteristic; one behavior per indicator; wording that a trained reader could code as present or absent from a written account.
4. Cite at least one public source with a locator and add it to the bibliography.
5. Fill the required fields from the schema. Do not assign an identifier; the maintainer allocates the next unused ID in the tactic at merge. Do not add scores; a new indicator enters the vocabulary without any overlay entry, and whether it later receives one is a separate overlay decision.
6. Run the gate commands locally and open a pull request.
7. Review under section 3. Expect wording changes for clarity and distinctness from neighbouring indicators.
8. On merge the indicator is `active`, the contributor is credited in the change record if they wish, and the ID manifest is updated at the next release.
9. The new indicator carries no reliability claim. If the presence-coding study in `docs/study/` runs, new indicators enter it in the next round.

Contributions are accepted under the repository's MIT license. Contributors confirm they have the right to submit the text and that it contains no confidential or personal case information.

## 6. Release process and immutability

- Releases are cut from the default branch by the maintainer after all gate commands pass in continuous integration.
- Each release is a tagged version with: the vocabulary file, its schema, the ID manifest, checksums for each published file, and a changelog entry.
- **Published releases are immutable.** A released file is never edited in place. A defect is fixed by a new release. A tag is never moved.
- Identifiers are never reused. Reserved and retired identifiers are recorded in the ID manifest.
- The overlay has its own version and its own release notes and states which vocabulary version it applies to.
- The viewer is a convenience. The data files in a tagged release are the reference.

Whether each of these is enforced by tooling today, and not only stated, is tracked in the repository's gate documentation; where a rule is stated here and not yet gated, that is a defect to be reported.

## 7. Succession and archival

If the maintainer stops (by choice, incapacity, or six months without response to issues or security reports):

1. **The last release stays available** under the MIT license. Nothing is withdrawn.
2. **The repository is archived read-only** with a notice at the top of the README giving the date, the last release, and a statement that the vocabulary is no longer maintained and should be used with that in mind.
3. **An invitation for a successor** is posted in the README and as a pinned issue before archiving, open for at least 90 days where the maintainer is able to do so.
4. **Criteria for handing over** the repository, name, and release rights. A successor (person or organization) must:
   - have documented practice in threat assessment, protective intelligence, or a closely related field, or be an organization that employs such practitioners;
   - accept this governance document, including the non-normative status of the overlay, the ban on personal data, and the immutability and no-reuse rules;
   - commit in writing to keep the vocabulary open under MIT or a license at least as permissive;
   - disclose funding and conflicts under sections 2.3 and 8;
   - not make use of the vocabulary conditional on buying a product or service.
5. If no successor meets the criteria, the archive stands. Anyone may fork under the license; a fork must use a different name and identifier namespace so that it is not mistaken for this project.

To make an unplanned stop survivable, the maintainer will name a **continuity contact** with repository administration rights whose only duty is to carry out steps 1 to 3. Status: **not yet named.**

## 8. Funding and independence

- **There is no funder today.** The project has received no grant, sponsorship, or payment, and has no commercial arrangement with any vendor, employer, or customer. Work is unpaid.
- If a patron, grant, or sponsor is accepted, it will be disclosed in this section and in the README within 30 days: who, how much or in what form, for what period, and any conditions attached.
- No funder receives a right to change content, block a release, see unpublished material early, or be described as having endorsed the vocabulary. Funders may contribute through the same public process as anyone else.
- Funding conditions that conflict with section 1 are declined.
- The maintainer's own employment and any related commercial interests are disclosed under the conflict-of-interest rule in section 2.3.

## 9. Steward path

**A neutral steward is sought only after outside adoption exists. None exists today, and no steward has been approached.**

Adoption evidence, stated neutrally: the project has no known outside adopter, no second participating organization, and no funder. The steward routes listed below, by their own published entry rules, ask for more than one participating organization or run a consensus process that needs committed participants. A project with one maintainer and no outside user does not meet those conditions, and joining a steward does not by itself produce users. So the order is: enforce the contract, build something others use (section 10), recruit a second organization, then consider a steward.

Options, with their published requirements. No contact with any of these bodies has occurred, and nothing here implies their interest or agreement.

| Option | Published requirement (as read on 2026-11-15) | Source | Fit |
|---|---|---|---|
| ASIS International guideline or standard proposal | ASIS develops standards and guidelines through its Professional Standards Board and technical committees under published procedures, with public review through ANSI for American National Standards. Who may submit a new project proposal, and the difference in process between a guideline and a standard, are **to be confirmed** against the current procedures and proposal template before any approach | https://www.asisonline.org/globalassets/standards-and-guidelines/asis-asd-procedures-8th-edition.pdf (200); https://www.asisonline.org/globalassets/asis-new-project-proposal-template-3.12.19-7.doc (200); https://www.asisonline.org/globalassets/standards-and-guidelines/documents/new-member-guide.pdf (200) | Domain-correct for physical security and workplace violence. The output would be an ASIS consensus document, so editorial control would pass to a committee |
| OASIS Open Project | Launch sponsorship threshold "determined by specific project needs", with each sponsor paying dues | https://www.oasis-open.org/?p=12271 (200) | Needs sponsoring organizations; none exists |
| OASIS Technical Committee | Five participants representing at least two OASIS member organizations | https://www.oasis-open.org/?p=12271 (200) | Needs two member organizations; none exists |
| OpenSSF project lifecycle (Linux Foundation) | Maintainer and organization counts rise by stage; scope is open source software security. Exact counts **to be confirmed** | https://github.com/ossf/tac/blob/main/process/project-lifecycle.md (200) | Out of scope for a physical-threat vocabulary; listed for completeness |
| Stay author-led | None | | Available now. Depends entirely on sections 2.3 and 7 being carried out |

Staying author-led with a working review board is a legitimate end state. A steward is one option, not the goal.

## 10. Twelve-month decision gate

Twelve months after the first release under this scope (the "pivot release"; date to be recorded here when it is tagged), the maintainer, with the review board if one exists, publishes a written decision to continue, change course, or stop, against the conditions below. The decision and the evidence for each condition are published in the repository.

**Continue** requires all of:

- at least one outside reviewer, second maintainer, or pilot adopter recruited within six months of the pivot release;
- the presence-coding study (`docs/study/`) staffed with independent raters and either completed with a result that meets its own continue condition, or under way under a registered protocol;
- a patron, grant, or sponsoring organization secured, or a second maintainer or seated review board sharing the curation work, by month twelve;
- the blocking technical findings from the most recent audit closed within 90 days of the pivot release;
- no legal review has concluded that the People matrix cannot be used in an employment setting even without scores.

**Stop** (archive under section 7) if any of:

- no external reviewer, second maintainer, or pilot adopter has been recruited within six months of the pivot release;
- the presence-coding study shows agreement below its stated threshold after its one permitted rework, or cannot be staffed with independent raters;
- by month twelve there is no patron, grant, or sponsoring organization and curation still rests on one person;
- an incumbent has occupied the position first: an established open physical-security matrix has extended into behavioral indicators, a platform vendor has published its own open behavior vocabulary, or a revised professional standard specifies one;
- a legal review concludes the People matrix cannot be used in an employment setting even without scores;
- the blocking technical findings remain open at 90 days.

**What would reopen the questions of scoring and the word "standard"** (all of): a published reliability study by independent, credentialed raters covering band assignment and not only presence, meeting a threshold fixed in advance; a standalone scoring specification with a normative formula, rounding rule, and test vectors; a written legal review of the People matrix; and at least one outside organization depending on a pinned release, with a second maintainer able to cut a release. Until then the overlay stays experimental and non-normative.

Status against these conditions today: none met; none yet failed; the clock has not started.

## 11. Code of conduct

Participants are expected to follow the Contributor Covenant, version 2.1 (https://www.contributor-covenant.org/version/2/1/code_of_conduct/). A `CODE_OF_CONDUCT.md` file adopting it, with a reporting contact, is **to be added** to the repository root; until then, conduct concerns go to the maintainer through the private channel described in `SECURITY.md`.

Two project-specific rules apply in every venue: do not post details of real cases or identifiable people, and do not use project spaces to assess or speculate about any individual.

## 12. Reporting a security or privacy problem

See `SECURITY.md` for how to report privately. Use it for: a vulnerability in the viewer or tooling; personal or case information that has appeared in the repository, an issue, or a dataset; a request from a person described in study material for correction or removal; and misuse of the vocabulary to score or act against individuals. Do not open a public issue for any of these.

## 13. Changing this document

Changes to sections 1, 4, 6, 7, 8, and 10 follow the breaking-change process in section 4, including 30 days of notice. Other changes follow section 3. The status line at the top is updated when a second maintainer, a reviewer, or a board member is seated.
