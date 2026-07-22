# Architect — Per-Option Seam Routing Rules

Produced by Architect agent during Session 26 BUILD. Brief: pre-briefed on planned shape; asked to draft routing rules under each option, stress-test, and deliver an architectural-fit verdict (NOT a "which is right" judgment).

---

### Option 1 — Keep specific-individual
**Routing rule:** Person matrix activates only when the adversary's objective is a single named individual; all other harm-to-people scenarios route by location or asset to facility. Collateral casualties co-located with the named target do not change matrix assignment — the matrix follows the adversary's selection criterion, not the body count. When the adversary's selection criterion is the location or the people present at it (rather than one named subject), routing moves to facility regardless of whether anyone present happens to be notable.
**Case routings:** A → person · B → facility · C → facility · D → person
**Stress-test case:** A' — Named executive is shot in the lobby of their employer during a workday; gunman also kills two unrelated employees standing nearby. Under "single named individual" the case routes person, but the venue is a workplace open to multiple people, and "selection criterion" can read as either the named subject or the workplace as access vector — the rule does not crisply separate vector-of-access from objective.

### Option 2 — Broaden person
**Routing rule:** Person matrix activates when the adversary's primary objective is harming one or more humans, named or unnamed, single or mass. Facility matrix activates when the adversary's primary objective is damaging, denying, or symbolically attacking a location or asset, with human harm as instrument or byproduct rather than goal. Routing follows objective-of-harm, not the physical setting in which harm occurs.
**Case routings:** A → person · B → person · C → person · D → person
**Stress-test case:** B' — Vehicle is driven into the lobby of a corporate headquarters during business hours; attacker's stated objective references both the company-as-target and the people inside. Primary-objective is genuinely mixed (location-symbolic + human-harm), and the rule offers no tie-breaker — the same act can be argued either way and the matrix assignment depends on adversary statements that may not exist or may be unreliable.

### Option 3 — Split person
**Routing rule:** Person matrix is the parent; dispatch within it is by target-set cardinality and selection mode. Targeted-Individual sub-matrix activates when the adversary selected one named subject; Mass-Casualty-Against-People sub-matrix activates when the adversary selected a population, crowd, or unnamed multi-victim set as the objective. Facility matrix activates only when the location or asset itself is the objective and humans are instrument or byproduct; the parent person/facility seam still requires the Option 2 objective-of-harm test, so Option 3 inherits Option 2's seam and adds an internal dispatch on top.
**Case routings:** A → person/Targeted-Individual · B → person/Mass-Casualty (or Targeted-Individual if family unit is treated as the named target-set) · C → person/Mass-Casualty · D → person/Targeted-Individual
**Stress-test case:** B' — Family of four is attacked at home; adversary's selection criterion is "this household" rather than one named person, but the target-set is bounded, named-by-relationship, and small. The rule offers two defensible reads (Targeted-Individual extended to a named small set, vs. Mass-Casualty as any multi-victim event) and no cardinality threshold — dispatch between the two sub-matrices is undefined for small named groups.

### Architectural-fit verdict
**Strongest:** Option 2 — One orthogonal axis (objective-of-harm: people vs. location/asset) collapses all four seam cases to a single matrix without a secondary rule, and the only ambiguity is genuinely mixed-objective adversaries, which is a real-world property rather than a taxonomy artifact. Fewest seam edge cases and the cleanest single test at the matrix boundary.
**Weakest:** Option 3 — It inherits Option 2's parent-level objective-of-harm seam and adds a second seam inside person (cardinality / named-set dispatch) that has no clean threshold, so it is strictly more boundary surface than Option 2 for strictly more routing decisions per case.

---

**Seam cases reviewed:**
- (A) Named individual attacked at home; spouse and child also killed
- (B) Family unit attacked at home; no single dominant named target
- (C) Multiple unrelated people attacked in car or public-area
- (D) Named individual attacked at workplace; other employees also killed
