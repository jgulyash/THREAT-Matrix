# Contributing to the THREAT Matrix

The THREAT Matrix grows through practitioner contribution. You don't need to be a developer to make this framework better — most of the high-value contributions come from operators, analysts, and researchers who have seen adversary behavior firsthand and can name what's missing.

This document explains what kinds of contributions are useful, how to submit them, and what to expect after you do.

---

## Who should contribute

- **Protective intelligence analysts** — fixated individuals, approach behavior, surveillance detection
- **Insider threat practitioners** — grievance pathways, behavioral indicators, access misuse
- **Physical security operators** — facility infiltration, access control bypass, hostile reconnaissance
- **Threat intelligence analysts** — actor profiling, TTP attribution, source analysis
- **Researchers** — academic studies, after-action reviews, primary source documents
- **Software developers** — schema work, React SPA features, V1.3–V1.5 matrix tooling

Contributions from any of these backgrounds are welcome. Operational experience and source-backed claims carry the most weight.

---

## What to contribute

### 1. Suggest a new tactic

If you have observed (or have documented evidence of) adversary behavior that isn't represented in the framework, open an issue describing it. The framework is intentionally incomplete in V1 — V1.3–V1.5 add the Facilities, Organizations, and Infrastructure matrices, and even the People matrix has known gaps.

**Good tactic suggestions include:**
- A short, behavior-first name (what the adversary is *doing*, not what defenders are worried about)
- Which phase it belongs to (Target Development, Mobilization, Execution, Aftermath)
- Which target matrix it applies to (People, Facilities, Organizations, Infrastructure)
- 2–4 sentences describing the behavior in operational terms
- A reference: a public after-action review, court document, NTAC publication, peer-reviewed study, or first-person account
- (If applicable) Whether it has a Cyber-Physical Nexus dimension

**Use the issue template:** `New Tactic Suggestion`

### 2. Flag an inconsistency or error

If you spot something wrong — terminology drift, scope mismatch, an actor profile that doesn't fit its category, a tactic placed in the wrong phase, or a description that contradicts the source it cites — open an issue describing the problem and pointing to the specific record in `docs/data/framework.json`.

**Use the issue template:** `Framework Issue`

### 3. Propose a use case

Real-world scenarios validate the framework against operational reality. If you have a use case where the THREAT Matrix would have helped (or where it falls short), describe it. This is especially valuable for sectors that aren't yet well-represented: healthcare, education, transportation, critical infrastructure, public events.

Use cases that include actual or composite incidents (with appropriate redaction) are more useful than abstract ones. Use cases that surface gaps in the framework are more useful than ones that confirm it works.

**Use the issue template:** `Use Case Proposal`

### 4. Contribute a behavioral indicator

Detection indicators map observable behaviors to tactics. V1.1 populated all 34 People-matrix tactics with indicators (190 total); V1.3–V1.5 author indicators for the Facilities, Organizations, and Infrastructure matrices as those matrices land. If you have indicator content for a specific tactic, open an issue describing the behavior, its detection sources, and the source you're drawing from — peer-reviewed study, after-action review, NTAC publication, or first-person operational account. Indicator contributions go through editorial review the same way tactic contributions do; PRs are accepted only after the issue discussion has reached agreement on the indicator's scope and grounding.

### 5. Populate or extend Detection Mesh cross-references

The Detection Mesh weaves the framework's indicators, countermeasures, and response protocols into a single traversable graph across the four matrices and the four threat-lifecycle phases. Three fields carry the mesh:

- `correlates_with` on indicators — other indicator IDs that this indicator typically co-occurs with or precedes (cross-phase, cross-matrix, or within-tactic)
- `compensates_for` on countermeasures — other countermeasure IDs whose coverage gap this countermeasure addresses
- `coordinates_with` on response protocols — other response protocol IDs that fire in parallel on the same indicator set across stakeholder authorities

**What counts as a mesh link worth noting:**

- Same actor profile typically exhibits both behaviors (one operational thread)
- Observable handoff between two indicator types in field practice (e.g., grievance articulation → subject profiling)
- Defense-in-depth complementarity for countermeasures (one detects what the other prevents)
- Parallel-authority response coordination that's documented operationally (HR + Legal + Law Enforcement converging on the same case)

**What is NOT a mesh link:**

- "Vaguely related" or "topically similar" — the mesh is a precision instrument, not a tag soup
- Speculative correlations not grounded in field observation or documented case material

**Granularity.** 2–4 references per item is typical. More than 4 usually signals over-linking; consider whether the additional references are genuine or just topically adjacent.

**ID format.** `IND-XXXX-XX` (indicators), `CM-XXXX-XX` (countermeasures), `RP-XXXX-XX` (response protocols), where `XXXX` is the parent tactic's `TM` number and `XX` is the sequence within the tactic. The pre-commit hook validates that all mesh references resolve to existing IDs in `framework.json`; broken references block the commit. Hook source: `scripts/git-hooks/`.

### 6. Code contributions

The interactive browser is a React SPA built with Vite. Source lives in `src/`; the build emits hashed bundles to `docs/assets/`. Data lives in `docs/data/framework.json`. Build with `bun run build`. Requires Bun 1.3.9+ (`curl -fsSL https://bun.sh/install | bash` if not installed).

**Welcome code contributions:**
- Bug fixes in the SPA (rendering, navigation, routing)
- Accessibility improvements
- Performance work (the SPA loads ~140KB of JSON; this can be improved)
- New filter or view modes that don't conflict with the V2 roadmap (see [ROADMAP.md](ROADMAP.md))
- Schema additions discussed and approved in an issue first

**Hold on these for now:**
- New tactics or actor profiles via PR — open an issue first so the addition can be reviewed against the framework's editorial standards
- Major UI redesigns — the V1 visual identity (Amber Noir palette, IBM Plex Sans, the layout system) is intentional. See `docs/design/palette-comparison.html` for context.
- V1.3–V1.5 matrix work — these are scheduled and will be opened for contribution as each version begins

---

## Responsible content

Some kinds of content are intentionally out of scope. Pull requests must not contain operational instructions, exploit code, weapon construction, or step-by-step attack tradecraft. THREAT Matrix describes adversary behavior at the tactic and indicator level — what adversaries do, when in the threat lifecycle, in what patterns, and against what countermeasures and response protocols. It does not describe how to operationally execute attacks.

Case examples must reference public-record incidents only. Do not name living persons. For deceased perpetrators in publicly adjudicated cases, stay within court-record and news-record facts; treat the source material with restraint.

If you're unsure whether content fits, open an issue describing what you have in mind before submitting a PR.

---

## Build hygiene — pre-commit hook setup

THREAT Matrix's SPA bundles `docs/data/framework.json` into the JavaScript at build time (Vite). Edits to `framework.json` only reach the live viewer when the bundle is rebuilt. To prevent shipping a stale bundle (the v1.1.1 regression), this repository ships a pre-commit hook that catches `framework.json` edits without a corresponding bundle rebuild.

**Install the hook once after cloning** (from repo root):

```bash
git config core.hooksPath scripts/git-hooks
```

The hook runs automatically on every `git commit`. If you stage `framework.json` without staging a `docs/assets/index-*.{js,css}` file, the commit is blocked with a clear message. To clear it, run:

```bash
rm -f docs/assets/index-*
bun run build
git add docs/assets/ docs/index.html
```

then re-run your commit.

**Bypass (avoid):** `git commit --no-verify` skips the local hook. The CI workflow (`.github/workflows/bundle-freshness.yml`) re-runs the same check on every PR to `main` and every push to `v1-build`, so bypassing locally only defers the failure. If CI fails on bundle freshness, the same rebuild-and-recommit sequence above is the fix.

---

## How to submit

### Issues

Open an issue at <https://github.com/jgulyash/THREAT-Matrix/issues>. Use the template that matches your contribution type. If none of the templates fit, use a blank issue and describe what you're suggesting.

Include sources where possible. "I read about this in a Department of Energy report" is fine — you don't have to track down the exact citation, but pointing to *something* makes the suggestion easier to evaluate.

### Pull requests

For code, schema, or documentation changes:

1. Fork the repository
2. Create a branch with a descriptive name (e.g., `fix-actor-filter-rendering`, `add-phase-1-keyboard-nav`)
3. Make your changes. Keep commits focused — one logical change per commit.
4. Submit a pull request against the `main` branch
5. In the PR description, explain *what* the change does and *why* it's needed. Link to the relevant issue if one exists.

For changes that touch `framework.json`, the PR description should explain the editorial reasoning behind the change, not just the data diff. The framework is opinionated — every record reflects deliberate decomposition choices.

---

## What to expect

This is a practitioner-led project maintained by [Jay Gulyash](https://www.linkedin.com/in/jay-gulyash-750489207). Response time on issues and PRs is typically a few days, sometimes longer during operational periods.

**You will get:**
- A response that engages seriously with what you submitted
- A clear yes/no/needs-more-discussion on whether the change goes in
- Credit in commit messages or release notes for accepted contributions

**You will not get:**
- A merge of every well-intentioned PR — the framework's value depends on editorial consistency
- A debate about the framework's positioning relative to MITRE ATT&CK (the relationship is documented in the README; please read it before opening that thread)
- Acceptance of fabricated metrics, AI-generated boilerplate, or content not grounded in real sources

---

## Editorial standards

If you're contributing tactics, profiles, or descriptions, the following principles apply:

1. **Behavior-first naming.** Tactic names describe what the adversary is *doing*, not what defenders are *worried about*. "Physical Surveillance" not "Surveillance Threat." "Identity Fabrication" not "Identity Risk."
2. **Function over jargon.** A name that an analyst can read and immediately understand beats a name that requires the reader to look it up.
3. **Source-backed claims.** Every tactic and actor profile should be defensible against a reviewer who asks "where did this come from?" Public sources are preferred. Operator experience is valid but should be flagged as such.
4. **No fabricated metrics.** Don't include numbers like "70% of attacks involve X" unless you can cite the study. Made-up percentages destroy credibility.
5. **Phase placement reflects behavioral logic, not convention.** If a behavior spans phases, document that. If it's ambiguous, discuss it before placing it.

---

## Schema design principles

THREAT Matrix is a type system for the physical-threat domain — a dictionary of stable, named descriptions of tactic classes, indicator classes, countermeasure types, response protocol types, and actor profile archetypes. Downstream consumers (RAG systems, AI agents, threat-management platforms like WARDEN) cite these definitions as the vocabulary for what they're observing, but the actual evidence, scoring, and decisions about specific threats live in the consumer's own data store, not in the framework.

Before proposing a new field for `framework.schema.json`, apply this test:

> **Could two competent consumers, observing the same world on the same day, legitimately disagree on this field's value for the same indicator/tactic — without either being wrong?**
>
> - **No** → dictionary-level. The value is a property of the *type*, not the consumer's read of the world. Goes in THREAT Matrix.
> - **Yes** → consumer-level. The value depends on a specific assessment, telemetry, posture, or judgment that varies legitimately across consumers and across time. Goes in WARDEN / downstream.
> - **Sometimes** → split it. There's almost certainly a stable type-property hiding inside an unstable case-property; expose the type-property and document the consumer-property as a recommended downstream pattern.

Examples:

- `temporal_signature` (whether an indicator typically signals horizon / advancing / imminent / etc.) → **dictionary**. The temporal positioning is a property of the indicator class.
- `realization_probability` (how likely a specific threat is to land in 30 days) → **consumer**. Depends entirely on the consumer's telemetry and intel.
- `escalation_weight` and its constituent `escalation_axes` → **dictionary** for the type-level potentials (impact, blast radius, recoverability, detectability of the indicator class); **consumer** for the case-level realizations (impact at *my* facility, *my* response time).

If you're proposing a field that fails this test, the right home is documentation of a recommended downstream pattern — not the schema.

---

## Code of conduct

Be civil. Critique ideas, not people. If a contribution gets rejected, it's a judgment about the contribution, not the contributor — try again with a different angle, or ask what would make it acceptable.

This framework exists to give practitioners a shared vocabulary. That goal only works if the project stays serious, source-backed, and free of bad-faith participation. Disagreement is welcome. Bullshit is not.

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License (see [LICENSE](LICENSE)). The THREAT Matrix is an open reference standard. Its value compounds with adoption.
