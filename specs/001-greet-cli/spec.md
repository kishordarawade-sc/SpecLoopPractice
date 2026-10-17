# Feature Specification: Greet CLI

**Spec Version**: 1.1.0

**Feature Branch**: `001-greet-cli`

**Created**: 2026-10-16

**Status**: Draft

**Input**: User description: "Add a CLI command that greets a user by name"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Greet a named user (Priority: P1)

A user runs the tool with their name and sees a personalized greeting printed back to them.

**Why this priority**: This is the entire point of the feature; without it there is nothing to
demo.

**Independent Test**: Run the command with a name argument and confirm the greeting line contains
that name.

**Acceptance Scenarios**:

1. **Given** the tool is installed, **When** the user runs `greet Alice`, **Then** the output is
   `Hello, Alice!`.
2. **Given** the tool is installed, **When** the user runs `greet "Alice Smith"`, **Then** the
   output is `Hello, Alice Smith!`.
3. **Given** the tool is installed, **When** the user runs `greet Alice --shout`, **Then** the output is `HELLO, ALICE!`

---

### User Story 2 - Greet with no name provided (Priority: P2)

A user runs the tool without any argument and still gets a friendly, generic greeting instead of
an error.

**Why this priority**: Makes the tool usable as a smoke-test / demo command with zero setup, but
the feature is still useful without this (P1 alone is a viable MVP).

**Independent Test**: Run the command with no arguments and confirm a default greeting is printed
instead of an error.

**Acceptance Scenarios**:

1. **Given** the tool is installed, **When** the user runs `greet` with no argument, **Then** the
   output is `Hello, World!`.

---

### Edge Cases

- What happens when the name argument is only whitespace? System treats it the same as no name
  provided (falls back to the default greeting).
- What happens when the name contains leading/trailing whitespace? System trims it before greeting
  (`greet "  Alice  "` → `Hello, Alice!`).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a `greet` command that accepts a single optional name argument.
- **FR-002**: When a non-blank name is provided, system MUST print `Hello, <name>!` to stdout.
- **FR-003**: When no name is provided, or the name is blank/whitespace-only, system MUST print
  `Hello, World!` to stdout.
- **FR-004**: System MUST trim leading and trailing whitespace from the provided name before
  using it in the greeting.
- **FR-005**: System MUST exit with status code 0 after printing the greeting.
- **FR-006**: System MUST support an optional `--shout` flag; when present, the greeting is printed in all uppercase.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user supplying their name receives a greeting containing that exact name, with no
  extra formatting characters, 100% of the time.
- **SC-002**: A user running the command with no arguments receives the default greeting instead
  of an error message or crash, 100% of the time.
- **SC-003**: A new user can correctly produce a personalized greeting on their first attempt
  without reading external documentation (the command's own `--help`/usage text is sufficient).

## Assumptions

- This is a single-shot CLI invocation; no persistence, configuration file, or session state is
  needed.
- Output is plain, unformatted text to stdout; no internationalization/localization in this
  version.
- A multi-word name is supplied as one shell argument (the user is responsible for quoting it).
- Packaging/installation/distribution mechanics are out of scope for the spec and are decided in
  the implementation plan.

## Change Log

- **1.1.0** (2026-10-17): Added FR-006 (`--shout` flag). Reason: demo request for a louder/emphasized
  greeting mode for presentations; purely additive, no existing behavior changes.
- **1.0.0** (2026-10-16): Initial spec — named greeting (US1) and default greeting (US2).
