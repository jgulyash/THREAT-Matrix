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
- **Software developers** — schema work, React SPA features, V2–V4 matrix tooling

Contributions from any of these backgrounds are welcome. Operational experience and source-backed claims carry the most weight.

---

## What to contribute

### 1. Suggest a new tactic

If you have observed (or have documented evidence of) adversary behavior that isn't represented in the framework, open an issue describing it. The framework is intentionally incomplete in V1 — V2-V4 add the Facility, Organization, and System matrices, and even the Person matrix has known gaps.

**Good tactic suggestions include:**
- A short, behavior-first name (what the adversary is *doing*, not what defenders are worried about)
- Which phase it belongs to (Target Development, Mobilization, Execution, Aftermath)
- Which target matrix it applies to (Person, Facility, Organization, System)
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

### 4. Contribute a behavioral indicator (V3+)

Detection indicators map observable behaviors to tactics. V1 ships with `indicators: []` arrays as placeholders — these populate in V3 alongside the Organization matrix. If you have indicator content for V1 Person tactics, open an issue. Don't submit a pull request to populate them yet — the schema for indicator records is still being designed.

### 5. Code contributions

The interactive browser at `docs/index.html` is a single-file React SPA loaded via CDN (no build step). The data model lives in `docs/data/framework.json`.

**Welcome code contributions:**
- Bug fixes in the SPA (rendering, navigation, routing)
- Accessibility improvements
- Performance work (the SPA loads ~140KB of JSON; this can be improved)
- New filter or view modes that don't conflict with the V2 roadmap (see [ROADMAP.md](ROADMAP.md))
- Schema additions discussed and approved in an issue first

**Hold on these for now:**
- New tactics or actor profiles via PR — open an issue first so the addition can be reviewed against the framework's editorial standards
- Major UI redesigns — the V1 visual identity (Amber Noir palette, IBM Plex Sans, the layout system) is intentional. See `docs/design/palette-comparison.html` for context.
- V2–V4 matrix work — these are scheduled and will be opened for contribution as each version begins

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

## Code of conduct

Be civil. Critique ideas, not people. If a contribution gets rejected, it's a judgment about the contribution, not the contributor — try again with a different angle, or ask what would make it acceptable.

This framework exists to give practitioners a shared vocabulary. That goal only works if the project stays serious, source-backed, and free of bad-faith participation. Disagreement is welcome. Bullshit is not.

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License (see [LICENSE](LICENSE)). The THREAT Matrix is an open reference standard. Its value compounds with adoption.
