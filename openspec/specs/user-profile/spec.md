# Capability: User Profile

## Purpose

Stores a default name so the user doesn't have to type it on every invocation.

## Requirements

### Requirement: Store a default name
The system SHALL allow a user to save a default name to their profile.

#### Scenario: Save a default name
- WHEN the user runs `profile set-name Alice`
- THEN subsequent greetings use "Alice" when no name argument is given

### Requirement: Fall back to profile when no name given
The system SHALL use the stored profile name instead of the generic default greeting, when a profile name exists and no name argument is provided.

#### Scenario: Profile name exists, no argument given
- WHEN a profile name "Alice" is stored AND the user runs `greet` with no argument
- THEN the output is `Hello, Alice!`

#### Scenario: No profile name stored, no argument given
- WHEN no profile name is stored AND the user runs `greet` with no argument
- THEN the output is `Hello, World!`