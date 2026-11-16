# Deprecation Policy

The THREAT Matrix does not silently remove or repurpose content. This document defines the lifecycle states an object can be in, the fields each state requires, how an object moves between states, and what a consumer should do with each. The JSON Schema (`docs/data/framework.schema.json`), the validator (`scripts/lint/validate.py`, check V26), the ID manifest tool (`scripts/lint/id-manifest.py`), and the viewer all follow the rules below.

In version 2.0.0, twelve Organizations tactics are deprecated, together with their 60 indicators, 48 countermeasures, and 24 response protocols (144 objects). Each names conduct that is commonly lawful or protected activity. The tactics are `TO0302`, `TO0303`, `TO0305` to `TO0312`, `TO0314`, and `TO0315`. Their content stays in the document and no replacement is named. Two actor profiles are `reserved`. No object is superseded: the superseded rules are defined and gated, and have not yet been exercised on real content.

## Lifecycle states

| State | Meaning | Who may carry it |
|---|---|---|
| `active` | Current. This is the state when `lifecycle_state` is absent. | Any object |
| `deprecated` | No longer recommended. No single replacement. Content is still present. | Any object |
| `superseded` | No longer recommended. A replacement is named in `superseded_by`. Content is still present. | Any object |
| `reserved` | The identifier is held and carries no content. | **Actor profiles only** |

"Any object" means a tactic, indicator, countermeasure, response protocol, or actor profile.

`lifecycle_state` is optional. An object without it is `active`. In version 2.0.0, 2 of the 34 actor-profile entries carry the field (both `reserved`), and 144 objects in the Organizations matrix carry it (all `deprecated`). No other object does.

### The reserved rule

- Only an actor profile may be `reserved` inside `framework.json`. A tactic, indicator, countermeasure, or response protocol with `lifecycle_state: reserved` is rejected by the schema and by the validator.
- A reserved actor profile carries exactly three properties: `id`, `lifecycle_state`, and `reserved_reason` (non-empty). Any other property is invalid, so a reserved profile cannot carry content.
- A reserved identifier never receives content later. It is held so the number is never assigned again.
- An identifier in one of the other four namespaces that must be held without an object is recorded in the ID manifest's `reserved` list, not in `framework.json`. See [IDENTIFIERS.md](./IDENTIFIERS.md).

## Required fields by state

| State | Required | Forbidden |
|---|---|---|
| `active` (or field absent) | none | `deprecated_in`, `deprecation_reason`, `superseded_by`, `reserved_reason` |
| `deprecated` | `deprecated_in`, `deprecation_reason` | `superseded_by`, `reserved_reason` |
| `superseded` | `deprecated_in`, `deprecation_reason`, `superseded_by` | `reserved_reason` |
| `reserved` (actor profiles only) | `reserved_reason` | every property other than `id`, `lifecycle_state`, `reserved_reason` |

Field rules:

- `deprecated_in` is the content version (SemVer) in which the object left `active`. It may not be later than the document's own `version`.
- `deprecation_reason` and `reserved_reason` are non-empty text.
- `superseded_by` must name an object that exists, is in the same namespace, is `active`, and is not the object itself. A set of supersessions may not form a cycle. Because the target must be active, a superseded object always points directly at a current object: there is no chain to walk.
- A deprecated or superseded object keeps all of its content and must still satisfy every other rule for its type.

The schema enforces the required and forbidden fields and the shape of each value. The validator enforces what a schema cannot: that `superseded_by` resolves, is active, is in the same namespace, is not a self-reference or part of a cycle, and that `deprecated_in` is not later than the document version.

### Examples

Each example below is a complete object that validates against the named schema definition. The deprecation and supersession shown are hypothetical: `CM-0101-02` is active in the published data.

A deprecated countermeasure, as it would appear in a document at content version 2.1.0:

<!-- validate: framework.schema.json#/$defs/countermeasure -->
```json
{
  "id": "CM-0101-02",
  "measure": "Deploy social media monitoring for mentions of protected individuals, organizational leaders, and key personnel across public platforms",
  "category": "detective",
  "domain": "technical_monitoring",
  "cost": "medium",
  "complexity": "medium",
  "time_to_implement": "weeks",
  "limitations": "Only captures public posts. Encrypted messaging and private communications are not visible. False positive rate is high without human analyst review.",
  "source_refs": ["CISA-CONVERGE-2021"],
  "phase_relevance": ["target_development", "mobilization"],
  "compensates_for": [],
  "lifecycle_state": "deprecated",
  "deprecated_in": "2.1.0",
  "deprecation_reason": "Hypothetical example. Withdrawn with no single replacement."
}
```

The same countermeasure superseded by another active countermeasure in the same namespace:

<!-- validate: framework.schema.json#/$defs/countermeasure -->
```json
{
  "id": "CM-0101-02",
  "measure": "Deploy social media monitoring for mentions of protected individuals, organizational leaders, and key personnel across public platforms",
  "category": "detective",
  "domain": "technical_monitoring",
  "cost": "medium",
  "complexity": "medium",
  "time_to_implement": "weeks",
  "limitations": "Only captures public posts. Encrypted messaging and private communications are not visible. False positive rate is high without human analyst review.",
  "source_refs": ["CISA-CONVERGE-2021"],
  "phase_relevance": ["target_development", "mobilization"],
  "compensates_for": [],
  "lifecycle_state": "superseded",
  "deprecated_in": "2.1.0",
  "deprecation_reason": "Hypothetical example. Merged into CM-0101-05.",
  "superseded_by": "CM-0101-05"
}
```

A reserved actor profile, exactly as `AP022` appears in the data:

<!-- validate: framework.schema.json#/$defs/actor_profile -->
```json
{
  "id": "AP022",
  "lifecycle_state": "reserved",
  "reserved_reason": "Former-insider behavior is modeled via the employment_status modifier on actor_associations rather than as a separate profile (V1.0 design review)."
}
```

## How an object moves between states

1. **Active to deprecated or superseded.** In a MINOR content release, the object gains `lifecycle_state`, `deprecated_in`, `deprecation_reason`, and, if a replacement exists, `superseded_by`. Its content stays.
2. **Deprecated to superseded.** If a replacement is identified later, a deprecated object may become superseded. A superseded object does not go back to deprecated, and neither state returns to active.
3. **Sunset.** A deprecated or superseded object keeps its content for at least one further MINOR release after the release that changed its state. Most are expected to stay indefinitely as a historical record.
4. **Content removal.** After the sunset, an object may be removed from `framework.json`. Removal is a MAJOR content change under [VERSIONING.md](./VERSIONING.md). The identifier is then recorded in the ID manifest's `removed` section with the release that removed it and a reason. A removed identifier is never assigned again.
5. **Splits.** When one object is split into several, it becomes `deprecated` (there is no single replacement) and the reason names the successors.
6. **Moves.** An object never changes parent tactic with its identifier intact. A move is a supersession: a new identifier is issued under the destination tactic and the original becomes `superseded` pointing at it.

The one-MINOR sunset in step 3 and the one-way transitions in step 2 are commitments by the maintainer. They cannot be seen from a single document and no gate checks them. Removal without a record is gated: an identifier that disappears from the document without a `removed` entry fails the ID manifest check.

## What the viewer does

The reference viewer implements the consumer guidance below as follows.

| State | Viewer behavior |
|---|---|
| `active` | Shown normally. |
| `deprecated` | Shown, marked with a "deprecated" tag in lists and a note on the detail view giving the version and the reason. Not hidden. |
| `superseded` | Shown, marked with a "superseded" tag and a note giving the version, the reason, and a link to the replacement. Not hidden. |
| `reserved` | Reserved actor profiles are kept out of the profile list and the profile count. Opening a reserved identifier directly (for example `#/actors/AP022`) shows a notice that the identifier is reserved, not a profile. |

## Consumer guidance

- **Treat a missing `lifecycle_state` as `active`.** The schema's `default` is an annotation. A validator does not insert the field.
- **Mark deprecated and superseded objects wherever you show them.** Showing them unmarked is the error to avoid. A consumer may also offer a filter that hides them; the reference viewer does not.
- **Follow `superseded_by`.** When stored data refers to a superseded identifier, show the replacement alongside it. The target is always active, so one hop is enough.
- **Never present a reserved identifier as data.** Skip reserved actor profiles in lists and counts.
- **For audit and longitudinal work, resolve every state.** Past records may refer to identifiers that have since been deprecated, superseded, or removed. Use the ID manifest's `removed` section to explain an identifier that is no longer in the document.
- **To mirror identifiers,** compare your copy against `docs/data/id-manifest.json` at each release.

## Disclosure

A state change is announced in the CHANGELOG entry of the release that makes it. The entry gives the identifier, the new state, the replacement if any, the reason, and the earliest release at which content removal would be considered. There is no separate announcement; the CHANGELOG is the notice. A removal, being a MAJOR change, also follows the pre-announcement rule in [VERSIONING.md](./VERSIONING.md).

## History of the two reserved profiles

- `AP022` was proposed in the V1.0 design as a "former insider" profile. Review concluded that "former" is better expressed as the `employment_status` modifier on a tactic's actor association. The identifier was withdrawn before publication and is reserved.
- `AP027` was withdrawn during V1.0 pre-publication review and is reserved.

Neither appeared in a published document before schema 3.0.0, which is the first schema able to express a reserved identifier. They appear as reserved stubs from content version 2.0.0, and in the ID manifest's `reserved` list.
