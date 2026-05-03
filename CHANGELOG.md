# CHANGELOG

All notable changes to THREAT Matrix are documented here, per [VERSIONING.md](VERSIONING.md).

This project adheres to [Semantic Versioning](https://semver.org). Framework
content and JSON Schema are versioned independently; both are at `1.1.0`
as of this release.

## [1.1.0] — 2026-05-02

The first release under the V1.1 standard contract. Promotes THREAT Matrix
from a framework to an open standard with a published versioning policy,
identifier contract, deprecation discipline, and reference consumer.
Person matrix Detection & Response is complete across all 34 tactics.

### Added

**Standard contract**
- `VERSIONING.md` — independent SemVer for content and schema, frozen-published rule, fixed-section CHANGELOG template
- `IDENTIFIERS.md` — five operational namespaces (TA####, AP###, IND-*, CM-*, RP-*), compound-ID anatomy, never-reused guarantee
- `DEPRECATION.md` — four-state lifecycle (active / deprecated / superseded / reserved), required fields per state, sunset window
- `NOTICES.md` — MIT License, bibliographic sources, related work, attribution format
- `VOICE.md` — six locked authoring rules (Rules 1–4 in pre-V1.1; Rules 5 + 6 added this release: canonical actor naming and voice variety palette)
- `examples/python_consumer.py` — minimum viable reference consumer (stdlib + jsonschema), demonstrating phase + actor filters
- `examples/README.md` — starting-point guide for five common consumer shapes

**Architecture**
- `schema_version` field in `framework.json` (independent from content `version`)
- Top-level `phase_mappings` cross-walk to NTAC, Calhoun & Weston, CERT, Cyber Kill Chain, MITRE ATT&CK, and MITRE ATLAS
- Top-level `detection_mesh` with five axes (cross_phase, cross_matrix, cross_domain, cross_countermeasure, cross_stakeholder)
- Mandatory tactic fields: `field_notes`, `observed_contexts`, `evidence_basis`, `source_refs`
- Formal JSON Schema published at `docs/data/framework.schema.json` (Draft 2020-12)

**Person Detection & Response**
- All 34 Person tactics (TA0101–TA0108, TA0201–TA0209, TA0301–TA0308, TA0401–TA0409) authored to V1.1 quality with full mandatory fields, indicators, countermeasures, response protocols, and Detection Mesh cross-links (`correlates_with`, `compensates_for`, `coordinates_with`) populated across all four phases
- `GULYASH-FIELD-OPS-2004-2026` source attribution applied across the corpus where framework content is observed in operational casework

**Schema enum extensions**
- `indicator.detection_sources`: added `rf_detection` (RF spectrum monitoring) and `anti_drone_systems` (acoustic / radar / RF triangulation)
- `countermeasure.time_to_implement`: added `weeks_to_months` (resolves TA0103 CM-0103-04 enum violation)

**Bibliography**
- `KIM-JONGNAM-KUL-2017` — Lowy Institute (The Interpreter) coverage of the 13 Feb 2017 Kim Jong-nam assassination, sourcing the unwitting-bystander media-production deception archetype in TA0306
- `CHAINALYSIS-CCR-2024` — Chainalysis Crypto Crime Report, sourcing the comparative blockchain-forensics tracing-speed claim in TA0405

**SPA + assets**
- Vite / React 18 / TypeScript single-page application; bundle prebuilt at `docs/assets/` so GitHub Pages serves without a build step
- 18 components (HeatMapGrid, TopNav, FilterBar, SplitView, PhasePanel, TacticDetail, ActorDetailView, ActorProfilesView, BibliographyView, StubLanding) plus detection-response subcomponents
- `docs/images/threat-lifecycle-diagram.svg` (light-mode SPA tokens, four-phase lifecycle with phase-accent color bars)
- `docs/images/matrix-overview.svg` (light-mode tokens, matrix accent color top strips, V1.1 LIVE / V1.3–V1.5 IN PROGRESS pill aesthetic)
- Sources dropdown UI across IndicatorSection / CountermeasureSection / ResponseProtocolSection

### Changed

- **Top-level matrix key:** `system` → `infrastructure` (and 9 actor-profile `primary_matrices` arrays updated accordingly)
- **SPA matrix version labels:** `V2` / `V3` / `V4` → `V1.3` / `V1.4` / `V1.5`
- **Bibliography ID:** `GULYASH-FIELD-OPS-2010-2025` → `GULYASH-FIELD-OPS-2004-2026`
- **Phase 4 actor track:** `FLIGHT` → `EVADE` (in SVG and SPA labels)
- **Countermeasure subcategory display label:** `Detective` → `Detection` (schema enum value `detective` retained — display-only)
- **WARDEN positioning** removed from README / ROADMAP consumer claims; `framework.json.warden_integration` retained as `status: reserved` per DEPRECATION.md "reserved" lifecycle state
- **Authoring voice canonicalization** (Rule 5): pre-canonical wording (`Subject` / `subject-target pair`) replaced with `Threat actor` / `threat actor — targeted subject pair` across all populated tactics; clinical diction (`incongruity`, `practitioner`) replaced with palette alternatives in tactic content

### Removed

- Legacy single-file React-via-Babel SPA in `docs/index.html` (replaced by Vite build)
- `docs/images/kill-chain-diagram.svg` (replaced by `threat-lifecycle-diagram.svg`)

### Fixed

- TA0103 IND-0103-03 typo: `targeted sujbect` → `targeted subject`
- TA0103 CM-0103-04 pre-existing `time_to_implement: weeks_to_months` enum violation (resolved via schema enum extension)
- `threat-lifecycle-diagram.svg` XML parse error (illegal `--` in comment)
- `matrix-overview.svg` IN PROGRESS pill sizing (text overflow at 108px → widened to 132px → narrowed to 120px for visual balance)
- `ROADMAP.md` line 19 extra columns and line 51 double-hash
- Broken `V1.1-Schema-Spec.md` link from README

### Security

- None specific to V1.1.0.

---

**Validation state at release:** 0 schema errors against `framework.json` (validated by `examples/python_consumer.py` + `jsonschema` Draft 2020-12).
