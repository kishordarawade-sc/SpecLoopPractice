# Feature Specification: Greeting Log

**Spec Version**: 1.0.0

**Feature Branch**: `003-greet-log`

**Created**: 2026-10-18

**Input**: User description: "Log every greeting to a file with a timestamp"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Log each greeting (Priority: P1)

Every time a greeting is generated, an entry is written to a log file so there's a record of past greetings.

**Why this priority**: Core purpose of the feature.

**Independent Test**: Generate a greeting and check that a new line appears in the log file.

**Acceptance Scenarios**:

1. **Given** the tool is installed, **When** a greeting is generated, **Then** a log entry is written containing the greeting and a timestamp.

### Edge Cases

- What happens if the log file doesn't exist yet? It should be created automatically.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST write a log entry each time a greeting is generated.
- **FR-002**: Each log entry SHOULD include a timestamp.
- **FR-003**: The system MUST create the log file if it does not already exist.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Greetings are logged reliably.

## Assumptions

- The log file lives somewhere reasonable on disk.