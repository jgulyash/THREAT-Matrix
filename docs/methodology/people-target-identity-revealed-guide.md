# People `target_identity` — revealed-reading authoring guide (S31, Step 2)

Adapts the LOCKED target-dimension rubric (2026-07-10, Field 3) to the 190 People
indicators. Replaces the near-constant **compatibility** reading (179/190 carry all
four values) with the **revealed** reading proven reproducible on facility
(spot-IRR κ 0.94/0.88). Method: author → independent review → blind spot-IRR (Hermes).
This CHANGES shipped values; do not write to framework.json until the spot-IRR passes.

## The core rule (LOCKED, from the rubric)

Tag only what observing **this indicator class actually reveals** about the actor's
victim selection — never "which classes it could serve." Empty/absent array = the
behavior reveals nothing about victim identity.

| value | reveals selection of… |
|---|---|
| `named_individual` | a specific pre-identified person is the object (surveil/stalk/develop/attack a known subject) |
| `role_or_identity_category` | selection is by role / what-they-are (a judge, cops by uniform, clinic staff, journalists) |
| `affinity_group` | a cohesive group property selects the victims (demographic, religious, ethnic — e.g. worshippers) |
| `indiscriminate` | anyone / a random crowd, no selection filter (mass-casualty by proximity/availability) |
| *(empty)* | nothing about victim identity (capability, tradecraft, logistics, financing, OPSEC, most evasion) |

## The target-COUPLING rule (the person-specific engine — this is what makes it revealed)

Ask per behavior: **does observing this class resolve WHO the victim is?**

1. **Victim-coupled behaviors → tag the revealed class.** These inherently reference/act-on a victim:
   - Target selection, subject profiling, surveillance-of-a-subject, pattern-of-life, approach to the subject, execution/attack on the subject, threats/communications naming or about the victim, captivity/leverage of the subject.
   - Default for "**the subject**" phrasing = **named_individual** — a specific pre-identified person is the object of the behavior (the person matrix's baseline). Escalate to role/affinity/indiscriminate ONLY when the behavior text specifies the selection basis (a role, a group property, or a crowd/mass).
2. **Victim-decoupled behaviors → empty.** These reveal nothing about who:
   - Capability acquisition, weapon/method practice, financing, generic tradecraft/cover/disguise, movement/logistics, OPSEC/concealment, evidence management, laundering, most flight/aftermath-evasion.
   - Even though an actor HAS a victim, the *behavior class* (buying a gun, laundering money) does not reveal which identity-class → empty.

## Person anchors (calibration)

| behavior pattern | revealed | why |
|---|---|---|
| surveils the subject's residence / follows the subject | `named_individual` | a specific person is the resolved object |
| researches/develops a specific named target | `named_individual` | |
| targets someone for their role (a judge, an officer, a journalist) | `role_or_identity_category` | selected by what-they-are |
| attack on worshippers / a demographic / an ethnic group | `affinity_group` | group property selects the victims |
| opens fire on a random crowd / public space by availability | `indiscriminate` | no selection filter |
| acquires a firearm / builds a device / raises funds | *(empty)* | capability — no victim signal |
| practices the method / rehearses tradecraft / disguise | *(empty)* | tradecraft — no victim signal |
| launders proceeds / destroys evidence / flees / establishes alibi | *(empty)* | aftermath evasion — no victim signal |
| leaks intent naming the subject / threatens the named person | `named_individual` | communication resolves the victim |
| manifesto naming a group as the enemy | `affinity_group` or `role_or_identity_category` | declares the victim class |

## Multi-tag discipline
Usually ONE value. Multi only when the behavior genuinely reveals two (e.g. a judge
attacked as role AND as a member of a targeted affinity → `role_or_identity_category`
+ `affinity_group`). Do not stack "could-also-be" classes — that recreates the
compatibility field.

## Boundary calls
- **named_individual vs role:** if the behavior acts on a *resolved specific person*
  (their residence, their routine, their name) → named_individual, even if they were
  originally selected by role. Use role only when the behavior reveals the selection
  is by category and no specific person is resolved (e.g. "targets police officers").
- **affinity vs indiscriminate:** did a group property select the victims or the
  venue? Yes → affinity_group; no (pure crowd/availability) → indiscriminate.
- **When the behavior is genuinely victim-agnostic at type level** (most capability/
  tradecraft/aftermath), leave empty — that IS the revealed answer, and it is the
  whole point of the re-read.

## CLARIFICATION (Jay, 2026-07-12) — named_individual is plural-capable; site couples to person(s)

A specific target-associated **site / environment / route / location is coupled to the
specific person(s)** who occupy or are associated with it — so a behavior directed at
that site DOES reveal the victim: it reveals that **specific known person(s) — one OR
MORE** — are the target → `named_individual`. A site can indicate that more than one
person is the target (a residence → a household; a specific office → its known occupants);
that is still `named_individual` (specific known persons), NOT affinity_group (property-
selected) or indiscriminate (random/mass).

**Consequence for the re-read:** site/environment-directed OBSERVATION behaviors —
environmental survey (TM0103), surveillance-detection recon of the subject's environment
(TM0108), site/route rehearsal (TM0201), pause-presence near the environment (TM0207),
approach of the target environment (TM0209) — reveal `named_individual` and are KEPT
named. (The spot-IRR's "empty" reading on these was the wrong direction.) `empty` remains
only for behaviors with NO coupling to a specific target or its site: generic capability
acquisition, financing, OPSEC/concealment not tied to the target's site, cover-building,
network-building, response/bystander tradecraft, and aftermath evasion. Breach/access
MECHANICS (TM0203/04/05) stay empty — they reveal HOW to get in, not WHO (the access-vs-
target line, same as informs_axes access≠method).
