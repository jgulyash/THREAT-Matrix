# Bottom-Cut Recalibration (low band)

Status: APPLIED (Ruling 7 — Jay, 2026-07-28). Register: the S30/v1.2.0
realized-population recalibration (which corrected only the top of the scale).

## The problem
Before this pass the low band held **zero of 815 indicators**. The severity
thresholds were an equal-quartile cut that had never been recalibrated at the
bottom: the S30/v1.2.0 pass fixed only the top (critical 7.5 -> 6.5) against the
realized population. Term analysis showed the bottom population's severity axes
were already at honest floors, propped above the 2.5 medium cut only by the
stealth term (10 - detectability) - the cut, not the values, was wrong. The
aftermath seam reconciliation (rulings 2-B/3/4-A/5-A/6-A) then re-authored
echo-scored trace behaviors downward, so the bottom is now honest on both counts.

## The adopted low-band definition (Ruling 7, verbatim)
> Low: behaviors whose direct residual harm is investigative or attributional
> trace - egress, cleanup, attribution, ambient pre-operational recon - rather
> than realized or imminently enabled harm.

## The cut (decided against the post-reconciliation distribution)
Candidate medium cuts 3.0 and 3.25 were tested against the definition:
- **Cut 3.0** - low band 15, one false-low, keeps the manifesto-naming-a-target
  signal (IND-O0101-01, 3.08) at medium.
- Cut 3.25 - low band 28, two false-lows, banded the manifesto signal low.

**Adopted: medium threshold 2.5 -> 3.0.** High and critical thresholds unchanged
(5.0 / 6.5). 15 indicators move medium -> low. A false-LOW (under-triaging a real
signal) is the deadliest miss, so the cut minimizes false-lows and accepts the
safe direction of error (trace behaviors over-triaged at medium). Verified zero
interaction with the severity_floor (lowest floored weight 4.16, far above 3.0).

## Weight-review flag (open follow-on)
Two organization target-development warning behaviors band low at the 3.0 cut and
are flagged for a **targeted weight review**, because the formula under-scores
early-phase fixation and leakage signals whose type-level blast and impact read
as diffuse:
- **IND-O0101-02** (2.78) - grievance narrows to repeated fixation on one named
  organization with rising hostility (a fixation/leakage warning behavior).
- **IND-O0101-04** (2.89) - collects identifying details of a candidate
  institution across sessions before committing to it as the target.
These are genuine pathway signals; their low band reflects an under-weighting to
be corrected in a scoped weight-review pass, not the cut.

## Regression guard
`scripts/lint/validate.py` now emits a non-failing **W-BAND** warning for any
severity band whose realized population is zero and is not documented as
intentionally empty - the guard that would have caught the silent dead low band.
