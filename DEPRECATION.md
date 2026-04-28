# Deprecation Policy

THREAT Matrix never silently removes content. This document defines the lifecycle states an identifier can occupy, how items move between states, and what consumers should do at each state.

## Lifecycle states

Every identifier is in exactly one of the following states at any given release:

| State | Meaning | Identifier preserved? | Content present? |
|---|---|---|---|
| `active` | The default. The item is current and recommended. | Yes | Yes |
| `deprecated` | The item is no longer recommended. No replacement is offered. The item is retained for one or more MINOR releases for consumer migration. | Yes | Yes |
| `superseded` | The item is no longer recommended. A replacement is identified (`superseded_by`). | Yes | Yes |
| `reserved` | The identifier slot is held intentionally. No content is present and none is planned. | Yes | No |

A document MUST surface lifecycle state via a `lifecycle_state` field on every tactic, actor profile, indicator, countermeasure, and response protocol object. The default value when the field is absent is `active` (this is the current convention while V1.1 backfills are in progress; future MAJOR releases may make the field mandatory).

## How an item moves between states

```
              ┌──────────────┐
   author ──> │   active     │
              └──────┬───────┘
                     │
            (no replacement)         (replacement identified)
                     │                       │
                     v                       v
              ┌──────────────┐        ┌──────────────┐
              │  deprecated  │ ─────> │  superseded  │
              │              │        │              │
              └──────┬───────┘        └──────┬───────┘
                     │                       │
                     │      (sunset window)   │
                     │                       │
                     v                       v
              ┌──────────────┐        ┌──────────────┐
              │   reserved   │ <───── │   reserved   │
              │ (no content) │        │ (no content) │
              └──────────────┘        └──────────────┘
```

A `deprecated` item may transition to `superseded` if a replacement is later identified. A `superseded` item does not return to `deprecated`.

A `reserved` slot may receive new content under exceptional circumstances (a pre-publication withdrawal that is later vindicated). This is rare and triggers a CHANGELOG entry calling out the slot reuse — note that this is not identifier reuse for *different* content, which is forbidden by [IDENTIFIERS.md](./IDENTIFIERS.md). It is the original assignment being activated.

## Sunset window

The minimum sunset window for `deprecated` and `superseded` items before any consideration of content removal is **one MINOR release**. The content of the deprecated item is preserved through that minor; only after the next minor ships may a future minor remove the content (transitioning the item to `reserved`).

In practice, content removal is rare. Most deprecated items remain in the framework as historical record, with `lifecycle_state` flagging them. Consumers can filter on the field at query time.

## Required fields by lifecycle state

### `deprecated`

```json
{
  "id": "TA####",
  "lifecycle_state": "deprecated",
  "deprecated_in": "X.Y.Z",
  "deprecation_reason": "Brief explanation suitable for inclusion in a CHANGELOG"
}
```

### `superseded`

```json
{
  "id": "TA####",
  "lifecycle_state": "superseded",
  "deprecated_in": "X.Y.Z",
  "superseded_by": "TA####",
  "deprecation_reason": "Brief explanation"
}
```

`superseded_by` MUST reference an `active` identifier in the same namespace. Cross-namespace supersession (e.g., a tactic superseded by an actor profile) is not supported by V1 — model that as deprecation with explanatory notes instead.

### `reserved`

```json
{
  "id": "AP###",
  "lifecycle_state": "reserved",
  "reserved_reason": "Brief explanation (e.g., 'withdrawn during V1.0 review')"
}
```

A `reserved` object has no behavioral content and validates against a relaxed schema. Consumers should treat reserved IDs as "do not use" rather than as data.

## Consumer guidance

### Filtering at query time

A consumer that surfaces tactics to an end user (UI, agent, report generator) SHOULD filter on `lifecycle_state` by default:

- Show `active` items.
- Hide `deprecated`, `superseded`, and `reserved` items unless the consumer explicitly opts in (e.g., a "Show retired items" toggle).
- When a `superseded` item is referenced — for example, a historical detection rule still pointing at the old ID — surface the `superseded_by` pointer prominently so the user can navigate to the replacement.

### Audit / forensic use

A consumer that performs audit, forensic, or longitudinal analysis MUST honor all four states. Past data may reference identifiers that have since transitioned, and the analysis would be incomplete or wrong if those references could not be resolved. THREAT Matrix's commitment to permanent identifier preservation exists precisely to make this analysis reliable.

### Bulk re-mapping

A consumer can perform a bulk re-mapping pass before ingest using the `superseded_by` chain. The chain is acyclic and finite (a `superseded` item cannot point to another `superseded` item that points back). A consumer SHOULD walk the chain to its terminal `active` item — typically a single hop, but the chain length is not bounded by this policy.

## Disclosure timing

Deprecation is announced in the CHANGELOG entry of the MINOR release that introduces the `deprecated` or `superseded` state. The CHANGELOG entry includes:

- The identifier
- The new state
- The replacement (if any)
- The reason
- The earliest release at which content removal would be considered

This is the consumer's notice. There is no separate deprecation announcement process; CHANGELOG is authoritative.

## Examples

### Worked example: AP022 → modifier on actor associations

In V1.0 design, `AP022` was proposed as "Former Insider." Review concluded that "former" is better modeled as an `employment_status` modifier on actor associations rather than a separate profile. AP022 was retired before V1.0 publication; the slot is `reserved`.

```json
{
  "id": "AP022",
  "lifecycle_state": "reserved",
  "reserved_reason": "Former-insider behavior is modeled via employment_status modifier on actor_associations rather than as a separate profile (decision: V1.0 design review)."
}
```

### Worked example: hypothetical tactic supersession

If a hypothetical `TA0190` were to be split into `TA0191` (selection) and `TA0192` (recruitment) in a MINOR release, `TA0190` would transition to `deprecated` (no single replacement) with the deprecation reason explaining the split:

```json
{
  "id": "TA0190",
  "lifecycle_state": "deprecated",
  "deprecated_in": "1.7.0",
  "deprecation_reason": "Split into TA0191 (selection) and TA0192 (recruitment) for clearer authoring boundaries. Consumers should map references to the appropriate successor based on the indicator set in use."
}
```

The next MINOR (1.8.0) would retain TA0190's content. The MINOR after that (1.9.0) would be the earliest at which content could be removed (transitioning to `reserved`); in practice, the maintainer would likely retain content indefinitely as historical record.
