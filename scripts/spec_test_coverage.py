#!/usr/bin/env python3
"""Check spec-to-test traceability coverage and gate on a minimum threshold."""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
THRESHOLD = 80.0

GATED_SPECS = [
    "specs/002-farewell-cli/spec.md",
    "specs/003-greet-log/spec.md",
]

SCENARIO_ANCHOR = re.compile(r'<a id="([^"]+)"></a>\s*\*\*Given\*\*')
LINK_COMMENT = re.compile(r'#\s*spec:\s*(\S+?\.md)#(\S+)')


def scenario_ids_for(spec_rel_path: str) -> list[str]:
    text = (REPO_ROOT / spec_rel_path).read_text(encoding="utf-8")
    return SCENARIO_ANCHOR.findall(text)


def linked_scenarios() -> set[tuple[str, str]]:
    linked = set()
    for test_file in (REPO_ROOT / "tests").glob("**/*.py"):
        text = test_file.read_text(encoding="utf-8")
        for spec_path, scenario_id in LINK_COMMENT.findall(text):
            linked.add((spec_path, scenario_id))
    return linked


def main() -> int:
    linked = linked_scenarios()
    total = 0
    covered = 0
    print("Spec-Test Coverage Report")
    print("==========================")
    for spec_rel_path in GATED_SPECS:
        for scenario_id in scenario_ids_for(spec_rel_path):
            total += 1
            is_linked = (spec_rel_path, scenario_id) in linked
            covered += 1 if is_linked else 0
            status = "LINKED" if is_linked else "MISSING"
            print(f"  [{status}] {spec_rel_path}#{scenario_id}")

    pct = (covered / total * 100) if total else 100.0
    print()
    print(f"Coverage: {covered}/{total} scenarios linked ({pct:.1f}%)")
    print(f"Threshold: {THRESHOLD:.1f}%")

    if pct < THRESHOLD:
        print("Result: FAIL - coverage below threshold.")
        return 1
    print("Result: PASS - coverage meets threshold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())