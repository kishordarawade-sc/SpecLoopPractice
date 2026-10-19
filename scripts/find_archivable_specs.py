#!/usr/bin/env python3
"""Find specs/<slug>/spec.md files marked Status: Archived that still live
outside specs/_archive/ (i.e. have not actually been moved yet).

This is the "what would the auto-archive CI job move" check. It only
reports candidates - it never moves anything. The auto-archive workflow
(.github/workflows/auto-archive.yml.example) is kept inert on purpose;
this script is the part of it safe to actually run and commit for real.
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = REPO_ROOT / "specs"

STATUS_PATTERN = re.compile(r'\*\*Status\*\*:\s*(\S+)')


def find_archivable() -> list[str]:
    candidates = []
    for spec_file in sorted(SPECS_DIR.glob("*/spec.md")):
        slug = spec_file.parent.name
        text = spec_file.read_text(encoding="utf-8")
        match = STATUS_PATTERN.search(text)
        if match and match.group(1) == "Archived":
            candidates.append(slug)
    return candidates


def main() -> int:
    candidates = find_archivable()
    print("Auto-Archive Candidate Report")
    print("==============================")
    if not candidates:
        print("No live specs are marked Status: Archived. Nothing to move.")
        return 0
    for slug in candidates:
        print(f"  specs/{slug} -> specs/_archive/{slug}  (Status: Archived)")
    return 0


if __name__ == "__main__":
    sys.exit(main())