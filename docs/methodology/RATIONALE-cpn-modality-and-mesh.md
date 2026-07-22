# RATIONALE — CPN, modality, and the Detection Mesh (methodology, for consumers)

**Status:** Draft methodology rationale, 2026-07-16. Destined to be consumer-facing (like the
escalation rubric) after adversarial validation. Purpose: make every CPN/modality decision and its
REASONING explicit, so a consumer who reasons differently can see WHY we ruled as we did and
deliberately diverge. **These are defensible calls on genuine boundaries, not laws of nature. A
consumer may re-rule any of them; this document exists so that re-ruling is informed.**

## 1. What CPN is (and is not)

Cyber-Physical Nexus is a **boundary-crossing** property, not an **endpoint-location** property. An
operation is "pure cyber" only if it never crosses — and never intends to cross — into a physical
delivery mechanism. The instant a kill chain crosses the cyber-physical seam, it is CPN.

- **Crossing-agnostic.** The crossing may run cyber-to-physical (a command drives an actuator) OR
  physical-to-cyber (a physical implant gains cyber reach). Real ICS attacks are often physical-first.
- **The handoff is the transduction point** — where a digital command becomes mechanical action, or
  a physical implant gains cyber reach. The actuator IS the physical delivery mechanism; no separate
  bomb/drone/person is required.
- **Intent clause.** In scope if the chain's INTENDED terminal effect is a cyber-physical handoff,
  whether or not it has fired. This keeps pre-positioning and early-phase access/persistence in,
  judged by objective. It is the irreducible analyst call separating positioning-for-disruption from
  espionage.

**Realized vs. intended (the two canonical cases).** Stuxnet = *realized* CPN: air-gap USB implant
(physical-to-cyber), OT recon, logic manipulation (cyber-to-physical), view falsification; the
physical terminus fired. Volt Typhoon = *intended* CPN: access/persistence reaching toward OT, handoff
not fired; in scope via the intent clause, with the mesh carrying the anticipated handoff. The contrast
is deliberately preserved — it is the clearest way to teach that CPN is about the crossing, not the
endpoint.

## 2. Two routes to CPN

1. **Intrinsic CPN (hinge behaviors).** A behavior that itself crosses the seam. CPN on its own.
2. **CPN by participation.** A strictly-cyber, strictly-physical, or human/social behavior. On its own
   it crosses nothing; its CPN character is conferred by COMBINATION, expressed by the mesh linking it
   to a hinge or physical terminus in the same chain. A chain containing no hinge and reaching no
   physical terminus (IT ransomware for money, pure espionage) is just cyber, forever.

## 3. Stored vs. computed (the Decision-2 move)

- **STORED per behavior:** an intrinsic **modality** (one of four; Section 4).
- **COMPUTED over the mesh:** CPN participation (per behavior and per operation). Never a stored flag.
  This is the identical move to compensation-as-computed-gap-query (Gate-0 Decision 2): do not store a
  derived property; compute it from the structure. It also means CPN maturity tracks mesh maturity —
  the participation computation is only fully real once the cross-domain mesh is authored.

## 4. The four modalities and the governing principle

**Governing principle: modality follows the behavior's OWN mechanism and where its access lands — NOT
its effect or the importance of its target.** Effect and OT-relevance are what the mesh computes; they
are never what the intrinsic tag stores. This one principle decides most classifications and resolves
four of the five boundary cases below.

- **`physical`** — the behavior's own execution and detection are physical: kinetic act, on-site
  casing, physical breach, hand-emplacement/contamination.
- **`cyber`** — the behavior's own signature and object are digital on IT / open-source / non-control
  assets: OSINT, IT-network action, consuming already-exposed data. Not a crossing by itself.
- **`cyber_physical`** — the behavior itself crosses the seam: a cyber action reaching/reading/writing
  the OT control plane, a physical implant gaining cyber reach, or a technical (digital OR
  electromagnetic) means producing a physical-infrastructure effect.
- **`human_social`** — human/social/financial/communication tradecraft: recruiting, insider
  cultivation, grievance/pathway leakage, coercive demand. A distinct axis the seam-crossing
  trichotomy does not cover; it must not be forced into `cyber` merely because it is digitally
  observed. (Added framework-wide 2026-07-16.)

## 5. The five boundary rulings — with reasoning (a consumer may diverge)

1. **RF / electronic-warfare attacks on an OT timing/comms dependency (GNSS spoofing AND jamming) ->
   `cyber_physical`.** Reasoning: both are remote, non-kinetic, technical attacks on a physical
   infrastructure dependency. Calling a jammer "physical" conflates it with kinetic sabotage and
   creates an inconsistency — packet-flooding an OT network is a crossing, so RF-jamming the same
   operators' comms must be too (identical effect, different transport). We therefore read
   `cyber_physical` as "technical crossing, digital OR electromagnetic." **A consumer who defines
   cyber_physical as strictly digital would instead create a 5th electronic/EW modality; we judged ~4
   indicators do not justify that.**
2. **An operator station / HMI counts as control plane; a RAT on one -> `cyber_physical`.** Reasoning:
   an operator station is Purdue Level 2 — it IS the control environment. The crossing is "access
   lands on an OT asset," consistent with how reaching a PLC and pivoting into the OT zone are already
   treated as crossings. IT/DMZ perimeter gateways (VPN concentrator, perimeter RDP) stay `cyber`
   until access lands on L2/L1. **A consumer using a stricter "must actuate the process" test would
   keep the RAT `cyber` until it issues a command.**
3. **Corrupting control-logic backups -> keep `cyber`.** Reasoning: the mechanism is IT-data-at-rest
   corruption; the OT-restoration-denial significance is an EFFECT, and effect is mesh-computed, not
   stored. This is the model working — a cyber behavior participating in a CPN operation via the mesh.
   **Exception a consumer should apply locally: if the backups literally reside on the engineering
   workstation (OT), the access lands on OT and it becomes `cyber_physical`.**
4. **A hand-defeated hardwired interlock -> `physical`.** Reasoning: mechanism-not-effect in its purest
   form — a person physically jumpering/bypassing a hardwired safety interlock is a physical act, the
   same modality as smashing relays, even though it defeats a safety function. This makes the
   safety-defeat tactic honestly mixed. **A consumer who reads the same behavior as "disable the
   interlock through the controller" would rule `cyber_physical`; the mechanism, not the target,
   decides.**
5. **Passively reading publicly-exposed OT telemetry (OSINT for battle-damage assessment) ->
   `cyber`.** Reasoning: a crossing requires active reach INTO the OT plane; consuming data that has
   already leaked to the public internet is OSINT, the same activity as the other BDA indicators.
   **A consumer who tags by data-nativity rather than access would rule `cyber_physical` because the
   data is OT-native.**

## 6. Known limits (stated honestly)

- The intent clause requires an analyst judgment (objective) that cannot be mechanized — anticipatory
  CPN (Volt Typhoon) and espionage look identical on the wire.
- The physical/cyber line at the IT/OT boundary (Purdue levels) is a modeling choice; environments
  differ, so several rulings above carry an explicit "consumer may diverge" note.
- CPN participation is only as complete as the authored mesh; until the cross-domain mesh is dense,
  computed CPN under-reports.
