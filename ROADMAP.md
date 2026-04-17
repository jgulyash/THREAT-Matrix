# THREAT Matrix — Development Roadmap

**Current Version:** V1 (THREAT/Person — 34 tactics)
**Product:** THREAT Matrix

---

## Version Summary

| Version | Matrix | Tactics | Status |
|---------|--------|---------|--------|
| **V1** | Person | 34 | Shipped |
| **V1.1** | Person D&R | — | In Progress |
| **V1.2** | Person Assessment | — | Planned |
| **V1.3** | Person Techniques | — | Planned |
| **V2** | Facility | 40 | Planned |
| **V3** | Organization | 42 | Planned |
| **V4** | System | 38 | Planned |
| **V7** | AI Integration | — | Future |
| **V8+** | Continuous Learning | — | Future |

**Detection & Response Guide ships per matrix.** Each release (V1–V4) includes the behavioral indicators, response protocols, and countermeasures for that matrix's tactics. There is no separate V5 — the operational guidance is built into every matrix release alongside the taxonomy.

---

## V1 — THREAT/Person
**Tactic ID Range:** TA01xx–TA04xx (34 tactics)
**Target:** Specific individual (targeted violence, stalking, kidnapping, assassination)

**Delivered:**
- Complete tactic schema across all 4 phases
- 27 actor profiles across 7 categories
- Phase 4 bifurcation (FLIGHT track / CLAIM track)
- Operational Feedback Loop cycle (Phase 4 AAR → Phase 1 Target Development)
- AI architecture metadata block (`ai_architecture` at framework.json root)
- AI capability modifier (`ai_enabled_risks`) on all 21 actor profiles
- 4 attack vectors including `ai_initiated_physical`
- Matrix browser with phase / CPN / actor profile filters
- GitHub Pages deployment from `docs/`

**Source coverage at launch:** 80%+ (PACER federal indictments; Secret Service NTAC series; FBI BAU publications)

---

## V1.1 — Person Detection & Response Slice
**Status:** In Progress

**Delivers:**
- Behavioral indicators for all 34 Person tactics (observable behaviors with detection sources and source citations)
- Countermeasures for all 34 Person tactics (actionable measures with cost, complexity, time-to-implement, and limitations)
- Response protocols for all 34 Person tactics (stakeholder-assigned actions with escalation triggers and legal/compliance notes)
- Central bibliography with per-tactic source citations (addresses LLNL-TR-858139 Section 4.2 requirement: all data sources clearly cited and linked)
- GitHub issue templates for community contribution (New Tactic Suggestion, Framework Issue, Use Case Proposal)

**Schema additions:**
- `bibliography` — top-level citation library keyed by short reference IDs
- `source_refs` — per-tactic array referencing bibliography entries (minimum 3 per tactic)
- `response_protocols` — new per-tactic array (detect/prevent/respond as distinct practitioner workflows)
- `indicators` and `countermeasures` populated with structured objects

---

## V1.2 — Assessment Guidance & Scoring Rubric
**Status:** Planned (after V1.1 content authoring completes)

**Delivers:**
- Per-tactic `assessment_guidance` with structured scoring dimensions (credibility, capability, intent, opportunity)
- High-signal and low-signal anchors per dimension for structured professional judgment
- Per-tactic false positive context (what benign behaviors look like for each tactic)
- Threshold guidance for escalation (when indicator combinations warrant formal assessment, enhanced monitoring, or documentation only)
- Escalation priority framework (Urgent, Immediate, Priority, Routine) — organizations define their own timeframes within each priority tier

**Why V1.2 and not V1.1:** The raw behavioral data (indicators, countermeasures, response protocols) must exist before a scoring framework can reference it. V1.1 = detect and respond. V1.2 = assess and prioritize.

**Design principle:** The scoring rubric is a framework practitioners apply to their specific case, not a pre-computed score. No fabricated confidence numbers. Structured professional judgment with defined dimensions and anchored signal levels, consistent with TRAP-18 and WAVR-21 assessment methodology.

---

## V1.3 — Person Technique Decomposition
**Status:** Planned (after V1.2 assessment guidance completes)

**Delivers:**
- Technique decomposition for all 34 Person tactics (how the adversary executes each tactic, not just what they do)
- Sub-techniques where applicable (e.g., TA0103 Physical Surveillance → foot surveillance, mobile surveillance, static observation post)
- Procedure examples grounded in source-documented incidents
- Fully completes LLNL R7 requirement for Person matrix: "techniques, sub-techniques, and procedure examples beyond high-level tactics"

**Why V1.3 and not V2:** Completing the Person matrix before starting Facility means one matrix is the fully finished reference implementation: taxonomy + D&R + assessment guidance + techniques. Practitioners working Person-domain cases get the complete toolkit. V2 scope is cleaner (Facility only, not Facility + Person retrofit).

**Design note:** Technique authoring benefits from V1.1 indicator work — knowing which indicators detect a tactic reveals which techniques produce those indicators. The authoring sequence (indicators first → techniques second) is intentional.

---

## V2 — THREAT/Facility
**Tactic ID Range:** TA11xx–TA14xx (40 tactics)
**Target:** Physical location (active shooter, IED/VBIED, venue/campus attack, workplace violence at a site)

**New Schema:**
- Cross-matrix `related_tactics` fields populated — Person ↔ Facility links
- `partial_approach_rehearsal` cross-matrix link (Person/Facility/Org)
- `proxy_actor` AP022 — reserved in V1, implemented in V2

**New Capabilities:**
- Scenario pathway composer — build multi-phase adversary operation sequences
- Operations view — cross-matrix incident reconstruction
- Cross-matrix tactic navigation

**Source coverage at launch:** 70–80%
- NTAC Mass Attacks in Public Spaces series
- FBI Las Vegas After-Action Review
- Bataclan parliamentary inquiry
- RAND mass casualty event research

---

## V3 — THREAT/Organization
**Tactic ID Range:** TA21xx–TA24xx (42 tactics)
**Target:** Enterprise / trusted-access adversary (insider threat, corporate espionage, sabotage, fraud)

**New Schema:**
- Indicator content begins populating (observable behaviors mapped to tactics)
- Insider actor profiles deepened (grievance pathway, behavioral deterioration indicators)

**New Capabilities:**
- Agentic ingestion pipeline — WARDEN alerts → structured TTP assessment → THREAT taxonomy mapping
- WARDEN API integration point activated (`warden_integration` stub from V1 schema populated)
- Portfolio proof point: WARDEN + THREAT Matrix demonstrably more powerful together

**Source coverage at launch:** 30–40% (majority stubs)
- Federal indictments via PACER
- PERSEREC (Personnel Security Research Center) studies
- NTAC workplace violence series
- CERT Insider Threat research database

---

## V4 — THREAT/System
**Tactic ID Range:** TA31xx–TA34xx (38 tactics)
**Target:** Physical infrastructure (critical infrastructure sabotage, ICS/OT attack, pipeline/grid/water disruption)

**New Schema:**
- Operation objects populated (multi-phase, cross-matrix adversary operation sequences)
- System CPN editorial review — cyber-physical nexus at infrastructure scale
- Countermeasure content begins populating (field schema: cost, time, complexity, limitations)

**New Capabilities:**
- Full indicator reverse lookup: observable → tactic → phase
- Countermeasure design layer at infrastructure scale

**Source coverage at launch:** 50–60% (power/water/pipeline deep; dam/telecom stubs)
- NERC reliability reports
- EPA Water Security Initiative
- NTSB transportation security database
- Metcalf sniper attack analysis
- ICS-CERT advisory database

---

## Detection & Response Guide — Per-Matrix Delivery

**The defender mirror to the adversary taxonomy ships with each matrix release.** There is no separate companion version. Each matrix (V1 Person, V2 Facility, V3 Organization, V4 System) delivers its own slice of the Detection & Response Guide alongside the taxonomy itself.

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

**Technique content:** V1 ships with `techniques: []` on all 34 Person tactics. V1.3 delivers full technique decomposition for Person. Each subsequent matrix version (V2 Facility, V3 Organization, V4 System) delivers its own techniques alongside the taxonomy. Person is the reference implementation — fully complete before V2 begins.

---

## V7 — AI Integration & Vector Embeddings
**Status:** Future (after V6 Real-World Case Library establishes the training data layer)

**Purpose:** Enable AI agents and frontier models to reason over the THREAT Matrix taxonomy for automated incident identification, tactic mapping, and case support.

**Planned capabilities:**
- Vector embeddings of all tactic descriptions, indicators, and actor profiles as canonical anchor points in embedding space
- Semantic search API: incoming case data (reports, tips, incident descriptions) mapped to nearest THREAT Matrix tactics via embedding similarity
- AI-assisted tactic mapping: frontier model suggests tactic classifications from unstructured incident narratives, practitioner confirms or corrects
- Embedding-optimized parallel text fields on each tactic (standardized for retrieval, alongside human-readable descriptions)

**Architectural position — taxonomy vs. vector databases:**
The THREAT Matrix is the canonical ontology. Vector databases are a retrieval mechanism that indexes the ontology. They are complementary, not competitive. The taxonomy defines what the categories ARE. Embeddings provide fuzzy matching to map real-world observations to those categories. Structured reasoning (kill chain phase, actor profile, response protocol, escalation logic) requires the taxonomy. Cosine similarity alone cannot drive an escalation decision.

**Integration with case management:**
The THREAT Matrix is designed to plug into existing and future AI-native case management platforms, not to replace them. The market has capable case management products that will continue to evolve with AI capabilities. The framework provides the structured adversary behavior taxonomy that case management tools can consume. The WARDEN framework (open-source personnel threat platform) is a parallel project that demonstrates this integration model: WARDEN handles case operations, THREAT Matrix provides the TTP classification layer. Whether THREAT Matrix integrates with WARDEN, commercial case management tools, or both is a decision deferred until V5+ when the Operations Composer and cross-matrix composition are proven.

---

## V8+ — Continuous Learning Loop
**Status:** Future

**Purpose:** Close the feedback loop between AI-assisted case identification and the taxonomy itself.

**Planned capabilities:**
- Practitioner correction feedback: when an AI agent maps an incident to a tactic and the practitioner corrects the mapping, the correction feeds back into the embedding model
- Taxonomy evolution recommendations: AI identifies patterns in correction data that suggest new tactics, tactic refinements, or indicator additions
- Automated source monitoring: AI agents scan new government reports, academic publications, and after-action reviews for content that validates or challenges existing tactic definitions
- Cross-organization learning (privacy-preserving): anonymized pattern data shared across participating organizations to improve detection without exposing case details

**Design constraint:** The human practitioner remains the authority. AI agents recommend, practitioners decide. The taxonomy is authored by practitioners, validated by sources, and refined through operational feedback. AI accelerates the cycle but does not replace the editorial judgment.

---

*THREAT Matrix is an open reference standard. MIT License. Value compounds with adoption.*
