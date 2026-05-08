# THREAT Matrix — Development Roadmap
 
**Current Version:** V1 (THREAT/Person — 34 tactics)
**Product:** THREAT Matrix
 
---
 
## Version Summary
 
| Version | Scope | Tactics | Status |
|---------|-------|---------|--------|
| **V1** | Person matrix taxonomy | 34 | Shipped |
| **V1.1** | Standard contract + Person D&R + AI-native foundations | — | In Progress |
| **V1.2** | Phase Lens UI + assessment guidance | — | In Progress |
| **V1.3** | Facility matrix complete | 40 | In Progress |
| **V1.4** | Organization matrix complete | 42 | In Progress |
| **V1.5** | Infrastructure matrix complete | 38 | In Progress |
| **V2** | Headless build / AI consumption layer | — | Planned |
| **V3** | Case Library | — | Planned |
| **V4** | AI Integration & Vector Embeddings | — | Planned |
| **V5** | Continuous Learning Loop| — | Future |
 
**Each minor (V1.3–V1.5) ships a complete matrix.** Each release includes the full behavioral indicators, countermeasures, response protocols, evidence_basis declarations, and Detection Mesh links for that matrix's tactics. Operational guidance is built into every matrix release alongside the taxonomy.
 
**Roadmap revision (2026-04-27):** two changes.
 
(1) **Category reframe.** V1.1 is now positioned as the release that promotes THREAT Matrix from a framework to an open standard. The standard contract — formal JSON Schema, versioning policy, stable identifier guarantees, reference consumer — ships in V1.1 alongside the Person Detection & Response slice and the AI-native architecture additions.
 
(2) **Matrix cadence compression.** The original V2/V3/V4 path (Facility/Organization/Infrastructure as separate majors) was compressed to V1.3/V1.4/V1.5 (matrix-per-minor). V2 was reassigned to the platform release that turns the standard into an ecosystem (MCP server, SDKs, custom domain, pre-built embeddings, change feed). Rationale: schema lockdown completed in V1.1; remaining matrix authoring is mechanical with AI assistance and warrants human-in-the-loop review; V2 concentrates the platform infrastructure into one focused release on top of the V1.1 contract.
---
 
## V1 — THREAT/Person
**Tactic ID Range:** TA01xx–TA04xx (34 tactics)
**Target:** Specific individual (targeted violence, stalking, kidnapping, assassination)
 
**Delivered:**
- Complete tactic schema across all 4 phases
- 27 actor profiles across 7 categories
- Phase 4 bifurcation (EVADE track / CLAIM track)
- Operational Feedback Loop cycle (Phase 4 AAR → Phase 1 Target Development)
- AI architecture metadata block (`ai_architecture` at framework.json root)
- AI capability modifier (`ai_enabled_risks`) on all 21 actor profiles
- 4 attack vectors including `ai_initiated_physical`
- Matrix browser with phase / CPN / actor profile filters
- GitHub Pages deployment from `docs/`
 
**Source coverage at launch:** 80%+ (PACER federal indictments; Secret Service NTAC series; FBI BAU publications)
 
---
 
## V1.1 — Standard Contract + Person D&R + AI-Native Foundations
**Status:** In Progress
**Theme:** Promote THREAT Matrix from framework to open standard. V1.1 publishes the contract — formal JSON Schema, versioning policy, stable identifier guarantees — and ships the first non-SPA reference consumer that proves the contract works end-to-end. The Person Detection & Response slice and the AI-native architecture additions ship under that contract.
 
**Delivers (standard contract):**
- Formal JSON Schema published at `docs/data/framework.schema.json`
- Versioning + breaking-change policy — semver applied to framework artifact and schema independently; stable identifier contract (`TA####`, `AP###`, `IND-*`, `CM-*`, `RP-*`); deprecation discipline
- Reference consumer at `examples/python_consumer.py` — minimal non-SPA artifact that fetches `framework.json`, validates against the schema, and demonstrates filtering by phase and actor profile lookup
- `examples/README.md` — "minimum viable consumer; build your own"
- Consumers section in `README.md` — SPA, and community consumers listed as peers
 
**Delivers (Person Detection & Response):**
- Behavioral indicators for all 34 Person tactics (observable behaviors with detection sources, phase relevance, mesh links, and source citations)
- Countermeasures for all 34 Person tactics (actionable measures with cost, complexity, time-to-implement, phase relevance, and limitations)
- Response protocols for all 34 Person tactics (stakeholder-assigned actions with escalation triggers, parallel-execution coordination links, and legal/compliance notes)
- Three mandatory practitioner-grounding fields per tactic: `field_notes`, `observed_contexts`, `evidence_basis`
- TM0103 Environmental Survey pilot fully authored as the canonical exemplar
- GitHub issue templates for community contribution (New Tactic Suggestion, Framework Issue, Use Case Proposal)
 
**Delivers (AI-native architecture):**
- `bibliography` central citation library with 13 source types including operational experience (`field_observation`, `practitioner_elicitation`, `partner_attestation`, `case_composite`)
- Tier 1 source system that includes attested operational experience as first-class evidence
- `phase_mappings` top-level cross-walk to NTAC, Calhoun-Weston, CERT, and Cyber Kill Chain stages — enables AI/RAG cross-framework interoperability natively
- `detection_mesh` top-level architectural object documenting the cross-cutting Detection Mesh property along five axes (cross-phase, cross-matrix, cross-domain, cross-countermeasure, cross-stakeholder)
- Detection Mesh graph links: `correlates_with` on indicators, `compensates_for` on countermeasures, `coordinates_with` on response protocols
- `evidence_basis` enum on every tactic — machine-queryable provenance (`operational_primary`, `hybrid`, `literature_primary`, `literature_only`)
- `schema_version` field — stable contract tracking for downstream consumers
- Headless-first architectural commitment with formal JSON Schema published at `docs/data/framework.schema.json`
- VOICE.md authoring guidelines codifying four locked voice rules
 
**Why V1.1 ships separately from V2:**
The contract has to be in writing before the platform is built on top of it. Schemas, versioning policy, and the reference consumer are V1.1 because every V2 platform deliverable (SDKs, MCP server, vector embeddings, webhooks, custom domain) assumes them. Shipping the contract first lets contributors build their own consumers now instead of waiting for the SDKs, and removes the "show me a consumer that isn't your SPA" question from every conversation about the project for the next six months.
 
**Out of scope for V1.1:**
- New tactics, actor profiles, or matrix content (V1.3+)
- SDKs, hosted API endpoints, MCP server, embeddings, change feed (V2 platform release)
- Phase Lens UI, assessment guidance (V1.2)
 
**Schema bumps:** framework `1.0.0` → `1.1.0`; `schema_version` introduced at `1.1.0`.
 
---
 
## V1.2 — Phase Lens UI + Assessment Guidance
**Status:** In Progress (after V1.1 content authoring completes)
 
**Delivers (UI experience):**
- Phase Mode UI as a peer to Tactic Mode — cross-tactic rollup of all indicators relevant to a chosen phase, across the entire framework
- Cross-phase indicator badges with clickable navigation back to parent tactic (e.g., `↳ prep for Response Suppression (Phase 3 · TM0305)`)
- Heat map cell layered count format: "9 tactics · 35 indicators" with hover-state evidence_basis split (e.g., "9 tactics · 35 indicators · 22 operational / 13 literature")
- Parent tactic page inverse callout — "this tactic's preparation indicators surface in earlier phases" notice for cross-phase indicators authored under this tactic
 
**Delivers (assessment guidance):**
- Per-tactic `assessment_guidance` with structured scoring dimensions (credibility, capability, intent, opportunity)
- High-signal and low-signal anchors per dimension for structured professional judgment
- Per-tactic false positive context (what benign behaviors look like for each tactic)
- Threshold guidance for escalation
- Escalation priority framework (Urgent, Immediate, Priority, Routine)
 
**Delivers (AI-grounding additions):**
- `temporal_signature` enum on indicators — separate axis from `phase_relevance`, captures temporal proximity to action (`horizon`, `advancing`, `imminent`, `staging`, `in_progress`, `aftermath`)
- `escalation_weight` on indicators — AI prioritization and alert scoring support
 
**Design principle:** The scoring rubric is a framework practitioners apply to their specific case, not a pre-computed score. No fabricated confidence numbers. Structured professional judgment with defined dimensions and anchored signal levels.
 
---
 
## V1.3 — THREAT/Facility Matrix Complete
**Status:** In Progress (after V1.2 ships)
 
**Delivers:**
- Complete Facility matrix taxonomy (~40 tactics)
- Full V1.1 schema applied to every Facility tactic: indicators, countermeasures, response protocols, field_notes, observed_contexts, evidence_basis, source_refs, Detection Mesh links
- Cross-matrix links populated where Facility tactics interact with Person tactics
 
**Why minor not major:** schema and framework lockdown completed in V1.1. Remaining matrix authoring is mechanical with AI assistance and warrants minor versions for shipping cadence.
 
---
 
## V1.4 — THREAT/Organization Matrix Complete
**Status:** In Progress (after V1.3 ships)
 
**Delivers:**
- Complete Organization matrix taxonomy (~42 tactics)
- Full V1.1 schema applied to every Organization tactic
- Cross-matrix links populated where Organization tactics interact with Person and Facility tactics
- Insider actor profiles deepened
 
---
 
## V1.5 — THREAT/Infrastructure Matrix Complete
**Status:** In Progress (after V1.4 ships)
 
**Delivers:**
- Complete Infrastructure matrix taxonomy (~38 tactics)
- Full V1.1 schema applied to every Infrastructure tactic
- Cross-matrix links across all four matrices populated
- Infrastructure -domain CPN editorial review (cyber-physical nexus at infrastructure scale)
- Operations / scenario composer foundations
 
**Source coverage at launch:** 50–60% (power/water/pipeline deep; dam/telecom stubs)
- NERC reliability reports
- EPA Water Security Initiative
- NTSB transportation security database
- Metcalf sniper attack analysis
- ICS-CERT advisory database
 
---
 
## V2 — Headless Build / AI Consumption Layer
**Status:** Planned (after V1.5 content-complete state)
 
**Delivers:**
- Custom domain (e.g., `threatmatrix.dev`) with versioned URL pattern (`/api/v1/`, `/api/v2/`)
- Python SDK (thin wrapper around schema-validated framework.json fetch)
- TypeScript SDK (same)
- MCP server — AI agents query the framework natively over the Model Context Protocol
- Pre-built vector embeddings for RAG against framework content (tactics, indicators, countermeasures, field_notes)
- Webhooks / change feed for dependent tools to subscribe to framework updates
- Countermeasure severity / criticality / effectiveness ratings (research problem; "minimum CM set to reduce risk by X%")
 
**Strategic position:** V1.1 establishes the standard (contract, schema, reference consumer). V1.3–V1.5 fill out the content surface across all four matrices under that contract. V2 ships the platform that turns the standard into an ecosystem — versioned API endpoints, language SDKs, MCP server for native AI-agent access, pre-built RAG embeddings, and a change feed for dependent tools to subscribe against. The standard is fully defended from V1.1 forward; V2 is the amplifier, not a precondition.
 
---
 
## V3 — Case Library
**Status:** Planned (after V2 Headless Build)
 
**Delivers:**
- Real-World Case Library — executed and thwarted incidents mapped to tactics, profiles, and Detection Mesh links
- Operations / scenario composer matured to V5 capability level
 
---
 
## V4 — AI Integration & Vector Embeddings
**Status:** Planned (after V3 Real-World Case Library establishes the training data layer)
 
**Purpose:** Enable AI agents and frontier models to reason over the THREAT Matrix taxonomy for automated incident identification, tactic mapping, and case support.
 
**Planned capabilities:**
- Vector embeddings of all tactic descriptions, indicators, and actor profiles as canonical anchor points in embedding space
- Semantic search API: incoming case data (reports, tips, incident descriptions) mapped to nearest THREAT Matrix tactics via embedding similarity
- AI-assisted tactic mapping: frontier model suggests tactic classifications from unstructured incident narratives, practitioner confirms or corrects
- Embedding-optimized parallel text fields on each tactic (standardized for retrieval, alongside human-readable descriptions)
 
**Architectural position — taxonomy vs. vector databases:**
The THREAT Matrix is the canonical ontology. Vector databases are a retrieval mechanism that indexes the ontology. They are complementary, not competitive. The taxonomy defines what the categories ARE. Embeddings provide fuzzy matching to map real-world observations to those categories. Structured reasoning (Threat Lifecycle phase, actor profile, response protocol, escalation logic) requires the taxonomy. Cosine similarity alone cannot drive an escalation decision.
 
**Integration with case management:**
The THREAT Matrix is designed to plug into existing and future AI-native case management platforms, not to replace them. The market has capable case management products that will continue to evolve with AI capabilities. The framework provides the structured physical-threat behavior taxonomy that case management tools can consume. Any open-source or SaaS physical threat platform demonstrates this integration model: The SaaS handles case operations, THREAT Matrix provides the TTP classification layer.
 
---

## V5 — Continuous Learning Loop
**Status:** Planned (after V3 Case Library)
 
**Delivers:**
- Continuous learning pipeline — AI integration for incident-feedback loop
- Advanced AI-grounding fields based on what the AI pipeline learns it needs
 
**Purpose:** Close the feedback loop between AI-assisted case identification and the taxonomy itself.
 
**Planned capabilities:**
- Practitioner correction feedback: when an AI agent maps an incident to a tactic and the practitioner corrects the mapping, the correction feeds back into the embedding model
- Taxonomy evolution recommendations: AI identifies patterns in correction data that suggest new tactics, tactic refinements, or indicator additions
- Automated source monitoring: AI agents scan new government reports, academic publications, and after-action reviews for content that validates or challenges existing tactic definitions
- Cross-organization learning (privacy-preserving): anonymized pattern data shared across participating organizations to improve detection without exposing case details
 
**Design constraint:** The human practitioner remains the authority. AI agents recommend, practitioners decide. The taxonomy is authored by practitioners, validated by sources, and refined through operational feedback. AI accelerates the cycle but does not replace the editorial judgment.

---
 
## Detection & Response Guide — Per-Matrix Delivery
 
**The defender mirror to the adversary taxonomy ships with each matrix release.** There is no separate companion version. Each matrix (V1 Person, V2 Facility, V3 Organization, V4 Infrastructure) delivers its own slice of the Detection & Response Guide alongside the taxonomy itself.
 
**Per-matrix deliverables (each version):**
- Detection methodology for every tactic in that matrix
- Investigative response protocols
- Intervention strategy
- Post-incident investigation workflow
- Behavioral indicators populated (observable → tactic → phase reverse lookup)
- Countermeasures populated with full schema: cost / time / complexity / limitations
- Defender overlay view for the matrix (adversary view ↔ defender view toggle)
 
**Why per-matrix instead of a single companion release:** Practitioners working a Person-matrix case shouldn't have to wait until V4 ships to get detection guidance. Each release is operationally complete on its own — taxonomy plus detection plus response plus countermeasures — for the domain it covers.
 
**Governing principle:** Defender activity lives in the Detection & Response slice, not in the adversary taxonomy. CPN tags and indicator anchors in the tactic schema are the bridge between the two.
 
---
 
## Cross-Version Architecture Notes
 
**Navigation axes:**
- Axis 1 (V1): Matrix-primary — browse by matrix, phase, actor profile, CPN
- Axis 2 (V2): Operations-primary — build and analyze multi-phase, cross-matrix adversary operations
 
**WARDEN integration:** Reserved in V1 schema at zero build cost. V3 activation: WARDEN alert schema maps to THREAT taxonomy via agentic ingestion pipeline. Both tools more powerful together.
 
**Tactic families:** 56 families enable cross-matrix grouping. Stable identifiers — not renamed after framework.json build. Powers Operations composer in V2+.
 
**Technique content:** V1 ships with `techniques: []` on all 34 Person tactics. V1.3 delivers full technique decomposition for Person. Each subsequent matrix version (V2 Facility, V3 Organization, V4 Infrastructure) delivers its own techniques alongside the taxonomy. Person is the reference implementation — fully complete before V2 begins.
 
---
 
*THREAT Matrix is an open-standard, shared vocabulary for the physical-threat domain. Canonical artifact under a published contract, MIT licensed, consumer ecosystem welcome. Value compounds with adoption.*