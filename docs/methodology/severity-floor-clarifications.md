# Severity-Floor Clarifications (lineage)

The `severity_floor_rule` is a narrow triage override: an indicator whose behavior
applies direct physical force to a person's body carries `severity_band = critical`
regardless of its computed `escalation_weight` (the weight itself is never floored,
so the severity gradient is preserved). It corrects one specific blind spot — the
weight formula gates the top band on `blast_radius` (population scope), which
under-bands a single-victim direct-force event. It is deliberately unconditional and
therefore deliberately narrow: it applies only where "critical" is *always* correct.
Instance-variable severity (this asset, this location, this person) lives in the
weight formula and the escalate-only instance-conditioning layer, not the floor.

Extensions are added narrowly and by explicit ruling:

- **V1.3 (2026-07-05) — base rule.** Direct physical force to a person: weapon
  discharge, vehicle ramming, explosive detonation, physical assault, overpowering
  or incapacitating personnel, taking physical custody by restraint, forcible
  extraction, physical restraint or force against a captive.
- **V1.4 (2026-07-18) — infrastructure narrow extension.** Mechanism-specific
  critical-floor on infrastructure execution behaviors whose direct mechanism is
  human casualties (safety-instrumented-system defeat, finished-water poisoning);
  narrow, not a blanket infra floor.
- **Ruling 8-A (2026-07-28) — weapon-threat custody.** Taking or maintaining custody
  or control of a person by weapon threat or credible threat of immediate force
  during in-progress execution (weapon displayed at the victim, control being
  established or maintained) counts as taking physical custody under the rule.
  Scope guard: threatened force without the custody/control context (a brandish
  during a dispute, a communicated or conditional threat outside an in-progress
  seizure) does NOT floor. Applied to IND-0303-04 (weapon displayed to compel
  surrender of a person); band medium → critical, weight 4.86 unchanged. Floored
  count 42 → 43. IND-0304-02 (psychological captive management) considered and left
  unfloored — already high by the math and covered by its floored physical-restraint
  siblings; standalone psychological pressure is instance-variable.
