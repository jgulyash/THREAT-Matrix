# B1 — Infrastructure Matrix scaffold design (V1.4, Session 32)

**Status:** SUPERSEDED 2026-07-16 by `B1-infrastructure-scaffold-design-v2-APPROVED.md` (rebalanced
to 37 tactics, 10/10/9/8, after two-method validation). Retained for provenance. No framework.json
writes until approved.
**Method:** FirstPrinciples (Deconstruct → Challenge → Reconstruct), templated against the
shipped Facilities matrix (40 tactics) as the structural reference.

---

## First Principles Analysis: threats to infrastructure

### Deconstruction — what is the target actually made of?

People matrix → target is a **person** (a body with a routine, in space).
Facility matrix → target is a **place** (a bounded site with a perimeter and occupants).
Infrastructure matrix → target is a **function**: the continuous delivery of a service
(power, water, signal, movement) produced by a distributed **control system** (sensors →
logic → actuators) governing physical **process** across **geographically dispersed assets**.

Irreducible facts that make infrastructure *different in kind*, not degree:

1. **The kill-chain is cyber-physical.** The consequence is physical (blackout, flood,
   derailment) but the reachable attack surface is frequently a network/logic layer (SCADA,
   PLC, HMI, RTU, protocol). Recon includes network/firmware enumeration; execution includes
   malicious control logic — not just a bomb or a breach.

2. **Access can be effect-at-distance.** Unlike a person or a building, an infrastructure
   function can be degraded without the actor being physically present — remote access to a
   control network, a supply-chain-implanted device, a compromised vendor VPN. "Approach"
   generalizes from *walking up to* → *obtaining a path to the control plane* (physical OR
   logical OR via a trusted third party).

3. **The insider/operator is a first-class vector, not a subtype.** OT environments run on a
   small population of privileged operators, engineers, and integrators whose *legitimate*
   actions are indistinguishable at the wire from sabotage. On People/Facility, insiders are a
   recruited enabler (Network Development). On Infrastructure, an insider's own hands on the
   console is a primary *execution* pathway.

4. **Effect is indirect, delayed, and cascading.** Attacking a substation can black out a
   hospital; poisoning a setpoint can rupture a pipe hours later; a comms outage cascades to
   dependent sectors. Target *selection* reasons about **dependency and cascade**, not
   proximity. Aftermath reasons about **persistence** (leave-behind access) as much as flight.

5. **Reconnaissance targets the process, not just the place.** The actor must learn the
   engineering: which setpoint is safety-critical, which interlock to defeat, what "normal"
   telemetry looks like (to spoof it). This is *process/engineering reconnaissance* — a class
   with no People/Facility analog.

6. **Execution includes safety-system defeat and manipulation-of-view.** The signature ICS
   attack pattern (Triton/Trisis, Stuxnet, Oldsmar) is: defeat the safety instrumented
   system, falsify the operator's view so the anomaly isn't seen, then drive the process to an
   unsafe state. "Force Application" → **process manipulation + protection defeat + view
   falsification**.

### Constraint classification — what to inherit vs. what must diverge

| Element | Type | Verdict |
|---|---|---|
| 4-phase kill chain (recon → access → execution → aftermath) | Hard (any operation has these) | **INHERIT** — the phase spine is domain-agnostic |
| Phase-4 evasion/attribution split | Soft (framework convention, proven useful) | **INHERIT** — it works and keeps mesh alignment |
| "Perimeter breach / interior penetration" as the only access model | Assumption (physical-only) | **CHALLENGE** — add logical + supply-chain + insider-console access |
| "Target = a place with a perimeter" | Assumption | **REJECT** — target = a function/process on dispersed assets |
| Aftermath = flight + claim | Soft | **EXTEND** — add **persistence / re-access** as a distinct aftermath behavior (leave-behind is the ICS norm) |
| CPN flag mostly-optional (People) | Soft | **INVERT** — Infrastructure is CPN-*heavy*; CPN is the default, non-CPN the exception |
| Recon = casing a site | Assumption | **SPLIT** — physical recon AND process/engineering recon AND network enumeration |

### Reconstruction — the optimal tactic set from the fundamentals

Keep the phase spine and the id grammar (`TI####`, phase-encoded second pair; indicators
`IND-I####-##`). Diverge the tactic *content* wherever the fundamentals above demand it.
Result: **38 tactics** (10 / 12 / 8 / 8), CPN-heavy.

---

## Proposed tactic scaffold (38) — `TI####`

### Phase 1 — Reconnaissance & Preparation (10)
| id | name | CPN | rationale / divergence from Facility |
|---|---|---|---|
| TI0101 | Infrastructure Target Selection | ✓ | selects on **dependency/cascade value**, not proximity (fact 4) |
| TI0102 | Service & Dependency Mapping | ✓ | **NEW** — maps downstream dependents & single points of failure (fact 4) |
| TI0103 | Physical Site Reconnaissance | ✓ | substations, pump stations, cell sites, rail signals — dispersed asset casing |
| TI0104 | Process & Engineering Reconnaissance | ✓ | **NEW** — learns setpoints, interlocks, safety limits, normal telemetry (fact 5) |
| TI0105 | Control-Network Enumeration | ✓ | **NEW** — SCADA/PLC/RTU/HMI/protocol & remote-access discovery (fact 1) |
| TI0106 | Capability Acquisition | ✓ | ICS malware, protocol tooling, engineering credentials/software, physical means |
| TI0107 | Network Development | ✓ | co-conspirators + material support (mesh-aligned to TM/TF0107) |
| TI0108 | Insider & Operator Cultivation | ✓ | **elevated** — operator/engineer/integrator recruitment (fact 3) |
| TI0109 | Supply-Chain & Third-Party Vectoring | ✓ | **NEW** — vendor/integrator/firmware/remote-maintenance path (fact 2) |
| TI0110 | Pathway / Escalation Indicators | ✓ | actor-level pathway markers (mesh-aligned to TM0107/TF0109) |

### Phase 2 — Access & Positioning (12)
| id | name | CPN | rationale / divergence |
|---|---|---|---|
| TI0201 | Operational Rehearsal | ✓ | dry-runs incl. test commands in lab/twin environments |
| TI0202 | Cover Construction | ✓ | vendor/inspector/contractor persona (physical + credential) |
| TI0203 | Surveillance Detection & Counter-Detection | ✓ | evades physical + network monitoring |
| TI0204 | Physical Perimeter Breach | ✓ | fence/gate/enclosure at a dispersed asset |
| TI0205 | Remote Access Acquisition | ✓ | **NEW** — obtains logical path to control network (VPN, exposed HMI, RAT) (fact 2) |
| TI0206 | Control-System Access | ✓ | **NEW** — reaches PLC/RTU/HMI/engineering workstation (fact 1) |
| TI0207 | Privilege & Zone Escalation | ✓ | IT→OT pivot, safety-zone crossing, engineering-role elevation |
| TI0208 | Insider-Enabled Access | ✓ | **NEW** — operator's own credentials/console as the access path (fact 3) |
| TI0209 | Device / Implant Emplacement | ✓ | rogue device, malicious firmware, physical tap on the process |
| TI0210 | Persistence Establishment | ✓ | **NEW** — foothold/backdoor for later or repeat action (fact 4/6) |
| TI0211 | Timing Exploitation | ✓ | peak-load, maintenance window, seasonal-demand alignment |
| TI0212 | Position Establishment | ✓ | staging (physical or logical) prior to execution |

### Phase 3 — Execution (8)
| id | name | CPN | rationale / divergence |
|---|---|---|---|
| TI0301 | Process Manipulation | ✓ | **NEW/core** — malicious setpoint/logic change driving the process unsafe (fact 6) |
| TI0302 | Protection & Safety-System Defeat | ✓ | **NEW/core** — disable/spoof SIS, interlocks, relays (Triton pattern) (fact 6) |
| TI0303 | Operational View Falsification | ✓ | **NEW/core** — spoof HMI/telemetry so operators don't see the anomaly (fact 6) |
| TI0304 | Physical Sabotage | ✓ | destruction of transformer/pump/valve/line/tower |
| TI0305 | Service Denial / Disruption | ✓ | forced outage, load-shed trigger, comms jam, flow stoppage |
| TI0306 | Contamination / Adulteration | ✓ | water/fuel/chemical process contamination |
| TI0307 | Cascade Induction | ✓ | **NEW** — action chosen to propagate failure to dependents (fact 4) |
| TI0308 | Response & Recovery Suppression | ✓ | defeat failover, alarms, backups, restoration capability |

### Phase 4 — Aftermath (8: 6 evasion + 2 attribution)
| id | name | track | CPN | rationale |
|---|---|---|---|---|
| TI0401 | Withdrawal | evasion | ✓ | physical or session egress |
| TI0402 | Access Persistence & Re-entry Positioning | evasion | ✓ | **NEW** — keep the foothold for re-attack (fact 4/6) |
| TI0403 | Evidence & Log Manipulation | evasion | ✓ | wipe/forge control-system + physical logs |
| TI0404 | Attribution Obfuscation | evasion | ✓ | false-flag artifacts, third-party-looking TTPs |
| TI0405 | Network Protection | evasion | ✓ | protect co-conspirators/insiders (mesh-aligned) |
| TI0406 | After-Action Assessment | evasion | ✓ | BDA — did the process actually fail as intended |
| TI0407 | Attribution Declaration | attribution | ✓ | claim of responsibility |
| TI0408 | Coercive Demand / Leverage | attribution | ✓ | extortion / ransom / political demand tied to the service |

---

## Coverage self-check

- **Sectors** (fact-driven, not per-sector tactics — tactics are behavior-general, sectors ride
  in indicators/CPN notes): ICS/SCADA ✓ (0104/0105/0206/0301-0303), electric grid ✓
  (0102/0304/0305/0307), water/wastewater ✓ (0306), comms ✓ (0305 jam/outage), transport/rail
  ✓ (0301 signaling, 0304), OT/manufacturing ✓ (0301/0302). Sector specificity lives at the
  indicator layer, matching how People/Facility handle actor variation.
- **CPN:** 38/38 flagged CPN — infrastructure is cyber-physical by nature (inverted default,
  per the constraint table). B1b will assign `cpn_id`/`cpn_notes` per tactic in authoring.
- **Divergent (no copy-rename) tactics:** 12 marked NEW/core — Service&Dependency Mapping,
  Process&Eng Recon, Control-Network Enum, Supply-Chain Vectoring, Remote Access, Control-System
  Access, Insider-Enabled Access, Persistence, Process Manipulation, Protection Defeat, View
  Falsification, Cascade Induction, Access Persistence. These are the first-principles payload;
  the rest are mesh-aligned inheritances kept deliberately for cross-domain link symmetry.
- **Mesh alignment (A3 later):** TI0107↔TM/TF0107, TI0110↔pathway, TI04xx aftermath family all
  keep positional correspondence so the cross-domain grid extends cleanly.

## Open questions for Jay (before scaffold write)
1. **Count:** 38 exactly (10/12/8/8). OK, or trim toward the "~38"? (Phase-2 is 12 — the access
   divergence is where infrastructure genuinely needs more tactics than Facility.)
2. **`TI####` id grammar + `IND-I####-##` indicator grammar** — confirm (schema pattern already
   allows `[FOI]?`, so `IND-I…` validates).
3. **Persistence as its own tactic (TI0210) AND an aftermath tactic (TI0402)** — intended: entry
   persistence vs. exit re-entry positioning. Keep both or merge?
4. **Cascade Induction (TI0307) as a distinct execution tactic** vs. a property of other
   execution tactics — I made it distinct because target *selection* already reasons about
   cascade; confirm.
5. Any sector you want represented as its own tactic rather than at the indicator layer?
