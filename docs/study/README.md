# Presence-coding reliability study

**Status: protocol drafted; not preregistered; no raters recruited; no cases selected; no data; no results.**

Everything in this directory is a draft protocol and an empty scaffold for a study that has not been run. Nothing here is evidence about the vocabulary.

## What the study is

A planned test of whether independent, credentialed practitioners agree on which People and Facilities indicators are present in written narratives of public, adjudicated cases. It measures reliability of presence coding. It does not measure predictive validity and it does not validate any scoring.

## Contents

| File | What it is | State |
|---|---|---|
| `PROTOCOL.md` | Preregistration-style protocol: purpose, materials, raters, statistics and thresholds fixed in advance, ethics, release, decision gate | draft 0.1.0, not registered |
| `CODING-MANUAL.md` | Instructions a rater follows, with fictional micro-examples | draft, not piloted |
| `coded-case.schema.json` | JSON Schema (draft 2020-12) for one rater's codes for one case | draft |
| `candidate-cases.md` | 34 candidate public cases with primary documents and link status | draft list, nothing selected |
| `analysis/agreement.py` | Computes percent agreement, Krippendorff's alpha, Gwet's AC1, prevalence and bias indices per indicator, tactic, and matrix. Standard library only | working, tested on synthetic inputs |
| `analysis/test_agreement.py` | Tests with synthetic fixtures whose expected values are known by hand or from a published worked example | passes |
| `dataset/README.md` | Planned dataset layout | empty scaffold |
| `dataset/cases/` | Where coded case files will go | empty |

## Before the study can start

1. A coordinator who is not the maintainer and not a rater.
2. Four to six independent, credentialed raters with signed conflict-of-interest declarations.
3. A decision on ethics review and on the dataset license.
4. Selected cases, written and checked narratives, and a completed pilot.
5. The protocol lodged with a public registry, with checksums of the vocabulary release, manual, and analysis script.

None of these has happened.

## What a result would and would not allow

See `PROTOCOL.md` sections 1, 8, and 15. In short: a passing result allows the statement that trained raters agreed on presence at a stated level in this sample. It allows no statement about prediction, risk, or scores.

## Checks

```
python3 docs/study/analysis/test_agreement.py
python3 docs/study/analysis/agreement.py docs/study/dataset/cases
```
