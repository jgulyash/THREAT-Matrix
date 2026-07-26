# THREAT Matrix — Development Roadmap
 
**Current Version:** V1.5 (Organizations — 159 tactics across four matrices)
**Product:** THREAT Matrix
 
---
 
## Version Summary
 
| Version | Scope | Tactics | Status |
|---------|-------|---------|--------|
| **V1** | Person matrix taxonomy | 34 | Shipped |
| **V1.1** | Standard contract + Person D&R + AI-native foundations | — | Shipped |
| **V1.2** | Phase Lens UI + assessment guidance + escalation scoring | — | Shipped |
| **V1.3** | Facility matrix complete + escalation scoring on the full People matrix | 40 | Shipped |
| **V1.4** | Infrastructure matrix complete + cross-domain Detection Mesh (People–Facility–Infrastructure) | 37 | Shipped |
| **V1.5** | Organizations matrix complete + `informs_axes` matrix-wide + full cross-domain Detection Mesh (indicator, countermeasure, stakeholder links) | 48 | Shipped |
| **V1.6** | Contract Hardening — full JSON Schema closure (pre-platform gate) | — | Next |
| **V1.7** | Consequence Layer — target-impact scoring (`risk = threat × vulnerability × consequence`) | — | Planned |
| **V2** | Platform release — MCP server, SDKs, ingestion contract, RAG embeddings, custom domain, change feed | — | Planned |
| **V3** | Case Library | — | Planned |
| **V4** | AI Integration & Vector Embeddings | — | Planned |
| **V5** | Continuous Learning Loop | — | Future |
 
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
**Status:** Shipped
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
- Response protocols for all 34 Person tactics (stakeholder-assigned actions with escalation triggers, co-activation coordination links (`coordinates_with`), and legal/compliance notes)
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
**Status:** Shipped
 
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
**Status:** Shipped
 
**Delivers:**
- Complete Facility matrix taxonomy (~40 tactics)
- Full V1.1 schema applied to every Facility tactic: indicators, countermeasures, response protocols, field_notes, observed_contexts, evidence_basis, source_refs, Detection Mesh links
- Cross-matrix links populated where Facility tactics interact with Person tactics
 
**Why minor not major:** schema and framework lockdown completed in V1.1. Remaining matrix authoring is mechanical with AI assistance and warrants minor versions for shipping cadence.
 
---
 
## V1.4 — THREAT/Infrastructure Matrix Complete
**Status:** Shipped

**Delivers:**
- Complete Infrastructure matrix taxonomy (37 tactics) — control systems, OT/ICS, and critical service delivery
- Full schema applied to every Infrastructure tactic: indicators, countermeasures, response protocols, escalation scoring, `field_notes`, `observed_contexts`, `evidence_basis`, and Detection Mesh links
- Cross-domain Detection Mesh woven across People, Facility, and Infrastructure (112 inter-rater-validated cross-matrix indicator edges) — closes the "zero cross-matrix links" gap for the three shipped matrices
- Per-indicator cyber-physical facets (`crossing` + `human_social`) replacing the earlier tactic-level CPN flag; CPN computed over the mesh rather than stored
- Rendering fixes (1.4.1): heat-map column alignment and the Aftermath evade/claim track split

---

## V1.5 — THREAT/Organization Matrix Complete
**Status:** Shipped

**Delivers:**
- Complete Organization matrix taxonomy (48 tactics) — attacks on an institution's function, legitimacy, governance, and what it does or represents, distinct from its people, facilities, or systems
- Full schema applied to every Organization tactic: 240 indicators, 192 countermeasures, 96 response protocols, per-tactic assessment guidance, and escalation scoring
- `informs_axes` completed matrix-wide — all 815 indicators across all four matrices now carry the six-axis resolution signal, authored per matrix through sealed-blind inter-rater reliability (weighted κ ≥ 0.60)
- Full cross-domain Detection Mesh: 176 cross-matrix indicator edges, 291 cross-matrix countermeasure-compensation links, and 182 cross-matrix stakeholder-coordination links — all five mesh axes now deliver
- Organizations promoted from stub to live in the browser; four live matrices

---

## V1.6 — Contract Hardening
**Status:** Next

**Theme:** Close the JSON Schema so external consumers can trust the contract against malformed input. The content surface is complete across all four matrices as of V1.5; V1.6 hardens the boundary. This is the deliberate pre-platform gate — the V2 platform (MCP server, SDKs, embeddings) is built on a frozen, fully-typed schema, so the schema must stop churning first.

**Delivers:**
- Object-level `additionalProperties: false` on every schema definition (root-level closure already shipped in 1.4.x)
- Complete field typing for the currently loose fields (actor-profile fields, the `escalation_rubric` block, the `ai_architecture`/`warden` objects)
- Structural constraints: `required`, `minItems`, `uniqueItems` where the contract implies them
- Closes the invalid-input mutations the reference validator flags but the schema still tolerates
- Bundled schema-bump housekeeping: retire the legacy tactic-level `cpn` flag in favor of the per-indicator facets, and author the CPN facets for Organizations

**Schema bump:** the first `schema_version` change since 1.1.0 — a breaking bump, since `additionalProperties: false` rejects previously-tolerated input.

---
 
## V1.7 — Consequence Layer
**Status:** Planned

**Theme:** The third scoring layer. Where the taxonomy names a behavior (Layer 1) and escalation scoring weighs the threat it signals (Layer 2), the Consequence Layer scores target impact — the harm realized if an operation succeeds. It completes the operational risk model: `risk = threat × vulnerability × consequence`.

**Delivers:**
- Outcome-class taxonomy — a framework-defined vocabulary of consequence classes, authored per matrix and never inherited across matrices
- Consequence rubric — the structured method for characterizing an outcome's severity, parallel to the escalation rubric
- Instance-conditioning pattern — the framework defines the classes and rubric at the type level; specific target-value records live consumer-side, so the framework stays type-level and consumers hold their own case data

**Sequencing:** developable in parallel (spec-first, person-matrix outcome classes as the pilot). Additive to the hardened schema; the V2 platform surfaces it additively as it lands.

---

## V2 — Platform Release / AI Consumption Layer
**Status:** Planned (after V1.6 schema freeze)
 
**Front of V2 (the adoption-critical layer):**
- **MCP server** — AI agents query the framework natively over the Model Context Protocol; a transport layer over a pinned released `framework.json`, additive as matrices already shipped. Its one precondition is the V1.6 schema freeze.
- **Ingestion contract** — the minimal observation schema (source, timestamp, subject, behavior, evidence pointer) that defines what an observation must look like to be mappable to an indicator; makes every "how do I integrate" conversation concrete.
- **Python SDK / TypeScript SDK** — thin wrappers around schema-validated `framework.json` fetch.
- **Pre-built vector embeddings** for RAG against framework content (tactics, indicators, countermeasures, field_notes).

**Rest of V2:**
- Custom domain with a versioned URL pattern
- Webhooks / change feed for dependent tools to subscribe to framework updates
- Countermeasure severity / criticality / effectiveness ratings (research problem; "minimum CM set to reduce risk by X%")
 
**Strategic position:** V1.1 established the standard (contract, schema, reference consumer); V1.3–V1.5 filled the content surface across all four matrices; V1.6 freezes and hardens the schema. V2 ships the platform that turns the standard into an ecosystem — MCP server and SDKs for native AI-agent and application access, an ingestion contract that makes integration concrete, pre-built RAG embeddings, and a change feed. The standard is defended from V1.1 forward; V2 is the amplifier, gated only on the V1.6 freeze.
 
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
 
**The defender mirror to the adversary taxonomy ships with each matrix release.** There is no separate companion version. Each matrix (V1 Person, V1.3 Facility, V1.4 Infrastructure, V1.5 Organization) delivers its own slice of the Detection & Response Guide alongside the taxonomy itself.
 
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
 
**Tactic families:** 41 families enable cross-matrix grouping. Stable identifiers — not renamed after framework.json build. Powers Operations composer in V2+.
 
**Technique content:** The `techniques` layer was retired in V1.3 (removed from data, schema, and types) after the type-versus-instance review determined tactics are the terminal taxonomy level for this framework. Case-varying method detail belongs to the instance-conditioning layer, not a type-level techniques array.
 
---
 
*THREAT Matrix is an open-standard, shared vocabulary for the physical-threat domain. Canonical artifact under a published contract, MIT licensed, consumer ecosystem welcome. Value compounds with adoption.*