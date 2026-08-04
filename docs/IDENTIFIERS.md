# Identifier Contract

Stable identifiers are the load-bearing surface of THREAT Matrix. Vector databases, AI agents, mappings to other frameworks, detection-rule libraries, and case-management systems all anchor on these IDs. This document is the formal contract.

## Identifier formats

| Namespace | Format | Example | Refers to |
|---|---|---|---|
| **Tactic** | `T<X>####` | `TM0103`, `TF0102` | A behavioral category — what the threat actor is trying to accomplish |
| **Actor profile** | `AP###` | `AP005` | A category of threat actor (e.g., insider, lone actor, nation-state) |
| **Indicator** | `IND-<x>####-##` | `IND-0103-01`, `IND-F0102-03` | An observable behavior tied to a specific tactic |
| **Countermeasure** | `CM-<x>####-##` | `CM-0103-01`, `CM-F0102-03` | A defensive measure tied to a specific tactic |
| **Response protocol** | `RP-<x>####-##` | `RP-0103-01`, `RP-F0101-01` | An operational response sequence tied to a specific tactic |
| **Cyber-Physical Nexus marker** (retired v1.6) | `CPN-<x>####` | `CPN-0103`, `CPN-F0101` | Retired tactic-level convergence flag; cyber-physical convergence now lives on the per-indicator `modality` facet, and CPN participation is computed over the Detection Mesh |
| **Bibliography reference** | `<ORG>-<SLUG>-<YEAR>[-<YEAR>]` | `NTAC-MASS-2021` | A cited source in `framework.json` `bibliography` |

### The matrix letter

Tactic IDs carry a matrix letter after the `T`: `M` (People), `F` (Facilities), `O` (Organizations), `I` (Infrastructure) — `TM0103`, `TF0102`, `TO####`, `TI####`. Compound IDs (and the retired CPN markers) carry the same letter after their prefix hyphen for every matrix except People, whose IDs predate the letter and carry none: `IND-0103-01` (People) vs. `IND-F0102-03` (Facilities). The People letterless form is permanent — retrofitting a letter would violate the no-rename guarantee below.

### Anatomy of compound IDs

Indicator, countermeasure, and response-protocol IDs encode their parent tactic in their structure:

```
IND-F0102-03
    ^^^^^ ^^
    ││    └── sequence within the tactic (zero-padded, two digits)
    │└─────── parent tactic number (zero-padded, four digits)
    └──────── matrix letter (matches TF0102; absent on People-matrix IDs)
```

This is intentional. A consumer that sees `IND-F0102-03` knows without dereferencing the schema that this indicator belongs to tactic `TF0102` (and `IND-0103-01` to `TM0103`). The structural redundancy with the `tactic_id` field on the indicator object is a feature: it enables flat consumption (a consumer that flattens the document does not lose parent-child information).

### Tactic numbering scheme

Tactic IDs are four-digit zero-padded numbers organized by Threat Lifecycle phase, within each matrix's letter:

| Phase | Range |
|---|---|
| Phase 1 — Target Development | `T<X>01##` |
| Phase 2 — Mobilization | `T<X>02##` |
| Phase 3 — Execution | `T<X>03##` |
| Phase 4 — Aftermath | `T<X>04##` |

Within a phase, tactic numbers are assigned in authoring order, not in any semantic priority. New tactics added to a phase get the next available number.

### Actor profile numbering scheme

Actor profile IDs are three-digit zero-padded numbers assigned in authoring order. They are not grouped by category; the `category` field on the profile object handles that. The current categories are: `lone_actor`, `insider`, `criminal`, `corporate_espionage`, `ideological`, `nation_state`, `customer_aggressor`.

## Stability guarantees

### IDs are never reused

Once an identifier is assigned to a published item, that identifier slot is **permanently reserved** to that item. This holds across:

- Renames (the identifier survives a `name` change)
- Deprecation (a deprecated item retains its identifier indefinitely)
- Removal (a removed item's identifier is held in a reserved state — see [DEPRECATION.md](./DEPRECATION.md))
- Major-version bumps (V1, V2, V3 do not renumber)

This is the strongest guarantee in this contract. Downstream consumers (vector indices, mappings, custom forks, published rule sets) depend on it absolutely. A reused ID would silently break those consumers without any way to detect the breakage from inside the document.

### Names can change

The `name` field on every object is a human-readable label that may evolve — for clarity, voice consistency, or terminology updates. A `name` change is not a breaking change. Consumers must not key on `name`.

### Descriptions can change

The `notes`, `field_notes`, `description`, and `behavior` (etc.) fields are subject to revision. Consumers must not depend on exact text matching.

### Items never change parents

Compound IDs encode their parent tactic (`IND-0103-01` belongs to `TM0103`), and that encoding is permanent. An item is never moved to a different parent tactic with its identifier intact — the identifier would then misreport its own structure to every flat consumer.

When reorganization calls for an indicator, countermeasure, or response protocol to live under a different tactic, the move is modeled as **supersession, not mutation**:

1. A new identifier is issued under the destination tactic (next available sequence number).
2. The original item transitions to `superseded`, with `superseded_by` pointing at the new identifier — same-namespace, per [DEPRECATION.md](./DEPRECATION.md).
3. A one-to-many reorganization (one item split across several tactics) uses `deprecated` instead, following the split pattern documented in [DEPRECATION.md](./DEPRECATION.md).

The no-reuse guarantee covers the rest: the original identifier remains permanently reserved to its original content, and consumers walk the `superseded_by` chain to the current item.

### Cross-framework mappings preserve source IDs verbatim

`phase_mappings` and any future cross-walk fields preserve the source framework's identifier exactly. THREAT Matrix does not transliterate, normalize, or alias mapped IDs — `mitre_attack: ["reconnaissance", "resource_development"]` uses the exact tactic-name keys MITRE publishes.

## The `reserved` lifecycle state

Some identifiers exist in the framework as `reserved` rather than `active`, `deprecated`, or `superseded`. A reserved ID is intentionally held — it is not in use, not a tombstone of prior content, and not available for assignment. Reasons an ID may be reserved:

- The item was withdrawn during pre-publication review (e.g., AP027 in V1.0)
- The slot is being held for a planned future addition with a known semantic
- The slot was assigned in a draft and the maintainer chose not to ship it

A reserved ID will never appear with content. It exists in the framework so that the next available number does not conflict with its slot. See [DEPRECATION.md](./DEPRECATION.md) for the full lifecycle-state taxonomy.

## Per-namespace stability discipline

THREAT Matrix has five operational namespaces with different rates of change. The stability contract is the same for all five (no reuse), but the expected churn differs:

| Namespace | Expected churn | Rationale |
|---|---|---|
| `TM####` (tactics) | Very low | Tactics are behavioral categories. A new tactic represents a recognized threat actor behavior that was not previously captured. |
| `AP###` (actor profiles) | Low | Actor profiles are taxonomic groupings. They evolve as the taxonomy matures. |
| `IND-*` (indicators) | Higher | Indicators evolve with detection practice and emerging attack patterns. |
| `CM-*` (countermeasures) | Higher | Countermeasures evolve with defensive technology and operational practice. |
| `RP-*` (response protocols) | Highest | Response protocols evolve with organizational maturity and regulatory context. |

A MINOR release will commonly add new indicators, countermeasures, and response protocols. New tactics and actor profiles are less frequent and trigger more substantial CHANGELOG entries.

## Identifiers from other frameworks

THREAT Matrix references the following external identifier conventions verbatim, treating them as opaque strings:

- **MITRE ATT&CK**: `T####`, `T####.###`, `S####`, `G####`, `TA####`
- **MITRE CAPEC**: `CAPEC-####`
- **MITRE D3FEND**: `D3-[ACRONYM]`
- **MITRE ATLAS**: `AML.T####`, `AML.TA####`
- **NTAC pathway / Calhoun-Weston / CERT insider**: free-text stage names, used as keys in `phase_mappings`

Cross-walks live in `phase_mappings` (Threat Lifecycle phase to source-framework stage) and on per-object cross-reference fields (TBD per framework).
