# NOTICES
 
THREAT Matrix is released under the MIT License. See `LICENSE` for full terms.
 
This framework draws on decades of field investigations, public news articles and case files, and on published threat-assessment and physical-security research. The following notices acknowledge the published works that informed this framework's development.
 
---
 
## Bibliographic Sources
 
The framework cites the following works as research foundation. Full bibliographic metadata (title, author, date, URL/DOI) appears in `docs/data/framework.json` under the `bibliography` object.
 
### U.S. Government Works (Public Domain per 17 USC § 105)
 
The following works are publications of the U.S. federal government or its employees acting in the course of official duties, and are in the public domain in the United States:
 
- **U.S. Secret Service, National Threat Assessment Center (NTAC):**
  - *Mass Attacks in Public Spaces: 2016-2020* (2021)
  - *Protecting America's Schools: A U.S. Secret Service Analysis of Targeted School Violence* (2019)
  - *Averting Targeted School Violence: A U.S. Secret Service Analysis of Plots Against Schools* (2021)
  - Analysis of targeted attacks against K-12 education systems (2020)
- **Federal Bureau of Investigation:**
  - Silver, J., Simons, A., & Craun, S. (2018). *A Study of the Pre-Attack Behaviors of Active Shooters in the United States Between 2000 and 2013.*
- **Office of the Director of National Intelligence / National Insider Threat Task Force (NITTF):**
  - *Insider Threat Program Maturity Framework* (2017)
- **Cybersecurity and Infrastructure Security Agency (CISA):**
  - Domestic Improvised Terrorism guidance (2023)
  - Cybersecurity and Physical Security Convergence Action Guide (2021)
- **U.S. Department of Justice / National Institute of Justice (NIJ):**
  - Fein, R.A., Vossekuil, B., & Holden, G.A. (1995). *Threat Assessment: An Approach to Prevent Targeted Violence.*
- **National Institute of Standards and Technology (NIST):**
  - Special Publication 800-53 (Rev. 5), *Security and Privacy Controls for Information Systems and Organizations.*
 
### Contractor-Authored Works (Distribution Subject to Publisher Terms)
 
The following works are authored by personnel of federally-funded research and development centers (FFRDCs) or national laboratory contractors. They are cited here by metadata reference; reproduction of their content is governed by the publisher's distribution terms.
 
**Carnegie Mellon University, Software Engineering Institute (SEI), CERT Division — *Common Sense Guide to Mitigating Insider Threats, Seventh Edition* (2022)**
 
> Copyright 2022 Carnegie Mellon University.
> 
> This material is based upon work funded and supported by the Department of Defense under Contract No. FA8702-15-D-0002 with Carnegie Mellon University for the operation of the Software Engineering Institute, a federally funded research and development center.
> 
> [DISTRIBUTION STATEMENT A] This material has been approved for public release and unlimited distribution.
> 
> Carnegie Mellon® and CERT® are registered in the U.S. Patent and Trademark Office by Carnegie Mellon University.
> 
> DM21-0782.
 
THREAT Matrix cites the *Common Sense Guide* by bibliographic reference. Derivative works based on the Guide (including reformulated indicators mirroring the 22 Best Practices) require written SEI permission: `permission@sei.cmu.edu`.
 
**Lawrence Livermore National Laboratory — LLNL-TR-858139 (McGrath, Scott & Slone, 2023)**
 
> This document was prepared as an account of work sponsored by an agency of the United States government. Neither the United States government nor Lawrence Livermore National Security, LLC, nor any of their employees makes any warranty, expressed or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States government or Lawrence Livermore National Security, LLC. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States government or Lawrence Livermore National Security, LLC, and shall not be used for advertising or product endorsement purposes.
> 
> This work performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344.
 
THREAT Matrix cites LLNL-TR-858139 by bibliographic reference. The report itself is governed by DOE Government Purpose Rights and is not relicensed under MIT.
 
### Peer-Reviewed Academic Works
 
Cited as scholarly references. Bibliographic citation is permitted without license under standard academic practice. Reproduction of abstracts, figures, tables, or substantial text beyond fair use requires permission from the copyright holder.
 
- **Journal of Forensic Sciences (ASTM / Wiley):**
  - Fein, R.A., & Vossekuil, B. (1999). *Assassination in the United States: An Operational Study of Recent Assassins, Attackers, and Near-Lethal Approachers.* DOI: 10.1520/JFS14457J.
- **Journal of Threat Assessment and Management (American Psychological Association):**
  - Meloy, J.R., & Gill, P. (2016). *The Lone-Actor Terrorist and the TRAP-18.* DOI: 10.1037/tam0000061.
 
### Standards Body Publications (Cited; Not Reproduced)
 
- **ASIS International / SHRM:**
  - *ANSI/ASIS WVPI.1-2020 — Workplace Violence Prevention and Intervention Standard* (published 2021).
  - ANSI-accredited standard. Copyright ASIS International. Cited by title and designation only. Reproduction of standard text requires written permission from ASIS International.
 
### Independent Research and Industry Analysis

- **Lowy Institute (The Interpreter):**
  - Robertson, J. (2017). *The brazen, broad-daylight assassination of Kim Jong-nam.* https://www.lowyinstitute.org/the-interpreter/brazen-broad-daylight-assassination-kim-jong-nam
  - Cited by URL reference. Lowy Institute is a non-partisan international policy think tank; The Interpreter publishes analysis intended for public reference.
- **Chainalysis Inc.:**
  - *Crypto Crime Report* (2024). https://www.chainalysis.com/crypto-crime-report/
  - Cited by title and date. Chainalysis is a commercial blockchain-analytics firm; the Crypto Crime Report is a published industry reference.
 
---
 
## Related Work and Structural Pattern
 
THREAT Matrix's organizational structure of tactics, techniques, and lifecycle phases is a pattern widely used in modern threat modeling. Notable examples include the Lockheed Martin Cyber Kill Chain® (Hutchins, Cloppert & Amin, 2011), MITRE ATT&CK®, MITRE CAPEC, MITRE D3FEND, MITRE ATLAS, and the DISARM disinformation framework. The lineage of distinguishing tactics (strategic ends) from techniques (means of achieving them) predates these artifacts and traces to classical military and intelligence doctrine.
 
THREAT Matrix adopts the organizational pattern common to this body of work and does not reproduce content from any of these frameworks. THREAT Matrix's tactic and technique set, actor profiles, Threat Lifecycle phase definitions, Detection Mesh architecture, `phase_mappings` cross-walk, JSON Schema, versioning policy, stable identifier contract, and operational playbooks are independent original work addressing the physical adversary-behavior domain, where no analogous structured public taxonomy existed prior to THREAT Matrix.
 
### Trademarks
 
MITRE ATT&CK®, ATT&CK®, D3FEND®, and ATLAS® are registered trademarks of The MITRE Corporation. Cyber Kill Chain® is a registered trademark of Lockheed Martin Corporation. Other framework names referenced above are the property of their respective owners. THREAT Matrix is an independent work, not affiliated with, sponsored by, or endorsed by any of these organizations.
 
Reference: https://attack.mitre.org/resources/legal-and-branding/
 
---
 
## Proprietary Assessment Instruments (Cited as Prior Art, Not Reproduced)
 
The framework references the following proprietary threat and violence assessment instruments for context. THREAT Matrix does not reproduce, reconstruct, or redistribute any instrument items, scoring anchors, coding rules, or manual content.
 
- **TRAP-18 (Terrorist Radicalization Assessment Protocol-18)** by J. Reid Meloy. Published by Global Institute of Forensic Research / Multi-Health Systems. Use of the instrument requires authorized training and license from the publisher. The 8 proximal warning behaviors and 10 distal characteristics are named in the peer-reviewed paper Meloy & Gill (2016) and are referenced in this framework at the construct level with that citation.
 
- **WAVR-21 (Workplace Assessment of Violence Risk)** by Stephen G. White & J. Reid Meloy. Published by Specialized Training Services. Use of the instrument requires purchase of the manual and STS-approved training. THREAT Matrix references the instrument at the construct/domain level and does not list or describe the 21 items.
 
- **Pathway to Violence Model** by Frederick S. Calhoun & Stephen W. Weston. Published in *Contemporary Threat Management* (2003) and related works by Specialized Training Services / CRC Press. Referenced by conceptual model.
 
---
 
## Attribution Format
 
Citations in `docs/data/framework.json` follow the format:
- **Short reference ID** (e.g., `MELOY-TRAP18-2016`)
- **Full metadata:** type, title, author, date, URL or DOI, relevance summary
 
For each cited work, the "relevance_summary" field is original text authored for this framework, describing why the work is cited. It does not reproduce source text beyond naming widely-used concepts that are part of the threat-assessment field's shared vocabulary.
 
---
 
## Disclaimer
 
This NOTICES file is an informational attribution record prepared in good faith. It is not legal advice, does not constitute a license grant from any third party, and does not warrant that the attribution provided here satisfies any license obligation of any cited publisher, author, or organization. Users who fork, redistribute, build upon, or commercialize this framework are responsible for independently verifying third-party permissions applicable to their specific use. Nothing in this file operates as a representation by the THREAT Matrix maintainer that any cited source has reviewed or approved THREAT Matrix's use of that source. Consult qualified IP counsel for any use beyond personal research.
 
The THREAT Matrix open standard itself — the JSON Schema at `docs/data/framework.schema.json`, the canonical `framework.json` artifact, the matrix structure, the original tactic and technique descriptions, actor profiles, Threat Lifecycle phase definitions, Detection Mesh architecture, `phase_mappings` cross-walk, the reference consumer at `examples/python_consumer.py`, and the operational playbooks — is released under the MIT License and is free to use, modify, and redistribute subject to the terms of that license.
---
 
*Last updated: 2026-04-27. Revisions tracked in repository git history.*