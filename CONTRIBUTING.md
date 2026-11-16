# Contributing to the THREAT Matrix

The THREAT Matrix is an open behavioral vocabulary and evidence index for threat assessment and protective work. It improves when people who know the subject point out what is missing, wrong, unclear, or poorly sourced. You do not need to write code to help.

Read these first:

- [docs/METHODOLOGY.md](docs/METHODOLOGY.md), starting with its limitations and intended-use section.
- [GOVERNANCE.md](GOVERNANCE.md), for how decisions are made. There is one maintainer and no outside reviewer today.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- [SECURITY.md](SECURITY.md), for anything that must be reported privately.

## Two rules that apply to everything

### 1. Public sources only

Every behavioral claim in the vocabulary must rest on a public source that a reader can obtain: a published report, standard, court document, after-action review, peer-reviewed paper, book, or reputable news investigation. Give a locator (page, paragraph, or section) where you can.

Unpublished experience, private casework, and uncited assertion are not accepted as sources. If your experience tells you something is missing, that is a good reason to open an issue; the entry that results still has to cite a public source that describes the behavior.

Do not include numbers such as "70 percent of cases involve X" unless you cite the study they come from.

### 2. No real case data and no personal information

Never post, in an issue, pull request, discussion, commit message, or file:

- details of a real incident that are not already in published public sources;
- the name or identifying details of any person, including people of concern, victims, witnesses, employees, and investigators;
- anything about an open or recent investigation;
- confidential material belonging to an employer or client.

Use a fictionalized example, or cite a published public source. Do not use project spaces to assess or speculate about any individual.

Public issues are indexed and effectively permanent. If personal or case information has been posted, or if you need to report a vulnerability or misuse of the vocabulary against individuals, use the private route in [SECURITY.md](SECURITY.md). Do not open a public issue with the details.

## How to propose a change

### Open an issue first

Use the template that fits. Blank issues are disabled.

| Template | Use it for |
|---|---|
| New Tactic Suggestion | A category of behavior that the vocabulary does not cover |
| Framework Issue | Something wrong or unclear in existing content: wording, scope, a tactic in the wrong phase, a citation that does not support its entry, a broken link |
| Use Case Proposal | How the vocabulary would be used, or where it falls short, illustrated with a fictionalized or public-source example only |

A useful suggestion for a tactic or indicator includes:

- a short name that says what is being done, not what a defender fears;
- the matrix (People, Facilities, Organizations, Infrastructure) and the phase (Target Development, Mobilization, Execution, Aftermath);
- two to four sentences describing the behavior as something observable;
- at least one public source, with a locator.

The People and Facilities matrices are the core. Organizations and Infrastructure are drafts. Reports that a draft entry describes lawful or protected activity, or that a citation does not support its entry, are especially useful.

### Then, if agreed, a pull request

1. Fork the repository and create a branch with a descriptive name.
2. Make the change. Keep each commit to one logical change.
3. Run the gates (below).
4. Open a pull request against `main`. Say what the change does and why, and link the issue. For a content change, explain the reasoning, not only the diff.

For a new indicator, follow the steps in [GOVERNANCE.md](GOVERNANCE.md) section 5. In particular:

- Write an observable behavior, not a trait, diagnosis, belief, or protected characteristic. One behavior per indicator.
- Do not assign an identifier. The maintainer allocates the next unused one at merge. Identifiers are never reused or renumbered ([docs/IDENTIFIERS.md](docs/IDENTIFIERS.md)).
- Do not add scores. The vocabulary carries none, and a new indicator enters without any entry in the experimental scoring overlay.
- Do not change what an existing identifier means. A change of meaning is a deprecation or supersession under [docs/DEPRECATION.md](docs/DEPRECATION.md).
- Follow the writing rules in [docs/VOICE.md](docs/VOICE.md).

### What review to expect

The maintainer reviews every change. While no outside reviewer has been recruited, a content pull request stays open for at least seven days for public comment, and the merge note says that no outside review was obtained ([GOVERNANCE.md](GOVERNANCE.md) section 3). The maintainer merges or declines with reasons. Accepted contributions are credited in the change record if you wish.

A change that would need a gate relaxed, or that removes or renames a field, is a breaking change and follows [GOVERNANCE.md](GOVERNANCE.md) section 4 and [docs/VERSIONING.md](docs/VERSIONING.md).

## The relations, defined

If you add or correct links between objects, use these meanings. Coverage of each relation today is described in [docs/METHODOLOGY.md](docs/METHODOLOGY.md#3-relations-between-objects).

| Field | On | Holds | Meaning |
|---|---|---|---|
| `correlates_with` | indicator | indicator identifiers | The two behaviors tend to occur together. Stored in both directions: if A lists B, B must list A. |
| `mitigates` | countermeasure | edge objects `{"indicator": "<indicator id>", "function": "<value>"}` | The countermeasure acts on that behavior. `function` is `prevent`, `detect`, `deny`, or `unreviewed`. |
| `compensates_for` | countermeasure | countermeasure identifiers only | This countermeasure covers for the absence or failure of that one. An indicator identifier here is an error. |
| `coordinates_with` | response protocol | response protocol identifiers | The two protocols are activated together or in a set order. |

Notes:

- Indicator coverage belongs in `mitigates`, never in `compensates_for`. Before schema 3.0.0 the two were mixed in one field.
- Every existing `mitigates` edge has the function `unreviewed`. If you propose a typed function for an edge, cite the source that supports it.
- A link is worth adding when the two objects are concretely related: the same act, one shared resource, or one documented handoff. Topical similarity is not enough. Two to four links per object is typical.
- No link may point to its own object or repeat. Every identifier must resolve. The gates check both.

## The gates

Run these from the repository root before opening a pull request. They need Python 3 and the `jsonschema` package (`pip install jsonschema`); without it the validator fails, because schema validation is a required part of every run. Continuous integration runs every one of them on every push and pull request.

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

The fixture harness takes about 20 seconds. What each gate checks, and what none of them checks, is in [docs/METHODOLOGY.md](docs/METHODOLOGY.md#5-review-process-and-gates). Passing the gates shows that a change is well formed. It does not show that the content is right. That is what review is for.

The manifest gate as continuous integration and the hook run it, with the published baseline:

```
python3 scripts/lint/id-manifest.py --check docs/data/framework.json docs/data/id-manifest.json --baseline docs/data/baselines/id-manifest-1.7.0.json
```

Do not edit or remove `docs/data/baselines/id-manifest-1.7.0.json`. It is the record of the identifiers in the published 1.7.0 release, and the hook fails without it.

If your change adds an identifier, the ID manifest has to be regenerated, or the manifest gate fails:

```
python3 scripts/lint/id-manifest.py --write docs/data/id-manifest.json --previous docs/data/id-manifest.json
```

### The local hook

`scripts/git-hooks/pre-commit` is opt-in: enable it once with `git config core.hooksPath scripts/git-hooks`. It acts when a staged path is under `docs/data/`, `src/`, `scripts/`, `examples/`, `docs/assets/`, or `.github/workflows/`, or is `index.html`, `docs/index.html`, `package.json`, `bun.lock`, `vite.config.ts`, or a `tsconfig` file. It exports the staged content to a temporary directory and checks that copy, never the working tree. It requires the `jsonschema` package and stops with a message if it is not installed; nothing is skipped for lack of it. It runs: `validate.py` on the framework, on the framework with the overlay, and on the scored worked cases; `field-parity.py`; `mesh-refs.py`; `id-manifest.py --check` with two baselines, the committed published baseline `docs/data/baselines/id-manifest-1.7.0.json` and the manifest in the previous commit; `derive-axis-confidence.py --check`; and `consumer-smoke.py`. It runs the `validate.py` fixture harness only when a file under `scripts/lint/` or a `docs/data/*.schema.json` file is staged. If a viewer build input is staged (anything under `src/`, `index.html`, `package.json`, `bun.lock`, `vite.config.ts`, a `tsconfig` file, or a `docs/data` file the viewer imports), it requires a rebuilt bundle to be staged as well (a new or changed file under `docs/assets/` and `docs/index.html`). On every commit it checks, it confirms that the staged `docs/index.html` references exactly the files in the staged `docs/assets/`. It does not run the viewer build, and for a change to a workflow file it runs the data gates but cannot judge the workflow itself. It can be bypassed with `git commit --no-verify`.

Bypassing the hook only defers the failure: continuous integration runs the same gates and cannot be bypassed locally.

### Continuous integration

Three workflows run on every push and every pull request for `main`, `v1-build`, and `v3-design`: *Framework Validator* (every gate above, with the ID manifest compared against the committed published baseline `docs/data/baselines/id-manifest-1.7.0.json` and against the previous manifest, plus the axis-confidence check), *Mesh Refs*, and *Bundle Freshness* (the committed viewer must equal a fresh build of the committed sources).

### If you change a schema

Open an issue first: any schema change changes the schema version ([docs/VERSIONING.md](docs/VERSIONING.md)). The validator pins a digest of each schema file's constraints in `SCHEMA_PINS` in `scripts/lint/validate.py`. If you change a required list, an enum, a pattern, or any other constraint in a `docs/data/*.schema.json` file, the schema checks fail until you update `SCHEMA_PINS` in the same commit. Print the current digests with:

```
python3 scripts/lint/validate.py --print-schema-pins
```

Copy the printed values into `SCHEMA_PINS`. A change to `description` text alone does not change a digest. The point of the pin is that a constraint cannot be loosened without the change being visible in review, so say in the pull request which constraint changed and why.

## Code contributions

The viewer is a React application built with Vite. Source is in `src/`. The build writes hashed files to `docs/assets/` and `docs/index.html`, and it bundles `docs/data/framework.json`, so a change to the data or the source needs a rebuild. Build with Bun 1.3.9, the version continuous integration uses:

```
rm -f docs/assets/index-*
bun run build
git add -A docs/assets docs/index.html
```

Welcome:

- bug fixes, accessibility improvements, and performance work in the viewer;
- improvements to the scripts and their tests;
- other consumers of the data (list yours in the README's Consumers section).

Open an issue before starting on:

- any schema change;
- a redesign of the viewer. Its visual identity is deliberate; the palette study is at `design/palette-comparison.html`.

The viewer shows no score unless the reader switches the experimental overlay on. Changes must keep it that way.

## What is not being accepted now

See [ROADMAP.md](ROADMAP.md). In short: no new matrices, no new scoring layers, and no further schema major until 3.0.0 is released. Proposals that the scoring overlay be treated as part of the vocabulary, or that the project call itself a standard, are deferred to the conditions in [GOVERNANCE.md](GOVERNANCE.md) section 10.

## Responsible content

Pull requests must not contain operational instructions, exploit code, weapon construction, or step-by-step attack tradecraft. The vocabulary describes behavior at the tactic and indicator level: what is observable, when, and what relates to it. It does not describe how to carry out an attack.

Examples that refer to real events must stay within what the cited public record states. Do not name living persons. If you are unsure whether something fits, open an issue describing it in general terms before submitting it.

## Writing rules for content

1. **Name the behavior.** "Physical Surveillance", not "Surveillance Threat".
2. **Plain function over jargon.** A reader should understand a name without looking it up.
3. **Observable, not inferred.** Describe what can be seen or recorded, not a state of mind.
4. **Cited.** Every entry answers "where does this come from?" with a public source.
5. **No invented metrics.**
6. **Say what else it could be.** Many of these behaviors have ordinary explanations. False-positive context is part of the entry, not an afterthought.
7. **Phase by behavior.** If a behavior spans phases, say so in `phase_relevance`, which must include the parent tactic's phase.

## Schema design principles

The vocabulary describes classes of behavior. It holds nothing about any case. Before proposing a field, apply this test:

> Could two competent users, looking at the same world on the same day, legitimately disagree about this field's value for the same indicator or tactic?
>
> - **No.** The value is a property of the class. It may belong in the vocabulary.
> - **Yes.** The value depends on a particular case, organization, or judgment. It belongs in the user's own records, not here.
> - **Sometimes.** Split it: publish the stable part, and describe the case-dependent part as something users record themselves.

`temporal_signature` passes: where a class of behavior typically sits relative to action is a property of the class. The likelihood that a particular person will act fails: it depends entirely on the case, and the vocabulary does not estimate it.

## License

By contributing, you agree that your contribution is licensed under the MIT License (see [LICENSE](LICENSE)), that you have the right to submit it, and that it contains no confidential or personal case information.
