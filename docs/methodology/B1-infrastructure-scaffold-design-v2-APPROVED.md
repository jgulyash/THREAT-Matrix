# B1 — Infrastructure Matrix scaffold design v2 (APPROVED)

**Status:** APPROVED by Jay 2026-07-16. Supersedes `B1-infrastructure-scaffold-design.md` (v1, the
38-tactic 10/12/8/8 draft). This is the tactic set authoring proceeds from. Still no framework.json
writes until the scaffold-write step (B1b) — this doc is the locked design, not the data.

**How v2 differs from v1:** v1 was FirstPrinciples-derived and structurally sound. v2 applies a
two-method validation pass (independent FirstPrinciples decomposition + ICS-doctrine adversarial
review grounded in Stuxnet / Triton-Trisis / Oldsmar / Industroyer-CRASHOVERRIDE / MadIoT /
MITRE ATT&CK for ICS / NIST SP 800-82). Both methods converged on one correction: **10/12/8/8
optimized the wrong phase** — Access was over-built on staging modifiers, Execution under-built in
the one domain whose novelty *is* cyber-physical execution.

**Result: 37 tactics, 10 / 10 / 9 / 8.**

## Changes from v1 (Jay-approved 2026-07-16)

1. **Rebalance Access → Execution.** Phase 2: 12 → 10. Phase 3: 8 → 9.
2. **Merge two Access staging tactics.** v1 `TI0210 Persistence Establishment` + `TI0212 Position
   Establishment` → one **`TI0210 Foothold & Position Establishment`** (intra-operation
   survivability + staging). Stays distinct from the Phase-4 re-entry tactic (see #4).
3. **Fold Timing Exploitation.** v1 `TI0211 Timing Exploitation` is a *modifier* on execution, not
   an access behavior → becomes an escalation/indicator dimension on execution tactics, not a tactic.
4. **Keep persistence-vs-re-entry distinct.** `TI0210` (foothold, intra-op) ≠ `TI0402` (strategic
   leave-behind for re-attack — the Volt Typhoon pattern). Confirmed distinct; the merge in #2 is
   with Position, not with re-entry.
5. **Demote Cascade Induction.** v1 `TI0307 Cascade Induction` is a *consequence* of acting on a
   high-dependency node, not a distinct adversary action → folded into `TI0101`/`TI0102` (selection
   already reasons about cascade) + a cascade-intent indicator on execution tactics.
6. **Add two Execution tactics with hard ICS precedent and no v1 home:**
   - **`TI0307 Demand-Side / Edge Manipulation`** — MadIoT high-wattage-load botnets, DER /
     smart-inverter abuse. Destabilizes the grid from the *demand edge* **without touching SCADA** —
     v1's control-plane-centric access model literally could not express it.
   - **`TI0308 Timing & Positioning-Reference Manipulation`** — GNSS/GPS spoofing & jamming of the
     shared time/position substrate that grid PMUs, telecom sync, and rail signaling depend on.
     (v1 covered only comms *jamming* under service denial.)
7. **Denial-of-View note.** MITRE ATT&CK for ICS distinguishes *Manipulation of View* from *Loss/
   Denial of View*. Handled as a technique split within `TI0303`, not a new tactic.

## Approved tactic scaffold (37) — `TI####`, CPN-heavy (38/38 → 37/37 CPN)

### Phase 1 — Reconnaissance & Preparation (10) — unchanged from v1
| id | name | note |
|---|---|---|
| TI0101 | Infrastructure Target Selection | now also carries cascade-value selection (absorbs demoted 0307 reasoning) |
| TI0102 | Service & Dependency Mapping | SPOF + downstream-dependent mapping (cascade prerequisite) |
| TI0103 | Physical Site Reconnaissance | dispersed-asset casing |
| TI0104 | Process & Engineering Reconnaissance | NEW-class: setpoints, interlocks, safety limits, normal telemetry |
| TI0105 | Control-Network Enumeration | NEW-class: SCADA/PLC/RTU/HMI/protocol + remote-access discovery |
| TI0106 | Capability Acquisition | ICS malware, protocol tooling, engineering creds, physical means |
| TI0107 | Network Development | co-conspirators + material support (mesh-aligned TM/TF0107) |
| TI0108 | Insider & Operator Cultivation | elevated: operator/engineer/integrator recruitment |
| TI0109 | Supply-Chain & Third-Party Vectoring | NEW-class: vendor/integrator/firmware/remote-maintenance path |
| TI0110 | Pathway / Escalation Indicators | actor-level pathway markers (mesh-aligned) |

### Phase 2 — Access & Positioning (10) — was 12
| id | name | note |
|---|---|---|
| TI0201 | Operational Rehearsal | dry-runs incl. test commands in lab/twin environments |
| TI0202 | Cover Construction | vendor/inspector/contractor persona (physical + credential) |
| TI0203 | Surveillance Detection & Counter-Detection | evades physical + network monitoring |
| TI0204 | Physical Perimeter Breach | fence/gate/enclosure at a dispersed asset |
| TI0205 | Remote Access Acquisition | NEW-class: logical path onto control network (VPN, exposed HMI, RAT) |
| TI0206 | Control-System Access | NEW-class: reach PLC/RTU/HMI/engineering workstation |
| TI0207 | Privilege & Zone Escalation | IT→OT pivot, safety-zone crossing, engineering-role elevation |
| TI0208 | Insider-Enabled Access | NEW-class: operator's own credentials/console as the access path |
| TI0209 | Device / Implant Emplacement | rogue device, malicious firmware, physical tap |
| TI0210 | Foothold & Position Establishment | **MERGED** (v1 Persistence + Position); intra-op foothold + staging; distinct from TI0402 |

*Access mediums explicitly admitted at the indicator layer: physical, IP-network, RF/wireless, insider-console, supply-chain.*

### Phase 3 — Execution (9) — was 8
| id | name | note |
|---|---|---|
| TI0301 | Process Manipulation | core: malicious setpoint/logic driving process unsafe (incl. subtle-drift indicator) |
| TI0302 | Protection & Safety-System Defeat | core: disable/spoof SIS, interlocks, relays (Triton) |
| TI0303 | Operational View Falsification | core: spoof HMI/telemetry (+ denial-of-view technique split per ATT&CK-ICS) |
| TI0304 | Physical Sabotage | destruction of transformer/pump/valve/line/tower |
| TI0305 | Service Denial / Disruption | forced outage, load-shed trigger, comms jam, flow stoppage |
| TI0306 | Contamination / Adulteration | water/fuel/chemical process contamination |
| TI0307 | Demand-Side / Edge Manipulation | **NEW** (MadIoT/DER) — destabilize from the demand edge, no SCADA touch |
| TI0308 | Timing & Positioning-Reference Manipulation | **NEW** (GNSS spoof/jam) — attack the shared time/position substrate |
| TI0309 | Response & Recovery Suppression | defeat failover, alarms, backups, restoration (renumbered from v1 0308) |

*Folded here as escalation/indicator dimensions, not tactics: timing exploitation (peak-load/maintenance-window alignment), cascade intent.*

### Phase 4 — Aftermath (8: 6 evasion + 2 attribution) — unchanged from v1
| id | name | track |
|---|---|---|
| TI0401 | Withdrawal | evasion |
| TI0402 | Access Persistence & Re-entry Positioning | evasion (strategic leave-behind; distinct from TI0210) |
| TI0403 | Evidence & Log Manipulation | evasion |
| TI0404 | Attribution Obfuscation | evasion |
| TI0405 | Network Protection | evasion (mesh-aligned) |
| TI0406 | After-Action Assessment | evasion (BDA) |
| TI0407 | Attribution Declaration | attribution |
| TI0408 | Coercive Demand / Leverage | attribution (extortion/ransom/political demand tied to the service) |

## Scaffold-write reconciliation (B1b — next step, gated)

- **`src/lib/constants.ts`** currently holds the placeholder `infrastructure: { phases: { 1: 8, 2: 9,
  3: 9 }, flight: 8, claim: 4 }`. Update to **`{ phases: { 1: 10, 2: 10, 3: 9 }, flight: 6, claim: 2 }`**
  (= 37) at scaffold-write. Neither the placeholder nor the v1 draft matches; v2 is canonical.
- **id grammar:** `TI####` tactics, `IND-I####-##` / `CM-I####-##` / `RP-I####-##` compound IDs —
  all validate against the shipped `[FOI]?` schema patterns (Phase 1 lock).
- **CPN:** every tactic flagged; `cpn_id` / `cpn_notes` assigned per tactic during authoring.
- **Mesh alignment (A3 later):** TI0107↔TM/TF0107, TI0110↔pathway, TI04xx aftermath family retain
  positional correspondence; the two NEW execution tactics (0307/0308) are infra-only, no cross-domain
  positional partner — expected, they are the domain's unique-in-kind payload.

## Open questions from v1 — all resolved
1. Count/distribution → **37, 10/10/9/8** (rebalanced, Jay-approved).
2. id grammar → **confirmed** (validates against shipped schema).
3. Persistence (TI0210) vs re-entry (TI0402) → **keep distinct**; TI0210 merges with Position, not re-entry.
4. Cascade Induction → **demoted** to selection + indicator.
5. Sector-as-tactic → **no**; sector specificity stays at the indicator layer (matches how People/Facility handle actor variation).
