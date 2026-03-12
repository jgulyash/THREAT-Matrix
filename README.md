# The THREAT Framework

**Tactics, Techniques, and Procedures for Human Risk Evaluation and Assessment Taxonomy**

A structured TTP taxonomy for physical security threats and human risk evaluation, built on the same structural logic as MITRE ATT&CK and applied to the physical domain.

---

## The Problem

Physical security has no equivalent to MITRE ATT&CK. Threat intelligence teams can map adversary behavior against a standardized cyber TTP library, but physical threat analysis still relies on informal, organization-specific frameworks that vary by analyst and team. There is no shared language for categorizing how a physical threat actor conducts reconnaissance, gains access, evades detection, or manages attribution after an incident.

The THREAT Framework fills that gap. It gives protective intelligence practitioners, physical security teams, and insider threat analysts a common taxonomy for structuring threat analysis, communicating findings, and developing detection and mitigation strategies against physical threat actors.

---

## What This Demonstrates

- Application of IC analytical tradecraft to structured framework development
- MITRE ATT&CK fluency extended to the physical security domain
- Ability to translate unstructured operational knowledge into systematic, reusable taxonomy
- Cross-domain thinking that bridges physical threat intelligence, insider risk, and cyber threat frameworks
- Structured analytical methodology: tactic-to-technique decomposition with sub-technique specificity

---

## Relationship to MITRE ATT&CK

The THREAT Framework mirrors the structural design of MITRE ATT&CK: tactics define the adversarial objective, techniques define how that objective is achieved, and sub-techniques provide specificity. It is not a fork or extension of ATT&CK. It is a parallel framework built for the physical domain with the same structural logic, intended to integrate naturally into programs that already use ATT&CK for cyber threat analysis.

---

## Framework Structure

The taxonomy covers three attack phases with 16 tactics and over 80 techniques:

**Phase 1: Pre-Attack**
- Reconnaissance (TA0001)
- Resource Development (TA0002)
- Initial Access (TA0003)

**Phase 2: Attack**
- Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Impact (TA0004-TA0011)

**Phase 3: Post-Attack**
- Exfiltration, Command and Control, Attribution Management, Public Messaging, Surrender/Capture (TA0012-TA0016)

Each tactic includes technique entries with sub-techniques following the T####.### numbering convention.

---

## How to Use It

The framework is a reference taxonomy. Use it to:

- Categorize threat actor behavior during case analysis or incident review
- Structure threat assessments against specific TTP patterns
- Build detection and monitoring logic tied to specific techniques
- Communicate findings in a standardized format across teams
- Develop training scenarios based on realistic adversary behavior chains

---

## Current Status

**v0.1 — Framework in development.**

The core tactical matrix is complete. Actor profiles, detection indicators, and mitigation guidance are included as initial drafts. The framework is functional as a reference taxonomy and will continue to expand based on operational feedback and threat landscape changes.

---

## License

MIT
