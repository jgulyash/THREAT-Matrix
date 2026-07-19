# Validator negative fixtures

These fixtures exercise `scripts/lint/validate.py`. Each one is a small JSON
file, not a full copy of `framework.json` (the canonical document is about
2.65 MB). A fixture names the mutations to apply to a fresh copy of canonical
data, and the harness confirms that validation then fails with the expected
check among the checks that fired.

Run the harness:

```
python3 scripts/lint/validate.py docs/data/framework.json --fixtures scripts/lint/fixtures
```

A fixture passes when validation fails on the mutated data AND its
`expected_check` is among the fired checks. A fixture that validates clean, or
that fires only the wrong checks, is a harness failure. Some fixtures fire an
extra check as a side effect (for example, moving a tactic id also breaks the
child-id embedding). That is expected; the harness requires only that the named
check fires.

## Mutation ops

- `set` sets the value at a dot-separated path (integer segments index lists).
- `append` appends a value to the list at a path.
- `del` removes the key or list index at a path.
- `raw_replace` edits the raw document text before parsing, which the raw
  duplicate-key fixture needs because `json.load` collapses repeated keys.

## Fixture map

Each fixture reconstructs one of the categories a Principal Architecture Review
screens for. The review did not enumerate its individual mutations, so these
fixtures reconstruct its stated categories rather than copy specific edits.

| Fixture | Check | Review category | What it plants |
| --- | --- | --- | --- |
| F01 | V01 | duplicate IDs | Two tactics share one tactic id. |
| F02 | V02 | duplicate IDs | Two indicators share one indicator id. |
| F03 | V06 | dangling refs | A same-matrix correlates_with points at no indicator. |
| F04 | V07 | dangling refs | A compensates_for points at no countermeasure or indicator. |
| F05 | V09 | dangling refs | A source_refs entry is not a bibliography key. |
| F06 | V10 | dangling refs | A cross-matrix correlates_with edge points at no indicator. |
| F07 | V11 | wrong matrix placement | A tactic id prefix contradicts its matrix key. |
| F08 | V19 | wrong matrix placement | A tactic matrix field contradicts its containing key. |
| F09 | V05 | typo'd keys | A JSON object repeats a key in the raw text. |
| F10 | V17 | typo'd keys | phase_4_track is misspelled phase_4_trak on an aftermath tactic. |
| F11 | V13 | contradictory scoring | severity_band low on a weight 8.0 indicator. |
| F12 | V14 | contradictory scoring | escalation_weight drifts about 2.0 off its axes composite. |
| F13 | V17 | invalid lifecycle values | phase_4_track carries the invalid value retired. |
| F14 | V18 | conditioned-priority lowering | conditioned_priority low sits under a high severity_band. |

## Check reference

| Check | Meaning |
| --- | --- |
| V01 | Duplicate tactic id, global. |
| V02 | Duplicate indicator id. |
| V03 | Duplicate countermeasure id. |
| V04 | Duplicate response-protocol id. |
| V05 | Duplicate JSON object key anywhere in the raw document. |
| V06 | Dangling same-matrix correlates_with. |
| V07 | Dangling compensates_for. |
| V08 | Dangling coordinates_with. |
| V09 | source_refs entry that is not a bibliography key. |
| V10 | Dangling cross-matrix correlates_with, reported apart from V06. |
| V11 | Tactic id prefix that disagrees with its matrix key. |
| V12 | Child id whose letter and digits disagree with the parent tactic. |
| V13 | severity_band that contradicts escalation_weight, respecting the floor. |
| V14 | escalation_weight that drifts off the axes composite past tolerance. |
| V15 | severity_floor with an invalid value, or a band below the floor. |
| V16 | phase outside 1 to 4, or a phase_name that does not match the phase. |
| V17 | phase_4_track missing or invalid on a phase-4 tactic, or present below phase 4. |
| V18 | conditioned_priority ranked below its type severity_band. |
| V19 | Tactic matrix field that differs from its containing matrix key. |
