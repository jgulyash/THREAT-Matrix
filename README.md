# THREAT Matrix
 
*Tactical Human Risk Enumeration and Adversary Taxonomy Matrix*
 
**An open-standard, shared vocabulary for the physical-threat domain. Built for the analysts, investigators, field teams, and engineers across corporate security, law enforcement, and the Intelligence Community — and for the leaders who rely on their work, and the educators and researchers shaping the discipline. Drawn from 15+ years of experience leading high-stakes threat investigations with more than 70 domestic and international partners.**

The physical threat domain lacks a shared, standardized vocabulary. The THREAT Matrix is built to be that standard. Four matrices, 154 tactics, 27 actor profiles spanning seven threat categories, accompanied by Detection Mesh and Response options. Structured from V1 to function as headless-first machine-consumable threat signal library for RAG systems, AI agents, and downstream detection and investigation tooling. Shipped with a UI and reference consumer that demonstrates the contract end-to-end.  
 
**[→ Launch THREAT Matrix in Browser](https://jgulyash.github.io/THREAT-Matrix/)** · **[framework.json](docs/data/framework.json)** · **[JSON Schema](docs/data/framework.schema.json)** · **[Reference consumer](examples/python_consumer.py)** · MIT License
 
![THREAT Matrix V1 — Person Matrix browser](docs/images/v1-spa-screenshot.png)
 
![THREAT Matrix V1 — Tactic detail with actor associations](docs/images/v1-spa-tactic-detail.png)
 
---
 
## The Problem
 
The same pattern surfaced in most partner relationship: each organization had its own vocabulary for physical threat behavior. Some had mature processes and detection methodology. Others had not yet identified advesary tactics, techniques, or behavior that recurred across cases the field had been seeing for years. There was no shared language, no common reference standard, wasted time syncing incidents across teams, and no shared framework to build tooling against a stable taxonomy.
 
In 2023, a Lawrence Livermore National Laboratory study, sponsored by DOE/NNSA and prepared for DHS/CISA examined whether any existing methodology could serve as a structured framework for characterizing physical adversary action across critical infrastructure sectors. The conclusion: existing frameworks are inadequate. Most are sector- or facility-specific, focus on security assessment rather than adversary behavior, and fail to address cyber-physical risks. The THREAT Matrix is a direct response to both the documented institutional gap and the operational reality that produced it.
> McGrath, J.K., Scott, H.R., & Slone, L.R. (2023). *Requirements and Recommendations
> for a Physical Attack Characterization Framework* (LLNL-TR-858139). Lawrence Livermore
> National Laboratory. https://doi.org/10.2172/2229613
 
## Framework Architecture
 
**Four target matrices. A four-phase Threat Lifecycle. 154 total tactics** (34 live in V1; 120 across V1.3–V1.5 planned).
 
### Threat Lifecycle
 
![THREAT Matrix Threat Lifecycle](docs/images/threat-lifecycle-diagram.svg)
 
The Threat Lifecycle is descriptive, not prescriptive — adversaries compress, skip, and reorder phases based on opportunity and capability. The framework makes behavioral patterns visible; it doesn't assert they are inevitable or sequential. Detection and response operate as a Detection Mesh across the lifecycle (see below), not as a linear chain.
 
### Target Matrices
 
![THREAT Matrix Target Matrices](docs/images/matrix-overview.svg)
 
### Actor Profiles
 
**27 actor profiles across 7 threat categories.** Each profile documents awareness, direction, access relationship, phase compression risk, attack vectors, behavioral markers, AI capability amplifiers, and the tactics each actor type is most likely to employ.
 
| Category | Profiles | Examples |
|----------|---------:|----------|
| Lone Actor | 3 | Fixated individuals, public-figure stalkers, grievance-driven attackers |
| Insider | 5 | Malicious, negligent, and compromised insiders (coerced, recruited, unwitting) |
| Criminal | 7 | Organized crime, kidnap-for-ransom, contract violence |
| Corporate Espionage | 2 | Trade secret theft, competitive intelligence operations |
| Ideological | 4 | Domestic violent extremism, terrorism, mass-casualty actors |
| Nation-State | 4 | Foreign intelligence services, state-directed disruption |
| Customer / Client Aggressor | 2 | Workplace violence escalation from customer or client relationships |
 
Profiles are referenced by stable ID (`AP001`–`AP029`) and connect directly to the tactics each actor type is most likely to employ. Browse them in the [interactive matrix](https://jgulyash.github.io/THREAT-Matrix/#/actors).
 
### Cyber-Physical Nexus (CPN)
 
Cyber capabilities enable and accelerate physical operations across virtually every phase for sophisticated actors. The `[CPN]` tag marks tactics where digital capabilities play a significant or primary enabling role — showing practitioners where to look for digital indicators alongside physical behaviors.
 
### Detection Mesh
 
THREAT Matrix treats detection and response as a mesh, not a chain. Indicators from any phase, any matrix, and any detection domain can correlate with indicators from anywhere else in the framework. Countermeasures from any domain can compensate for gaps in another. Response protocols from any stakeholder — threat management teams, HR, legal, law enforcement, protective operations, EAP — fire in parallel on the same indicator set, each acting within their own authority.
 
The mesh is machine-walkable. Three graph link fields make it traversable by AI agents, correlation engines, and coverage-gap analysis tools:
 
| Field | Lives on | Purpose |
|---|---|---|
| `correlates_with` | Indicators | Cross-phase, cross-matrix indicator correlation |
| `compensates_for` | Countermeasures | Coverage-gap analysis across countermeasure domains |
| `coordinates_with` | Response Protocols | Parallel-execution links across stakeholder authorities |
 
Full architectural rationale is in the `detection_mesh` block in `docs/data/framework.json`.
 
### Cross-Framework Interoperability
 
THREAT Matrix's four-phase Threat Lifecycle is cross-walked to established adversary threat frameworks via the `phase_mappings` block in `docs/data/framework.json`
 
A query against THREAT Matrix Phase 2 (Mobilization) can retrieve documents tagged to the other frameworks mapped phase because the mapping is machine-readable. THREAT Matrix is the physical-adversary lane. Other frameworks address the cyber-adversary and AI-systems-adversarial lanes, while others cover aspects of an insider threat adversary. The frameworks meet at the cross-walk; they do not compete.
 
### AI Integration Architecture
 
The THREAT Matrix treats AI as a **force multiplier on existing attack vectors** — not a separate pathway. AI compresses Phase 1 timelines, lowers tradecraft requirements, and extends capabilities previously requiring nation-state resources to less sophisticated actors.
 
**Four-vector taxonomy:**
 
| Vector | Definition |
|--------|-----------|
| `physical_primary` | Physical action; no meaningful cyber or AI component |
| `cyber_enabled_physical` | Cyber tools support or enable a physical attack |
| `cyber_initiated_physical` | A cyber attack IS the attack; physical harm is the consequence |
| `ai_initiated_physical` | An autonomous or semi-autonomous AI system executes physical harm without real-time human direction |
 
The `ai_initiated_physical` vector is architecturally distinct: the attack does not route through networked cyberspace — the AI agent operates locally, autonomously, in physical space. Current documented examples include AI-directed autonomous drones and compromised autonomous vehicle systems. Every actor profile carries an `ai_enabled_risks` field documenting which AI capability amplifiers apply. Full AI architecture rationale is in the `ai_architecture` block in `docs/data/framework.json`.
 
---
 
## Standard Contract
 
V1.1 establishes THREAT Matrix as a headless-first open standard. The contract has four properties:
 
| Property | Where it lives |
|---|---|
| **Canonical artifact** | [`docs/data/framework.json`](docs/data/framework.json) — single source of truth. The SPA is one consumer of this file, not its primary expression. |
| **Formal schema** | [`docs/data/framework.schema.json`](docs/data/framework.schema.json) — JSON Schema (draft 2020-12) that every consumer validates against. |
| **Versioning + stability policy** | Semver applied independently to the framework artifact (`version`) and the schema (`schema_version`) — see [VERSIONING.md](VERSIONING.md). Stable identifier contract (`TA####`, `AP###`, `IND-*`, `CM-*`, `RP-*`) defined in [IDENTIFIERS.md](IDENTIFIERS.md) — IDs are never reused, even after deprecation. Lifecycle states and sunset rules in [DEPRECATION.md](DEPRECATION.md). |
| **Multiple independent consumers** | The React SPA at jgulyash.github.io/THREAT-Matrix; the reference Python consumer at [`examples/python_consumer.py`](examples/python_consumer.py) (with [`examples/README.md`](examples/README.md) as a starting-point guide); community consumers welcome. |
 
Standards talk to platforms. The contract is what makes integrations with RAG systems, AI agents, MCP-based tooling, and downstream security platforms tractable rather than bespoke.
 
---
 
## Build Status
 
| Version | Scope | Status |
|---|---|---|
| **V1** | Person matrix taxonomy (34 tactics) | Shipped |
| **V1.1** | Standard contract (JSON Schema, versioning policy, stable IDs, reference consumer) + Person Detection & Response + AI-native foundations (`phase_mappings`, `detection_mesh`, `evidence_basis`) | In Progress |
| **V1.2** | Phase Lens UI + assessment guidance | In Progress |
| **V1.3** | Facility matrix complete (~40 tactics) | In Progress |
| **V1.4** | Organization matrix complete (~42 tactics) | In Progress |
| **V1.5** | Infrastructure matrix complete (~38 tactics) | In Progress |
| **V2** | Platform release: custom domain, Python and TypeScript SDKs, MCP server, RAG embeddings, change feed | Planned |
| **V3** | Real-world case library | Planned |
| **V4** | AI integration and vector embeddings | Planned |
| **V5** | Continuous learning loop | Future |
 
*Each matrix release (V1.3–V1.5) ships its own Detection & Response slice — behavioral indicators, response protocols, and countermeasures mapped to every tactic — building practitioner-ready operational guidance alongside the taxonomy. Full roadmap: [`ROADMAP.md`](ROADMAP.md).*
 
---
 
## Using the Framework
 
**Browse it:** [jgulyash.github.io/THREAT-Matrix](https://jgulyash.github.io/THREAT-Matrix/) — filter by phase, CPN tag, or actor profile. Click any tactic for full detail including notes, CPN analysis, AI risk factors, and Detection Mesh links.
 
**Build with it:** `docs/data/framework.json` is MIT licensed, semver versioned, schema-validated, and machine-readable. Validate against [`framework.schema.json`](docs/data/framework.schema.json), then use the framework in detection tooling, threat-assessment workflows, training platforms, RAG pipelines, or agentic systems.
 
### Consumers
 
The SPA is one consumer of the standard. Other consumers shipped or planned:
 
- **[Reference Python consumer](examples/python_consumer.py)** — minimal worked example: fetch, validate, filter by phase, look up actor profiles by ID. Build your own from it.
- **MCP server** — AI agents query the framework natively over Model Context Protocol (planned, V2).
- **Python and TypeScript SDKs** — thin wrappers over schema-validated fetch (planned, V2).
- **Pre-built RAG embeddings** — tactics, indicators, countermeasures, field_notes embedded for semantic retrieval (planned, V2).
- **Community consumers** — visualizations, integrations, ingestion pipelines welcome. Submit a link via issue and yours gets listed here.
 
---
 
## Contributing
 
The THREAT Matrix grows through practitioner contribution. You don't need to be a developer.
 
- **Suggest a tactic** — open an issue describing an adversary behavior not yet in the framework
- **Flag an inconsistency** — terminology, scope, or classification issues
- **Propose a use case** — real-world scenarios help validate the framework against operational reality
- - **Developer contributions** — schema work, React SPA features, V1.3–V1.5 matrix tooling, alternative consumers (CLIs, language SDKs, MCP integrations, visualizations)
 
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
 
---
 
## License
 
MIT. Open standard for physical adversary behavior. Value compounds with adoption.
 
---
 
## Acknowledgments and Notices
 
THREAT Matrix is grounded in decades of field investigations, public news articles and case files, and published threat-assessment research from NTAC, FBI, CISA, ODNI/NITTF, LLNL, SEI/CERT, ASIS International, and peer-reviewed scholarship by Fein, Vossekuil, Meloy, Gill, White, Calhoun, and Weston. Full citations live in [`docs/data/framework.json`](docs/data/framework.json) under `bibliography`. Source license notices, prior-art positioning, and trademark statements: [`NOTICES.md`](NOTICES.md).
