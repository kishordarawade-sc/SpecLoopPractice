# End-to-End Beginner Workflow Log (Module 4)

This log traces one complete pass of the beginner Spec Kit workflow -
specify -> CI lint -> plan -> task -> implement -> test -> archive - using the
003-greet-log feature as the running example, with commit hashes and a real
CI run as evidence.

## 1. Specify

A spec was drafted for a greeting-log feature, simulating "ask Claude to draft
a spec from a one-line prompt":

- Prompt used: "Draft a Spec-Kit feature specification, matching the existing
  spec.md format in this repo, for a feature that logs every greeting to a
  file with a timestamp."
- specs/003-greet-log/spec.md created - commit f644327.

## 2. CI Lint (red)

Ran the structural lint against the fresh draft:

    python scripts/spec_lint.py

Result: [FAIL] specs\003-greet-log\spec.md - missing **Status**: field and
## Change Log section. This showed the lint tool doing its job: catching
structural gaps mechanically, before any human review.

## 3. Critical review (the "AI output needs review" step)

Wrote specs/003-greet-log/ai-review-notes.md - commit 6d137a8 - listing:
- The two lint-caught structural gaps.
- Gaps the lint tool cannot catch: an inconsistent "SHOULD" requirement, an
  unspecified timestamp format, an unmeasurable success criterion, and three
  missing edge cases (unwritable path, concurrent writes, unbounded log growth).

This is the "reviewing AI output critically" skill in practice - a passing
lint result only proves the shape is right, not that the content is
unambiguous.

## 4. Plan / revise

Applied the fixes identified in the review directly to the spec - commit
7c3458f - adding the missing fields, a concrete ISO 8601 UTC timestamp
format, a defined log line format, three new edge cases, and measurable
success criteria.

## 5. CI Lint (green)

Re-ran the lint:

    python scripts/spec_lint.py

Result: PASS - all spec files meet structural conventions. (all 3 specs,
including 002-farewell-cli and the archived 001-greet-cli.)

## 6. Task / Implement / Test

Picked the spec's own acceptance scenario - Given the tool is installed,
When a greeting is generated, Then a log entry is appended in the form
<ISO-8601 UTC timestamp> <greeting text> - and wired it to one real test:

- Wrote test_log_greeting_appends_timestamped_line first, with no
  implementation behind it. Ran pytest - red: ImportError: cannot
  import name 'log_greeting'.
- Implemented log_greeting() in greet.py. Ran pytest again - green:
  9/9 passed.
- Committed together as 93423c3.

## 7. Push + real CI run

- Pushed 003-greet-log, opened PR #1 against main.
- GitHub Actions ran spec-lint.yml for the first time on a real PR:
  spec-lint succeeded in 7s (checkout -> setup-python -> spec compliance
  check -> complete job, all green).
- Squash-merged into origin/main as 56e7d86.

## 8. Archive

001-greet-cli is already archived under specs/_archive/001-greet-cli/ from
an earlier module, and still passes lint today - confirming the lint rules
hold up across the full lifecycle, not just for brand-new specs. 002 and
003 remain active (not yet archived, since they haven't been superseded).

## Evidence summary

| Stage                 | Evidence                                             |
|------------------------|-------------------------------------------------------|
| Spec drafted           | commit f644327                                        |
| Lint red               | FAIL - missing Status / Change Log                    |
| Critical review        | commit 6d137a8 (ai-review-notes.md)                   |
| Spec fixed             | commit 7c3458f                                        |
| Lint green             | PASS - all spec files meet structural conventions.    |
| Test red               | ImportError: cannot import name 'log_greeting'        |
| Test green             | 9 passed in 0.06s                                     |
| Test + impl committed  | commit 93423c3                                        |
| PR + CI run            | PR #1, spec-lint succeeded in 7s                      |
| Merged                 | 56e7d86 on origin/main                                |
