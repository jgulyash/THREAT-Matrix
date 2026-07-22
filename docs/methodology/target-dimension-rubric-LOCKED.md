# Target-dimension authoring rubric — LOCKED 2026-07-10

Locks the value definitions for the facility target fields and the re-read of
People's `target_identity`, so authoring across ~390 indicators is consistent.
Locked by Jay 2026-07-10; author against this. Method: author + independent
review, validated by a blind spot-IRR (reliability gate); escalate any field
that spot-checks weak.

## The core rule: REVEALED reading (not applicability)

Tag only what observing **this indicator class actually reveals** about the
actor's target selection — never "which classes could it apply to." Most
indicators reveal one class; some reveal none (leave empty = unrevealed). This
is the fix for People's near-constant field. All fields are optional
multi-select arrays; an empty/absent array means the behavior reveals nothing on
that dimension.

---

## Field 1 — `facility_target_scope` (breadth of site selection) · facility

| value | reveals the actor is selecting… | anchor |
|---|---|---|
| `specific_site` | one identified building | grievance tied to a named facility; surveillance of a specific building; as-built drawings of this site |
| `site_class` | any facility of a function/organization class | researching "similar facilities"; targeting any branch of an org; any clinic/school of a type |
| `symbolic_category` | sites sharing symbolic/ideological meaning across function | "government buildings" generally; places of worship of a faith; landmarks |
| `indiscriminate` | any accessible site; opportunistic, no site preference | soft-target seeking with no site tie |
| *(empty)* | nothing about breadth | acquiring generic materials; a capability with no site tie |

## Field 2 — `within_site_focus` (what inside the facility bears the harm) · facility

| value | reveals the harm focus is… | anchor |
|---|---|---|
| `structure` | the building/physical asset | arson, structural sabotage, defacement, demolition |
| `occupants` | the people inside | mass-casualty intent, hostage-taking, active-shooter positioning, bystander management |
| `systems` | utilities / controls / functional systems | power, water, HVAC/contamination, fire/security-system defeat |
| `whole_site` | the site as an undifferentiated unit | seizure/occupation of the whole facility; a threat against "the site" |
| *(empty)* | nothing about within-site focus | early recon that hasn't resolved the aim |

**Decision rule (locked) — the interpretive boundaries:**
- **Occupied-structure attacks (structure vs occupants):** tag `occupants` when
  the behavior shows casualty intent — people are the aim (mass-casualty,
  attack timed to occupancy, targeting where people gather). Tag `structure`
  when the aim is property/denial/symbolic damage and casualties are incidental
  (arson/sabotage of an unoccupied or off-hours site, defacement). Tag BOTH only
  when the behavior genuinely reveals both aims (e.g., bombing timed to
  occupancy to destroy the building AND kill occupants).
- **`whole_site` vs a specific focus:** use `whole_site` only when the behavior
  targets the site as a unit without resolving structure/occupants/systems
  (seizure, occupation, a generic threat "against the facility"). If the behavior
  resolves a specific aim, use that instead.
- **`systems` scope:** utilities/controls/functional systems whose defeat or
  contamination is the aim — including fire/security-system defeat that is the
  attack itself. (Defeating a security system merely to *gain access* is
  access tradecraft, not a systems-focus attack — leave empty on those.)

## Field 3 — People `target_identity` (re-read to the revealed reading)

Same four values, same array — but author only what the indicator **reveals**,
not all classes (fixes the near-constant 190/190). Values unchanged:

| value | reveals selection of… |
|---|---|
| `named_individual` | a specific known person (assassination, stalking, kidnapping of a known target) |
| `role_or_identity_category` | anyone in a role/identity (a judge; a member of a group) |
| `affinity_group` | a specific cohesive group |
| `indiscriminate` | anyone / mass victim, no selection |
| *(empty)* | nothing about victim breadth (e.g., capability acquisition) |

---

## Mechanics to confirm at lock
- **Empty vs a `not_revealed` token.** Recommend empty/absent array = unrevealed
  (clean, no new enum value). Fields optional.
- **Single vs multi tag.** Multi-select allowed but author tightly — usually one
  value; two only when the behavior genuinely reveals two (e.g., a bombing of a
  specific site targeting occupants → scope `specific_site` + focus `occupants`,
  which are different fields anyway, so each field is usually single).
- **Verification.** Author + independent review pass (lighter than the full
  sealed-blind IRR, since these are less interpretive than informs_axes) — or
  escalate to sealed-blind IRR if you want the same rigor. Your call at lock.

## Execution roadmap once locked
1. Schema: add `facility_target_scope` + `within_site_focus` (facility indicators); update `target_identity` description to the revealed reading.
2. Author facility: 200 indicators × 2 fields (chunked + review).
3. Re-author People `target_identity`: 190 indicators, revealed reading.
4. SPA: render the new facility target fields (mirror the People target_identity render).
5. **Gate 2 — informs_axes IRR extension to facility** (200 × 6 axes, sealed-blind chunks). The large one.
6. Release checklist.
