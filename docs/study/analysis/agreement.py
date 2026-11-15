#!/usr/bin/env python3
"""Agreement statistics for the indicator presence-coding study.

STATUS: analysis script for a DRAFT protocol that has not been run. No coded
data exists yet. See docs/study/PROTOCOL.md.

Reads coded case files (one JSON file per rater per case, shaped like
docs/study/coded-case.schema.json) and reports, per indicator, per tactic,
and per matrix:

  - percent agreement (mean pairwise observed agreement)
  - Krippendorff's alpha for nominal data
  - Gwet's AC1
  - prevalence of "present", prevalence index, bias index
  - share of codes that were "cannot_determine"

A unit is one (case, indicator) pair. Tactic and matrix figures pool every
unit that belongs to the tactic or matrix.

Missing data: by default "cannot_determine" is treated as missing, the same
as an indicator a rater did not code. Use --cd-as-category to treat it as a
third nominal category instead. Units with fewer than two usable codes do
not enter observed agreement or alpha.

Standard library only. Python 3.8 or later.

Usage:
  python3 docs/study/analysis/agreement.py docs/study/dataset/cases
  python3 docs/study/analysis/agreement.py DIR --json out.json --bootstrap 2000 --seed 1
"""

import argparse
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations

INDICATOR_RE = re.compile(r"\AIND-(F?)([0-9]{4})-([0-9]{2})\Z")
CODE_VALUES = ("present", "absent", "cannot_determine")
PRESENT, ABSENT, CANNOT = CODE_VALUES

# Thresholds fixed in docs/study/PROTOCOL.md section 8. Change them there first.
ALPHA_TENTATIVE = 0.67
ALPHA_ACCEPTABLE = 0.80


class InputError(Exception):
    """A coded case file is malformed or conflicts with another file."""


# ---------------------------------------------------------------------------
# Coefficients. Each takes `units`: a list of lists of nominal labels, one
# inner list per unit, holding only the usable (non-missing) codes.
# ---------------------------------------------------------------------------

def percent_agreement(units):
    """Mean over units of the share of rater pairs that agree."""
    pairable = [u for u in units if len(u) >= 2]
    if not pairable:
        return None
    total = 0.0
    for u in pairable:
        r = len(u)
        counts = Counter(u)
        total += sum(v * (v - 1) for v in counts.values()) / (r * (r - 1))
    return total / len(pairable)


def krippendorff_alpha_nominal(units):
    """Krippendorff's alpha, nominal metric, any number of raters, missing data allowed.

    alpha = 1 - Do / De, computed from the coincidence matrix. Returns None
    when it is undefined: fewer than two pairable values, or no variation in
    the pooled values (expected disagreement is zero).
    """
    pairable = [u for u in units if len(u) >= 2]
    n = sum(len(u) for u in pairable)
    if n <= 1:
        return None
    totals = Counter()
    observed = 0.0
    for u in pairable:
        m = len(u)
        counts = Counter(u)
        totals.update(counts)
        observed += (m * m - sum(v * v for v in counts.values())) / (m - 1)
    expected = n * n - sum(v * v for v in totals.values())
    if expected == 0:
        return None
    return 1.0 - (n - 1) * observed / expected


def gwet_ac1(units, categories):
    """Gwet's AC1 for any number of raters, missing data allowed.

    `categories` is the full set of categories a rater could have used, so
    that a category nobody happened to use still counts toward q.
    """
    q = len(categories)
    rated = [u for u in units if len(u) >= 1]
    pa = percent_agreement(units)
    if pa is None or q < 2:
        return None
    pe = 0.0
    for k in categories:
        pi_k = sum(u.count(k) / len(u) for u in rated) / len(rated)
        pe += pi_k * (1.0 - pi_k)
    pe /= (q - 1)
    if pe >= 1.0:
        return None
    return (pa - pe) / (1.0 - pe)


def prevalence(units):
    """Share of usable codes that are "present"."""
    flat = [c for u in units for c in u]
    if not flat:
        return None
    return flat.count(PRESENT) / len(flat)


def prevalence_index(units):
    """|p(present) - p(absent)| over present and absent codes. 0 balanced, 1 one-sided."""
    flat = [c for u in units for c in u if c in (PRESENT, ABSENT)]
    if not flat:
        return None
    return abs(flat.count(PRESENT) - flat.count(ABSENT)) / len(flat)


def bias_index(rater_units):
    """Mean over rater pairs of |b - c| / n.

    `rater_units` is a list of dicts {rater: code}, one per unit. For a pair
    of raters, b counts units the first coded present and the second absent,
    c the reverse, n the units both coded present or absent.
    """
    raters = sorted({r for u in rater_units for r in u})
    values = []
    for r1, r2 in combinations(raters, 2):
        b = c = n = 0
        for u in rater_units:
            x, y = u.get(r1), u.get(r2)
            if x in (PRESENT, ABSENT) and y in (PRESENT, ABSENT):
                n += 1
                if x == PRESENT and y == ABSENT:
                    b += 1
                elif x == ABSENT and y == PRESENT:
                    c += 1
        if n:
            values.append(abs(b - c) / n)
    if not values:
        return None
    return sum(values) / len(values)


def band(alpha):
    """Protocol section 8 classification of an alpha value."""
    if alpha is None:
        return "not_computable"
    if alpha >= ALPHA_ACCEPTABLE:
        return "acceptable"
    if alpha >= ALPHA_TENTATIVE:
        return "tentative"
    return "below_threshold"


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def indicator_parents(indicator_id):
    """Return (tactic_id, matrix) for a People or Facilities indicator ID."""
    m = INDICATOR_RE.match(indicator_id)
    if not m:
        raise InputError("indicator_id outside study scope or malformed: %r" % (indicator_id,))
    if m.group(1) == "F":
        return "TF" + m.group(2), "facility"
    return "TM" + m.group(2), "person"


def load_cases(directory):
    """Return {(case_id, indicator_id): {rater: code}} from every *.json file under directory."""
    table = defaultdict(dict)
    files = []
    for root, _dirs, names in os.walk(directory):
        for name in sorted(names):
            if name.endswith(".json"):
                files.append(os.path.join(root, name))
    for path in sorted(files):
        try:
            with open(path, encoding="utf-8") as fh:
                doc = json.load(fh)
        except (OSError, ValueError) as exc:
            raise InputError("%s: cannot read as JSON: %s" % (path, exc))
        if not isinstance(doc, dict):
            raise InputError("%s: top level must be an object" % path)
        for key in ("case_id", "rater_pseudonym", "codes"):
            if key not in doc:
                raise InputError("%s: missing required key %r" % (path, key))
        case_id, rater = doc["case_id"], doc["rater_pseudonym"]
        if not isinstance(case_id, str) or not isinstance(rater, str) or not isinstance(doc["codes"], list):
            raise InputError("%s: case_id and rater_pseudonym must be strings, codes an array" % path)
        seen = set()
        for entry in doc["codes"]:
            if not isinstance(entry, dict) or "indicator_id" not in entry or "code" not in entry:
                raise InputError("%s: each code needs indicator_id and code" % path)
            ind, code = entry["indicator_id"], entry["code"]
            if not isinstance(ind, str):
                raise InputError("%s: indicator_id must be a string" % path)
            indicator_parents(ind)
            if code not in CODE_VALUES:
                raise InputError("%s: %s has unknown code %r" % (path, ind, code))
            if ind in seen:
                raise InputError("%s: %s coded twice in one file" % (path, ind))
            seen.add(ind)
            unit = table[(case_id, ind)]
            if rater in unit:
                raise InputError("%s: rater %s already coded %s for case %s in another file"
                                 % (path, rater, ind, case_id))
            unit[rater] = code
    return dict(table)


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def _usable(unit, cd_as_category):
    if cd_as_category:
        return dict(unit)
    return {r: c for r, c in unit.items() if c != CANNOT}


def _stats(raw_units, cd_as_category):
    """raw_units: list of (case_id, {rater: code}) with every code as recorded."""
    categories = CODE_VALUES if cd_as_category else (PRESENT, ABSENT)
    usable = [_usable(u, cd_as_category) for _case, u in raw_units]
    labels = [list(u.values()) for u in usable]
    all_codes = [c for _case, u in raw_units for c in u.values()]
    alpha = krippendorff_alpha_nominal(labels)
    return {
        "n_units": len(raw_units),
        "n_units_pairable": sum(1 for u in labels if len(u) >= 2),
        "n_codes": len(all_codes),
        "n_raters": len({r for _case, u in raw_units for r in u}),
        "prevalence_present": prevalence(labels),
        "percent_agreement": percent_agreement(labels),
        "krippendorff_alpha": alpha,
        "gwet_ac1": gwet_ac1(labels, categories),
        "prevalence_index": prevalence_index(labels),
        "bias_index": bias_index(usable),
        "cannot_determine_rate": (all_codes.count(CANNOT) / len(all_codes)) if all_codes else None,
        "band": band(alpha),
    }


def _bootstrap_alpha(raw_units, cd_as_category, replicates, rng):
    """Percentile 95 percent interval for alpha, resampling cases with replacement."""
    by_case = defaultdict(list)
    for case_id, unit in raw_units:
        by_case[case_id].append(list(_usable(unit, cd_as_category).values()))
    cases = sorted(by_case)
    if len(cases) < 2:
        return None
    values = []
    for _ in range(replicates):
        sample = []
        for _i in range(len(cases)):
            sample.extend(by_case[rng.choice(cases)])
        a = krippendorff_alpha_nominal(sample)
        if a is not None:
            values.append(a)
    if len(values) < max(10, replicates // 2):
        return None
    values.sort()
    lo = values[int(0.025 * (len(values) - 1))]
    hi = values[int(round(0.975 * (len(values) - 1)))]
    return [lo, hi]


def analyse(table, cd_as_category=False, bootstrap=0, seed=0):
    """Return a list of result rows for every indicator, tactic, and matrix."""
    groups = {"indicator": defaultdict(list), "tactic": defaultdict(list), "matrix": defaultdict(list)}
    for (case_id, ind), unit in sorted(table.items()):
        tactic, matrix = indicator_parents(ind)
        groups["indicator"][ind].append((case_id, unit))
        groups["tactic"][tactic].append((case_id, unit))
        groups["matrix"][matrix].append((case_id, unit))
    rng = random.Random(seed)
    rows = []
    for level in ("matrix", "tactic", "indicator"):
        for key in sorted(groups[level]):
            row = {"level": level, "id": key}
            row.update(_stats(groups[level][key], cd_as_category))
            if bootstrap and level != "indicator":
                row["alpha_ci95"] = _bootstrap_alpha(groups[level][key], cd_as_category, bootstrap, rng)
            rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def _fmt(value):
    if value is None:
        return "   n/a"
    return "%6.3f" % value


def format_table(rows):
    header = ("%-9s %-13s %6s %6s %6s %6s %6s %6s %6s %6s %6s  %s"
              % ("level", "id", "units", "pairs", "prev", "agree", "alpha", "AC1", "PI", "BI", "CD", "band"))
    lines = [header, "-" * len(header)]
    for r in rows:
        line = ("%-9s %-13s %6d %6d %s %s %s %s %s %s %s  %s"
                % (r["level"], r["id"], r["n_units"], r["n_units_pairable"],
                   _fmt(r["prevalence_present"]), _fmt(r["percent_agreement"]),
                   _fmt(r["krippendorff_alpha"]), _fmt(r["gwet_ac1"]),
                   _fmt(r["prevalence_index"]), _fmt(r["bias_index"]),
                   _fmt(r["cannot_determine_rate"]), r["band"]))
        if r.get("alpha_ci95"):
            line += "  alpha 95%% CI [%.3f, %.3f]" % tuple(r["alpha_ci95"])
        lines.append(line)
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("directory", help="directory holding coded case JSON files")
    parser.add_argument("--cd-as-category", action="store_true",
                        help="treat cannot_determine as a third category instead of missing")
    parser.add_argument("--level", choices=("all", "matrix", "tactic", "indicator"), default="all")
    parser.add_argument("--json", metavar="PATH", help="also write results as JSON (use - for stdout)")
    parser.add_argument("--bootstrap", type=int, default=0, metavar="N",
                        help="case-level bootstrap replicates for tactic and matrix alpha intervals")
    parser.add_argument("--seed", type=int, default=0, help="random seed for the bootstrap")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.directory):
        print("error: not a directory: %s" % args.directory, file=sys.stderr)
        return 2
    try:
        table = load_cases(args.directory)
    except InputError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    if not table:
        print("No coded case files found in %s. Nothing to analyse." % args.directory)
        return 0

    rows = analyse(table, args.cd_as_category, args.bootstrap, args.seed)
    if args.level != "all":
        rows = [r for r in rows if r["level"] == args.level]
    result = {
        "cannot_determine_handling": "category" if args.cd_as_category else "missing",
        "thresholds": {"alpha_tentative": ALPHA_TENTATIVE, "alpha_acceptable": ALPHA_ACCEPTABLE},
        "bootstrap_replicates": args.bootstrap,
        "seed": args.seed,
        "rows": rows,
    }
    if args.json == "-":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(format_table(rows))
        print()
        print("prev = share of usable codes that are present; agree = percent agreement; "
              "PI = prevalence index; BI = bias index; CD = cannot_determine rate.")
        if args.json:
            with open(args.json, "w", encoding="utf-8") as fh:
                json.dump(result, fh, indent=2, sort_keys=True)
                fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
