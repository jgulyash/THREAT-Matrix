# Test-Case Exercise — v1.6.0

Three workstreams run the v1.6.0 contract end-to-end from three directions, sharing one validation harness:

| Workstream | Directory | What it tests | Result |
|---|---|---|---|
| A — Fictional suite | [`fictional-suite/`](fictional-suite/) | Six fictional scenarios covering ground the shipped worked-cases leave untested: all four matrices, phases 2–4, all four modalities, all four type bands, ceiling hold, two-band raise, trace-layer raise, credibility brake | 6/6 schema-valid, all layers pass |
| B — Retrospective mapping | [`retrospective-mapping/`](retrospective-mapping/) | Four well-documented public incidents (Metcalf 2013, Oldsmar 2021, Whitmer plot 2020, YouTube HQ 2018) mapped behavior-by-behavior against the taxonomy, boundary rule, and instance contract | 15 strong / 11 partial / 5 GAP rows; 9 numbered gap findings (RG-1…RG-9) |
| C — Contract stress tests | [`contract-stress-tests/`](contract-stress-tests/) | Eleven adversarial fixtures against the `conditioned_assessment` contract plus analytic probes of `matrices.boundary_rule` | 11/11 behave as declared; 5 findings (ST-F1…ST-F5) |

**Run everything:** `python3 examples/test-cases/validate_cases.py` — three layers over every case record: C1 schema (`$defs/conditioned_assessment`), C2 cross-ref (indicator exists; `type_severity_band` matches the authored `severity_band`), C3 escalate-only ordering. The positive suites (A, B, and the shipped `examples/worked-cases/`) must pass all layers; the stress fixtures must match their declared expectations exactly. Requires `pip install jsonschema`.

## Headline results

**The core doctrine holds.** Across 13 positive records and 11 adversarial fixtures: the type band floors every case, only converging positive evidence raises, the credibility brake and unknown-safe defaults behave as ruled (Q1–Q4), and the V1.6 schema closure mechanically enforces the inhibitors exclusion, the derive-don't-store rule, the six-factor record, and the ID grammar. The boundary rule resolved every placement put to it, including a genuine three-matrix incident (YouTube HQ). Retrospective records written "as-of" real decision moments demonstrate the contract's purpose on the historical record — most sharply the YouTube HQ 02:00 welfare-contact record, a type-medium indicator that conditions to high roughly eleven hours before the attack: the textbook false-LOW the escalate-only rule exists to catch.

**The findings cluster on the consumer-record seam.** Everything that broke sits where consumer-held records meet the type-level artifact — precisely the seam the V2 platform (SDKs, MCP server, ingestion contract) will occupy:

1. **Escalate-only is not schema-enforced, contradicting its own documentation** (ST-F1). Demotion records — including below a `severity_floor: critical` direct-force indicator — validate cleanly. `instance_conditioning.escalate_only_rule` claims schema encoding; the schema's own text disclaims it. Fix with three `if/then` branches or correct the prose and ship a reference check.
2. **Floor laundering via a misquoted type band evades both schema and ordering checks** (ST-F2); only a cross-reference against the authored band catches it. The binding contract should state band-fidelity as an explicit obligation.
3. **`primary_objective_evidence_tier` is homeless** (ST-F5 = RG-1). Boundary-rule prose calls it an incident-level annotation; the schema defines it only on the type-level indicator object (carried by zero of 815 indicators); the incident-facing objects reject it. Two real incidents (Metcalf, Oldsmar) had nowhere to write it, and the enum lacks a value for contested actor existence.
4. **The framework's success case is unrepresentable** (RG-3). A plot disrupted pre-execution (Whitmer) has no pathway/disposition vocabulary; benign-cause reassessment (Oldsmar 2023) likewise (RG-2). Both are doc-level fixes consistent with the demotion doctrine.
5. **The Detection Mesh's cross-domain promise is directionally incomplete** (RG-6, verified census): zero person→infrastructure edges, zero facility→outbound cross-matrix edges, zero organization→inbound cross-matrix edges. Multi-matrix incidents cannot always walk the mesh in the direction the case develops.
6. **Taxonomy gaps from the historical record** (RG-4, RG-5, RG-7, RG-8): infrastructure-matrix standoff-team tradecraft (position pre-marking, operational signaling, timing exploitation), transportation-structure and area-communications asset classes, physical counter-forensics, and a documented rule that legitimate-context carve-outs (licensed range use, lawful purchase) re-enter scope when co-occurring with active indicators from the same actor.

**One calibration vindication** (RG-9): Metcalf's rifle-fire indicator banding *medium* at type level is correct, not a miss — the instance layer is what carries the specific coordinated case to critical, and the retrospective record shows it doing exactly that.

## Suggested priority

Doc-only, high leverage: ST-F1 prose-vs-schema contradiction, ST-F2 band-fidelity sentence, RG-2/RG-3 disposition vocabulary, RG-7 carve-out override rule, Probe-1 "achieved vs intended" clarification. Schema, small: escalate-only `if/then` encoding; re-home `primary_objective_evidence_tier`. Data, incremental: RG-6 mesh edges; RG-4/RG-5/RG-8 indicators.

---

*All case records are fictional or drawn from adjudicated/public historical reporting; behavior-level only; written under the framework's acceptable-use terms for case mapping and framework validation. All indicator IDs, bands, and quoted texts verified against `docs/data/framework.json` v1.6.0 by script.*
