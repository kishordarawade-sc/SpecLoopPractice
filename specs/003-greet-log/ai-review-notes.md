# Critical Review: AI-Drafted Spec (003-greet-log)

**Prompt used**: "Draft a Spec-Kit feature specification, matching the existing
spec.md format in this repo, for a feature that logs every greeting to a file
with a timestamp."

## What the AI got right

- Correct overall section structure (User Scenarios, Requirements, Success
  Criteria, Assumptions) matching 001-greet-cli and 002-farewell-cli.
- FR numbering format and Given/When/Then scenario format both correct.

## Gaps caught by the lint tool (structural)

- Missing **Status** field — present in both 001 and 002, silently dropped here.
- Missing ## Change Log section — same issue; without it there's no record of
  what changed between spec versions.

These two are mechanical: `spec_lint.py` catches them because they're a fixed
pattern match. That's the ceiling of what a lint tool can do — it checks
*shape*, not *content*.

## Gaps NOT caught by the lint tool (content quality — needs a human)

- **FR-002 uses "SHOULD" instead of "MUST"**: every other FR in this spec (and
  in 001/002) uses MUST. "SHOULD" makes the timestamp optional, which
  contradicts User Story 1's own acceptance scenario, which requires a
  timestamp unconditionally. Inconsistent requirement strength.
- **No timestamp format specified**: ISO 8601? Local time or UTC? Two
  implementers could build incompatible log formats from this spec as written.
- **SC-001 ("logged reliably") is not measurable**: contrast with 002's
  SC-001/SC-002, which name an exact, checkable outcome. "Reliably" can't be
  tested — it should state something like "100% of greetings produce exactly
  one log line, in <format>, within <N>ms."
- **No log entry format defined**: the spec never says what fields go in a log
  line (timestamp + greeting text? name? delimiter?). FR-001 says "a log
  entry is written" but two correct implementations could disagree on its
  shape.
- **Missing edge case — unwritable log location**: what happens if the log
  directory doesn't exist or isn't writable (permissions, full disk)? Current
  edge cases only cover "file doesn't exist yet," not "can't be created."
- **Missing edge case — concurrent writes**: if the command runs twice at once,
  are writes interleaved/corrupted, or is there an append guarantee?
- **Missing edge case — unbounded growth**: no mention of log rotation or size
  limits; the file grows forever with no stated policy.
- **Assumptions section is vague**: "somewhere reasonable on disk" should be a
  concrete, fixed path (the Config capability's "fixed, well-known path"
  convention would be a better model to follow here).

## Takeaway

The AI draft is structurally plausible but under-specified exactly where
ambiguity is expensive: data format, failure modes, and concurrency. A lint
pass is necessary but not sufficient — passing `spec_lint.py` only means the
*skeleton* is complete, not that the *requirements* are unambiguous. Both
checks are needed before a spec is implementation-ready.