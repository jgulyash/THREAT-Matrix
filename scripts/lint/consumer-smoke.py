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

if failures:
    print("✗ consumer-smoke FAILED:")
    for f in failures:
        print(f"  - {f}")
    print("--- consumer output (tail) ---")
    print(combined[-1000:])
    sys.exit(1)

print("✓ consumer-smoke PASSED — reference consumer loads, schema-validates clean, and reads the framework.")
