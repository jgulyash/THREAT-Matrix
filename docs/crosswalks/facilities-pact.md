# Crosswalk: Facilities matrix to PACT

**Status: DRAFT. Concept-level. Unreviewed. Not endorsed by any author or organization cited.**

Crosswalk version 0.1.0-draft. Machine-readable copy: `facilities-pact.json` (generated from the same table). Checked against `docs/data/framework.json` on 2026-11-15.

## What PACT is

The Physical Access & Control Taxonomy (PACT) is an open matrix of physical-intrusion tactics, techniques, and procedures published by slashsec Red Teaming GmbH, with mitigations, detections, and data sources. It describes how an intruder gets into and moves through a facility. It does not describe behavioral warning signs, violent attack methods, or what happens after an attack.

| Item | Value |
|---|---|
| Site | https://pact.slashsec.at/ |
| Matrix page | https://pact.slashsec.at/ttps/ |
| License page | https://pact.slashsec.at/license/ |
| JSON data | https://github.com/slashsec-Red-Teaming-GmbH/pact-data-json |
| STIX data | https://github.com/slashsec-Red-Teaming-GmbH/pact-data-stix |
| Retrieved | 2026-11-15 (GET only); all links above returned 200 |
| JSON repository state read | commit `bacd977bc011` (2026-06-29) |
| Objects seen | 12 tactics, 37 techniques, 47 sub-techniques in the site navigation |

PACT publishes no release version number that this draft could find; the commit above identifies the state that was read. If PACT renumbers or renames objects, this crosswalk is stale until re-checked.

## License and compatibility

PACT's license page states that the taxonomy, including its descriptions, identifiers, structure, and published exports, is made available under the Apache License, Version 2.0 (https://www.apache.org/licenses/LICENSE-2.0), and the JSON repository carries the same license.

This crosswalk reproduces PACT identifiers and names only. It copies no PACT description text and is not a modified version of PACT. Referencing identifiers and names with attribution is compatible with the Apache License 2.0 as published, and with this repository's MIT license for its own content. This is the project's reading, not legal advice, and has not been confirmed with the publisher.

Attribution, in the form PACT's license page asks for:

> Physical Access & Control Taxonomy (PACT), (c) slashsec Red Teaming GmbH, licensed under the Apache License, Version 2.0 (https://www.apache.org/licenses/LICENSE-2.0).

MITRE ATT&CK is a registered trademark of The MITRE Corporation; PACT states that it is aligned with the ATT&CK conceptual model. Nothing here implies endorsement by slashsec or MITRE.

## Confidence values

- **direct**: the Facilities tactic and the PACT objects describe the same activity.
- **partial**: overlap on part of the tactic, or at PACT tactic level only.
- **none**: no PACT counterpart.

## Tactic mappings

| Facilities tactic | Name | PACT objects | Confidence | Reason |
|---|---|---|---|---|
| TF0101 | Facility Target Selection | none | none | Choosing which facility to attack, and why, precedes anything PACT describes; PACT starts with reconnaissance of a facility already chosen. |
| TF0102 | Site Profiling | PT0001 Reconnaissance; P0001 Gather Victim Facility Information; P0001.002 Facility Rhythms; P0002.002 Remote Surveillance | direct | Remote collection on a chosen site's function, rhythms, and occupancy matches PACT reconnaissance of facility information and remote surveillance. |
| TF0103 | Physical Reconnaissance | PT0001 Reconnaissance; P0002 Surveillance; P0002.001 On-site Surveillance; P0003 Gather Victim Facility Perimeter | direct | Casing visits and on-foot observation match on-site surveillance and perimeter mapping. |
| TF0104 | Structural & Blueprint Study | PT0001 Reconnaissance; P0001.001 Facility Plans | partial | Obtaining floor plans matches Facility Plans; study of structural engineering detail to cause damage has no PACT counterpart. |
| TF0105 | Security Posture Assessment | PT0001 Reconnaissance; P0002 Surveillance; P0003 Gather Victim Facility Perimeter | partial | Mapping cameras, guards, and controls falls under PACT surveillance and perimeter mapping; PACT has no separate technique for measuring response timing or probing reactions. |
| TF0106 | Capability Acquisition | PT0002 Resource Development | partial | Same stage as PACT Resource Development, but PACT resources are IDs, pretexts, and props, not accelerants, explosive components, breaching tools, or vehicles. |
| TF0107 | Network Development | P0011 Establish Trust; P0008 Valid Credentials | partial | Cultivating an insider relates to Establish Trust and to credentials obtained through insider assistance; recruiting co-conspirators has no PACT counterpart. |
| TF0108 | Cover Construction | PT0002 Resource Development; P0004 Fabricate ID; P0004.001 Fabricate Victim Company ID; P0004.002 Fabricate Victim Vendor ID; P0005 Develop Pretext; P0005.001 Develop Pretext Story; P0005.002 Gather Pretext Props; P0005.003 Gather Pretext Uniform; P0007.002 Impersonate Staff or Vendor; P0007.005 Wear Cover Dress; P0015 Forge Key; P0016 Clone Badge | direct | Fabricated vendor identities, forged credentials, uniforms, and rehearsed pretexts match Fabricate ID, Develop Pretext, impersonation, and cover dress; badge and key copying is the nearest PACT credential technique. |
| TF0109 | Pathway / Escalation Indicators | none | none | Behavioral leakage and escalation signals about a place; PACT has no behavioral warning content. |
| TF0110 | Surveillance Detection | PT0008 Stealth; P0021 Select Low-Visibility Route | partial | Avoiding observation relates to PACT Stealth and low-visibility routes; testing for and detecting the site's surveillance of the actor has no PACT technique. |
| TF0201 | Operational Rehearsal | P0006 Tailgate; P0026.001 Trigger False Alarm | partial | Rehearsal has no PACT counterpart; the probing acts some indicators describe (tailgating an entry, tripping an alarm to watch the response) correspond to PACT techniques used for a different purpose. |
| TF0202 | Concealment | PT0008 Stealth; P0007.005 Wear Cover Dress; P0013 Hide on Premises | partial | Physical disguise and hiding relate to Stealth, cover dress, and Hide on Premises; caching attack materiel and disguising a device have no PACT counterpart. |
| TF0203 | Perimeter Breach | PT0003 Initial Access; P0009 Bypass Physical Access Controls; P0009.003 Bypass Perimeter Controls; P0010 Exploit Physical Access Weaknesses; P0010.001 Exploit Perimeter Controls | direct | Defeating fences, gates, and walls matches bypass and exploitation of perimeter controls under Initial Access. |
| TF0204 | Interior Penetration | PT0007 Lateral Movement; P0006 Tailgate; P0009.002 Bypass Door; P0017 Cross Security Zone; P0017.001 Cross Zone via Internal Door; P0018 Use Vertical Circulation; P0018.001 Use Stairwell; P0019 Use Service Route | direct | Moving past interior doors and checkpoints by service corridors, stairwells, and tailgating matches PACT Lateral Movement techniques. |
| TF0205 | Device/Materiel Emplacement | none | none | Placing an explosive, incendiary, or vehicle-borne load has no PACT counterpart. PACT's planted device is a surveillance device for collection. |
| TF0206 | Position Establishment | P0013 Hide on Premises | partial | Holding a concealed static position on or near the site loosely relates to Hide on Premises; firing points, standoff positions, and vehicle staging have no PACT counterpart. |
| TF0207 | Timing Exploitation | P0022 Activity Timing; P0022.001 Time Activity to Normal Operations; P0022.002 Time Activity Outside Regular Business Hours; P0001.002 Facility Rhythms | direct | Choosing an occupancy or low-security window matches Activity Timing and collection on facility rhythms. The Facilities tactic also covers symbolic dates, which PACT does not. |
| TF0208 | Utility & Systems Access | PT0007 Lateral Movement; P0019 Use Service Route; P0038 Manipulate Electronic Access Control | partial | Reaching plant rooms and control systems relates to service routes and manipulation of electronic access control; PACT does not cover HVAC, fire, power, or building-automation access as such. |
| TF0209 | Approach | none | none | The final movement to the point of attack while carrying attack means has no PACT counterpart. |
| TF0301 | Incendiary Attack | PT0012 Impact | partial | Tactic-level only. PACT Impact names physical damage in general; it has no technique for fire. |
| TF0302 | Explosive Attack | PT0012 Impact | partial | Tactic-level only. PACT Impact names physical damage in general; it has no technique for explosives. |
| TF0303 | Structural Sabotage | PT0012 Impact; P0035 Sabotage | partial | PACT Sabotage covers damage to equipment, utilities, and processes; attack on a building's load-bearing structure is not described. |
| TF0304 | Systems Sabotage | PT0012 Impact; P0035 Sabotage; PT0009 Defense Impairment; P0024 Disable Sensor; P0024.001 Disable Camera; P0024.002 Disable Intrusion Sensor; P0024.003 Disable Alarm Device; P0038 Manipulate Electronic Access Control | direct | Disabling power, safety, and security systems matches PACT Sabotage and the Defense Impairment sensor and alarm techniques. |
| TF0305 | Forced Entry / Vehicle Ram | P0009 Bypass Physical Access Controls; P0009.002 Bypass Door; P0009.003 Bypass Perimeter Controls | partial | PACT bypass includes defeating doors and barriers through force; ramming with a vehicle and overpowering staff have no PACT counterpart. |
| TF0306 | Occupation & Blockade | none | none | Occupation, lock-ons, and blockades have no PACT counterpart. |
| TF0307 | Vandalism & Defacement | PT0012 Impact | partial | Tactic-level only. Defacement is physical damage in a broad sense; PACT has no technique for it. |
| TF0308 | Contamination | none | none | Introducing a hazardous substance has no PACT counterpart. |
| TF0309 | Response Suppression | PT0009 Defense Impairment; P0024.003 Disable Alarm Device; P0026 Employ Distraction; P0026.001 Trigger False Alarm; P0026.002 Stage Diversion; P0037 Distraction | partial | Disabling alarms and staging diversions match Defense Impairment and Distraction; blocking exits, secondary hazards, and jamming communications have no PACT counterpart. |
| TF0401 | Withdrawal | PT0011 Exfiltration; P0031 Exfiltrate via Entry Route; P0032 Exfiltrate via Emergency Route; P0033 Exfiltrate via Alternative Route | partial | Leaving the site matches PACT exit routes under Exfiltration; vehicle switches, appearance changes, and flight from the jurisdiction are not covered. |
| TF0402 | Evidence Management | none | none | Removal, destruction, or planting of physical evidence has no PACT counterpart. |
| TF0403 | Cover Reestablishment | none | none | Post-attack return to a normal routine has no PACT counterpart. |
| TF0404 | Network Protection | none | none | Post-attack protection of co-conspirators has no PACT counterpart. |
| TF0405 | Financial Disposition | none | none | Movement of funds has no PACT counterpart. |
| TF0406 | After-Action Assessment | none | none | The actor's own review of a completed attack has no PACT counterpart. |
| TF0407 | Counter-Forensics | none | none | Defeating forensic reconstruction has no PACT counterpart. |
| TF0408 | Secondary Device / Re-attack Positioning | none | none | Secondary devices and re-attack positioning have no PACT counterpart. |
| TF0409 | Attribution Declaration | none | none | Claims of responsibility have no PACT counterpart. |
| TF0410 | Audience Amplification | none | none | Publicising a completed attack has no PACT counterpart. |
| TF0411 | Symbolic Messaging | none | none | Symbolic messaging has no PACT counterpart. |
| TF0412 | Coercive Demand | none | none | Demands that leverage a completed attack have no PACT counterpart. |

## Facilities tactics with no PACT counterpart

17 of 40: TF0101, TF0109, TF0205, TF0209, TF0306, TF0308, TF0402, TF0403, TF0404, TF0405, TF0406, TF0407, TF0408, TF0409, TF0410, TF0411, TF0412.

These fall into three groups: target choice and behavioral escalation signals (TF0101, TF0109); violent attack methods and the final approach (TF0205, TF0209, TF0306, TF0308); and the whole aftermath phase other than leaving the site (TF0402 to TF0412).

Mapped direct: 7 (TF0102, TF0103, TF0108, TF0203, TF0204, TF0207, TF0304). Mapped partial: 16 (TF0104, TF0105, TF0106, TF0107, TF0110, TF0201, TF0202, TF0206, TF0208, TF0301, TF0302, TF0303, TF0305, TF0307, TF0309, TF0401).

## PACT objects with no Facilities counterpart

PACT tactics not referenced by any mapping: PT0004 Persistence; PT0005 Privilege Escalation; PT0006 Credential Access; PT0010 Collection.

PT0005 Privilege Escalation is unreferenced as a tactic, but PACT lists under it techniques (Tailgate, Social Engineering, Valid Credentials) that are referenced above under other tactics.

PACT techniques not referenced by any mapping (neither the technique nor any of its sub-techniques):

| PACT ID | Name |
|---|---|
| P0012 | Manipulate Physical Access Controls |
| P0014 | Steal Valid Credentials |
| P0025 | Block Camera View |
| P0027 | Steal Hardware |
| P0028 | Copy Information |
| P0029 | Steal Information |
| P0030 | Plant Surveillance Device |
| P0034 | Espionage |
| P0036 | Theft |
| P0039 | Dumpster Diving |

What this shows: PACT is more detailed than the Facilities matrix on covert entry, persistence on site, credential theft and copying, and collection of information or hardware. The Facilities matrix has no tactic for persistence, credential access as an end in itself, or theft and espionage objectives, because it is written around attacks on the facility rather than intrusion for collection. A user concerned with intrusion should use PACT for that detail.

## How the two fit together

- Reconnaissance, cover and pretext, perimeter and interior access, timing, and systems tampering overlap. For those, a Facilities indicator can point to the PACT technique that describes the method, and a PACT detection can point to the Facilities indicator that describes the surrounding behavior.
- Behavioral escalation, violent attack methods, and aftermath exist only on the Facilities side.
- Persistence, credential access, collection, and exfiltration of material exist only on the PACT side.

## Known limits of this draft

- One reader's judgment from names and a sample of PACT descriptions, unreviewed. Not confirmed with the PACT publisher.
- Mapped at Facilities tactic level. Indicator-to-technique links are not yet drawn.
- PACT mitigations, detections, and assets are not mapped to countermeasures or detection sources.
- PACT lists some techniques under several tactics; the mapping cites the technique once.
- No STIX relationship objects are published for this crosswalk.

Corrections: see `README.md` in this directory.
