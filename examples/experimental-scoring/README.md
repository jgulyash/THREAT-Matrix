# Experimental Scoring Examples

> **Overlay notice.** Everything in this folder is **experimental and non-normative**. The scoring overlay (`docs/data/scoring-overlay.json`) holds authored, **type-level** estimates for classes of behavior. They are **unvalidated**: they have not been tested against outcomes or checked by independent human reviewers. They are **not a risk score** and never a score of a person. They do not predict violence. They must **not be used as grounds for adverse action**. The vocabulary in `framework.json` and the score-free case record in `../` are complete without anything here.

If you are looking for a record to use in casework, use the score-free record: `../case-record-template.json`, `../case-record-worksheet.md`, and `../worked-cases/`. This folder exists so that people who want to study the scoring experiment can see its record format and check it.

## What is here

| File | What it is |
|---|---|
| `scored-record-template.json` | A placeholder scored record. Uses a real indicator ID (IND-0101-01) with that indicator's overlay type band (medium), all six factors at `unknown`, priority held at the type band. |
| `worked-cases/case-3-held-at-type-band.json` | Scored version of fictional worked case 3. IND-0101-01, type band medium, priority medium, disposition `closed_benign`. |
| `worked-cases/case-4-raised-one-band.json` | Scored version of fictional worked case 4. IND-0101-02, type band high, priority critical, disposition `heightened_monitoring`. |
| `worked-cases/case-5-disrupted-by-interdiction.json` | Scored version of fictional worked case 5 as it stood just before the interdiction. IND-0104-01, type band high, priority critical, disposition `disrupted_by_interdiction`. |

All three cases are fictional and say so in their `basis` text.

## The scored record

A scored record joins one indicator's type band from the overlay to the six instance factors for one case, and states a resulting priority:

```json
{
  "indicator_id": "IND-0101-01",
  "type_band": "medium",
  "instance": { "target_focus": "...", "pathway_stage": "...", "means_in_hand": "...", "tempo_trajectory": "...", "proximity_access": "...", "source_credibility": "...", "basis": "..." },
  "conditioned_priority": "medium",
  "primary_objective_evidence_tier": "optional",
  "disposition": "optional"
}
```

- `type_band` must equal the overlay's `indicator_scores[indicator_id].type_band`. The gate checks this, and checks that the indicator exists.
- `instance` holds the same six factors as the score-free record, with the same meanings. Means in hand is about means actually possessed or acquired; lawful ability to acquire something is not means in hand.
- `conditioned_priority` is the priority the assessor assigns after considering the instance.
- The definition lives in `docs/data/scoring-overlay.schema.json` (`$defs.scored_case_record` and `$defs.instance_assessment`).

## The escalate-only rule, as an experiment

In this experiment the instance factors may raise `conditioned_priority` above `type_band` but may never put it below. A record whose priority is under its type band is rejected. The idea being tested is that a type-level band should act as a floor, so that a mild-looking class of behavior can be raised by case facts while missing information can never lower a case.

Read these limits before drawing anything from it:

- **The rule only moves one way.** A scored record cannot show concern going down. In worked case 3 the team lowered its concern twice and closed the case as benign, and the scored version still reads medium, the type band for a stated grievance. The outcome is carried only by `disposition`. The score-free record shows the same case with its lowered reassessments written out.
- **The floor is authored, not measured.** The type bands are estimates for classes of behavior. A floor built on them inherits their uncertainty.
- **One indicator per record.** A scored record is tied to a single indicator. A real case usually involves several, and this format gives no rule for combining them. The score-free record lists every observation.
- **No protective factors.** The scored record has no place for them. The score-free record requires them.
- **The overlay's raise patterns are advisory.** `instance_conditioning.raise_guidance` in the overlay lists patterns such as a specific target together with means assessed or confirmed present. They are prompts for discussion, not a formula, and they have not been validated.

For these reasons a scored record should not be placed in a case file or used to make a decision about a person.

## How the three examples were filled in

- **Case 3, held.** A grievance about a named manager, with a confirmed benign explanation for the schedule questions. Means in hand is `unknown`, because nothing indicates possession. No raise pattern applies, so priority stays at the type band.
- **Case 4, raised.** Sustained research on one named executive, a firsthand account of a recently bought handgun (`assessed_present`, on possession), camera footage at the residence, and observations coming closer together. Priority is raised from high to critical.
- **Case 5, raised, then interdicted.** Acquisition directly observed and later recovered (`confirmed_present`), a specific target, workplace access, and an accelerating tempo. Priority is raised from high to critical. The record keeps the pre-interdiction picture, and `disposition` records the interdiction.

## Check the files

From the repository root:

```bash
python3 scripts/lint/validate.py docs/data/framework.json --overlay docs/data/scoring-overlay.json --records examples/experimental-scoring/worked-cases
python3 scripts/lint/consumer-smoke.py
```

The first command checks each scored record in `worked-cases/`: the indicator exists, `type_band` matches the overlay, and the priority is not below the type band. The second also validates the template.
