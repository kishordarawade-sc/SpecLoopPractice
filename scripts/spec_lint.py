#!/usr/bin/env python3
"""Lint Spec Kit spec.md files for required structural conventions."""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_GLOB = "specs/**/spec.md"

RULES = [
    ("spec_version", re.compile(r"\*\*Spec Version\*\*:\s*\S+"),
     "missing '**Spec Version**:' header"),
    ("status", re.compile(r"\*\*Status\*\*:\s*\S+"),
     "missing '**Status**:' field"),
    ("functional_requirement", re.compile(r"\*\*FR-\d{3}\*\*:"),
     "no '**FR-00X**:' functional requirements found"),
    ("given_when_then", re.compile(r"\*\*Given\*\*.*?\*\*When\*\*.*?\*\*Then\*\*", re.DOTALL),
     "no Given/When/Then acceptance scenario found"),
    ("change_log", re.compile(r"^## Change Log", re.MULTILINE),
     "missing '## Change Log' section"),
]


def lint_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    violations = []
    for _name, pattern, message in RULES:
        if not pattern.search(text):
            violations.append(message)
    return violations


def main() -> int:
    spec_files = sorted(REPO_ROOT.glob(SPEC_GLOB))
    if not spec_files:
        print("No spec.md files found under specs/ - nothing to lint.")
        return 0

    had_failure = False
    print("Spec Compliance Report")
    print("=======================")
    for path in spec_files:
        rel = path.relative_to(REPO_ROOT)
        violations = lint_file(path)
        if violations:
            had_failure = True
            print(f"[FAIL] {rel}")
            for v in violations:
                print(f"    - {v}")
        else:
            print(f"[PASS] {rel}")

    print()
    if had_failure:
        print("Result: FAIL - one or more spec files are missing required sections.")
        return 1
    print("Result: PASS - all spec files meet structural conventions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())