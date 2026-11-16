# Validator fixtures

These fixtures exercise `scripts/lint/validate.py`. Each fixture is a small
JSON file that names mutations to apply to a fresh copy of a canonical
document. The harness applies them and confirms the validator behaves as the
fixture declares.

Run the harness:

```
python3 scripts/lint/validate.py docs/data/framework.json --fixtures scripts/lint/fixtures
```

The overlay used by overlay and record fixtures is `scoring-overlay.json`
beside the framework file, or the file given with `--overlay`.

## What the harness guarantees

The harness exits non-zero unless all of the following hold.

- The canonical documents pass every check on their own. A fixture can
  therefore never pass on a failure that was already present.
- The manifest lists at least one fixture, lists none twice, and lists every
  fixture file in the directory.
- Every mutation applies and changes the document. A path that does not
  exist, a `set` that writes the value already there, a `raw_replace` whose
  text is absent, and an empty mutation list are harness failures.
- A negative fixture (the default) passes only when its `expected_check`
  fires and one failure line of that check contains the fixture's
  `expected_message`. The message is mandatory on every negative fixture, so
  a fixture cannot pass on the wrong rule of a check that has several. Other
  checks that fired are printed after "also fired".
- A positive fixture (`"expect": "pass"`) passes only when the mutated
  document produces no failure at all, with the JSON Schema run as well.
- Every check id has at least one passing negative fixture.

The trailing-newline rule on identifiers and keys is enforced twice: by the validator (exact full match, checks V24, V27, V36, V37) and by the schemas, which pair every anchored pattern with a `not` whitespace pattern (and `maxLength` on fixed-width IDs) because Python's schema validator treats a closing `$` leniently and would otherwise accept a final newline.

The harness needs the `jsonschema` package. Without it the harness fails
outright; it never runs in part and never reports a skipped fixture as
covered. Outside the harness, schema validation is also required by default:
a missing package is a failure unless `--no-schema` is passed explicitly.

Schema self-tests. Fixtures with target `framework_schema` or
`overlay_schema` mutate a copy of the SCHEMA file and leave the documents
alone. They pass only when the schema check notices, which it does through
the constraint digest pinned in `SCHEMA_PINS` in `validate.py`: the digest
covers every schema keyword except annotations, so cutting a `required`
list, widening an enum, or opening a closed object fails V39 or V46. After
an intended schema change, run `python3 scripts/lint/validate.py
docs/data/framework.json --print-schema-pins` and update `SCHEMA_PINS` in
the same commit.

## Fixture format

| Key | Meaning |
| --- | --- |
| `id` | Fixture id, unique. |
| `target` | `framework` (default), `overlay`, `record`, `coverage`, `framework_schema`, or `overlay_schema`. Which document the mutations edit. |
| `expect` | `fail` (default) or `pass`. |
| `expected_check` | The check id that must fire (negative) or the check the fixture is about (positive). |
| `expected_message` | Required on negative fixtures. Text that one failure line of the expected check must contain. |
| `audit_findings` | Optional. Audit finding ids the fixture reproduces. |
| `base` | For `record` and `coverage` targets: the document the mutations edit. It must pass on its own. |
| `mutations` | The list of ops. |

Mutation ops:

- `set` replaces the value at a path. The path must exist and the value must change.
- `add` creates a key that must not exist yet.
- `append` appends to the list at a path.
- `del` removes the key or list element at a path, which must exist.
- `raw_replace` edits the document text before parsing (`find`, `replace`,
  `count`). It is for defects a parser would hide: a repeated key, a bare NaN.

Paths are dot-separated. A segment is an object key, a list index, or a
selector `[key=value]` that picks the one list element whose key has that
value, for example `matrices.person.tactics.[id=TM0101].indicators.[id=IND-0101-01]`.
Selectors keep a fixture pointed at the same object when the data is reordered.

## Check reference

Scope says which mode runs the check: `framework` always, `overlay` with
`--overlay`, `records` with `--records`, `coverage` with `--coverage`.

| Check | Scope | What it checks | Negative fixtures | Positive fixtures |
| --- | --- | --- | --- | --- |
| V01 | framework | A tactic id used by more than one tactic, across all matrices. | F001 | none |
| V02 | framework | An indicator id used more than once. | F002 | none |
| V03 | framework | A countermeasure id used more than once. | F003 | none |
| V04 | framework | A response-protocol id used more than once. | F004 | none |
| V05 | framework | A JSON object key repeated anywhere in the raw document. | F005 | none |
| V06 | framework | A same-matrix correlates_with entry that resolves to no indicator. | F006 | none |
| V07 | framework | A compensates_for entry that resolves to no countermeasure, or that names an indicator. | F007, F008 | none |
| V08 | framework | A coordinates_with entry that resolves to no response protocol. | F009 | none |
| V09 | framework | A source_refs entry that is not a bibliography key. | F010 | none |
| V10 | framework | A cross-matrix correlates_with entry that resolves to no indicator, reported apart from V06. | F011 | none |
| V11 | framework | A tactic id prefix that disagrees with its matrix key. | F012 | none |
| V12 | framework | A child id whose letter and digits disagree with the parent tactic. | F013 | none |
| V16 | framework | A phase that is not an integer from 1 to 4, or a phase_name that does not match the phase. | F014, F015, F016 | none |
| V17 | framework | phase_4_track missing or invalid on a phase 4 tactic, or present below phase 4. | F017, F018, F019 | none |
| V19 | framework | A tactic matrix field that differs from its containing matrix key. | F020 | none |
| V21 | framework | Modality facet: modality and human_social present and valid; human_social modality forces the flag; crossing_mechanism exactly on cyber_physical. | F021, F022, F023 | none |
| V22 | framework | conditioning_guidance: exactly probe_factors and guidance, valid factor names, at most 420 characters, no em or en dash or other dash-like character (U+2012 to U+2015, U+2212). | F024, F025, F194, F195 | none |
| V23 | framework | A mitigates edge that is malformed, has an invalid function, or resolves to no indicator. | F026, F027 | none |
| V24 | framework | schema_version other than the pinned value, or a content version that is not SemVer 2.0.0. | F028, F029, F157 | none |
| V25 | framework | evidence_basis outside the 3.0.0 values; retired 2.x values get a rename hint. | F030 | none |
| V26 | framework | Lifecycle contract. Only actor profiles may be reserved, and a reserved profile carries only id, lifecycle_state, reserved_reason. deprecated needs deprecated_in and deprecation_reason. superseded also needs superseded_by, which must resolve to an active object of the same namespace, not itself, with no cycle. Active objects carry no lifecycle detail field. deprecated_in is SemVer and not later than the document version. | F031, F032, F033, F034, F035, F036, F037, F038, F039, F040, F041, F042, F043, F044, F045, F046, F047, F048, F049 | F050, F051, F052, F053, F054 |
| V27 | framework | A bibliography key or source_refs entry that breaks the key format or has the shape of an indicator, countermeasure, or response-protocol id. | F055, F056, F155, F156 | none |
| V28 | framework | Document structure: top level is an object with the required keys, the four matrices each with a maturity and a non-empty tactics list, every tactic with at least one indicator, non-empty actor_profiles and bibliography. An empty or one-key document fails here. | F057, F058, F059, F060, F061, F062, F063, F064, F065 | none |
| V29 | framework | A scoring field in the vocabulary: any retired score field on an indicator, escalation_priority in assessment_guidance, or a retired top-level scoring block. | F066, F067, F068 | none |
| V30 | framework | An actor profile id used more than once. | F069 | none |
| V31 | framework | An actor association that resolves to no profile, resolves to a reserved profile, or repeats an actor_id and employment_status pair. | F070, F071, F072 | none |
| V32 | framework | A related_tactics or v2_tactic_associations entry that resolves to no tactic. | F073, F074 | none |
| V33 | framework | A relation that refers to its own object or lists an entry twice: correlates_with, compensates_for, coordinates_with, related_tactics, source_refs, mitigates (one edge per indicator). | F075, F076, F077, F078, F079, F080 | none |
| V34 | framework | A tactic id whose third and fourth characters do not encode the tactic's phase. | F081 | none |
| V35 | framework | An indicator or countermeasure whose phase_relevance omits the parent tactic's phase. | F082, F083 | none |
| V36 | framework | A bibliography entry that nothing cites, or whose url is not null or http(s), whose doi is not null or a bare DOI, or whose date is not in an accepted form. | F084, F085, F086, F087, F088, F089, F090, F196 | none |
| V37 | framework | An identifier or id reference that does not match its grammar exactly: trailing newline or other whitespace, zero sequence number, wrong shape. | F091, F092, F093, F094, F095, F096 | none |
| V38 | framework | A bare NaN or Infinity token, or a number that overflows to infinity, in any document checked. | F097, F135 | none |
| V39 | framework | The vocabulary validated against framework.schema.json, and that schema's constraint digest against SCHEMA_PINS in validate.py, so a loosened required list, enum, pattern, or closed object fails here. | F098, F099, F100, F101, F102, F164, F165, F166, F167, F168, F169, F170, F171, F172, F173, F174, F175, F176, F177, F178, F179, F180, F186, F187, F188 | none |
| V40 | framework | An empty string, or a string with leading or trailing whitespace, anywhere in the vocabulary or the overlay. | F103, F104 | none |
| V50 | framework | An actor profile whose category_label does not match its category, or a matrix-scoped field outside its matrix (target_identity and target_identity_scope are person-matrix fields; facility_target_scope and within_site_focus are facility-matrix fields). | F191, F192, F193 | none |
| V13 | overlay | Overlay: type_band missing or invalid, or not the band of the STORED type_weight under rubric.type_band_thresholds raised to the floor. | F105, F106, F107 | F136 |
| V14 | overlay | Overlay: axes missing, incomplete, or non-numeric; type_weight missing or non-numeric; or the weight further than 0.005 from the composite of the axes. Never skipped. | F108, F109, F110, F111, F112, F113 | none |
| V15 | overlay | Overlay: type_band_floor outside high and critical, or a band below its floor. | F114, F115 | none |
| V20 | overlay | Overlay: axis_confidence missing an axis, carrying an invalid level, or differing from the derivation rule. | F116, F117, F118 | none |
| V41 | overlay | Overlay: required keys, no unknown keys, the constants (status experimental, validation_status unvalidated, normative false, scope type_level, not_a_risk_score true), SemVer overlay_version, and applies_to_framework_version equal to the vocabulary's version. | F119, F120, F121, F122, F123, F124, F162 | none |
| V42 | overlay | Overlay: indicator_scores keys equal the vocabulary's indicator ids, none missing and none extra. | F125, F126 | none |
| V43 | overlay | Overlay: tactic_priorities has exactly one entry for every tactic of the vocabulary, none missing and none extra, with values Urgent, Immediate, Priority, or Routine. | F127, F128, F137 | none |
| V44 | overlay | Overlay: an axis not recorded to one decimal place, or a weight not recorded to two. | F129, F130 | none |
| V45 | overlay | Overlay: band thresholds that are not numeric, do not start at 0, are not strictly increasing, or exceed 10; a base rate outside 0 to 10; a non-SemVer rubric_version; instance_conditioning.factors other than the six factors. | F131, F132, F133 | none |
| V46 | overlay | The overlay validated against scoring-overlay.schema.json, and that schema's constraint digest against SCHEMA_PINS. | F134, F163, F181, F182, F183, F189, F190 | none |
| V51 | overlay | Overlay: the set of score entries carrying type_band_floor must equal rubric.type_band_floor_rule.floored_indicators exactly, so a floor cannot be added or removed without changing the published list. | F158, F159, F160, F161 | none |
| V18 | records | Scored record: conditioned_priority below the stated type_band, or below the overlay's authored band for the indicator. | F138, F140 | F146 |
| V47 | records | Scored record: indicator_id not in the vocabulary, type_band not equal to the overlay's authored type_band, or a stated framework_version or overlay_version that is not the one being checked. | F139, F141, F142 | F147 |
| V48 | records | Scored record: not an object, a missing or unknown key, an invalid band, instance factor, tier, or disposition; also the scored_case_record schema when jsonschema is installed. The directory is walked with its subdirectories, .json is matched in any letter case, an unparseable file fails, and a directory with no record fails. | F143, F144, F145 | none |
| V49 | coverage | Coverage document (--coverage): the coverage schema when jsonschema is installed, plus a cm_id listed in more than one deployment entry, ids that are not in the vocabulary, dates that are not real calendar dates or lie in the future, disposition without its review date, and, when one document holds both parts, a derivation for a different target or a covered band with nothing deployed. | F148, F149, F150, F151, F152, F153, F184, F185, F197, F198, F199 | F154 |

## Check id history

The scores moved out of the vocabulary into the experimental overlay. Checks
that read score fields kept their ids and moved to overlay or record scope.

| Id | Before the split | Now |
| --- | --- | --- |
| V13 | severity_band against escalation_weight on indicators in framework.json | type_band against the stored type_weight and floor in the overlay |
| V14 | escalation_weight against the axes composite, tolerance 0.06, skipped on missing input | type_weight against the composite, tolerance 0.005, fails on missing or non-numeric input |
| V15 | severity_floor value and band below floor | type_band_floor value and band below floor, in the overlay |
| V18 | conditioned_priority beside severity_band anywhere in framework.json | conditioned_priority against type_band in scored case records (`--records`) |
| V20 | axis_confidence enum values on indicators | axis_confidence complete, valid, and equal to the derivation rule, in the overlay |
| V24 | schema_version pin | schema_version pin and SemVer content version |
| V26 | lifecycle state, SemVer, superseded_by, reserved_reason | the full lifecycle contract above |
| V43 | (added with the overlay) keys must be tactic ids | exactly one entry per tactic |
| V28 to V51 | not present | added |

No id was renumbered and none was reused for a different subject.

## Fixture list

| Fixture | Target | Expectation | Audit findings | What it does |
| --- | --- | --- | --- | --- |
| F001 | framework | V01 |  | Give a second infrastructure tactic an id that already exists. |
| F002 | framework | V02 |  | Give a second indicator an id that already exists in the same tactic. |
| F003 | framework | V03 |  | Give a second countermeasure an id that already exists. |
| F004 | framework | V04 |  | Give a second response protocol an id that already exists. |
| F005 | framework | V05 |  | Repeat the id key inside one tactic in the raw text, which a JSON parser would silently collapse. |
| F006 | framework | V06 |  | Add a same-matrix correlates_with reference that resolves to no indicator. |
| F007 | framework | V07 |  | Add a compensates_for reference that resolves to no countermeasure. |
| F008 | framework | V07 |  | Put an indicator id in compensates_for, which holds countermeasure-to-countermeasure redundancy only. |
| F009 | framework | V08 |  | Add a coordinates_with reference that resolves to no response protocol. |
| F010 | framework | V09 |  | Add a source_refs entry that is not a bibliography key. |
| F011 | framework | V10 |  | Add a cross-matrix correlates_with reference (infrastructure letter on a person indicator) that resolves to no indicator. |
| F012 | framework | V11 |  | Give a person tactic a facility prefix. |
| F013 | framework | V12 |  | Give an indicator an id that embeds a different parent tactic. |
| F014 | framework | V16 |  | Set a tactic phase outside 1 to 4. |
| F015 | framework | V16 |  | Set a phase_name that does not match the phase. |
| F016 | framework | V16 |  | Set phase to the JSON boolean true, which is not an integer phase. |
| F017 | framework | V17 | F13 | Remove phase_4_track from an aftermath tactic. |
| F018 | framework | V17 |  | Set phase_4_track to a value outside evasion and attribution. |
| F019 | framework | V17 | F13 | Add phase_4_track to a phase 1 tactic. |
| F020 | framework | V19 |  | Set a person tactic's matrix field to facility. |
| F021 | framework | V21 |  | Set human_social false on an indicator whose modality is human_social. |
| F022 | framework | V21 |  | Add crossing_mechanism to an indicator that is not cyber_physical. |
| F023 | framework | V21 |  | Remove crossing_mechanism from a cyber_physical indicator. |
| F024 | framework | V22 |  | Give conditioning_guidance an invented probe factor. |
| F025 | framework | V22 |  | Put an em dash in conditioning_guidance.guidance. |
| F026 | framework | V23 |  | Add a mitigates edge whose indicator resolves to nothing. |
| F027 | framework | V23 |  | Add a mitigates edge with an invalid function. |
| F028 | framework | V24 |  | Declare a schema_version other than the one this validator targets. |
| F029 | framework | V24 | F14 | Set a content version that is not SemVer. |
| F030 | framework | V25 |  | Set evidence_basis to the retired 2.x value operational_primary. |
| F031 | framework | V26 |  | Mark a countermeasure superseded without superseded_by. |
| F032 | framework | V26 | F03 S04 C06 | Mark an indicator deprecated without deprecated_in. |
| F033 | framework | V26 | F03 C06 | Mark an indicator deprecated without deprecation_reason. |
| F034 | framework | V26 | F03 S04 C06 | Put deprecated_in on an active indicator. |
| F035 | framework | V26 | F03 | Put reserved_reason on an active actor profile. |
| F036 | framework | V26 | F03 S04 C05 | Point superseded_by at a deprecated indicator. |
| F037 | framework | V26 | S04 C05 | Build a two-node supersession cycle. |
| F038 | framework | V26 |  | Point superseded_by at the object itself. |
| F039 | framework | V26 | F03 S04 C05 | Point an actor profile's superseded_by at a reserved profile. |
| F040 | framework | V26 |  | Point superseded_by at an id from another namespace. |
| F041 | framework | V26 | F02 F04 S05 C04 | Mark a tactic reserved while it keeps its content; only actor profiles may be reserved. |
| F042 | framework | V26 | F02 F04 S05 C04 | Mark an indicator reserved while it keeps its content. |
| F043 | framework | V26 | F02 | Mark a countermeasure reserved while it keeps its content. |
| F044 | framework | V26 | F02 | Mark a response protocol reserved while it keeps its content. |
| F045 | framework | V26 | F04 S05 C04 | Append a bare reserved indicator stub; indicators may not be reserved. |
| F046 | framework | V26 | F02 C06 | Mark an actor profile reserved while it keeps its content and drops description. |
| F047 | framework | V26 |  | Remove reserved_reason from a reserved actor profile. |
| F048 | framework | V26 | F03 C06 | Set deprecated_in to a version later than the document version. |
| F049 | framework | V26 |  | Set lifecycle_state to a value outside the four states. |
| F050 | framework | accepts (V26) |  | A deprecated indicator with deprecated_in and deprecation_reason is legal. |
| F051 | framework | accepts (V26) |  | A superseded countermeasure whose superseded_by names an active countermeasure is legal. |
| F052 | framework | accepts (V26) |  | A deprecated tactic with deprecated_in and deprecation_reason is legal. |
| F053 | framework | accepts (V26) |  | A reserved actor profile stub (id, lifecycle_state, reserved_reason only) is legal. |
| F054 | framework | accepts (V26) |  | An explicit lifecycle_state active with no lifecycle detail field is legal. |
| F055 | framework | V27 |  | Add a source_refs entry that breaks the bibliography key format. |
| F056 | framework | V27 | F14 | Add a bibliography entry whose key has the shape of an indicator id. |
| F057 | framework | V28 | S06 | Remove the matrices block. |
| F058 | framework | V28 | S06 | Empty one matrix's tactics list. |
| F059 | framework | V28 |  | Empty one tactic's indicators list. |
| F060 | framework | V28 |  | Remove a matrix's maturity. |
| F061 | framework | V28 |  | Set a matrix maturity outside core and draft. |
| F062 | framework | V28 |  | Add an unknown matrix key. |
| F063 | framework | V28 | F08 | Empty the actor_profiles list. |
| F064 | framework | V28 |  | Put a string where an indicator object belongs. |
| F065 | framework | V28 |  | Remove the top-level version. |
| F066 | framework | V29 | F05 S01 | Put a retired scoring field back on an indicator. |
| F067 | framework | V29 |  | Put the retired top-level escalation_rubric back. |
| F068 | framework | V29 |  | Put escalation_priority back in a tactic's assessment_guidance. |
| F069 | framework | V30 | F08 S03 | Give a second actor profile an id that already exists. |
| F070 | framework | V31 | F08 S03 | Associate a tactic with an actor profile that does not exist. |
| F071 | framework | V31 | F08 S03 | Associate a tactic with a reserved actor profile. |
| F072 | framework | V31 | F08 | Repeat an actor association. |
| F073 | framework | V32 | F08 S03 | Add a related_tactics entry that resolves to no tactic. |
| F074 | framework | V32 | F08 | Add a v2_tactic_associations entry that resolves to no tactic. |
| F075 | framework | V33 | F08 S03 | Make an indicator correlate with itself. |
| F076 | framework | V33 |  | Repeat a correlates_with entry. |
| F077 | framework | V33 | F08 | Make a countermeasure compensate for itself. |
| F078 | framework | V33 | F08 | Make a response protocol coordinate with itself. |
| F079 | framework | V33 | F08 | Name the same indicator in two mitigates edges with different functions. |
| F080 | framework | V33 | F08 | Make a tactic relate to itself. |
| F081 | framework | V34 | C14 | Relabel a phase 1 tactic as phase 3 without changing its id. |
| F082 | framework | V35 |  | Set an indicator's phase_relevance so it omits the parent tactic's phase. |
| F083 | framework | V35 |  | Set a countermeasure's phase_relevance so it omits the parent tactic's phase. |
| F084 | framework | V36 | F06 | Give a bibliography entry a javascript: URL. |
| F085 | framework | V36 | F06 | Give a bibliography entry a data: URL. |
| F086 | framework | V36 | F06 F07 | Give a bibliography entry a URL with a trailing newline. |
| F087 | framework | V36 | F06 | Give a bibliography entry a DOI that is not a DOI. |
| F088 | framework | V36 | F06 | Give a bibliography entry a free-text date. |
| F089 | framework | V36 | F06 | Give a bibliography entry an impossible date. |
| F090 | framework | V36 |  | Add a bibliography entry that nothing cites. |
| F091 | framework | V37 | F07 | Give a tactic an id with a trailing newline. |
| F092 | framework | V37 | F07 | Give an actor profile an id with a trailing newline. |
| F093 | framework | V37 | F07 | Give an actor association an actor_id with a trailing newline. |
| F094 | framework | V37 | F07 | Give related_tactics an entry with a trailing newline. |
| F095 | framework | V37 | F14 | Give an indicator the zero sequence number. |
| F096 | framework | V37 | F14 | Give an actor profile the all-zero id. |
| F097 | framework | V38 | F09 | Write a bare NaN token where a number belongs. |
| F098 | framework | V39 |  | Add an unknown property to a tactic; only the closed schema rejects it. |
| F099 | framework | V39 | F05 | Empty informs_axes on an indicator; the schema requires all six axes when the block is present. |
| F100 | framework | V39 | F18 | Use a bibliography type that is no longer in the enum. |
| F101 | framework | V39 | F11 | Set a license other than the published one. |
| F102 | framework | V39 | F05 | Empty a tactic's assessment_guidance; the schema requires all six parts when the block is present. |
| F103 | framework | V40 | F11 | Set a tactic name to the empty string. |
| F104 | framework | V40 | F11 | Give an indicator behavior a leading space. |
| F105 | overlay | V13 |  | Label a weight 4.49 indicator low; the stored weight implies medium. |
| F106 | overlay | V13 | S01 | Remove type_band from a score entry. |
| F107 | overlay | V13 | D-04 | Relabel a weight 6.5 indicator high without touching the weight. |
| F108 | overlay | V14 | F05 S01 | Empty the axes and claim weight 9.9 and band critical. |
| F109 | overlay | V14 | F05 S01 | Remove one axis. |
| F110 | overlay | V14 | S01 | Store an axis as a string. |
| F111 | overlay | V14 | S01 | Store the weight as a string. |
| F112 | overlay | V14 | S02 | Nudge a weight 6.5 to 6.49 and relabel the band high; the composite still rounds to 6.50. |
| F113 | overlay | V14 | S01 | Set a negative axis value. |
| F114 | overlay | V15 |  | Set a floor value outside high and critical. |
| F115 | overlay | V15 |  | Label a floored-critical indicator high. |
| F116 | overlay | V20 |  | Set an axis_confidence value outside the three levels. |
| F117 | overlay | V20 | F05 | Remove one axis from axis_confidence. |
| F118 | overlay | V20 |  | Hand-set an axis_confidence value that the derivation rule does not give. |
| F119 | overlay | V41 |  | Declare the overlay stable. |
| F120 | overlay | V41 |  | Declare the overlay normative. |
| F121 | overlay | V41 |  | Declare the overlay a risk score. |
| F122 | overlay | V41 |  | Bind the overlay to a different framework version. |
| F123 | overlay | V41 |  | Remove the notice. |
| F124 | overlay | V41 |  | Add an unknown key to a score entry. |
| F125 | overlay | V42 |  | Remove one indicator's score entry. |
| F126 | overlay | V42 |  | Add a score entry for an indicator the vocabulary does not hold. |
| F127 | overlay | V43 |  | Add a tactic priority for a tactic the vocabulary does not hold. |
| F128 | overlay | V43 |  | Set a tactic priority outside the four values. |
| F129 | overlay | V44 | C14 | Record an axis to five decimals. |
| F130 | overlay | V44 |  | Record a weight to three decimals. |
| F131 | overlay | V45 | F12 | Invert the band thresholds. |
| F132 | overlay | V45 | F12 | Set a method base rate outside the 0 to 10 scale. |
| F133 | overlay | V45 | F12 | List an invented instance factor. |
| F134 | overlay | V46 |  | Add an unknown key inside the rubric; only the closed overlay schema rejects it. |
| F135 | overlay | V38 | F09 | Write a weight that overflows to infinity. |
| F136 | overlay | accepts (V13) |  | A floor may raise the band above what the weight implies: add a high floor to a medium-weight indicator, list it in the published floored list, and label it high. |
| F137 | overlay | V43 | N9 | Remove one tactic's priority entry; every tactic needs exactly one. |
| F138 | record | V18 | S13 | Lower conditioned_priority below a correctly quoted type band. |
| F139 | record | V47 | C02 S13 | Quote a floored-critical indicator as low and set priority low: the band-laundering case. |
| F140 | record | V18 | C02 S13 | The same laundering case also fails the escalate-only rule against the authored band. |
| F141 | record | V47 | F15 | Name an indicator the vocabulary does not hold. |
| F142 | record | V47 | F15 | State a framework version other than the one being checked. |
| F143 | record | V48 |  | Remove the instance block. |
| F144 | record | V48 |  | Add a score field the record contract does not define. |
| F145 | record | V48 |  | Set an instance factor outside its values. |
| F146 | record | accepts (V18) |  | Raising priority above the type band is legal. |
| F147 | record | accepts (V47) |  | Stating the framework and overlay versions being checked is legal. |
| F148 | coverage | V49 | F10 | List the same countermeasure twice with contradictory status. |
| F149 | coverage | V49 | F10 | Set a review date that is not a date. |
| F150 | coverage | V49 | F10 | Set a verified date that does not exist in the calendar. |
| F151 | coverage | V49 | F10 | Record a disposition without its review date. |
| F152 | coverage | V49 |  | Name a countermeasure the vocabulary does not hold. |
| F153 | coverage | V49 | F10 | Empty the coverage document. |
| F154 | coverage | accepts (V49) |  | A partial deployment is legal. |
| F155 | framework | V27 | F07 S15 | Add a source_refs entry that is a real bibliography key followed by a newline. |
| F156 | framework | V27 | F07 S15 | Add a bibliography key with a trailing newline, cited by a tactic. |
| F157 | framework | V24 | F07 | Give the content version a trailing newline. |
| F158 | overlay | V51 | N1 | Fabricate a floor: add type_band_floor critical to an unfloored medium indicator and raise its band to critical. |
| F159 | overlay | V51 | N1 | Remove the floor from a floored indicator whose weight is already critical. |
| F160 | overlay | V51 | N1 | Drop one id from the published floored list while its score entry keeps the floor. |
| F161 | overlay | V51 | N1 | Add an unfloored indicator to the published floored list. |
| F162 | overlay | V41 | N2 | Declare the overlay validated. |
| F163 | overlay | V46 | N2 | Declare the overlay validated; the overlay schema holds validation_status constant. |
| F164 | framework | V39 | N12 | Empty the bibliography; the schema requires at least one entry. |
| F165 | framework | V39 | N8 | Remove a tactic's required notes. |
| F166 | framework | V39 | N8 | Remove an indicator's required category. |
| F167 | framework | V39 | N8 | Set an indicator category outside the enum. |
| F168 | framework | V39 | N8 | Add an unknown property to an indicator. |
| F169 | framework | V39 | N8 | Remove a countermeasure's required measure. |
| F170 | framework | V39 | N8 | Set a countermeasure domain outside the enum. |
| F171 | framework | V39 | N8 | Remove a response protocol's required trigger. |
| F172 | framework | V39 | N8 | Set a response protocol priority outside the enum. |
| F173 | framework | V39 | N8 | Remove an actor profile's required name. |
| F174 | framework | V39 | N8 | Set an actor profile awareness outside the enum. |
| F175 | framework | V39 | N8 | Remove a bibliography entry's required title. |
| F176 | framework | V39 | N8 | Add an unknown property to a bibliography entry. |
| F177 | framework | V39 | N8 | Set an actor association relevance outside the enum. |
| F178 | framework | V39 | N8 | Add an unknown property at the top level. |
| F179 | framework | V39 | N8 | Add an unknown property to a matrix object. |
| F180 | framework | V39 | F12 | Set ai_architecture.version to free text. |
| F181 | overlay | V46 | N8 | Remove a required rubric part. |
| F182 | overlay | V46 | N8 | Add an unknown key to the detectability guidance. |
| F183 | overlay | V46 | N8 | Remove a required part of instance_conditioning. |
| F184 | coverage | V49 | N8 | Set a deployment status outside the enum; only the coverage schema knows the enum. |
| F185 | coverage | V49 | N8 | Remove the deployment record's required basis. |
| F186 | framework_schema | V39 | N8 | Self-test: cut $defs.indicator.required down to id in the schema file itself. |
| F187 | framework_schema | V39 | N8 | Self-test: open the tactic object to unknown properties in the schema file. |
| F188 | framework_schema | V39 | N8 | Self-test: widen an enum in the schema file. |
| F189 | overlay_schema | V46 | N8 | Self-test: cut the score entry's required list in the overlay schema file. |
| F190 | overlay_schema | V46 | N2 N8 | Self-test: let the overlay schema accept validated. |
| F191 | framework | V50 | F12 | Give an actor profile a label that belongs to another category. |
| F192 | framework | V50 | F12 | Put the person-matrix field target_identity on a facility indicator. |
| F193 | framework | V50 | F12 | Put the facility-matrix field within_site_focus on a person indicator. |
| F194 | framework | V22 | F14 | Put a horizontal bar (U+2015) in conditioning_guidance.guidance. |
| F195 | framework | V22 | F14 | Put a minus sign (U+2212) in conditioning_guidance.guidance. |
| F196 | framework | V36 |  | Give a bibliography entry a year range that runs backward. |
| F197 | coverage | V49 |  | Claim covered while the deployment record holds no deployed countermeasure. |
| F198 | coverage | V49 |  | Derive coverage for a target other than the deployment record's. |
| F199 | coverage | V49 |  | Set a verified date in the future. |
