# Facility Bibliography — Verified Research (2026-07-06)

Parallel research across 5 agents to verify sourcing for the Facilities matrix. `.gov` PDF endpoints (ATF, CISA, DHS, FBI, USFA) return HTTP 403 to automated fetchers (Akamai/CDN bot protection) but are live canonical URLs; non-blocked hosts (WBDG, CDC, GAO, OSTI, START, RAND, NAF, CTC, Elsevier, NFPA, ANSI) resolved 200. All entries below are REAL and confirmed present.

## Corrections to my original 7 candidates
- ATF EIR: latest is CY2024; CY2023 also available. There is a separate ATF **Arson** Incident Report (AIR).
- START GTD: **no 2022 dataset** — data through 2020 (+partial H1 2021). Re-key to 2020.
- ISC RMP: 2016 (2nd ed) superseded by **2021** edition (a 2024 FOUO edition exists). Use 2021.
- NFPA report retitled **"Intentional Structure Fires"** (2020+); Sept 2021 is latest.
- DHS Soft Targets: the May-2018 "Security Plan Overview" is real; the more citable companion is the CISA **April-2019 Resource Guide**.

## Verified sources by domain (proposed_key | title | date | url | verify)

### Incident data / frameworks / risk methodology
- START-GTD-2020 | Global Terrorism Database (GTD) | data→2020 | https://www.start.umd.edu/research-projects/global-terrorism-database-gtd | 200 | Facility/Infrastructure Attack + Barricade attack-type categories
- DHS-ISC-RMP-2021 | Risk Management Process for Federal Facilities (ISC Standard) | 2021 | https://www.wbdg.org/FFC/DHS/isc_risk_mgmt_process_2021.pdf | 200 | FSL determination, undesirable events
- SANDIA-RAM-2008 | Overview of Sandia's Security Risk Assessment Methodologies (RAMs), SAND2008-1604P | 2008 | https://www.osti.gov/biblio/1713138 | 200
- SANDIA-GARCIA-DEPPS-2007 | Design and Evaluation of Physical Protection Systems, 2nd ed. (M.L. Garcia) | 2007 | https://shop.elsevier.com/books/design-and-evaluation-of-physical-protection-systems/garcia/978-0-08-055428-0 | 200 | ISBN 9780750683524
- SANDIA-GARCIA-VAPPS-2006 | Vulnerability Assessment of Physical Protection Systems (M.L. Garcia) | 2006 | https://shop.elsevier.com/books/vulnerability-assessment-of-physical-protection-systems/garcia/978-0-7506-7788-2 | 200

### Explosives / bombing
- ATF-EIR-2023 | US Bomb Data Center Explosives Incident Report (EIR), CY2023 | 2024 | https://www.atf.gov/explosives/enforcement-tools-services/us-bomb-data-center | canonical(403) | BATS IED/VBIED data (2024 EIR: atf.gov/media/19821/download)
- CISA-BOMBTHREAT-2023 | Bomb Threat Guide v1.9 (Office for Bombing Prevention) | 2023 | https://www.cisa.gov/sites/default/files/2023-08/Bomb%20Threat%20Guide_v1.9_508.pdf | canonical(403)
- FEMA-426-2011 | Reference Manual to Mitigate Potential Terrorist Attacks Against Buildings (FEMA-426/BIPS-06, 2nd ed) | 2011 | https://www.wbdg.org/dhs/criteria/bips-06 | 200 | blast/standoff/structural + CBR chapter (multi-domain workhorse)

### Arson / fire
- ATF-AIR-2023 | US Bomb Data Center Arson Incident Report (AIR), CY2023 | 2024 | https://www.atf.gov/explosives/enforcement-tools-services/us-bomb-data-center | canonical(403) | BATS incendiary data
- NFPA-INTENTIONAL-2021 | Intentional Structure Fires (R. Campbell, NFPA) | 2021 | https://www.nfpa.org/education-and-research/research/nfpa-research/fire-statistical-reports/intentional-fires | 200
- USFA-ARSON-2021 (optional) | Arson and Fire Investigation (USFA Topical Fire Report Series) | 2021 | https://www.usfa.fema.gov/a-z/arson-fire-investigation/ | canonical(403)

### Structural / forced entry / vehicle / hardening standards
- DOD-UFC4010-2018 | UFC 4-010-01 DoD Minimum Antiterrorism Standards for Buildings | 2018 (Chg 3) | https://www.wbdg.org/FFC/DOD/UFC/ufc_4_010_01_2018_c3.pdf | 200
- DOD-UFC4022-2017 | UFC 4-022-01 Security Engineering: Entry Control Facilities / Access Control Points | 2013(2017 rev) | https://www.wbdg.org/dod/ufc/ufc-4-022-01 | 200
- ASTM-F2656-2020 | ASTM F2656/F2656M-20 Crash Testing of Vehicle Security Barriers | 2020 | https://webstore.ansi.org/standards/astm/astmf2656f2656m20 | 200 | (PAS 68 / IWA 14-1 international equivalents)
- CISA-HVM-2023 | Vehicle Incident Prevention and Mitigation Security Guide (Hostile Vehicle Mitigation) | 2023 | https://www.cisa.gov/topics/physical-security/hostile-vehicle-mitigation | canonical(403)
- DOD-UFC4023-03 (flagged, NOT fetch-verified) | UFC 4-023-03 Design of Buildings to Resist Progressive Collapse | — | wbdg.org | verify before adding

### Soft targets / crowded places / target selection
- CISA-SOFTTARGETS-2019 | Security of Soft Targets and Crowded Places — Resource Guide | 2019 | https://www.cisa.gov/resources-tools/resources/security-soft-targets-and-crowded-places-resource-guide | canonical(403) | mirror: fema.gov/.../fema_faith-communities_security-soft-targets-crowded-places.pdf
- DHS-STCP-2018 (optional; overlaps above) | Soft Targets and Crowded Places Security Plan Overview | 2018 | https://www.hsdl.org/?abstract=&did=812763 | 200
- RAND-SOFTTARGETS-2024 | Improving the Security of Soft Targets and Crowded Places: A Landscape Assessment (RRA2260-1) | 2024 | https://www.rand.org/pubs/research_reports/RRA2260-1.html | 200 | target-type lethality weighting
- FBI-ACTIVESHOOTER-2024 | Active Shooter Incidents in the United States in 2024 | 2025 | https://www.fbi.gov/news/press-releases/fbi-releases-2024-active-shooter-incidents-in-the-united-states-report | canonical(403) | facility-location-type distribution

### CBRN / contamination / cyber-physical / building systems
- NIOSH-BLDG-CBR-2002 | Guidance for Protecting Building Environments from Airborne Chemical, Biological, or Radiological Attacks (Pub 2002-139) | 2002 | https://www.cdc.gov/niosh/docs/2002-139/ | 200 | HVAC/air-intake CBR vector
- NIST-SP800-82-2023 | Guide to Operational Technology (OT) Security (SP 800-82 Rev 3) | 2023 | https://csrc.nist.gov/pubs/sp/800/82/r3/final | 200 | DOI 10.6028/NIST.SP.800-82r3 | BAS/ICS/OT
- GAO-15-6-2014 | Federal Facility Cybersecurity: DHS and GSA Should Address Cyber Risk to Building and Access Control Systems | 2014 | https://www.gao.gov/products/gao-15-6 | 200
- GAO-19-138-2018 | Federal Building Security: ...Secure, Interoperable Physical Access Control | 2018 | https://www.gao.gov/products/gao-19-138 | 200
- GAO-24-106744-2024 | Critical Infrastructure Protection: EPA...Cybersecurity Risks to Water and Wastewater Systems | 2024 | https://www.gao.gov/products/gao-24-106744 | 200
- CISA-CFATS (optional, CAVEAT) | Chemical Facility Anti-Terrorism Standards | — | https://www.cisa.gov/resources-tools/programs/chemical-facility-anti-terrorism-standards-cfats | canonical(403) | **statutory authority LAPSED July 2023 — cite as historical framework only**

### Symbolic / ideological / occupation / siege
- NAF-CLINICVIOLENCE-2024 | NAF 2024 Violence & Disruption Statistics | 2024 | https://nationalabortionfederation.org/safety-security/2024-naf-violence-disruption/ | 200 | ideological clinic attacks; arson/bombing/invasion/blockade/occupation counts since 1977
- CTC-INFRATERROR-2026 | From Earth Liberation to Accelerationism: Fifty Years of Domestic Infrastructure Terrorism (J. Humpal, CTC Sentinel 19:3) | 2026 | https://ctc.westpoint.edu/from-earth-liberation-to-accelerationism-a-high-level-review-of-fifty-years-of-domestic-infrastructure-terrorism/ | 200 | 194-incident dataset
- FBI-HOBAS (optional) | HOBAS barricade/hostage dataset (FBI LEB article) | 2024 | https://leb.fbi.gov/articles/featured-articles/leveraging-data-to-predict-outcomes-in-hostage-and-barricade-incidents | canonical(403) | siege/barricade/occupation
- FBI-HATECRIME (optional) | FBI Hate Crime Statistics (UCR) | annual | https://www.fbi.gov/how-we-can-help-you/more-fbi-services-and-information/ucr/hate-crime | canonical(403) | houses-of-worship targeting

## Coverage gaps (could not source to rock-solid bar)
- Progressive-collapse standard (UFC 4-023-03) — real, not fetch-verified this pass.
- Fire-suppression / life-safety-system sabotage — no standalone authoritative source; partial in FEMA-426 / GAO-15-6.
- Non-cyber water-system contamination (physical/chemical injection) — cyber covered (GAO-24-106744); physical anchor (EPA AWIA §2013) not run down.
- Incendiary device-level methods (Molotov, accelerant, delay devices) — only generic in ATF-AIR/USFA.
- Non-violent building occupation/blockade dataset (campus takeovers, site blockades) — no coded dataset; closest is GTD barricade category / ACLED / Crowd Counting Consortium.
- International/non-US facility arson/bombing (UK Home Office, Europol TE-SAT) — not searched this pass.
