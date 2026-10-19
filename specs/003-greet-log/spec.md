# Feature Specification: Greeting Log

**Spec Version**: 1.1.0

**Feature Branch**: `003-greet-log`

**Created**: 2026-10-18

**Status**: Specified

**Input**: User description: "Log every greeting to a file with a timestamp"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Log each greeting (Priority: P1)

Every time a greeting is generated, an entry is written to a log file so there's a record of past greetings.

**Why this priority**: Core purpose of the feature.

**Independent Test**: Generate a greeting and check that a new line appears in the log file with the expected format.

**Acceptance Scenarios**:

1. **Given** the tool is installed, **When** a greeting is generated, **Then** a log entry is appended in the form `<ISO-8601 UTC timestamp> <greeting text>`.

### Edge Cases

- What happens if the log file doesn't exist yet? It is created automatically at the fixed log path.
- What happens if the log directory is not writable (permissions, full disk)? The system raises a log error and does not silently drop the greeting output itself — the greeting still prints to stdout even if logging fails.
- What happens when two invocations run at the same time? Each writes a single complete line; entries are appended, never overwritten or interleaved mid-line.
- What happens when the log file grows very large? Out of scope for this version — no rotation or size limit is defined yet (tracked as a known limitation, not silently ignored).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST append one log entry each time a greeting is generated.
- **FR-002**: Each log entry MUST include a UTC timestamp in ISO 8601 format (e.g. `2026-10-18T18:22:05Z`).
- **FR-003**: System MUST create the log file at a fixed, well-known path if it does not already exist.
- **FR-004**: Each log entry MUST be written as a single line: `<timestamp> <greeting text>`.
- **FR-005**: If the log file cannot be written to, the system MUST still print the greeting to stdout (logging failure does not block the primary feature).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of generated greetings produce exactly one log line in the `<timestamp> <greeting text>` format.
- **SC-002**: A logging failure (e.g. unwritable path) never prevents the greeting from being printed to stdout, 100% of the time.

## Assumptions

- The log file lives at a single fixed path (not user-configurable in this version).
- Log rotation/size limits are out of scope for v1.1.0; may be addressed in a future version.

## Change Log

- **1.1.0** (2026-10-18): Revised after critical review (see ai-review-notes.md) — added Status field, Change Log, concrete timestamp format (ISO 8601 UTC), defined log line format, added failure/concurrency edge cases, made success criteria measurable.
- **1.0.0** (2026-10-18): Initial AI-drafted spec.