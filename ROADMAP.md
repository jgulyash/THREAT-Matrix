# THREAT Matrix — Development Roadmap

**Current Version:** V1 (THREAT/Person — 34 tactics)
**Framework:** Tactical Human Risk Enumeration and Adversary Taxonomy (THREAT)

---

## Version Summary

| Version | Matrix | Tactics | Status |
|---------|--------|---------|--------|
| **V1** | Person | 34 | Shipping |
| **V2** | Facility | 40 | Planned |
| **V3** | Organization | 42 | Planned |
| **V4** | System | 38 | Planned |

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

**Technique content:** V1 ships with `techniques: []` on all 34 Person tactics — V1 delivers tactics, actor profiles, and the V1 Person Detection & Response slice. Technique decomposition and indicator population deepens through V2–V4 as each matrix lands.

---

*THREAT Matrix is an open reference standard. MIT License. Value compounds with adoption.*
