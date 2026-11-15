#!/usr/bin/env python3
"""Tests for agreement.py.

EVERY INPUT IN THIS FILE IS SYNTHETIC. Nothing here is rater data, a study
result, or a real case. The fixtures are constructed so the expected
coefficients can be checked by hand or against a published worked example.

Run:  python3 docs/study/analysis/test_agreement.py
"""

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agreement as ag  # noqa: E402

P, A, C = ag.PRESENT, ag.ABSENT, ag.CANNOT
BINARY = (P, A)

SYNTHETIC_NOTE = "SYNTHETIC TEST FIXTURE. Not rater data. Not a real case."


def synthetic_case(case_id, rater, codes):
    """Build a SYNTHETIC coded case document shaped like coded-case.schema.json."""
    return {
        "study_version": "0.1.0-draft",
        "case_id": case_id,
        "case_title": "SYNTHETIC fixture " + case_id,
        "case_class": "non_attack_comparison",
        "sources": [{"title": SYNTHETIC_NOTE, "url": "https://example.invalid/synthetic", "type": "court_document"}],
        "narrative_ref": "synthetic/" + case_id + ".md",
        "rater_pseudonym": rater,
        "framework_version": "2.0.0",
        "codes": [
            dict({"indicator_id": ind, "code": code, "confidence": "high"},
                 **({"evidence_passage": SYNTHETIC_NOTE} if code == P else {}))
            for ind, code in codes.items()
        ],
        "coded_on": "2000-01-01",
    }


class CoefficientTests(unittest.TestCase):

    def test_perfect_agreement_with_both_categories(self):
        # SYNTHETIC. Two raters agree on every unit and both categories occur.
        units = [[P, P], [A, A], [P, P], [A, A], [A, A]]
        self.assertAlmostEqual(ag.percent_agreement(units), 1.0)
        self.assertAlmostEqual(ag.krippendorff_alpha_nominal(units), 1.0)
        self.assertAlmostEqual(ag.gwet_ac1(units, BINARY), 1.0)

    def test_perfect_agreement_without_variation(self):
        # SYNTHETIC. Everyone codes absent everywhere. Alpha is undefined
        # (expected disagreement is zero); AC1 is 1. This is the prevalence
        # problem the protocol handles by reporting both.
        units = [[A, A, A]] * 6
        self.assertAlmostEqual(ag.percent_agreement(units), 1.0)
        self.assertIsNone(ag.krippendorff_alpha_nominal(units))
        self.assertAlmostEqual(ag.gwet_ac1(units, BINARY), 1.0)
        self.assertEqual(ag.band(None), "not_computable")

    def test_chance_level_agreement(self):
        # SYNTHETIC. Two raters, four units, one of each combination.
        # By hand: pa = 2/4 = 0.5. Each category has share 0.5, so
        # AC1 pe = 2 * 0.25 / (2 - 1) = 0.5 and AC1 = 0.
        # Alpha: n = 8 values, 4 present and 4 absent, 2 disagreeing units.
        # alpha = 1 - (n - 1) * 2 * 2 / (n^2 - 4^2 - 4^2) = 1 - 28/32 = 0.125
        # (the small-sample term keeps it slightly above zero).
        units = [[P, P], [P, A], [A, P], [A, A]]
        self.assertAlmostEqual(ag.percent_agreement(units), 0.5)
        self.assertAlmostEqual(ag.gwet_ac1(units, BINARY), 0.0)
        self.assertAlmostEqual(ag.krippendorff_alpha_nominal(units), 0.125)

    def test_complete_disagreement(self):
        # SYNTHETIC. Two raters disagree on every unit.
        # By hand: pa = 0; AC1 = (0 - 0.5) / 0.5 = -1;
        # alpha = 1 - 3 * 4 / (16 - 4 - 4) = -0.5.
        units = [[P, A], [A, P]]
        self.assertAlmostEqual(ag.percent_agreement(units), 0.0)
        self.assertAlmostEqual(ag.gwet_ac1(units, BINARY), -1.0)
        self.assertAlmostEqual(ag.krippendorff_alpha_nominal(units), -0.5)

    def test_krippendorff_published_binary_example(self):
        # Worked example B in Krippendorff, "Computing Krippendorff's
        # Alpha-Reliability" (2011), https://repository.upenn.edu/asc_papers/43
        # Two observers, ten units, binary data. Published alpha = 0.095.
        # By hand: n = 20, 14 zeros and 6 ones, 4 disagreeing units:
        # alpha = 1 - 19 * 4 / (14 * 6) = 0.0952.
        first = [0, 1, 0, 0, 0, 0, 0, 0, 1, 0]
        second = [1, 1, 1, 0, 0, 1, 0, 0, 0, 0]
        units = [[x, y] for x, y in zip(first, second)]
        self.assertAlmostEqual(ag.krippendorff_alpha_nominal(units), 1 - 76 / 84)
        self.assertAlmostEqual(round(ag.krippendorff_alpha_nominal(units), 3), 0.095)

    def test_krippendorff_published_missing_data_example(self):
        # Worked example C in the same paper: four observers, twelve units,
        # five nominal categories, missing values. Published nominal
        # alpha = 0.743. None marks a missing value.
        N = None
        obs_a = [1, 2, 3, 3, 2, 1, 4, 1, 2, N, N, N]
        obs_b = [1, 2, 3, 3, 2, 2, 4, 1, 2, 5, N, 3]
        obs_c = [N, 3, 3, 3, 2, 3, 4, 2, 2, 5, 1, N]
        obs_d = [1, 2, 3, 3, 2, 4, 4, 1, 2, 5, 1, N]
        units = [[v for v in col if v is not None] for col in zip(obs_a, obs_b, obs_c, obs_d)]
        self.assertAlmostEqual(round(ag.krippendorff_alpha_nominal(units), 3), 0.743)

    def test_high_prevalence_splits_alpha_and_ac1(self):
        # SYNTHETIC. Two raters, ten units: eight both present, two split.
        # By hand: pa = 0.8. Share present = 0.9, so
        # AC1 pe = 2 * 0.9 * 0.1 = 0.18 and AC1 = 0.62 / 0.82 = 0.7561.
        # Alpha: n = 20, 18 present and 2 absent, 2 disagreeing units:
        # alpha = 1 - 19 * 2 * 2 / (400 - 324 - 4) = 1 - 76/72 = -0.0556.
        units = [[P, P]] * 8 + [[P, A], [A, P]]
        self.assertAlmostEqual(ag.percent_agreement(units), 0.8)
        self.assertAlmostEqual(ag.gwet_ac1(units, BINARY), 0.62 / 0.82)
        self.assertAlmostEqual(ag.krippendorff_alpha_nominal(units), 1 - 76 / 72)
        self.assertAlmostEqual(ag.prevalence(units), 0.9)
        self.assertAlmostEqual(ag.prevalence_index(units), 0.8)

    def test_bias_index(self):
        # SYNTHETIC. R01 codes present where R02 codes absent on 3 of 10
        # units and never the reverse: bias index = |3 - 0| / 10 = 0.3.
        rater_units = [{"R01": P, "R02": A}] * 3 + [{"R01": A, "R02": A}] * 7
        self.assertAlmostEqual(ag.bias_index(rater_units), 0.3)

    def test_band_thresholds(self):
        self.assertEqual(ag.band(0.80), "acceptable")
        self.assertEqual(ag.band(0.799), "tentative")
        self.assertEqual(ag.band(0.67), "tentative")
        self.assertEqual(ag.band(0.669), "below_threshold")


class EndToEndTests(unittest.TestCase):
    """SYNTHETIC coded case files written to a temporary directory."""

    def _write(self, directory, docs):
        for i, doc in enumerate(docs):
            with open(os.path.join(directory, "synthetic-%02d.json" % i), "w", encoding="utf-8") as fh:
                json.dump(doc, fh)

    def _chance_fixture(self):
        # The chance-level pattern above, spread over four SYNTHETIC cases for
        # one People indicator and one Facilities indicator.
        pattern = [(P, P), (P, A), (A, P), (A, A)]
        docs = []
        for n, (x, y) in enumerate(pattern, start=1):
            case = "CASE-9%02d" % n
            docs.append(synthetic_case(case, "R01", {"IND-0101-01": x, "IND-F0101-01": x}))
            docs.append(synthetic_case(case, "R02", {"IND-0101-01": y, "IND-F0101-01": y}))
        return docs

    def test_levels_and_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._write(tmp, self._chance_fixture())
            rows = ag.analyse(ag.load_cases(tmp))
        by_id = {(r["level"], r["id"]): r for r in rows}
        self.assertEqual(set(by_id), {
            ("matrix", "person"), ("matrix", "facility"),
            ("tactic", "TM0101"), ("tactic", "TF0101"),
            ("indicator", "IND-0101-01"), ("indicator", "IND-F0101-01"),
        })
        for key, row in by_id.items():
            self.assertAlmostEqual(row["percent_agreement"], 0.5, msg=str(key))
            self.assertAlmostEqual(row["krippendorff_alpha"], 0.125, msg=str(key))
            self.assertAlmostEqual(row["gwet_ac1"], 0.0, msg=str(key))
            self.assertEqual(row["band"], "below_threshold")
            self.assertEqual(row["n_raters"], 2)

    def test_cannot_determine_is_missing_by_default(self):
        # SYNTHETIC. A third rater codes cannot_determine everywhere. Treated
        # as missing it changes nothing; treated as a category it lowers
        # agreement.
        docs = self._chance_fixture()
        for n in range(1, 5):
            docs.append(synthetic_case("CASE-9%02d" % n, "R03", {"IND-0101-01": C}))
        with tempfile.TemporaryDirectory() as tmp:
            self._write(tmp, docs)
            table = ag.load_cases(tmp)
        default = {r["id"]: r for r in ag.analyse(table)}
        as_cat = {r["id"]: r for r in ag.analyse(table, cd_as_category=True)}
        self.assertAlmostEqual(default["IND-0101-01"]["krippendorff_alpha"], 0.125)
        self.assertAlmostEqual(default["IND-0101-01"]["cannot_determine_rate"], 4 / 12)
        self.assertLess(as_cat["IND-0101-01"]["percent_agreement"], 0.5)

    def test_duplicate_coding_is_rejected(self):
        docs = [synthetic_case("CASE-901", "R01", {"IND-0101-01": P}),
                synthetic_case("CASE-901", "R01", {"IND-0101-01": A})]
        with tempfile.TemporaryDirectory() as tmp:
            self._write(tmp, docs)
            with self.assertRaises(ag.InputError):
                ag.load_cases(tmp)

    def test_out_of_scope_indicator_is_rejected(self):
        for bad in ("IND-O0101-01", "IND-0101-01\n", "IND-0101-1"):
            with self.assertRaises(ag.InputError):
                ag.indicator_parents(bad)

    def test_cli_runs_and_bootstrap_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._write(tmp, self._chance_fixture())
            outputs = []
            for _ in range(2):
                buf = io.StringIO()
                with redirect_stdout(buf):
                    code = ag.main([tmp, "--json", "-", "--bootstrap", "200", "--seed", "7"])
                self.assertEqual(code, 0)
                outputs.append(json.loads(buf.getvalue()))
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[0]["cannot_determine_handling"], "missing")

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(ag.main([tmp]), 0)
            self.assertIn("No coded case files", buf.getvalue())

    def test_synthetic_fixture_matches_schema(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "coded-case.schema.json")
        with open(schema_path, encoding="utf-8") as fh:
            schema = json.load(fh)
        validator = jsonschema.Draft202012Validator(schema)
        for doc in self._chance_fixture():
            self.assertEqual(list(validator.iter_errors(doc)), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
