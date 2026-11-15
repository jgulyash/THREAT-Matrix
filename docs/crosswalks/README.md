# Crosswalks

**Status: DRAFT. Both crosswalks are concept-level and unreviewed. Neither has been checked or endorsed by the authors or publishers of the works they point to.**

## What a crosswalk is here

A crosswalk is a table that says which THREAT Matrix tactics describe behavior related to a concept or object in another published framework, how close the relationship is, and why. It is a finding aid. It lets someone who works in one framework locate related material in the other.

A crosswalk here is not:

- a claim that the two things are equivalent, or that one measures the other;
- a substitute for the other framework, its training, or its license;
- part of the vocabulary's normative content. Nothing in `docs/data/framework.json` depends on these files, and they can change without a vocabulary release.

## Files

| File | Maps | To | State |
|---|---|---|---|
| `people-warning-behaviors.md` and `.json` | 34 People tactics | Published warning-behavior names, pathway stage names, and US Secret Service NTAC investigative theme names | draft 0.1.0 |
| `facilities-pact.md` and `.json` | 40 Facilities tactics | PACT (Physical Access & Control Taxonomy) tactics and techniques, by ID and name | draft 0.1.0 |

The Markdown and JSON files in each pair carry the same table. If they disagree, treat it as a defect and report it.

## Rules these files follow

- **Names and identifiers only.** No licensed instrument's items, criteria, scoring, or wording is reproduced. No description text is copied from PACT. One-line glosses of concepts are this project's own paraphrase and are labelled as such.
- **Public sources, cited.** Each crosswalk lists its sources with a link and the result of a link check, or says there is no public link.
- **Confidence is stated.** Every row is `direct`, `partial`, or `none`, with a one-line reason. `none` rows are kept so gaps are visible.
- **Coverage both ways.** Each crosswalk lists what on the other side has no THREAT Matrix counterpart, and which tactics map to nothing.
- **No scores.** Crosswalks never reference the experimental scoring overlay.
- **Dated.** Each file records when it was checked against the vocabulary and, for PACT, the state of the PACT data that was read.

## Limits

- Each is one reader's judgment and has had no outside review.
- Mapping is at tactic level, with a short list of indicator-level links on the People side.
- The other frameworks change. A crosswalk is only as current as its "checked" date.
- A `direct` label means the described behavior is the same. It says nothing about validity or about how either framework should be used.

## How to propose a correction

1. Open an issue titled "Crosswalk correction: <file>". Do not include details of any real case or person.
2. Name the row (tactic ID and the concept or PACT ID), say what you think the mapping and confidence should be, and give a public source for the reading (author, year, title, and a link where one exists, with a page or section).
3. If you are an author or publisher of a cited work and want a row changed or removed, say so; that request is given priority.

Corrections are handled under the content-change process in `GOVERNANCE.md`. A change of confidence or a new row needs a public source. Accepted corrections are recorded in the file's change note and the crosswalk version is raised.

Reviewers with practitioner or research standing in threat assessment or physical security are wanted for both files. See `MAINTAINERS.md` for how to offer review.
