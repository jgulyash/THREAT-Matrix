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
| **V5** | Detection & Response Companion | — | Planned |

---

## V1 — THREAT/Person
**Tactic ID Range:** TA01xx–TA04xx (34 tactics)
**Target:** Specific individual (targeted violence, stalking, kidnapping, assassination)

**Delivered:**
- Complete tactic schema across all 4 phases
- 21 actor profiles across 6 categories
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
- Countermeasure design layer (foundation for V5)

**Source coverage at launch:** 50–60% (power/water/pipeline deep; dam/telecom stubs)
- NERC reliability reports
- EPA Water Security Initiative
- NTSB transportation security database
- Metcalf sniper attack analysis
- ICS-CERT advisory database

---

## V5 — Detection & Response Companion Guide
**The defender mirror to the adversary taxonomy.**

For every phase and tactic across all four matrices:
- Detection methodology
- Investigative response
- Intervention strategy
- Post-incident investigation (debriefing, network tracing, full adversary picture reconstruction)

**Schema additions:**
- Countermeasures fully populated with all 4 fields: cost / time / complexity / limitations
- Defender overlay mapped to each tactic

**New Capabilities:**
- Defender overlay view (toggle: adversary view ↔ defender view)
- Phase-gate detection methodology — what to look for at each kill chain phase before escalation
- Post-incident investigation workflow builder

**Governing principle:** Defender activity lives here, not in the adversary taxonomy. V1-V4 are designed with V5 in mind — CPN tags and indicator stubs are anchors for this guide.

---

## Cross-Version Architecture Notes

**Navigation axes:**
- Axis 1 (V1): Matrix-primary — browse by matrix, phase, actor profile, CPN
- Axis 2 (V2): Operations-primary — build and analyze multi-phase, cross-matrix adversary operations

**WARDEN integration:** Reserved in V1 schema at zero build cost. V3 activation: WARDEN alert schema maps to THREAT taxonomy via agentic ingestion pipeline. Both tools more powerful together.

**Tactic families:** 56 families enable cross-matrix grouping. Stable identifiers — not renamed after framework.json build. Powers Operations composer in V2+.

**Technique content:** V1 ships with `techniques: []` on all 34 Person tactics. Content populates in V2 alongside the Detection & Response Guide design.

---

*THREAT Matrix is an open reference standard. MIT License. Value compounds with adoption.*
