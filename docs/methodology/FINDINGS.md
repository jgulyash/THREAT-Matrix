# THREAT Matrix Scoring Methodology — No-B.S. Review (V1.2.2)

Status: DRAFT — empirical + FirstPrinciples findings settled; perspective agents (maintainer/ops) and RedTeam pending fold-in.

## The headline finding (F1) — the VBIED gap is a category error, not a scoring bug

Jay: "a VBIED build manual scores high unless the actor is illiterate." Correct that the type-level `escalation_weight` (5.82–5.98, "high" for weapon-construction) does not move for an incapable actor. But FirstPrinciples shows this is NOT fixable inside the weight: `escalation_weight`'s inputs are properties of the indicator CLASS; "this actor is illiterate" is a property of the INSTANCE. A function over the class cannot output an instance fact.

Realized threat = COMPOSITION of two orthogonal quantities:
1. class escalation potential (ships today, honestly unconditioned) — "acts of this kind tend to be this severe."
2. instance capability/credibility discount (MISSING as a first-class object) — "can THIS actor execute this class."

They must not be silently averaged into one number: a "scary act, can't do it" case and a "can do it, not scary" case would collapse to the same middle value yet are operationally opposite. The framework already forbids this exact move for informs_axes ("do not average two sub-meanings to a false-precise middle") — the same discipline applies here.

Consequence: the fix is not a smarter weight. It's (a) give instance-capability a first-class home, (b) define the composition rule explicitly. This ALSO explains the acquisition cap/intent IRR inversion (F2).

## F2 — the acquisition capability/intent IRR inversion is the same bug in miniature
Jay coded acquisition indicators strong-capability/moderate-intent; locked doctrine says moderate-capability/strong-intent. Root cause: Jay annotated "realized ability to act" (acquiring a weapon → they can act → strong capability); doctrine annotated "what the class reveals" (buying takes resolve not skill → strong intent, moderate capability). Two different variables. Neither is wrong; the field conflates them. RESOLUTION for the 8 held IRR cells: adopt doctrine (moderate-cap/strong-intent) for the type-level informs_axes value, because informs_axes IS the "what-does-the-class-reveal" construct by definition; capture Jay's "realized ability" reading as the (missing) instance-capability object, not as informs_axes.actor_capability.

## F3 — severity_band has near-zero discriminative power (EMPIRICAL)
23 scored indicators: 20 high / 3 medium / 0 low / 0 critical. 87% "high"; the band never fires low or critical. A triage signal that says "high" for ~everything is noise, not signal. Weight range is 4.70–6.44 (span 1.74 on a nominal 0–10 scale). Targeted-assassination prep (~6.14) sits in the SAME band as sustained online research (5.67) and blueprint study (6.15) — the band cannot separate attack-prep from Googling.

## F4 — the person matrix structurally cannot reach "critical" (EMPIRICAL + arithmetic)
"critical" needs weight ≥7.5. With the geometric-mean formula, that requires a high blast_radius_potential (~8). The person matrix is single-subject, so blast_radius is definitionally 2.5–3.0 (only two values observed, stdev 0.25). Therefore no person-matrix indicator can EVER be "critical," and the top band ("high") is the de facto ceiling — collapsing all severe person-directed threats into one bucket. This is a design choice (multiplicative low-variance term) masquerading as a limit.

## F5 — blast_radius_potential does not earn its formula slot in the person matrix (EMPIRICAL)
Only two distinct values (2.5, 3.0), stdev 0.25 — a near-constant. It occupies 1 of 4 multiplicative slots, carries ~zero discriminative signal, and drags every composite toward the middle (a ~2.7 multiplier against ~7–8 terms compresses the range). It is the primary cause of both F3 (compression) and F4 (critical-unreachable).

## F6 — detectability-flip is DEFENSIBLE (DOWNGRADED after maintainer steelman + RedTeam-in-advance)
weight uses (10 − detectability), so stealthier → higher weight. This is CORRECT, not a flaw: detection is the defender's primary interdiction lever, so a covert capability of equal impact warrants more concern (stealth removes the intervention window). Matches CVSS/insider-threat/CT convention. Sign is well-motivated. HONEST CAVEAT (not a retraction): detectability is the most context-dependent of the four axes (the consumer's own sensors change it), so it's the axis most in tension with being "type-level"; and a data paradox — the stealthiest/highest-weighted indicators are the ones least often observed. ACTION: document the "expected residual harm" reading so a consumer doesn't misread stealth as severity. NOT a formula fix.

## F7 — geometric-mean weakest-link penalizes concentrated (targeted) severity (DESIGN)
Geometric mean = any low axis tanks the composite. For the person matrix the "low axis" is ALWAYS blast_radius (single-subject). So the formula systematically penalizes exactly the person matrix's core threat model: high-impact, low-blast, targeted attacks (assassination, stalking-to-lethal). Weakest-link is a defensible security heuristic in general, but here the "weakest link" is a near-constant that isn't a weakness — it's the matrix's definition.

## F8 — per-indicator deviation happens (61%) but doesn't move the band (EMPIRICAL)
14/23 (61%) deviate from category default on ≥1 axis — so scoring is NOT merely category-level (this REFUTES a natural criticism). But because of F5 compression, even real deviation rarely crosses a band threshold. The per-indicator work is real yet largely invisible in the output that consumers triage on (severity_band). Effort is being spent where it doesn't surface.

## F9 — instance-conditioning surface is per-tactic and thin (EMPIRICAL)
`assessment_guidance` (credibility/capability anchors) exists on 4/34 tactics (all 4 chunk-1). It is per-TACTIC — coarser than the per-indicator scores it would condition. And structurally it is a READING AID ("how to assess capability from evidence"), not a SCORE-CONDITIONER ("multiply the class weight by an instance discount"). So even where populated, it does not close the VBIED gap — it tells the analyst to think about capability but gives the tool no place to record the instance discount.

## F10 — definitional bootstrapping in some informs_axes classes (from IRR session)
Classes like IND-0104-02 ("items operationally relevant to the planned attack method") and IND-0104-06 ("to obtain attack-relevant items") presuppose observer knowledge of the attack. Their threat_method / intent signal is then partly baked into the definition rather than observed — circular. Audit which classes do this; consider rewording to observable-only criteria.

## F11 — the 4-bucket informs_axes scale is the right call for now (from IRR data)
This IRR's disagreements were 46/48 one-step, 0 three-step; the moderate/weak boundary carried most of them. That is exactly the signal a finer scale would WORSEN (more boundaries). AC2 0.78 is substantial at 4 buckets. Verdict: keep 4 buckets; the "low-moderate" nuance belongs in the (missing) instance layer, not in more type-level buckets. Numeric summing across axes (Jay's 14/18 idea) stays out — it asserts axis commensurability the axes don't have.

## ROOT CAUSE (maintainer synthesis) — F3+F4+F5 are one failure, not three
A geometric mean (power-mean p=0, the MOST impact-suppressing point) over four axes where blast is pinned low (2.5–3.0), scored against equal-quartile thresholds (0/2.5/5/7.5) calibrated for a 0–10 spread the data never reaches (4.70–6.44). That single structure produces the compressed range (F5), the 87%-high degenerate band (F3), and unreachable-critical (F4) at once. TWO fixes move all three: (a) a within-matrix-CONSTANT axis must not drive intra-matrix ranking/banding — factor blast OUT of the person-matrix composite (keep it in the SCHEMA; it's a legit cross-matrix axis that varies in facility/infra and is what makes "critical" mean the same everywhere); (b) recalibrate person-matrix band thresholds to the realized range (or stop showing empty standalone bands). Refinement to F4: critical-unreachable is FINE if critical = cross-matrix mass-casualty (cross-matrix discipline preventing person-matrix inflation); the real indictment is the degenerate WITHIN-person band from uncalibrated thresholds, not the ceiling itself.

## F1 STRENGTHENED — type/instance separation is the framework's BEST decision (maintainer + FirstPrinciples converge)
Independent convergence: the type-level/instance-level split is exactly CVSS Base vs Temporal/Environmental, and ATT&CK techniques carrying no actor weighting (analyst overlays the adversary). Under this design Jay's VBIED critique is NOT a bug — the manual SHOULD score high (severe behavior class); illiteracy is instance info the analyst applies to get realized risk. The catch: the two-layer design is only honest if BOTH layers exist. Layer 1 (type score) shipped but degenerate; Layer 2 (instance conditioning) is ~12% prose, no structured modifier, no read-time step — effectively unbuilt. So the type-level "high" is consumed AS IF final — exactly Jay's observed failure. "Capability is the analyst's job" is architecturally right (category error to bake it into the type score) but operationally unbacked. The BEST decision and the WORST outcome are the same fact from two sides: the architecture is right; the half that makes it honest was never finished.

## F12 — the false-LOW is deadlier than the false-HIGH (ops-analyst)
Jay's VBIED worry is the false-HIGH direction (incapable actor over-rated). Working-analyst view: the deadlier miss is the false-LOW — a class whose TYPE looks mild but whose INSTANCE (specific target + acquired means + a date) is screaming; the type score cannot hear it. Capability is the MOST volatile, most-acquirable, easiest-to-be-wrong-about variable; grievance and intent are the stable signals. A tool that nudges analysts to discount on presumed incapacity (exactly Jay's instinct on the illiterate) teaches a dangerous reflex — he buys a pre-made weapon or recruits someone who can. IMPLICATION: instance-conditioning must be able to raise as well as lower, and capability-discount specifically should be handled with suspicion, not automated.

## F13 — a computed capability "discount" is the wrong fix (ops-analyst, corrects earlier F1 phrasing)
Do NOT collapse instance capability into the weight as a computed multiplier. It launders a soft, uncertain judgment into false-precision math and can SILENTLY suppress a live case (the day the formula down-weights the one that mattered, no one can see why). Correct shape: TWO separate objects — (1) type weight as a stable coarse PRIOR, (2) a REQUIRED, STRUCTURED instance record (target-focus, pathway stage, means-in-hand, tempo, source credibility) captured separately — surfaced TOGETHER everywhere the score travels, bound so a queue/handoff/dashboard cannot separate them. The failure mode is the number arriving somewhere the conditioning didn't. assessment_guidance is the right SHAPE but prose-on-4-of-34-tactics is a suggestion, and suggestions lose to volume; it must be a required field, not a paragraph.

---
## RECOMMENDATIONS (design only — nothing written to framework.json this session) — DRAFT pre-RedTeam
R1 (VBIED gap / F1,F13): do NOT patch escalation_weight. Add a first-class, REQUIRED instance-conditioning record (separate object), bound to the type score wherever it travels. Never a computed discount. V1.3+ (schema work).
R2 (held IRR cells / F2): adopt DOCTRINE for the 8 held acquisition cells (moderate-cap/strong-intent) because informs_axes IS the what-the-class-reveals construct; capture Jay's realized-ability reading in the new instance record, not in informs_axes.actor_capability. Unblocks reconciliation NOW.
R3 (severity_band / F3,F4,F5,F12): de-emphasize or fix severity_band before it misleads. Options: (a) drop blast_radius from the person-matrix composite (it's a near-constant that causes the compression + critical-unreachability), or (b) recalibrate person-matrix thresholds so the band actually discriminates, or (c) mark severity_band non-authoritative for the person matrix pending fix. Pick in Council/with Jay. V1.3.
R4 (detectability-flip / F6): document the "expected residual harm" reading explicitly OR split detection out of the escalation composite; a consumer must not read stealth as severity unknowingly. V1.3.
R5 (bootstrapping / F10): audit the presuppositional classes; reword to observable-only criteria. V1.2.2-final candidate (prose).
R6 (scale / F11): keep informs_axes at 4 buckets; no numeric summing. Settled — no action.
R7 (deviation invisibility / F8): once the band is fixed, per-indicator deviation will surface; until then flag that deviation work isn't reaching consumers.

## RedTeam-hardened deltas (VERIFY pass, 2026-07-03)
- R1: SURVIVES-W-CAVEAT. Add: the instance record must be enforced at the CONSUMER/DISPLAY contract (score non-renderable/non-rankable without its instance record), or it degrades to assessment_guidance's 12% fate. "Required field" alone loses to volume.
- R2: SURVIVES but CONTINGENT ON R1 — routing Jay's realized-ability read into the instance record only works if the record ships. If R1 dies, revisit R2.
- R3: HARDENED — "de-emphasize/annotate" was too soft; the band is actively harmful as shipped (false authority on a degenerate distribution). DEFAULT: suppress standalone severity_band for the person matrix until recalibrated. Do BOTH fixes (drop blast from intra-person composite + recalibrate thresholds) — they're one root cause.
- R4/R6/R7: SURVIVE. R4 doc must note stealthiest = least-observed (self-censoring axis).
- R5: SURVIVES-W-CAVEAT — reword for observability WITHOUT narrowing scope; test each reword against the indicators it currently catches.
- R8 (NEW — the finding all 7 missed): COVERAGE. Every rec optimizes the scored 12%; 88% of the person matrix has NO score and NO conditioning surface. Decide explicitly: pilot (say so; don't let consumers read partial as complete) or shipped feature (coverage is P0 above every formula fix). The deadliest false-LOW miss lives disproportionately in the unscored 88%.

## SEVERITY RANKING + VERSION ROUTING
P0 (correctness/safety): R8 coverage decision; R3 suppress-degenerate-band. These are where a real miss originates.
P1 (unblocks current work): R2 adopt doctrine for 8 held IRR cells (do NOW — unblocks reconciliation). Contingent flag on R1.
P1 (architecture): R1 instance-conditioning record as first-class object w/ display-binding — V1.3 schema work (the honest Layer 2).
P2 (correctness, non-urgent): R3 formula fix (drop blast from intra-person composite + recalibrate) — V1.3.
P2 (docs): R4 document detectability reading; R5 reword bootstrapped classes (V1.2.2-final prose candidate).
Settled/no-action: R6 (4 buckets), R7 (observation).
