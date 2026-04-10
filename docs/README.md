# THREAT Matrix — Interactive Reference

The THREAT Matrix is a physical adversary TTP (Tactics, Techniques, and Procedures) taxonomy modeled after the behavioral structure of MITRE ATT&CK, built for the physical security domain.

**Live framework:** This directory deploys via GitHub Pages. The interactive browser is at `index.html`, reading `data/framework.json`.

## What You're Looking At

The THREAT Matrix organizes physical threat actor behavior across four attack phases and four target matrices:

| Phase | What It Covers |
|-------|----------------|
| **Phase 1 — Target Development** | Intent through capability ready: selection, profiling, survey, acquisition |
| **Phase 2 — Mobilization** | Staging, rehearsal, infiltration, position establishment |
| **Phase 3 — Execution** | Attack execution and concurrent operational activities |
| **Phase 4 — Aftermath: Flight and Claim** | Bifurcated — Flight track (evasion-seeking) and Claim track (attribution-seeking) |

## Version Status

| Matrix | Version | Tactics | Status |
|--------|---------|---------|--------|
| Person | V1 | 34 | Live |
| Facility | V2 | 40 | Planned |
| Organization | V3 | 42 | Planned |
| System | V4 | 38 | Planned |

## Framework Data

`data/framework.json` is the canonical data source. The React SPA reads it via `fetch()`. Schema is defined and versioned — all empty arrays in V1 are architecture placeholders for technique, indicator, and countermeasure content in subsequent versions.

## AI Integration

The THREAT Matrix treats AI as a **force multiplier on existing attack vectors** — not a separate pathway. AI compresses Phase 1 timelines, lowers tradecraft requirements, and makes capabilities previously requiring nation-state resources accessible to unsophisticated actors.

**Attack vector taxonomy** (four values):

| Vector | Definition |
|--------|-----------|
| `physical_primary` | Physical action; no meaningful cyber or AI component |
| `cyber_enabled_physical` | Cyber tools (including AI tools) support or enable a physical attack |
| `cyber_initiated_physical` | A cyber attack IS the attack; physical harm is the consequence |
| `ai_initiated_physical` | An autonomous or semi-autonomous AI system directly executes physical harm without real-time human direction at the point of attack |

**`ai_initiated_physical`** is distinct from `cyber_initiated_physical`: the attack does not necessarily route through networked cyberspace — the AI agent operates locally, autonomously, in physical space. Examples: AI-directed drones with autonomous targeting, compromised autonomous vehicle systems, robotic platforms executing without human oversight.

**`ai_enabled_risks`** is a capability modifier field on each actor profile — not a vector. It documents how AI tools lower the barrier for existing attack vectors on a per-profile basis.

The full AI architecture rationale is documented in the `ai_architecture` block in `data/framework.json`.

**License:** MIT
