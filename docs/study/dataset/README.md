# Coded case dataset

**Status: EMPTY SCAFFOLD. No cases have been selected, summarised, or coded. No rater has been recruited. This directory contains no data. The study protocol is a draft that has not been registered or run (see `../PROTOCOL.md`).**

This file describes the layout the dataset will have if and when the study runs, so that tooling and readers know what to expect.

## Planned layout

```
docs/study/dataset/
  README.md                  this file
  MANIFEST.json              per release: dataset version, vocabulary version, file checksums (not yet present)
  DEVIATIONS.md              copy of the protocol deviations log at release (not yet present)
  narratives/
    CASE-001.md              neutral case narrative read by raters, with source list (none yet)
  cases/
    .gitkeep                 placeholder so the empty directory is tracked
    CASE-001.R01.json        one file per rater per case, shaped like ../coded-case.schema.json (none yet)
  reference/
    CASE-001.reference.json  consensus reference coding, a separate labelled layer (none yet)
  pilot/                     pilot cases and codes, excluded from analysis (none yet)
  analysis/
    agreement.json           output of ../analysis/agreement.py for the release (none yet)
```

## File rules

- Coded case files validate against `../coded-case.schema.json`. The schema is closed: it has no field for a score, weight, band, or priority, and one cannot be added.
- File name: `<case_id>.<rater_pseudonym>.json`, for example `CASE-001.R01.json`.
- `rater_pseudonym` is a study-assigned code (R01, R02, ...). No name, initials, employer, or credential number appears in any file. The key that links pseudonyms to people is not stored in this repository.
- `evidence_passage` quotes the narrative in `narratives/`, not the underlying source.
- Narratives name no victim, witness, family member, or minor, and state nothing about a living private individual beyond what the cited court or official document published.
- Published releases are not edited. Corrections are issued as a new dataset version with a change note.

## Running the analysis

```
python3 docs/study/analysis/agreement.py docs/study/dataset/cases
```

On the current empty directory this prints "No coded case files found" and exits 0. The script's tests use synthetic inputs only:

```
python3 docs/study/analysis/test_agreement.py
```

## Use limits

When data exists, it will be research material about a vocabulary. A coded behavior is not a finding about any person. The dataset must not be used to assess, score, or take action against any individual, and it does not validate any scoring overlay (see `../PROTOCOL.md`, section 15).

## License

Not yet decided. See `../PROTOCOL.md`, section 12.
