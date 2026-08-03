#!/usr/bin/env python3
"""Smoke test for the reference consumer (examples/python_consumer.py).

The consumer is the one artifact that proves the JSON contract works end-to-end:
load framework.json, schema-validate it, and read tactics across every matrix.
The 2026-07-18 Principal Architecture Review found it broken (an AttributeError);
this guard runs it against the shipped framework so that regression cannot recur
silently. Asserts a clean schema validation via the consumer's own output, since
the consumer prints validation errors without setting a non-zero exit code.

Usage: python3 scripts/lint/consumer-smoke.py    (requires: pip install jsonschema)
"""
import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
CONSUMER = REPO / "examples" / "python_consumer.py"

r = subprocess.run(
    [sys.executable, str(CONSUMER)],
    capture_output=True,
    text=True,
)
out = r.stdout
combined = r.stdout + r.stderr

failures = []
if r.returncode != 0:
    failures.append(f"consumer exited {r.returncode} (expected 0)")
if "Validation: clean." not in out:
    failures.append("schema validation was not clean (expected 'Validation: clean.')")
if "Sample (one tactic per phase)" not in out:
    failures.append("consumer did not print the per-phase sample")
if "Tactics" not in out:
    failures.append("consumer did not print the framework summary")
if "Instance-conditioning join" not in out:
    failures.append("consumer did not exercise the instance-conditioning join")
if "escalate-only max" not in out:
    failures.append("consumer join did not report the escalate-only computation")

# V1.6: the instance-conditioning template and worked cases must validate
# against $defs.conditioned_assessment and honor the escalate-only invariant
# (conditioned_priority never below type_severity_band). The held-vs-raised
# distinction is derived by comparison, not stored, so there is no separate
# effect field to keep consistent. These are the affordance the contract
# ships in place of a case-data UI; a broken template is a broken contract
# advertisement.
try:
    import jsonschema

    schema = json.loads((REPO / "docs" / "data" / "framework.schema.json").read_text())
    ca_validator = jsonschema.Draft202012Validator(
        {"$ref": "#/$defs/conditioned_assessment", "$defs": schema["$defs"]}
    )
    rank = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    records = [REPO / "examples" / "instance-record-template.json"]
    records += sorted((REPO / "examples" / "worked-cases").glob("case-*.json"))
    for rec_path in records:
        rec = json.loads(rec_path.read_text())
        errs = list(ca_validator.iter_errors(rec))
        if errs:
            failures.append(f"{rec_path.name}: schema-invalid ({errs[0].message[:60]})")
            continue
        if rank[rec["conditioned_priority"]] < rank[rec["type_severity_band"]]:
            failures.append(f"{rec_path.name}: conditioned_priority below type band (escalate-only)")
        # held-vs-raised is derived, not stored: raised iff priority > band.
        _ = rank[rec["conditioned_priority"]] > rank[rec["type_severity_band"]]
except ImportError:
    pass  # jsonschema optional; the framework validator run already covers schema

if failures:
    print("✗ consumer-smoke FAILED:")
    for f in failures:
        print(f"  - {f}")
    print("--- consumer output (tail) ---")
    print(combined[-1000:])
    sys.exit(1)

print("✓ consumer-smoke PASSED — reference consumer loads, schema-validates clean, reads the framework, and the instance-conditioning template + worked cases validate escalate-only.")
