# Identifier Contract

Other systems refer to THREAT Matrix content by identifier: case records, tags, search indexes, crosswalks, and mappings. This document defines the identifier formats, what is guaranteed about them, and how the guarantee is checked.

## Identifier formats

| Namespace | Form | Examples | Refers to |
|---|---|---|---|
| Tactic | `T<letter><phase><nn>` | `TM0103`, `TF0102` | A category of behavior |
| Actor profile | `AP<nnn>` | `AP005` | A category of threat actor |
| Indicator | `IND-<letter?><phase><nn>-<nn>` | `IND-0103-01`, `IND-F0102-03` | One observable behavior under a tactic |
| Countermeasure | `CM-<letter?><phase><nn>-<nn>` | `CM-0103-01`, `CM-F0102-03` | A defensive measure under a tactic |
| Response protocol | `RP-<letter?><phase><nn>-<nn>` | `RP-0103-01`, `RP-F0101-01` | A response sequence under a tactic |
| Bibliography key | uppercase letters and digits in hyphen-separated parts | `NTAC-MASS-2021`, `LLNL-TR-858139` | A cited source under `bibliography` |

The exact grammar is the pattern in the schema (`docs/data/framework.schema.json`, definitions `tactic_id`, `actor_profile_id`, `indicator_id`, `countermeasure_id`, `response_protocol_id`, `bibliography_key`):

| Namespace | Pattern |
|---|---|
| Tactic | `^T[MFOI]0[1-4](0[1-9]\|[1-9][0-9])$` |
| Actor profile | `^AP(00[1-9]\|0[1-9][0-9]\|[1-9][0-9]{2})$` |
| Indicator | `^IND-[FOI]?0[1-4](0[1-9]\|[1-9][0-9])-(0[1-9]\|[1-9][0-9])$` |
| Countermeasure | `^CM-[FOI]?0[1-4](0[1-9]\|[1-9][0-9])-(0[1-9]\|[1-9][0-9])$` |
| Response protocol | `^RP-[FOI]?0[1-4](0[1-9]\|[1-9][0-9])-(0[1-9]\|[1-9][0-9])$` |
| Bibliography key | `^[A-Z][A-Z0-9]*(-[A-Z0-9]+)+$` |

A bibliography key usually ends in a year, but the pattern does not require one, and 9 of the 120 keys have none. A bibliography key may not have the shape of an indicator, countermeasure, or response-protocol identifier.

Identifiers are matched exactly. A value with trailing whitespace or a trailing newline is not a valid identifier. The validator enforces this with an exact full match; see the note on trailing newlines in [METHODOLOGY.md](./METHODOLOGY.md#5-review-process-and-gates).

### The matrix letter

A tactic identifier carries a matrix letter after the `T`: `M` (People), `F` (Facilities), `O` (Organizations), `I` (Infrastructure). Indicator, countermeasure, and response-protocol identifiers carry the same letter after the hyphen for every matrix except People, whose identifiers predate the letter and carry none: `IND-0103-01` (People) and `IND-F0102-03` (Facilities). The letterless People form is permanent.

### Anatomy of a child identifier

```
IND-F0102-03
    ^^^^^ ^^
    ||    sequence within the tactic (two digits, 01 to 99)
    |parent tactic number (four digits)
    matrix letter (absent on People identifiers)
```

`IND-F0102-03` belongs to tactic `TF0102`, and `IND-0103-01` to `TM0103`. A consumer that flattens the document does not lose the parent. The validator rejects a child whose letter and digits disagree with the tactic that contains it (check V12).

### Tactic numbering

The first two digits of a tactic number are its lifecycle phase.

| Phase | Tactic identifiers |
|---|---|
| 1, Target Development | `T<letter>01nn` |
| 2, Mobilization | `T<letter>02nn` |
| 3, Execution | `T<letter>03nn` |
| 4, Aftermath | `T<letter>04nn` |

The validator rejects a tactic whose identifier does not encode its phase (check V34) or whose letter disagrees with its matrix (check V11). Within a phase, numbers are assigned in authoring order and carry no meaning.

### Actor profile numbering

Actor profile identifiers are assigned in authoring order and are not grouped by category; the `category` field carries that. The identifiers in use run from `AP001` to `AP034`. Two of them, `AP022` and `AP027`, are reserved and carry no content, so there are 32 active profiles.

### A retired form

Until content version 1.6.0 a tactic could carry a `CPN-<letter?><nnnn>` marker for cyber-physical convergence. The marker was retired. Convergence is now recorded per indicator in `modality`. `CPN-` values do not appear in the data.

## Guarantees

### An identifier is never reused

Once an identifier has been assigned in a published release, it refers to that object permanently. This holds through:

- a change of `name` or description;
- deprecation or supersession (the object keeps its identifier and its content);
- removal of the object (the identifier is recorded as removed and never assigned again);
- reservation (a reserved identifier never receives content);
- MAJOR version changes (nothing is renumbered).

### An identifier never changes parent

A child identifier encodes its parent tactic, and that is permanent. When an indicator, countermeasure, or response protocol needs to live under a different tactic, a new identifier is issued there and the original becomes `superseded`, pointing at the new one. See [DEPRECATION.md](./DEPRECATION.md).

### Names and descriptions can change

`name`, `notes`, `field_notes`, `behavior`, and other text may be revised. Do not key on text. Changes that alter meaning are handled by deprecation or supersession, not by silent edit.

## The ID manifest

`docs/data/id-manifest.json` is the committed inventory of every identifier in the release. Its shape is defined by `docs/data/id-manifest.schema.json`. It is how the no-reuse guarantee is checked.

| Section | Holds |
|---|---|
| `version` | The content version the manifest describes |
| `generated` | A UTC timestamp |
| `ids.tactics`, `ids.actor_profiles`, `ids.indicators`, `ids.countermeasures`, `ids.response_protocols` | Every active, deprecated, or superseded identifier in that namespace, sorted |
| `ids.reserved` | Identifiers that are held and carry no content: reserved actor profiles in the document, and any identifier from another namespace reserved by hand |
| `removed` | Optional. Identifiers withdrawn from the document, each with `removed_in` (the content version) and `reason` |

An identifier appears in exactly one place: its namespace list, `reserved`, or `removed`.

The manifest for content 2.0.0 lists 161 tactics, 32 actor profiles, 828 indicators, 645 countermeasures, 323 response protocols, and 2 reserved identifiers (`AP022`, `AP027`). It has no `removed` section, because nothing has been removed.

For illustration, a complete small manifest with one removed identifier (the identifiers and the removal are invented for the example):

<!-- validate: id-manifest.schema.json -->
```json
{
  "version": "3.0.0",
  "generated": "2027-01-15T00:00:00Z",
  "ids": {
    "tactics": ["TM0101"],
    "actor_profiles": ["AP001"],
    "indicators": ["IND-0101-01"],
    "countermeasures": ["CM-0101-01"],
    "response_protocols": ["RP-0101-01"],
    "reserved": ["AP022", "AP027"]
  },
  "removed": [
    {
      "id": "CM-0101-02",
      "removed_in": "3.0.0",
      "reason": "Example only. Deprecated in 2.1.0 and removed after its sunset."
    }
  ]
}
```

### Checking

```
python3 scripts/lint/id-manifest.py --check docs/data/framework.json docs/data/id-manifest.json
```

This fails unless the manifest describes the document exactly. It detects:

- an identifier in the manifest that is missing from the document without a `removed` record;
- an identifier in the document that is missing from the manifest;
- a reserved or removed identifier that is live again;
- an identifier listed in two places, or twice;
- an identifier in a different namespace from the one the manifest records;
- a malformed or unsorted manifest, or a version that does not match the document.

With `--baseline OLDER_MANIFEST` it also compares against an older manifest and fails if any older identifier was dropped, reused, or moved to another namespace. Continuous integration runs the plain check on every push and, on pull requests, the baseline comparison against the base branch's manifest once that branch has one. Compared against a manifest generated from the published 1.7.0 document, the 2.0.0 manifest shows no identifier dropped, reused, or moved.

### Writing

```
python3 scripts/lint/id-manifest.py --write docs/data/id-manifest.json --previous docs/data/id-manifest.json
```

`--write OUT` builds the manifest from the document and writes it only if every check passes. `--previous MANIFEST` carries forward `removed` records and hand-reserved identifiers and runs the no-drop, no-reuse comparison first. `--removed "ID=reason"` records a withdrawal. `--reserve ID` holds an identifier that has no object in the document.

### What the manifest does not catch

- **Same identifier, different content.** The manifest records identifiers, not content. If an object's text were replaced with unrelated content under the same identifier, the manifest would not show it. Keeping an identifier's meaning stable is an obligation on the author and reviewer, visible in the CHANGELOG and the diff.
- **Bibliography keys.** Bibliography keys are not in the manifest. A key can be removed when its entry is retired, and one was, in content 1.7.1 (recorded in the CHANGELOG). The gates do check that every `source_refs` entry resolves to a bibliography key and that every bibliography entry is cited.
- **History before the first manifest.** The first committed manifest is for content 2.0.0.

## Expected rate of change

| Namespace | Expected change | Why |
|---|---|---|
| Tactics | Very low | A new tactic is a newly recognized category of behavior |
| Actor profiles | Low | Profiles are groupings that change slowly |
| Indicators | Higher | Indicators are refined as descriptions and sources improve |
| Countermeasures | Higher | Defensive practice changes |
| Response protocols | Highest | Response practice varies by organization and law |

The contract is the same for every namespace.

## Names from other frameworks

The vocabulary does not contain identifiers issued by other frameworks. The data holds no ATT&CK technique identifier, no CAPEC, D3FEND, or ATLAS identifier, and no PACT identifier.

`phase_mappings` relates each of the four lifecycle phases to stage or tactic names in six other published models, under the keys `ntac_pathway`, `calhoun_weston`, `cert_insider`, `cyber_kill_chain`, `mitre_attack`, and `mitre_atlas`. The values are short lowercase names such as `reconnaissance` or `grievance`. They are this project's own labels for those stages, written for lookup. They are not quotations or identifiers from the source frameworks, and a mapping is a finding aid, not a claim of equivalence.

The draft crosswalks in [docs/crosswalks/](./crosswalks/README.md) do reference PACT identifiers and names. They are separate files, outside `framework.json`, and nothing in the vocabulary depends on them.
