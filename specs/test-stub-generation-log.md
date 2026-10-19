# Claude-Generated Test Stubs (Module 5, Step 4)

This log documents using Claude to generate test stubs directly from a
spec's GIVEN-WHEN-THEN acceptance scenarios, at scale, across two specs.

## Prompting approach

For each spec, the following prompt pattern was used, pointing at one
acceptance scenario at a time (not the whole spec at once) so each
generated stub stays tightly scoped to a single scenario id:

    Given this GIVEN-WHEN-THEN acceptance scenario from
    specs/<feature>/spec.md, scenario id <id>:

    <paste the scenario line>

    Generate a pytest stub for it:
    - Use pytest.mark.skip, since the implementation does not exist yet.
    - Import the function under test inside the test body, not at module
      scope, so a missing function does not crash collection of the whole
      test file.
    - Add a `# spec: specs/<feature>/spec.md#<id>` comment directly above
      the test, matching this repo's traceability convention.
    - Name the test after the behavior, not the scenario id.

## Spec: 002-farewell-cli

### Scenario US1-S1
Given the tool is installed, When the user runs `farewell Alice`, Then the
output is `Goodbye, Alice!`.

### Generated stub
    # spec: specs/002-farewell-cli/spec.md#US1-S1
    @pytest.mark.skip(reason="stub: farewell() not implemented yet")
    def test_farewell_with_name():
        from greet import farewell
        assert farewell("Alice") == "Goodbye, Alice!"

### Scenario US2-S1
Given the tool is installed, When the user runs `farewell` with no
argument, Then the output is `Goodbye, World!`.

### Generated stub
    # spec: specs/002-farewell-cli/spec.md#US2-S1
    @pytest.mark.skip(reason="stub: farewell() not implemented yet")
    def test_farewell_without_name():
        from greet import farewell
        assert farewell(None) == "Goodbye, World!"

## Spec: 003-greet-log

### Scenario US1-S1
Already implemented in Module 4, before this stub-generation step existed:
test_log_greeting_appends_timestamped_line (commit 93423c3), linked via
`# spec: specs/003-greet-log/spec.md#US1-S1`. Not regenerated as a stub —
listed here only so this log is a complete record of every scenario across
both gated specs, implemented or not.

## Outcome

Both tests/test_greet.py (new skipped stubs) and specs/test-stub-generation-log.md
(this file) were added in the same step. Running the coverage gate
afterwards links all 3 scenarios across both specs, since the gate checks
for the `# spec:` comment, not whether the test passes or is skipped.
