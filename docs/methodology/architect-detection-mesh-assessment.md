# Detection Mesh — V1.2.2 architectural assessment

**Scope.** Read-only assessment of Detection Mesh as a feature in THREAT Matrix today. Focus question: real feature or structural placeholder? Inputs: `docs/data/framework.json`, `docs/data/framework.schema.json`, the React SPA in `src/`, `CONTRIBUTING.md`, `ROADMAP.md`, `CHANGELOG.md`, `docs/`. No edits made.

---

## A) Detection Mesh design intent

The `detection_mesh` block (`framework.json:13198–13228`) defines Detection Mesh as a five-axis cross-cutting property of the framework. Key passages, verbatim:

> "THREAT Matrix treats detection and response as a mesh, not a chain. Indicators from any phase, any matrix, and any detection domain can correlate with indicators from anywhere else in the framework. Countermeasures from any domain can compensate for gaps in another. Response protocols from any stakeholder … can fire in parallel on the same indicator set, each acting within their own authority."

The five axes are named and described:

- `cross_phase` — "An indicator observed in one phase can correlate to an indicator observed in another phase for the same actor."
- `cross_matrix` — "Adversaries do not respect matrix boundaries. The mesh weaves the four matrices (Person, Facility, Organization, System) into one coherent detection space."
- `cross_domain` — "Detection sources are cross-domain … Any domain's signal can activate any phase's detection."
- `cross_countermeasure` — "Countermeasures from any domain can compensate for gaps in another. Defense-in-depth is structural in the framework via the `compensates_for` links."
- `cross_stakeholder` — "Response protocols fire in parallel, not sequentially … coordinated via the `coordinates_with` links."

`schema_links` names the three carrying fields: `indicators → correlates_with`, `countermeasures → compensates_for`, `response_protocols → coordinates_with`.

**Schema-side reality** (`framework.schema.json:493–499, 692–698, 762–768`): all three are `array of strings` with **no `pattern` constraint, no enum, no `minItems`**. Structurally, any string is accepted — including IDs that don't resolve. Validation of reference resolution is not enforced by the JSON Schema; it must be a downstream lint or a CI check.

**Internal contradictions / under-specification:**

1. The `cross_matrix` axis names the four matrices as **"Person, Facility, Organization, System"** but the actual data key is `infrastructure` (used in `matrices.infrastructure`, `route.ts`, the SPA stub view). "System" is a vestigial label that disagrees with every other surface. Minor but it's in the prose principle.
2. The `cross_domain` axis is the only one not tied to a schema link — it lives implicitly in `indicator.detection_sources` (an enum). It is a real property of the data but not a graph edge; the SPA could surface it without any new edges.
3. The `detection_mesh` block describes the *principle*, not any rendering contract. There is no companion field that says "indicator detail pages MUST surface correlations" or "graph view is part of the standard." Mesh is defined as a property of the data model, not as a UI deliverable.

The principle is coherent and complete *as a model description*. It is silent on consumer obligations.

---

## B) Content population reality (data side)

**Chunk-1 indicator inventory (the 18 indicators across TM0101, TM0102, TM0104):**

| Tactic | Indicator | `correlates_with` |
|--------|-----------|-------------------|
| TM0101 Target Selection | IND-0101-01 | **field absent** |
| TM0101 | IND-0101-02 | **field absent** |
| TM0101 | IND-0101-03 | **field absent** |
| TM0101 | IND-0101-04 | **field absent** |
| TM0101 | IND-0101-05 | **field absent** |
| TM0101 | IND-0101-06 | **field absent** |
| TM0102 Subject Profiling | IND-0102-01 | `[IND-0103-04, IND-0101-02]` |
| TM0102 | IND-0102-02 | `[IND-0103-02, IND-0101-02]` |
| TM0102 | IND-0102-03 | `[IND-0103-04]` |
| TM0102 | IND-0102-04 | `[IND-0103-05]` |
| TM0102 | IND-0102-05 | `[IND-0103-01, IND-0103-03]` |
| TM0102 | IND-0102-06 | `[IND-0103-01]` |
| TM0104 Capability Acquisition | IND-0104-01 | `[IND-0107-03]` |
| TM0104 | IND-0104-02 | `[IND-0107-03]` |
| TM0104 | IND-0104-03 | `[IND-0106-02]` |
| TM0104 | IND-0104-04 | `[IND-0105-04]` |
| TM0104 | IND-0104-05 | `[IND-0101-05]` |
| TM0104 | IND-0104-06 | `[IND-0101-06]` |

**Counts:**

- 12 of 18 chunk-1 indicators have populated `correlates_with` (TM0102 and TM0104 fully populated; TM0101 0/6).
- All 15 reference IDs in chunk-1 resolve (0 broken).
- **All 15 correlations are within-matrix (Person → Person) and within-phase (Phase 1 → Phase 1).** Zero cross-matrix; zero cross-phase in chunk-1.

**Framework-wide (190 indicators, all in `matrices.person`):**

- 179 indicators carry the `correlates_with` field; 127 are populated (66.8%).
- 160 total correlation edges; 0 broken IDs.
- 80 within-phase, 80 cross-phase (the cross-phase axis IS exercised at the corpus level — chunk-1 just happens to live entirely in Phase 1).
- **0 cross-matrix correlations exist anywhere in the framework, because Facility, Organization, and Infrastructure matrices contain 0 tactics and 0 indicators.**

**Compensates_for / coordinates_with (parallel mesh edges):**

- 137 countermeasures total; 51 (37%) have populated `compensates_for`.
- 69 response protocols total; 64 (93%) have populated `coordinates_with`.

**Unauthored content:** The other three matrices are *empty arrays*, not skeleton populations:

```
person:          34 tactics, 190 indicators
facility:         0 tactics,   0 indicators
organization:     0 tactics,   0 indicators
infrastructure:   0 tactics,   0 indicators
```

ROADMAP commits these to V1.3 / V1.4 / V1.5. Cross-matrix correlations are explicitly described there as "populated where {Facility, Organization, Infrastructure} tactics interact with Person tactics" — i.e., **cross-matrix is roadmapped as a V1.3+ deliverable**, not V1.2.x.

---

## C) UI rendering reality

**Definitive search across `src/`:** No occurrences of `detection_mesh`, `detectionMesh`, `correlates_with`, `correlatesWith`, `network graph`, `phase_lens`, or any graph-rendering library (`d3`, `cytoscape`, `vis-network`, `react-flow`, `sigma`, `elk.js`). `package.json` dependencies are only `react`, `react-dom`, plus Vite + TypeScript dev tooling.

**Indicator rendering today** — `src/components/detection-response/IndicatorSection.tsx` reads exactly four fields from each indicator: `id` (display only, not clickable), `behavior`, `detection_sources` (rendered as tag chips), `source_refs` (collapsible). It does not read `correlates_with`, `temporal_signature`, `escalation_weight`, `escalation_axes`, `severity_band`, `informs_axes`, or `phase_relevance`.

**TypeScript surface** — `src/types/framework.ts` declares the `Indicator` interface with only `id, behavior, category, detection_sources, phase_relevance?, source_refs`. **The SPA type system does not even know `correlates_with` exists.** Same for every other V1.2 indicator field. The compiler would currently strip references to those fields as unknown.

**Routing** — `src/lib/route.ts` defines six route types: `heatmap`, `phase`, `tactic`, `actors`, `actorDetail`, `stub`, `references`. There is **no `indicator` route**. Indicator IDs are not navigable.

**What exists for Detection Mesh in the rendered SPA today: nothing.** No graph view, no related-indicators list, no hover popup, no click-through, no indicator detail page, no awareness of mesh edges at the type-system level.

**Roadmap commitment for the UI** (from `ROADMAP.md:93–113`, V1.2 section): the documented V1.2 UI deliverables are *Phase Mode UI* and *cross-phase indicator badges with clickable navigation back to parent tactic*. Plus the assessment-guidance prose surfaces and the heat-map count format. **The roadmap does not list a Detection Mesh network graph, an indicator detail page, related-indicators lists, or hover popups as V1.2 deliverables.** Those appear to be Jay's intent (he stated as much) but they are not written down in `ROADMAP.md`, `CHANGELOG.md`, or any doc under `docs/`. `Plans/` is empty.

The "Detection Mesh links populated" claim in `CHANGELOG.md` for 1.1.0 is true at the data layer for the Person matrix only — it carries no UI assertion.

---

## D) Author guidance reality

`CONTRIBUTING.md` contains **zero references** to `correlates_with`, `compensates_for`, `coordinates_with`, `detection_mesh`, "mesh," "cross-matrix," or "cross-phase." Grep returned no hits.

Worse, the existing indicator guidance is stale. `CONTRIBUTING.md:54` reads:

> "Detection indicators map observable behaviors to tactics. V1 ships with `indicators: []` arrays as placeholders — these populate in V3 alongside the Organization matrix. If you have indicator content for V1 Person tactics, open an issue. Don't submit a pull request to populate them yet — the schema for indicator records is still being designed."

This was true pre-V1.1. It is wrong today — 190 indicators are populated, the schema is locked, and they shipped in V1.1.0. The mesh fields are not described to authors at all. There is no rule for granularity, no rule for "what counts as a correlation worth noting," no naming convention (the convention exists in the schema as `^IND-[0-9]{4}-[0-9]{2}$` but is not surfaced in CONTRIBUTING).

`ROADMAP.md` references mesh population only as a release-level deliverable (e.g., "Detection Mesh links populated where Facility tactics interact with Person tactics"). It is not an author-facing rule.

---

## E) Verdict on Detection Mesh status

**Category (iii): structurally supported with substantial within-matrix content; UI not yet built; author guidance absent.**

Justification: the data layer is real and non-trivial (160 edges, 0 broken IDs, 80 cross-phase, ~67% indicator coverage in the only authored matrix); the principle is documented; but the SPA is blind to the field entirely, no rendering exists, no indicator-level route exists, the front-end type system doesn't even declare the field, and CONTRIBUTING gives authors no guidance on how to populate it. The cross-matrix axis is structurally supported but materially empty (and roadmapped for V1.3+). Calling this a "real feature" today overstates the consumer-facing reality; calling it a "placeholder" understates the data layer's substance. It is **a real machine-readable feature for downstream JSON consumers, and a deferred UI feature for human readers of the SPA.**

---

## F) Recommendations for V1.2.2 scope

Reading the four candidates against the question: *what must be true for `matrices.boundary_rule` to legitimately claim Detection Mesh as the cross-matrix mechanism?*

**REQUIRED for V1.2.2**

1. **Populate `correlates_with` on the 6 TM0101 indicators.** The chunk-1 hole is asymmetric — TM0102 and TM0104 are fully populated, TM0101 is empty. For internal consistency of the within-Person mesh, TM0101 needs the same treatment. Targets are obvious (Target Selection grievance and research indicators naturally correlate forward to Subject Profiling, sideways to peer-disclosure indicators, and forward to Mobilization-phase ideation). **Cost: ~half a work session.** This is a content authoring task with low novelty since the pattern exists in TM0102/TM0104.
2. **Add a `correlates_with` author rule to CONTRIBUTING.md.** Three things at minimum: (a) what counts as a correlation worth noting (same-actor, same-incident-class, observable handoff between two indicator types — not "vaguely related"), (b) granularity ceiling (suggested: 2–4 references per indicator; more becomes noise), (c) the IND-XXXX-XX naming convention and a note that broken references fail the validator. Also fix the stale paragraph at line 54 that says indicators are V3. **Cost: ~half a work session.**
3. **Fix the "System" vs `infrastructure` naming inconsistency** in the `cross_matrix` axis description in `detection_mesh.axes`. Either rename the data key (breaking change, defer) or align the prose to say "Infrastructure." Recommend the prose fix. **Cost: trivial, ~15 minutes including the schema_version patch note.**
4. **Add a reference-resolution lint** (or extend whatever validator exists) to catch broken IDs in `correlates_with`, `compensates_for`, `coordinates_with`. Zero broken IDs exist today; the test exists to keep that true as authoring expands. **Cost: ~half a work session.**

**DEFERRED to V1.2.3 or V1.3 (do NOT block V1.2.2)**

5. **SPA rendering of correlations on the existing tactic detail page** — a simple "related indicators" inline list under each indicator, displaying the IND IDs from `correlates_with` as text (no click-through yet). This is the smallest legitimate human-facing surface for the feature. Requires adding `correlates_with` to `Indicator` in `src/types/framework.ts` and a one-line render in `IndicatorSection.tsx`. **Could fit in V1.2.2 if scope allows; ~half to one work session.** I'd promote this from DEFERRED to RECOMMENDED if the boundary_rule claim is going to ship.
6. **Indicator detail page** — new route `/person/indicator/:id`, with a small component that resolves `correlates_with` IDs to behavior text and provides click-through. **~1–2 work sessions.** Justifies V1.2.3.
7. **Network graph view** — new top-level view, requires picking a graph library (cytoscape.js is the natural choice — actively maintained, license-clean, sub-MB bundle, designed for biological/network science visualization which is structurally similar to threat-detection meshes), data shaping, layout tuning, hover/click interactions, and significant UX work. **~3–5 work sessions plus iteration.** Belongs in V1.3 alongside the second matrix landing, when cross-matrix edges actually exist and a graph view starts paying for its complexity. Building the graph in V1.2.x while three of four matrices are empty would render a sparse, mostly-uninformative visualization that hurts the credibility of the feature.
8. **Cross-matrix correlations in data** — explicitly a V1.3+ deliverable already in `ROADMAP.md`. Not V1.2.2 work. Within-Person and cross-phase mesh edges carry the V1.2.2 story.

**Anything else load-bearing:** the Indicator TypeScript type should be brought into sync with the V1.2 schema (declare `correlates_with`, `temporal_signature`, `escalation_weight`, `escalation_axes`, `severity_band`, `informs_axes` as optional). This is hygiene — the front-end currently has a stale view of the indicator class even if it renders nothing extra. **~15 minutes.** Recommend including in V1.2.2.

---

## G) The integrity question

Proposed `matrices.boundary_rule` text:

> "Real-world incidents may legitimately invoke tactics from multiple matrices simultaneously; cross-matrix coverage is expressed through the Detection Mesh via indicator `correlates_with` references rather than by re-classifying tactics."

**Is this true today? No, not the cross-matrix half.**

Within-matrix coverage via `correlates_with` is true and well-populated for Person (160 edges, 80 cross-phase). The mesh works as a within-matrix detection scaffold today.

Cross-matrix coverage is not true. There are zero cross-matrix correlations in the framework. They are zero by force majeure — the other three matrices contain zero tactics, so there is nothing to correlate to. The schema permits cross-matrix references, the principle text describes them, and the roadmap commits them to V1.3+. But as of V1.2.x, the `correlates_with` field cannot express cross-matrix coverage because there are no IND-02XX-XX, IND-03XX-XX, IND-04XX-XX indicators in non-Person tactics to point at. (The framework uses IND-0203-01 etc. as Person-matrix Phase-2 indicators, not Facility — there is no namespace separation between matrices in the IND ID format, which is itself a future design question.)

**If V1.2.2 ships `matrices.boundary_rule` as written, the framework would claim a mechanism it materially does not yet provide for the cross-matrix axis.** The claim is forward-looking dressed as present-tense.

**Two honest paths forward:**

- **(a) Tense fix.** Change the boundary_rule prose to acknowledge the maturity gradient. Something like: "Real-world incidents may legitimately invoke tactics from multiple matrices simultaneously. Cross-matrix coverage is expressed through the Detection Mesh via indicator `correlates_with` references rather than by re-classifying tactics; the Detection Mesh's within-matrix edges are populated in V1.2 across the Person matrix, and cross-matrix edges populate as additional matrices land in V1.3–V1.5." This is true today.
- **(b) Scope expansion.** Defer `matrices.boundary_rule` to V1.3 when the first cross-matrix edges land (Facility ↔ Person), and ship V1.2.2 with only the within-matrix mesh story documented.

I'd take path (a). It preserves the V1.2.2 release shape, makes the claim defensible, and lines up with the staged-matrix roadmap already published. Path (b) is cleaner architecturally but slips a structural-honesty improvement that V1.2.2 is otherwise well-positioned to deliver.

---

## Summary

Detection Mesh is real at the data layer for the Person matrix, invisible at the SPA layer, undocumented at the author layer, and structurally pending at the cross-matrix axis. V1.2.2 can close three of the four gaps cheaply (TM0101 population, CONTRIBUTING guidance, minor schema prose fix + reference lint) and can optionally add the smallest legitimate UI surface (inline related-indicators list) without committing to the graph view that belongs in V1.3. The `matrices.boundary_rule` claim should be tense-adjusted to match material reality rather than ship as written.
