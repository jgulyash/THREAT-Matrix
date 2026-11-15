# Candidate public cases for the presence-coding study

**Status: DRAFT candidate list for a draft protocol that has not been run. No case here has been selected, summarised, or coded. Inclusion is not a finding about any person.**

This list supports section 3 of `PROTOCOL.md`. Each row names a matter that is adjudicated or officially closed, and one primary public document of an admitted class (court document, government after-action review, official commission or inquiry report). Rows say only what kind of document exists; they do not characterise any individual beyond the document's own title or caption.

## How links were checked

Every link was requested on 2026-11-15 with:

```
curl -s -o /dev/null -w "%{http_code}" -L -A "Mozilla/5.0" URL
```

| Status in table | Meaning |
|---|---|
| verified (200) | The request returned 200. For PDF links the first pages were also read to confirm the document is the one named |
| blocked to scripts (403), check in browser | The host refuses scripted clients. Where an archived copy returned 200 it is listed second and was read to confirm the document |
| verified (200), landing page | The link is an official index page for the report, not the report file itself; the file must be pinned by hand |

Links that returned 404 were dropped. A 200 proves the link resolves, not that the document is suitable; suitability is decided at case selection under the protocol's eligibility rules.

Class key: **A** attack (carried out or attempted at the target), **D** disrupted (interrupted before execution began), **C** non-attack comparison. Matrix key: **P** People, **F** Facilities. Where both are listed, the first is the better fit.

## Candidates

| # | Case | Year | Class | Matrix | Primary public document | Link | Link status |
|---|---|---|---|---|---|---|---|
| 1 | Tallahassee yoga studio attack | 2018 | A | P, F | US Secret Service NTAC case study (2022) | https://www.secretservice.gov/sites/default/files/reports/2022-03/NTAC%20Case%20Study%20-%20Hot%20Yoga%20Tallahassee.pdf | verified (200) |
| 2 | First Baptist Church of Sutherland Springs attack | 2017 | A | F, P | US Secret Service NTAC case study (2025) | https://www.secretservice.gov/sites/default/files/reports/2025-04/First-Baptist-Church-of-Sutherland-Springs-A-Case-Study-on-the-Link-Between-Domestic-Violence-and-Mass-Attacks.pdf | verified (200) |
| 3 | Marjory Stoneman Douglas High School attack | 2018 | A | F, P | MSD Public Safety Commission Initial Report (2019) | http://www.fdle.state.fl.us/MSDHS/CommissionReport.pdf ; archived copy https://web.archive.org/web/2024/http://www.fdle.state.fl.us/MSDHS/CommissionReport.pdf | blocked to scripts (403), check in browser; archived copy verified (200) |
| 4 | Buffalo supermarket attack | 2022 | A | F, P | New York Attorney General investigative report on online platforms (2022) | https://ag.ny.gov/sites/default/files/buffaloshooting-onlineplatformsreport.pdf | verified (200) |
| 5 | Christchurch mosque attacks | 2019 | A | F, P | Report of the Royal Commission of Inquiry (2020) | https://christchurchattack.royalcommission.nz/ ; archived copy https://web.archive.org/web/2024/https://christchurchattack.royalcommission.nz/ | blocked to scripts (403), check in browser; archived copy verified (200), landing page |
| 6 | Manchester Arena attack | 2017 | A | F | Manchester Arena Inquiry, Volume 1: Security for the Arena (2021) | https://www.gov.uk/government/publications/manchester-arena-inquiry-volume-1-security-for-the-arena | verified (200), landing page |
| 7 | Boston Marathon bombing | 2013 | A | F, P | United States v. Tsarnaev, 1st Cir. No. 16-6001 (2020); see also Supreme Court No. 20-443 (2022), https://www.supremecourt.gov/opinions/21pdf/20-443_new_2d8f.pdf | http://media.ca1.uscourts.gov/pdf.opinions/16-6001P-01A.pdf | verified (200) |
| 8 | Oklahoma City federal building bombing | 1995 | A | F | United States v. McVeigh, 153 F.3d 1166 (10th Cir. 1998) | https://law.resource.org/pub/us/case/reporter/F3/153/153.F3d.1166.97-1287.html | verified (200) |
| 9 | Virginia Tech attack | 2007 | A | F, P | Report of the Virginia Tech Review Panel (2007) | https://scholar.lib.vt.edu/prevail/docs/VTReviewPanelReport.pdf | verified (200) |
| 10 | Sandy Hook Elementary School attack | 2012 | A | F | Report of the State's Attorney for the Judicial District of Danbury (2013) | https://portal.ct.gov/-/media/DCJ/SandyHookFinalReportpdf.pdf | verified (200) |
| 11 | Fort Hood attack | 2009 | A | P, F | US Senate Committee on Homeland Security and Governmental Affairs special report (2011) | https://www.hsgac.senate.gov/wp-content/uploads/imo/media/doc/Fort_Hood/FortHoodReport.pdf | verified (200) |
| 12 | Washington Navy Yard attack | 2013 | A | F | Department of Defense Internal Review of the Washington Navy Yard Shooting (2013) | https://www.defense.gov/Portals/1/Documents/pubs/DoD-Internal-Review-of-the-WNY-Shooting-20-Nov-2013.pdf ; archived copy https://web.archive.org/web/2020/https://www.defense.gov/Portals/1/Documents/pubs/DoD-Internal-Review-of-the-WNY-Shooting-20-Nov-2013.pdf | blocked to scripts (403), check in browser; archived copy verified (200) |
| 13 | Emanuel AME Church attack, Charleston | 2015 | A | F, P | United States v. Roof, 4th Cir. No. 17-3 (2021) | https://www.ca4.uscourts.gov/opinions/173.P.pdf | verified (200) |
| 14 | Inland Regional Center attack, San Bernardino | 2015 | A | F | US Department of Justice COPS Office critical incident review, "Bringing Calm to Chaos" (2016) | https://portal.cops.usdoj.gov/resourcecenter/RIC/Publications/cops-w0808-pub.pdf | verified (200) |
| 15 | Robb Elementary School attack, Uvalde | 2022 | A | F | US Department of Justice Critical Incident Review (2024) | https://cops.usdoj.gov/uvalde | verified (200), landing page |
| 16 | Lewiston attacks | 2023 | A | P, F | Final Report of the Independent Commission to Investigate the Facts of the Tragedy in Lewiston (2024) | https://www.maine.gov/icl/ ; archived copy https://web.archive.org/web/2025/https://www.maine.gov/icl/ | blocked to scripts (403), check in browser; archived copy verified (200), landing page |
| 17 | 11 September attacks | 2001 | A | F | The 9/11 Commission Report (2004) | https://www.9-11commission.gov/report/911Report.pdf | verified (200) |
| 18 | Oslo government quarter and Utoya attacks | 2011 | A | F, P | Report of the 22 July Commission, NOU 2012:14, English version of selected chapters | https://www.regjeringen.no/contentassets/bb3dc76229c64735b4f6eb4dbfcdbfe8/en-gb/pdfs/nou2012_14_eng.pdf ; archived copy https://web.archive.org/web/2023/https://www.regjeringen.no/contentassets/bb3dc76229c64735b4f6eb4dbfcdbfe8/en-gb/pdfs/nou2012_14_eng.pdf | blocked to scripts (403), check in browser; archived copy verified (200) |
| 19 | Nova Scotia mass casualty | 2020 | A | P | Mass Casualty Commission Final Report, "Turning the Tide Together" (2023) | https://masscasualtycommission.ca/final-report/ | verified (200), landing page |
| 20 | Washington, DC area sniper attacks | 2002 | A | P | Malvo v. State, Court of Appeals of Maryland, No. 29, September Term 2021 (2022) | https://www.mdcourts.gov/data/opinions/coa/2022/29a21.pdf ; archived copy https://web.archive.org/web/2024/https://www.mdcourts.gov/data/opinions/coa/2022/29a21.pdf | blocked to scripts (403), check in browser; archived copy verified (200) |
| 21 | Tucson constituent event attack | 2011 | A | P | United States v. Loughner, 9th Cir. No. 11-10339 (2012) | https://cdn.ca9.uscourts.gov/datastore/opinions/2012/03/05/11-10339.pdf | verified (200) |
| 22 | Mass attacks in public spaces, 2016 to 2020 (multi-case report with named case descriptions, including the 2018 Annapolis newsroom attack) | 2016 to 2020 | A | P, F | US Secret Service NTAC, Mass Attacks in Public Spaces: 2016-2020 (2023) | https://www.secretservice.gov/sites/default/files/reports/2023-01/usss-ntac-maps-2016-2020.pdf | verified (200) |
| 23 | Targeted school attacks (41 incidents, schools not named) | 2008 to 2017 | A | F, P | US Secret Service NTAC, Protecting America's Schools (2019) | https://www.secretservice.gov/sites/default/files/2020-04/Protecting_Americas_Schools.pdf | verified (200) |
| 24 | Averted school attack plots (67 plots, anonymised) | 2006 to 2018 | D | F, P | US Secret Service NTAC, Averting Targeted School Violence (2021) | https://www.secretservice.gov/sites/default/files/reports/2021-03/USSS%20Averting%20Targeted%20School%20Violence.2021.03.pdf | verified (200) |
| 25 | United States v. Hasson | 2019 | D | P | 4th Cir. No. 20-4126 (2022) | https://www.ca4.uscourts.gov/opinions/204126.P.pdf | verified (200) |
| 26 | Fort Dix plot (United States v. Duka) | 2007 | D | F | 3d Cir. Nos. 09-2292 and consolidated (2011) | https://www2.ca3.uscourts.gov/opinarch/092292p.pdf | verified (200) |
| 27 | Los Angeles airport millennium plot (United States v. Ressam) | 1999 | D | F | 9th Cir. en banc No. 09-30000 (2012) | https://cdn.ca9.uscourts.gov/datastore/opinions/2012/03/12/09-30000.pdf | verified (200) |
| 28 | Portland tree-lighting plot (United States v. Mohamud) | 2010 | D | F | 9th Cir. No. 14-30217 (2016) | https://cdn.ca9.uscourts.gov/datastore/opinions/2016/12/05/14-30217.pdf | verified (200) |
| 29 | Averted School Violence database (anonymised averted and completed incidents; registration required) | ongoing | D | F, P | National Policing Institute, Averted School Violence database | https://www.avertedschoolviolence.org/ | verified (200), landing page |
| 30 | Federal extremism prosecutions, charging documents for interrupted plots (library, not a single case) | ongoing | D | P, F | George Washington University Program on Extremism, court document library | https://extremism.gwu.edu/legal-documents | verified (200), landing page |
| 31 | Watts v. United States | 1966 (decided 1969) | C | P | US Supreme Court, 394 U.S. 705 (1969) | https://www.law.cornell.edu/supremecourt/text/394/705 | verified (200) |
| 32 | United States v. Bagdasarian | 2008 (decided 2011) | C | P | 9th Cir. No. 09-50529 (2011) | https://cdn.ca9.uscourts.gov/datastore/opinions/2011/07/19/09-50529.pdf | verified (200) |
| 33 | Counterman v. Colorado | 2014 to 2016 (decided 2023) | C | P | US Supreme Court No. 22-138 (2023) | https://www.supremecourt.gov/opinions/22pdf/22-138_43j7.pdf | verified (200) |
| 34 | Elonis v. United States | 2010 (decided 2015) | C | P | US Supreme Court No. 13-983 (2015) | https://www.law.cornell.edu/supremecourt/text/13-983 | verified (200) |

Counts: 34 rows; 23 attack, 7 disrupted, 4 comparison (11 disrupted or comparison). 13 People-first or People-only, 21 Facilities-first or Facilities-only.

## Notes on particular rows

- **Rows 22, 23, 24, 29, 30 are collections, not single cases.** Each can yield several narratives. Rows 23, 24, and 29 are anonymised by their publishers, which suits the study's privacy rules but limits checking against other records.
- **Rows 14 and 15** are reviews of the emergency response. They hold little about behavior before the event and are candidates mainly for Facilities execution-phase tactics.
- **Rows 20 and 21** are opinions on sentencing and on competency. The factual background sections are short; they may not support a full narrative and would need a second admitted document.
- **Rows 26 and 28** involved government informants or undercover agents. That is part of the public record and must be stated in the narrative, since some observed behaviors were responses to an agent.
- **Rows 5, 6, 15, 16, 19** link to official landing pages. The report files themselves must be pinned by hand at case selection, with a checksum.
- **Rows with archived copies.** The archive link is given so the document can be read today; the live host link is given so the official location is on record.
- **Rows 31 to 34 are threat-communication cases, not benign cases.** See the next section.
- **Pending matters are excluded.** Several recent, well-documented incidents have detailed public charging documents but are not adjudicated. They are left out until they are.
- **Earlier project research** identified further repositories (state commission reports, additional NTAC and FBI publications, court-record archives). Several official hosts refuse scripted clients and could not be confirmed here; they are not listed.

## The comparison-case problem

True non-attack comparison cases are hard to source from public documents, and this list does not solve that.

Why: courts, commissions, and after-action reviews exist because something happened or was charged. A concern that was assessed and found benign leaves no public adjudicated record, and where records exist (school, workplace, clinical) they are private and must stay so.

What the four listed comparison rows are: appellate decisions about communications alleged to be threats, where the public record describes the communications and the surrounding conduct and describes no attack. In two (rows 31 and 32) the conviction was reversed. In two (rows 33 and 34) the Supreme Court set aside the judgment below on the mental-state standard and returned the case to the lower courts; what happened afterwards must be checked and stated in the dataset record. These are useful because the record shows concerning language without attack preparation, which tests whether raters code only what the text shows. They are not a sample of benign outcomes, they involve only communication-type behavior, and all four fit the People matrix; there is no Facilities comparison case on this list.

Proposed ways to find more, in order of preference:

1. **Published threat assessment case studies with benign or managed outcomes** in government guides. NTAC and FBI guides include short vignettes of concerns that were assessed and resolved without violence. They are anonymised and official. They are short, so several may be needed to exercise many indicators. The FBI guide "Making Prevention a Reality" (https://www.fbi.gov/file-repository/making-prevention-a-reality.pdf/view) is blocked to scripts (403), check in browser. The NTAC workplace guide (https://www.secretservice.gov/sites/default/files/reports/2026-10/Preventing-Targeted-Workplace-Violence-A-U.S-Secret-Service-Guide-to-Behavioral-Threat-Assessment-and-Management.pdf) returned 200. Whether either holds vignettes long enough to use is to be confirmed by reading them.
2. **Averted-plot collections** (rows 24 and 29). These are disrupted cases, not benign ones, but the NTAC averted-plot report describes plots at very different stages, including some stopped at the communication stage.
3. **Acquittals and reversals with a published factual record**, beyond rows 31 and 32, where a court set out the conduct and found it did not amount to the offence charged.
4. **Civil and administrative decisions** (for example published employment tribunal or arbitration decisions about dismissals for alleged threats, and published protective-order appeals) where the decision-maker found no threat. These are adjudicated and public but involve private individuals; under the protocol's privacy rules narratives would use roles only, and each would need a case-by-case check that publication adds nothing beyond the decision.
5. **Facilities comparisons** from published trespass, photography, or suspicious-activity decisions where a court or official review found an innocent explanation. None has been identified yet.

What is not acceptable: inventing comparison narratives, using news reports of "false alarms", or using any non-public record.

If, after this search, fewer than four usable comparison cases per matrix can be assembled, the protocol requires that to be logged as a deviation and stated as a limitation. For the Facilities matrix that outcome is likely.
