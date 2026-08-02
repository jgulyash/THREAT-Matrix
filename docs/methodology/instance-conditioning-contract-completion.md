# Instance-Conditioning Contract Completion (V1.6)

**Provenance:** Rulings Q1, Q2, Q3a, Q3b, Q4 — 2026-07-28 scoring-remediation session (prompt-series P5). Implemented 2026-08-02, V1.6 Contract Hardening window.

The Layer-2 instance-conditioning contract was defined in V1.3 (structured instance record, escalate-only rule, binding contract) and completed here. Five rulings close the design questions that stayed open through the scoring-remediation series.

## Q1 — Demotion doctrine (adopted verbatim)

> The conditioned priority is an escalation detector, not a queue-ranking model; de-prioritization is a case-management decision that must never be written back into the score.

This answers the volume objection directly. At scale, cases leave the queue by **disposition** — closure, monitoring tiers — never by score demotion. Any demotion path becomes a laundering machine for capability discounts (finding F13): every pressure to manage volume would flow through it, and the false-LOW (F12, the deadliest miss) would be manufactured at scale. Recorded as `instance_conditioning.demotion_doctrine`.

## Q2 — Raise guidance (advisory, never computed)

`instance_conditioning.raise_guidance` records five patterns for inter-analyst consistency: specific target + means in hand (raise at least one band); that pattern accelerating (consider critical); attained access + specific target (strong raise signal); pathway at or beyond preparation with narrowing focus (consider a raise); low source credibility (hold pending corroboration — the band still floors at type). The entry states explicitly that this is guidance, not a formula; nothing is computed and the escalate-only invariant is unchanged.

## Q3a — Sixth factor: proximity_access (breaking schema change)

`$defs.instance_assessment` gains a required sixth factor, `proximity_access`, enum `no_known_access / seeking_access / has_access / at_or_near_target / unknown` (enum approved 2026-08-01). Rationale: **access is a state, not a stage.** An insider has access without ever "breaching"; folding access into `pathway_stage` conflates *having* access with *seeking* it. Unknown-safe semantics match `means_in_hand`: `unknown` is the default and never lowers priority. Ships inside the V1.6 breaking schema bump (schema 2.0.0) — the factor is required, so pre-2.0 instance records do not validate against the new contract.

## Q3b — Inhibitors exclusion (deliberate asymmetry)

Protective factors / inhibitors (stabilizers, stake in conformity) are deliberately absent from the instance record. Under escalate-only they have no mechanical role — they only argue a case down — and they are the field's most misjudged, most gameable variable. Practitioners from SPJ traditions (WAVR-21, HCR-20) should read the record as deliberately asymmetric, not incomplete. Inhibitors inform case management, outside the score. Recorded as `instance_conditioning.inhibitors_exclusion`.

## Q4 — Credibility articulation

One sentence added to `source_credibility`'s schema description: in an escalate-only system it functions as a **brake on raising, never a scaler down** — a low-credibility screaming instance cannot be dismissed (the type floor holds) and cannot stampede the queue (the raise waits for corroboration).

## What did not change

The composite formula, the detectability flip, the severity-floor rule, the escalate-only invariant, and the binding contract (B-04) are all untouched. No instance data ships with the framework; the contract remains a type-level artifact that consumers instantiate per case.
