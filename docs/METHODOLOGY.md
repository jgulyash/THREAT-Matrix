# THREAT Matrix Methodology

This document explains how THREAT Matrix content is scoped, written, scored, checked, and grounded. It is written for security and threat-assessment professionals weighing adoption.

## 1. Scope and authorship

THREAT Matrix catalogs observable threat actor behavior against four target matrices: People, Facilities, Organizations, and Infrastructure. Each matrix runs across four lifecycle phases: Target Development, Mobilization, Execution, and Aftermath. The phases describe common patterns, not a required sequence. Threat actors skip, compress, and reorder them.

| Object | Count |
|---|---|
| Tactics | 161 |
| Indicators | 828 |
| Countermeasures | 641 |
| Response protocols | 322 |
| Actor profiles | 32 |

Each tactic sits in exactly one matrix, set by what the threat actor's primary objective targets. Motivation lives in actor profiles, not in matrix placement. A real incident can touch several matrices at once, and the Detection Mesh links those behaviors across matrices.

**Out of scope.** The framework does not contain exploit code, weapon construction, step-by-step attack tradecraft, or targeting information about specific persons or organizations. It describes behavior at the tactic and indicator level. It does not ship case data. Instance records, deployment records, and coverage derivations are held by the adopting organization.

**Maintenance.** The project is maintained by its author, with public sources cited throughout. It is released under the MIT license. Content and schema carry separate semantic version numbers under the published versioning policy, and stable identifiers are never reused.

## 2. Indicator rubric

Every indicator is a type-level description of a behavior class. It is not a case. The fields below are scored for the class as written, never for a vivid hypothetical instance.

**Escalation axes.** Each indicator carries four authored values from 0.0 to 10.0, recorded to one decimal place:

- **impact_potential** is the harm the behavior directly produces or imminently enables.
- **blast_radius_potential** is the total affected scope, meaning victims, stakeholders, or downstream population.
- **recoverability_inverse** is how hard the harm is to undo. Higher means harder.
- **detectability** is how observable the behavior is to trained personnel or telemetry.

Each matrix anchors these axes to its own harm type. Physical consequence anchors Infrastructure. Stakeholder scope anchors Organizations. The anchors live in the escalation rubric inside the framework data. Aftermath indicators score only the scope they enable going forward. The completed attack's scope belongs to the execution-phase indicators.

**Computed weight.** The escalation weight is computed at merge and never hand-authored:

```
escalation_weight = (impact × blast_radius × recoverability_inverse × (10 − detectability))^(1/4)
```

The geometric mean means one low axis pulls the whole weight down, so no axis can fully compensate for another. Detectability is inverted because an observable behavior leaves an interdiction window. The weight therefore reads as expected residual harm. A high weight on a stealthy behavior does not mean stealth is severe. It means the interdiction discount is gone.

**Bands.** The weight maps to a severity band at fixed thresholds:

| Band | Weight from |
|---|---|
| low | 0.0 |
| medium | 3.0 |
| high | 5.0 |
| critical | 6.5 |

The low band holds behaviors whose direct residual harm is investigative or attributional trace: egress, cleanup, attribution, and ambient pre-operational reconnaissance. The cut was set to keep false lows to a minimum, because under-triaging a real signal is the most dangerous miss.

**Severity floor.** An indicator whose behavior applies direct physical force to a person carries a band of critical whatever its weight. Force includes weapon discharge, ramming, detonation, assault, restraint, and taking or holding custody of a person by weapon threat during an attack in progress. The rule exists because the weight gates the top band on population scope, which would leave a single-victim killing at high. The weight itself is never floored, so the gap between one assault and a mass bombing stays visible. The floor is narrow on purpose. It applies only where critical is always correct. In Infrastructure it covers only execution behaviors whose direct mechanism is casualties. In Facilities it also covers three indicators that stage a second strike against responders or evacuees during an active incident: a secondary device on a responder route, an overwatch position over the response zone, and an unattended package at an assembly area. Organizations has no floor.

**Temporal signature.** A categorical value records how close to action the behavior typically appears: horizon, advancing, imminent, staging, in progress, or aftermath. This measures how soon, not how bad.

**informs_axes.** Each indicator also records what observing it reveals on six axes. Three concern the threat actor: capability, intent, and opportunity. Three concern the postulated event: timing, target, and method. Each axis takes none, weak, moderate, or strong. The scale measures resolution, not severity. Weak resolves only the coarsest fact on that axis. Moderate adds one narrowing below it. Strong pins a specific value. Intent is read as general intent to act, never specific motive. Opportunity at moderate means informational opportunity, such as pattern-of-life or security-gap knowledge. Strong means realized opportunity to act. Values are categorical only.

**Modality facets.** Each indicator carries a modality and a human_social flag. Modality follows the behavior's instrument, never its effect, its target's importance, or the channel it travels through:

- **physical** means matter, force, or presence is the instrument.
- **cyber** means the instrument acts on a computing system's technical properties, including reading exposed data.
- **cyber_physical** means the behavior itself crosses the seam, and it must name a crossing mechanism.
- **human_social** means the mechanism lies in the human, social, or institutional domain. This includes persuasion, coercion, legal or financial pressure, and the threat actor's own warning behaviors.

The flag is set whenever human tradecraft appears anywhere in the behavior. Concealment takes the modality of what it operates on. Bundled alternatives take the modality of the branch that achieves the objective.

**Target fields.** People indicators record target_identity. Facility indicators record facility_target_scope and within_site_focus. All three use the revealed reading. A value is tagged only when observing the behavior actually reveals it. Capability, financing, cover, and most aftermath evasion reveal nothing about the victim and stay empty. Site-directed observation of a subject's home or office reveals the specific known person or persons.

**Conditioning guidance.** Each indicator names the instance factors that are the hidden drivers of danger for its class. It uses machine-readable probe factors plus a directive of up to 420 characters telling the analyst what to collect. The six factors are target focus, pathway stage, means in hand, tempo and trajectory, proximity and access, and source credibility. The guidance is assessment tasking only, and response actions live in the tactic's response protocols. Claims are hedged in both directions, and no entry claims an act settles the threat actor picture. The guidance does not affect the score.

**Instance conditioning.** A band becomes a case priority only when joined to an instance record. The join may raise priority above the type band and may never lower it. Two checks enforce this. The schema rejects a conditioned priority below the stated band. The validator confirms the stated band matches the authored band. Cases leave a queue by disposition, never by score demotion.

**Mesh links.** A cross-matrix link is valid only when both behaviors meet one of three tests. They are the same act, they share one literal resource, or they are one whole-actor signal such as a final-act signature. Different methods, different artifacts, or shared category alone make a link invalid.

**Coverage.** Countermeasures link to the indicators they act on, typed as prevent, detect, or deny. An organization's coverage band is derived from its own deployment records. Detection alone caps coverage at partial.

## 3. Review process

Content reaches a release only after it passes a fixed sequence of gates. The same checks run in a local pre-commit hook and in continuous integration on the development and release branches.

1. **Framework validator.** This runs twenty-seven numbered checks: duplicate identifiers, dangling references, matrix and prefix agreement, misspelled keys, band and weight consistency, valid lifecycle values, and the escalate-only rule.
2. **Fixtures.** Twenty-two fixture copies of the data must each behave as expected: deliberately broken copies fail the specific check they target, and conforming copies pass.
3. **Field parity.** Any field fully populated in one matrix must not be missing from another, unless a documented design decision allows it. Every matrix must carry its own indicator mesh.
4. **Mesh references.** Every correlation, compensation, and coordination reference must resolve to an existing identifier of the right type and format.
5. **Consumer smoke test.** The reference consumer loads and schema-validates the data, reads every matrix, and runs the instance-conditioning join against the template and worked cases.
6. **Bundle freshness.** The published viewer must match a fresh build of the current data, so the site never shows stale content.

Prose is written to locked voice rules. Description comes first and taxonomy second, and citations live in source references rather than in prose. Observable action replaces academic phrasing, and register follows the declared evidence basis. "Threat actor" is the only label for the actor, and repeated openers are capped across the corpus.

Versioning is semantic. Content and schema version separately. A published version is frozen, and corrections ship as a new patch with a changelog entry. Major releases are announced at least thirty days ahead with a migration guide. Deprecation follows four lifecycle states: active, deprecated, superseded, and reserved. A deprecated item stays for at least one minor release, and its identifier is kept permanently. Items never change parent tactic. A move is handled as supersession.

## 4. Evidence basis

Every tactic declares an `evidence_basis` value stating where its structure came from.

- **practice_led** means tactic structure and indicators were authored from practitioner experience. Every indicator cites public sources that corroborate the pattern.
- **practice_and_literature** means the tactic was authored from practice and published literature together. Public sources are cited throughout.
- **literature_led** means the tactic was derived mainly from published literature with practitioner review.
- **literature_only** means the tactic was derived from published literature. No practitioner origin is claimed.

| Value | Tactics | By matrix |
|---|---|---|
| practice_led | 10 | facility 9, person 1 |
| practice_and_literature | 111 | person 33, facility 31, organization 47 |
| literature_led | 1 | infrastructure 1 |
| literature_only | 39 | infrastructure 37, organization 2 |

Whatever the value, every tactic, indicator, countermeasure, and response protocol cites public sources only.

These value names arrive with schema 3.0.0. They map from the 2.1.0 names: operational_primary maps to practice_led, hybrid to practice_and_literature, literature_primary to literature_led, and literature_only is unchanged.

## 5. Reliability

A reliability study with credentialed practitioners is planned. Its design:

- Four to six credentialed reviewers who had no part in authoring the content.
- Thirty to forty vignettes, mixed across matrices and severity.
- Each reviewer separately marks which indicators are present in each vignette.
- Agreement is reported per matrix, and low-agreement indicators go back for rewrite.

Results will be published here when the study is complete.

## 6. Document history

This file consolidates the former `docs/methodology` folder into one reference. Normative rules from that folder are absorbed into the sections above, and the coverage derivation rule is carried in full in Appendix A. Dated records and historical designs are retired from the working tree and remain available in the repository's version history.

| Former file | Disposition |
|---|---|
| README.md | Replaced by this document |
| aftermath-seam-reconciliation.md | Section 2 |
| bottom-cut-recalibration.md | Section 2 |
| conditioning-guidance-authoring-rubric.md | Section 2 |
| conditioning-guidance-field.md | Section 2 |
| coverage-derivation.md | Appendix A (in full) |
| informs-axes-boundary-rubric.md | Section 2 |
| instance-conditioning-contract-completion.md | Section 2 |
| mesh-link-rubric-v2.md | Section 2 |
| modality-authoring-rubric.md | Section 2 |
| people-target-identity-revealed-guide.md | Section 2 |
| severity-floor-clarifications.md | Section 2 |
| target-dimension-rubric-LOCKED.md | Section 2 |
| v1-6-1-contract-clarifications.md | Sections 1, 2, and 3 |
| scope-findings.md | Retired (dated working record) |
| FINDINGS.md | Retired (dated working record) |
| architect-detection-mesh-assessment.md | Retired (dated working record) |
| facility-bibliography-research-20260706.md | Retired (dated working record) |
| KAPPA-RESULTS.md | Retired (dated working record) |
| architect-routing-rules.md | Retired (historical design) |
| architect-sub-dimension-and-schema-patch.md | Retired (historical design) |
| B1-infrastructure-scaffold-design.md | Retired (historical design) |
| B1-infrastructure-scaffold-design-v2-APPROVED.md | Retired (historical design) |
| cross-domain-mesh-scope.md | Retired (historical design) |
| DESIGN-b5-infra-escalation-scoring.md | Retired (historical design) |
| DESIGN-b5-org-escalation-scoring.md | Retired (historical design) |
| RATIONALE-cpn-modality-and-mesh.md | Retired (historical design) |
| v2-design-constraints.md | Retired (historical design) |

## Appendix A. Coverage derivation rule (normative)

The coverage band is the vulnerability term of the risk equation. It answers, for one protected target and one indicator, whether the organization has deployed countermeasures that act on that behavior. The framework defines the shapes and this rule; each organization holds its own records. Machine shapes: `data/coverage.schema.json`. This appendix is normative for the derivation.

### Inputs

1. The framework's `mitigates` relation: countermeasure to indicator edges, each typed by function (`prevent`, `detect`, `deny`). An edge asserts that the countermeasure acts on that behavior's pathway. Edges may cross tactics; a countermeasure reaches wherever its function genuinely acts.
2. The organization's `cm_deployment_record` for the protected target: which countermeasures are deployed, where they apply, and when they were last verified operational.
3. The indicators in scope: a live case's indicator set, or a what-if set.

### The derivation, per target and indicator

1. Collect the mitigating countermeasures for the indicator from the `mitigates` relation.
2. If the indicator carries no `mitigates` edge because it is marked `not_assessable` (no organizationally deployable control exists for the behavior), the band is `not_assessable`. It is excluded from `covered` and it never drives a posture step up.
3. Intersect the mitigating countermeasures with the target's deployments. Exclude before banding:
   - deployments whose `applies_to` scope does not reach the assessed target;
   - deployments with status `planned` or `not_deployed`;
   - deployments that are unverified, or whose `verified` date is older than the staleness window (default twelve months) at derivation time; these contribute at most `partial`;
   - countermeasures the assessed threat actor's position defeats, such as access controls whose credentials the actor holds. Actor position is a case attribute on the threat side; a control the actor operates is not a control against that actor.
4. Band the result:
   - `covered`: every relevant mitigating countermeasure class is deployed, verified, and in scope, and at least one contributing edge has function `prevent` or `deny`. Detection alone does not fully cover a behavior; a detect-only edge set caps the band at `partial`. An edge with function `unreviewed` also caps at `partial`; unreviewed edges must reach zero before the coverage layer ships.
   - `partial`: some mitigation is deployed, or contributing deployments are unverified, stale, out of scope in part, or detect-only.
   - `exposed`: no relevant mitigating countermeasure is deployed, or critical path dominance applies.
5. Critical path dominance: if the countermeasures mitigating the highest severity band indicators in play are absent, the band is `exposed` regardless of other deployments. The absent countermeasures are recorded as the gap list.

### How coverage enters posture

The published posture matrix remains the reference join. Coverage adjusts within it, upward only:

- `exposed` steps `maintain` to `watch` and `watch` to `harden`. At a cell already at `harden` or above, `exposed` does not raise the tier further; it flags the gap as top priority within that tier.
- `covered` never lowers a cell automatically. An organization may take a signed deviation downward on the strength of verified coverage; the deviation machinery owns that move.
- `partial` holds the cell; the gap detail rides the documented rationale.

### Statelessness

The derivation is a function of the current records, recomputed at each derivation. It is not a ratchet. When remediation closes a gap and a re-derivation returns the cell to its default, that return is not a deviation and requires no signature; the signed deviation machinery applies only to moves below the cell default.

### The audit line

Every derivation records: the target, the indicator, the band, the derivation date, the framework version whose `mitigates` relation it ran against, and the age of the oldest input consumed. A stale join is visible on its face.

### The disposition discipline

An `exposed` band must carry a disposition: `funded`, `accepted_with_rationale`, `transferred`, or `compensating_interim`, with a review date. This keeps the record a remediation register rather than a gap map. A gap with a funded plan and a review date is a defensible record; a bare exposed flag with silence after it is not. Deployment records and derivations are consumer held, never published, and organizations with live litigation exposure should structure record generation under counsel.
