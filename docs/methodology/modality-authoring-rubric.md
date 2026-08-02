# Modality Authoring Rubric (V1.6)

**Provenance:** V1.6 modality rulings (2026-08-01 session) extending the locked S32 facet model (`RATIONALE-cpn-modality-and-mesh.md`, §7). Governs the matrix-wide authoring of per-indicator `modality` + `human_social` (+ `crossing_mechanism`) across People, Facilities, and Organizations (630 indicators), and any future modality assignment.

## The facet pair

Every indicator carries two independent facets:

- **`modality`** — the behavior's intrinsic instrument class: `physical / cyber / cyber_physical / human_social`.
- **`human_social`** (boolean) — human tradecraft is present anywhere in the behavior (influencing, recruiting, cultivating, coercing, deceiving, negotiating, or human warning-behavior leakage), regardless of medium.

The two co-occur: an armed approach with a coercive demand is `physical` + `human_social: true`. A behavior whose modality **is** `human_social` must carry the boolean `true` (schema-enforced); a behavior with neither a technical instrument nor human tradecraft is an unsplit ambiguous bundle — re-decompose it.

## The core test: instrument versus venue

**Modality is decided by the behavior's own mechanism — its instrument — and where its access lands. Never by its effect, its target's importance, or the venue it travels through.**

- `physical` — matter, force, or **presence** is the instrument: cutting, breaching, emplacing, striking, standing at the target's door. Presence itself can be the threatening act (venue-vs-instrument: showing up at a home is instrument; meeting a recruit at a coffee shop is venue).
- `cyber` — the instrument operates on a computing system's **technical properties**: access, code, data, configuration, or machinery. Consuming already-exposed data IS operating on data systems (locked doctrine). A platform used merely as a communication channel does **not** qualify.
- `cyber_physical` — the behavior itself crosses the seam (cyber action reaching the OT control plane, physical implant gaining cyber reach, EM means producing a physical effect). Requires `crossing_mechanism` (`digital / electromagnetic / physical_implant`).
- `human_social` — the behavior's mechanism lies in the **human, behavioral, social, or institutional domain** — the fourth domain the physical/cyber/crossing trichotomy does not cover (locked S32 definition). This covers BOTH (a) operations whose instrument acts on people or institutions (persuasion, coercion, recruitment, deception, legal process, financial pressure, institutional capture) AND (b) the actor's own observable **warning behaviors and state changes** — grievance and pathway leakage, fixation, identification with prior attackers, withdrawal, energy burst, final-act signature. Both are human-domain phenomena; both route to the same defensive surface (behavioral threat assessment, human observers); neither is physical (no matter/force/presence) or cyber (no computing system).

**Warning behaviors are `human_social`, not a gap.** A behavior does not need an outward instrument to have a modality: its domain decides it. An energy burst, a withdrawal, a grievance fixation live in the human-behavioral domain. Do NOT reach for physical (the observation channel is not the mechanism) or cyber (digitally-observed is not cyber). The operation-vs-signal distinction is real but it is carried by the `category` and `informs_axes` fields, NOT by modality — do not try to encode it here.

## Anchor cases (apply these before reasoning from scratch)

| Behavior | Assignment | Why |
|---|---|---|
| Threatening DM / email / letter | `human_social` | Identical instrument to a spoken threat; the inbox is the envelope. |
| Boycott or disinformation campaign run on platforms | `human_social` (+`true`) | The instrument is persuasion; the platform is venue. |
| Credential phishing / pretext for system access | `cyber` + `human_social: true` | The chain's instrument lands on system access; the deception is real tradecraft — both axes say so. |
| Digital-footprint recon, data-broker aggregation, registry/OSINT collection | `cyber` | Reading data systems is operating on data systems (locked: "consuming already-exposed data is cyber"). |
| Bot networks / fake-account amplification / algorithm gaming | `cyber` + `human_social: true` | The instrument manipulates the platform's machinery, not just its publish button. The same message posted manually by real people is `human_social`. |
| In-person surveillance, approach, site visit | `physical` | Presence/observation in space is the instrument. |
| Weapons or materiel acquisition | `physical` | Stages a physical instrument (acquisition takes the instrument class it stages). |
| Deepfake / forged-document operations | split, then `human_social` family | Same puzzle as a hand-forged letter: fabrication stages a deception instrument; dissemination to deceive is `human_social`. AI industrializes the forgery; it does not relabel it. |
| Building-system / access-control manipulation (BMS, HVAC, badge systems) via network | `cyber_physical` + mechanism | Cyber action producing a physical-environment effect. |
| Lawfare, regulatory abuse, hostile acquisition, front-org construction | `human_social` (+`true`) | The instrument is legal/financial/institutional process. |

**Two symmetric failure modes to avoid:** dumping human-tradecraft behaviors into `physical` because a body performed them somewhere (everything becomes physical — the label dies by universality), and dumping them into `cyber` because they were conducted online (digitally-observed or digitally-carried is not cyber).

## Multi-means bundles: the objective-achieving-means rule

Some indicators bundle several means as alternatives ("acquires drawings via insider elicitation OR contractor channels OR theft"). These are single authored indicators, not re-decomposed in this pass. Assign the modality of the branch that **achieves the operation's objective** — the decisive act — not the first-listed or most-elaborated branch. Set `human_social: true` if ANY branch is human tradecraft, so co-occurrence is never lost. A genuinely co-equal bundle with no decisive means takes its **highest-consequence** branch and is flagged (`uncertain`) as a split-candidate for future authoring.

## Warning-behavior worked examples (People-matrix core)

| Behavior | Assignment | Why |
|---|---|---|
| Grievance rumination, repeatedly returning to a grievance in conversation | `human_social` (+`true`) | Human-domain leakage; behavioral threat assessment owns it. |
| Final-act signature (distributing possessions, manifesto, recording) | `human_social` (+`true`) | Warning behavior in the human-behavioral domain. A manifesto's dissemination may separately be `communication`-category, but the signal's domain is human. |
| Identification with prior attackers (collecting their media, studying them) | `human_social` (+`true`) | Warning behavior. Not `cyber` — consuming the media is the observation channel, not the behavior's mechanism. |
| Energy burst — sudden increase in goal-directed activity | `human_social` (+`true`) | Behavioral-state change; human domain. |
| Withdrawal from family/peers, guarded behavior | `human_social` (+`true`) | Behavioral-state change; human domain. |

## Concealment and financial behaviors

**Concealment is not itself a modality — it takes the modality of its instrument.** A behavior that hides a trail is classified by *what it operates on*, never by the fact that it conceals:
- operates on data / ledgers / accounts (wiping devices, scrubbing search history, deleting posts, planting persistence, migrating infrastructure, crypto mixing / chain-hopping) → `cyber`;
- destroys or disposes of physical materials (burning documents, dumping a weapon) → `physical`;
- moves or pressures value through financial process (funding an operation, extortion, financial coercion, boycott) → `human_social`.

Set `human_social: true` on a `cyber` concealment act when the concealed content is human-domain — grievance/leakage (deleting grievance posts) or the money trail (crypto mixing conceals a financial-domain objective, parallel to how a bot network is `cyber` for the platform-machinery manipulation and `true` for the influence objective).

**The financial bright line:** *operate on ledger data to obscure traceability* is `cyber` (crypto mixing, chain-hopping); *move or pressure value through financial process* is `human_social` (self-financing via cash/assets, extortion, financial coercion). Money being involved does not make a behavior `cyber`; manipulating a ledger's technical traceability property does.

## Boundary discipline

- When one behavior seems to demand two modalities, apply the objective-achieving-means rule above; flag (`uncertain`) only genuinely co-equal bundles. Do not improvise splits during authoring.
- `cyber_physical` outside Infrastructure is rare and real (facility building-systems attacks); every assignment requires `crossing_mechanism` and should be individually defensible.
- Infrastructure's 185 shipped assignments are the precedent corpus; where a behavior has an infra analog, match it.
- Uncertain calls are **flagged, not guessed**. Adjudicated flags become new anchor rows in this rubric.
