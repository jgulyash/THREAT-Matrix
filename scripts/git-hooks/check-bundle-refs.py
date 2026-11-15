#!/usr/bin/env python3
"""Check that docs/index.html and docs/assets agree.

The viewer build writes hashed bundle files into docs/assets and bakes
their names into docs/index.html. This check fails when:

  - docs/index.html references an asset file that does not exist
    (the published page would load a 404 and render blank), or
  - docs/assets holds a file that nothing references (a stale bundle or a
    stray file that would be published).

A file in docs/assets counts as referenced when its name appears in
docs/index.html, or in the text of another referenced asset (so a bundle
that loads further chunks is handled).

It reads files only; it does not build anything. Used by the pre-commit
hook (against the staged tree) and by the Bundle Freshness workflow.

Exit codes: 0 consistent; 1 inconsistent; 2 a required path is missing.

Usage: python3 scripts/git-hooks/check-bundle-refs.py [REPO_ROOT]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

NAME = "check-bundle-refs"
ASSET_REF = re.compile(r"""(?:src|href)\s*=\s*["'](?:\./|/)?assets/([^"'?#]+)""")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    index = root / "docs" / "index.html"
    assets = root / "docs" / "assets"
    try:
        html = index.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: {NAME}: cannot read {index} ({exc.__class__.__name__})", file=sys.stderr)
        return 2
    if not assets.is_dir():
        print(f"error: {NAME}: {assets} is not a directory", file=sys.stderr)
        return 2

    present = {p.relative_to(assets).as_posix() for p in assets.rglob("*") if p.is_file()}
    direct = set(ASSET_REF.findall(html))
    problems = []
    if not direct:
        problems.append("docs/index.html references no file under assets/")
    for name in sorted(direct - present):
        problems.append(f"docs/index.html references assets/{name}, which does not exist in docs/assets")

    # Follow references from referenced assets to other asset files.
    referenced = direct & present
    queue = sorted(referenced)
    while queue:
        current = queue.pop()
        try:
            text = (assets / current).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for other in present - referenced:
            if Path(other).name in text:
                referenced.add(other)
                queue.append(other)
    for name in sorted(present - referenced):
        problems.append(f"docs/assets/{name} is not referenced by docs/index.html or by any referenced asset")

    if problems:
        print(f"FAILED {NAME}: {len(problems)} problem(s):", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1
    print(f"PASSED {NAME}: docs/index.html and docs/assets agree ({len(present)} asset file(s), all referenced).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
