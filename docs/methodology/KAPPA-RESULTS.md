# Infrastructure informs_axes — IRR results (all 8 chunks PASS, gate 0.60)

Weighted Cohen kappa (linear), Rater A (sealed AI) vs Rater B (Hermes), final certified:

| Chunk | kappa | | Chunk | kappa |
|---|---|---|---|---|
| I1A | 0.624 | | I3A | 0.656 |
| I1B | 0.620 | | I3B | 0.614 |
| I2A | 0.760 | | I4A | 0.759 |
| I2B | 0.614 | | I4B | 0.768 |

Rounds: initial (all 8) had I1B 0.596 and I3A 0.324 below gate. Clarification A
(threat_method inside execution: manipulation=strong, enabling/concealment=weak) rescued
I3A -> 0.656. Clarification B (phase-1 recon: method=none, intent=strong for operationally-
specific target dev, opportunity=weak for ambient reach) applied to I1B on a second pass
-> 0.620. All 8 then >= 0.60.

Reconciliation: 819/1110 cells agreed and shipped as-is; 291 disagreements reconciled per
B6-reconciliation-worksheet.md (83 net changes off the sealed Rater A baseline). Jay's ruling
applied: aftermath threat_target reflects the FOLLOW-UP attack target, so TI0402 re-attack
positioning behaviors = strong (kept Rater A); cleanup/attribution behaviors reconciled lower.
Rationale/leans documented on all 185 rows in the hermes-blind-sheet CSVs.
