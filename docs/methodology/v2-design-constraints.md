# V2 Design-Constraint Record

Decisions and open questions that must be settled before V2 (the platform release) is designed. Recorded now, during V1.6, so the platform is built against a known contract rather than rediscovering these under deadline. This is a constraints ledger, not a spec.

## Computed CPN (the mesh-walking contract)

The Cyber-Physical Nexus is **computed over the Detection Mesh, never stored** (locked S32 decision, `RATIONALE-cpn-modality-and-mesh.md`). The V1.6 modality migration supplies the last missing input: every one of the 815 indicators now carries a `modality` facet, so the computation is possible framework-wide rather than infrastructure-only. The S32 deferral trigger ("defer until the mesh graph exists") has fired — the within-matrix and cross-domain meshes now exist in all four matrices.

Constraints the V2 computation must honor:
- **Two routes to CPN.** (1) Intrinsic: a behavior whose own modality is `cyber_physical` is CPN on its own signature. (2) Participation: a `physical` or `cyber` behavior is CPN only when the mesh links it, within the same operation, to a `cyber_physical` crossing or a physical terminus reached from a cyber behavior. A behavior's own tag never changes; only its company does.
- **The participation predicate is same-operation.** Only same-operation kill-chain edges confer CPN. A cyber behavior in an IT-ransomware chain that reaches no physical terminus is cyber, forever.
- **Never written back.** The computed CPN value (per behavior, per operation) is a query result, never a stored field on `framework.json`. Same discipline as compensation-as-computed-gap-query.
- **Open question — output arity.** Whether computed CPN is a boolean or a three-valued output (realized / intended / not-CPN, distinguishing Stuxnet-style fired crossings from Volt-Typhoon-style intended-but-unfired) is deferred to the V2 design. The intent clause requires an analyst judgment that cannot be fully mechanized.
- **Reference implementation is a fast-follow, not a schema change.** `scripts/analysis/compute-cpn.py` (a read-only computation over the shipped modality facets + `correlates_with` edges) can ship in a 2.0.x minor with a methodology note; it needs no schema change because the doctrine forbids storing the output. CPN branding returns to the reference SPA only when it is powered by this computation, not by intrinsic tags alone.

## AI / agentic enablement

Decided in V1.6: AI is **not** a fifth `modality` value. AI is an amplifier that applies across all four modes (an AI-piloted drone strike is still `physical`; an AI-written spear-phish is still `cyber`), not a distinct instrument location, so a fifth value would both erase the seam fact a defender needs and die by universality as AI-assistance becomes ubiquitous. AI already lives correctly on the actor axis (`ai_enabled_risks`, all 32 profiles) and manifests at the instance layer as tempo and scale.

Open for V2: whether a per-behavior AI-enablement **overlay** (an orthogonal marker like the `human_social` boolean, not a modality value) earns its place. Authoring 815 speculative overlay values with thin evidence in a hardening release was declined as field creep; revisit when there is a labeled evidence basis.

## Instance-conditioning: structured raise trace

The `conditioned_assessment` record stores the outcome (`conditioned_priority`) but not which `raise_guidance` pattern drove a raise; `basis` (free text) can hold it, but there is no structured field, so an auditor cannot mechanically reconstruct why a case was raised. A structured trace field was declined for V1.6 as scope creep. Weigh for V2: audit/explainability value against field creep, alongside the interactive instance-entry surface (deferred to V2, ships with the SDKs where case data has a legitimate consumer-side home).

## Warning-behavior filter

Warning behaviors (grievance rumination, fixation, withdrawal, energy burst, final-act signature) resolve their `modality` cleanly to `human_social` (the human/behavioral domain), and are identifiable today only by combination (`category: behavioral_change` + `human_social` modality + an `informs_axes` signature). A dedicated one-field filter (an optional `is_warning_behavior` boolean) would match the BTAM audience's mental model (NTAC pathway vs. warning behaviors) but is a new authoring campaign of its own. Deferred by decision, pending a pros/cons discussion.

## Ingestion contract (observation schema)

The scoring engine's consumer-side contract is settled (consumers instantiate `conditioned_assessment`). The **observation schema** — the boundary interface by which raw observations enter a consumer's pipeline — should be published as its own normative, machine-readable file, NOT folded into `framework.json`'s `$defs`. It is a boundary interface, not part of the framework's type-level ontology. Design it before the V2 ingestion path.
