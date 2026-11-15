# NOTICES

THREAT Matrix is released under the MIT License. See `LICENSE` for full terms.

This file records third-party material: the published works the framework cites, the third-party software and typeface the viewer uses, and the trademarks and proprietary instruments it names. It is an attribution record, not a license grant.

---

## 1. Cited sources (bibliography)

The framework cites published sources by bibliographic reference. The complete and authoritative source list is the `bibliography` object in `docs/data/framework.json`; each entry carries its type, title, author, date, and URL or DOI where one exists. This file does not repeat that list, so it cannot fall out of step with it. To print the current list:

```
python3 scripts/export/flat.py --out out/flat && cat out/flat/bibliography.jsonl
```

The bibliography holds sources of these kinds: government reports, practitioner guides, standards, academic papers, court documents, incident databases, news investigations, books, and after-action reviews. THREAT Matrix cites these works; it does not reproduce their text, figures, or tables. The `relevance_summary` on each entry is original text written for this framework to say why the work is cited.

Citation does not change the terms a work is published under. The groups below describe those terms in general; the notices that specific publishers require are reproduced in full.

### U.S. federal government works

Works prepared by officers or employees of the U.S. federal government as part of their official duties are not subject to copyright protection in the United States (17 U.S.C. 105). The bibliography cites such works from, among others, the U.S. Secret Service National Threat Assessment Center, the Federal Bureau of Investigation, the Department of Justice and the National Institute of Justice, the Department of Homeland Security and the Cybersecurity and Infrastructure Security Agency, the Federal Emergency Management Agency and the U.S. Fire Administration, the Bureau of Alcohol, Tobacco, Firearms and Explosives, the Department of Defense, the National Institute of Standards and Technology, the Government Accountability Office, the Securities and Exchange Commission, and the federal courts.

This does not extend to works written for the government by contractors, to works of U.S. state governments, or to works of other governments. Those remain under their own terms.

### Works of other governments and public inquiries

The bibliography cites publications of the United Kingdom government and its agencies, a United Kingdom statutory public inquiry, a New Zealand Royal Commission of Inquiry, and U.S. state bodies. These are cited by reference under the terms each publisher sets (for United Kingdom Crown material, typically the Open Government Licence). Check the publisher's terms before reusing their content.

### Contractor-authored and laboratory works (publisher terms apply)

The following works are authored by personnel of federally funded research and development centers or national laboratory contractors. They are cited by bibliographic reference; reproduction of their content is governed by the publisher's distribution terms.

**Carnegie Mellon University, Software Engineering Institute (SEI), CERT Division: *Common Sense Guide to Mitigating Insider Threats, Seventh Edition* (2022)**

> Copyright 2022 Carnegie Mellon University.
>
> This material is based upon work funded and supported by the Department of Defense under Contract No. FA8702-15-D-0002 with Carnegie Mellon University for the operation of the Software Engineering Institute, a federally funded research and development center.
>
> [DISTRIBUTION STATEMENT A] This material has been approved for public release and unlimited distribution.
>
> Carnegie Mellon® and CERT® are registered in the U.S. Patent and Trademark Office by Carnegie Mellon University.
>
> DM21-0782.

THREAT Matrix cites the *Common Sense Guide* by bibliographic reference. Derivative works based on the Guide require written SEI permission: `permission@sei.cmu.edu`.

**Lawrence Livermore National Laboratory: LLNL-TR-858139 (McGrath, Scott & Slone, 2023)**

> This document was prepared as an account of work sponsored by an agency of the United States government. Neither the United States government nor Lawrence Livermore National Security, LLC, nor any of their employees makes any warranty, expressed or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States government or Lawrence Livermore National Security, LLC. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States government or Lawrence Livermore National Security, LLC, and shall not be used for advertising or product endorsement purposes.
>
> This work performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344.

THREAT Matrix cites LLNL-TR-858139 by bibliographic reference. The report is governed by its own terms and is not relicensed under MIT.

The bibliography also cites works from Sandia National Laboratories and from the RAND Corporation (including its Homeland Security Operational Analysis Center). These are cited by reference only and remain under their publishers' terms.

### Standards and codes (cited, not reproduced)

The bibliography cites standards and codes from private standards bodies, including ASIS International (with SHRM), ASTM International, the National Fire Protection Association, and the Financial Action Task Force. These are copyrighted by their publishers. THREAT Matrix cites them by title and designation only and reproduces none of their text. Obtain the documents from their publishers.

### Academic, research-institute, and non-governmental publications

Journal articles, research-institute reports, and publications of non-governmental and industry organizations are cited as references. Citation needs no license; reproducing abstracts, figures, tables, or substantial text beyond fair use needs the copyright holder's permission. Publishers in this group include academic journals and university research centers, policy research institutes, counter-terrorism and online-safety organizations, professional and humanitarian security associations, and one commercial analytics firm's published annual report.

### Court documents and legislation

Court opinions, complaints, affidavits, and statutes are cited as public records by case name, docket or citation, and court.

### News reporting

News articles are cited by title, author, outlet, and date. They are copyrighted by their publishers and are not reproduced.

---

## 2. Third-party software

### Distributed with the published site

The published site (`docs/assets/`) contains compiled or copied files from:

| Software | License | Copyright |
|---|---|---|
| React (`react`) | MIT | Copyright (c) Meta Platforms, Inc. and affiliates |
| React DOM (`react-dom`) and its `scheduler` dependency | MIT | Copyright (c) Meta Platforms, Inc. and affiliates |
| IBM Plex Sans font files, via `@fontsource/ibm-plex-sans` | SIL Open Font License 1.1 | Copyright (c) IBM Corp. |

The React license banners are preserved inside the bundle. The MIT License text is available in each package and at https://opensource.org/license/mit.

### Used to build and check, not distributed

These tools are used to build the viewer or to run the checks. They are not part of the published site or data.

| Software | Purpose | License |
|---|---|---|
| Vite (`vite`) and `@vitejs/plugin-react` | viewer build | MIT |
| TypeScript (`typescript`) | type checking | Apache-2.0 |
| `@types/react`, `@types/react-dom` | type definitions | MIT |
| Bun | package installation and build runner | MIT |
| `jsonschema` (Python) and its dependencies | JSON Schema validation in the scripts and CI | MIT |

Exact versions are pinned in `bun.lock` and in `.github/workflows/`. Transitive build dependencies are listed in `bun.lock` with their integrity hashes.

---

## 3. Typeface and third-party requests

The viewer uses the **IBM Plex Sans** typeface, Copyright (c) IBM Corp., licensed under the SIL Open Font License, Version 1.1 (https://openfontlicense.org). The font files are taken from the `@fontsource/ibm-plex-sans` package and are distributed with the published site under `docs/assets/` (the `index-ibm-plex-sans-*.woff2` files). Under the Open Font License the fonts may be redistributed with this project; they remain under that license and are not relicensed under MIT.

The published page loads its script, stylesheet, fonts, and data from its own origin only. It makes no request to any third-party host, and its Content-Security-Policy does not permit one.

---

## 4. Related work and structural pattern

THREAT Matrix organizes behavior into tactics and lifecycle phases, a pattern widely used in threat modeling. Notable examples include the Lockheed Martin Cyber Kill Chain® (Hutchins, Cloppert & Amin, 2011), MITRE ATT&CK®, MITRE CAPEC, MITRE D3FEND, MITRE ATLAS, and the DISARM disinformation framework. The distinction between tactics and techniques predates these works and traces to military and intelligence doctrine.

THREAT Matrix adopts this common organizational pattern and does not reproduce content from any of these frameworks.

### Crosswalk to PACT

`docs/crosswalks/facilities-pact.md` and `docs/crosswalks/facilities-pact.json` relate Facilities tactics to entries of **PACT, the Physical Access and Control Taxonomy** (https://pact.slashsec.at/), which its authors publish under the Apache License, Version 2.0. The crosswalk refers to PACT entries by name and identifier only. It reproduces no PACT descriptions or other PACT content, and it is not reviewed or endorsed by the PACT authors.

### Trademarks

MITRE ATT&CK®, ATT&CK®, D3FEND®, and ATLAS® are registered trademarks of The MITRE Corporation. Cyber Kill Chain® is a registered trademark of Lockheed Martin Corporation. Other names referenced in this repository are the property of their respective owners. THREAT Matrix is an independent work. It is not affiliated with, sponsored by, or endorsed by any of these organizations, or by any publisher, agency, or author it cites.

Reference: https://attack.mitre.org/resources/legal-and-branding/

---

## 5. Proprietary assessment instruments (named, not reproduced)

The framework names the following proprietary threat and violence assessment instruments for context. THREAT Matrix does not reproduce, reconstruct, or redistribute any instrument items, scoring anchors, coding rules, or manual content, and it is not a substitute for any of them.

- **TRAP-18 (Terrorist Radicalization Assessment Protocol-18)** by J. Reid Meloy. Use of the instrument requires authorized training and a license from its publisher. Its constructs are referenced at the level named in the peer-reviewed paper Meloy & Gill (2016), with that citation.

- **WAVR-21 (Workplace Assessment of Violence Risk)** by Stephen G. White & J. Reid Meloy. Use of the instrument requires the manual and approved training from its publisher. THREAT Matrix refers to the instrument by name only and does not list or describe its items.

- **Pathway to Violence model** by Frederick S. Calhoun & Stephen W. Weston, published in *Contemporary Threat Management* (2003) and related works. Referenced as a conceptual model.

---

## 6. Disclaimer

This file is an informational attribution record prepared in good faith. It is not legal advice, it grants no license on behalf of any third party, and it does not warrant that the attribution here satisfies any license obligation of any cited publisher, author, or organization. Anyone who forks, redistributes, builds on, or commercializes this framework is responsible for verifying the third-party permissions that apply to their use. Nothing in this file represents that any cited source has reviewed or approved THREAT Matrix or its use of that source.

The THREAT Matrix framework itself is released under the MIT License: the vocabulary in `docs/data/framework.json`, the experimental scoring overlay in `docs/data/scoring-overlay.json`, the JSON Schemas in `docs/data/`, the viewer source in `src/`, the scripts in `scripts/`, and the examples in `examples/`.

---

*Last updated: 2026-11-15. Revisions are tracked in the repository's git history.*
