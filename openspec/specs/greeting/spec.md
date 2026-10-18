# Capability: Greeting

## Purpose

Prints a friendly greeting to a named or anonymous user.

## Requirements

### Requirement: Greet a named user
The system SHALL print a personalized greeting when a name is provided.

#### Scenario: Name provided
- WHEN the user runs `greet Alice`
- THEN the output is `Hello, Alice!`

#### Scenario: Multi-word name provided
- WHEN the user runs `greet "Alice Smith"`
- THEN the output is `Hello, Alice Smith!`

### Requirement: Greet with no name
The system SHALL print a default greeting when no name is provided, or the name is blank/whitespace-only.

#### Scenario: No argument given
- WHEN the user runs `greet` with no argument
- THEN the output is `Hello, World!`

#### Scenario: Whitespace-only name given
- WHEN the user runs `greet "   "`
- THEN the output is `Hello, World!`

### Requirement: Trim whitespace
The system SHALL trim leading and trailing whitespace from the provided name before using it in the greeting.

#### Scenario: Name has surrounding whitespace
- WHEN the user runs `greet "  Alice  "`
- THEN the output is `Hello, Alice!`

### Requirement: Shout mode
The system SHALL support an optional `--shout` flag; when present, the greeting is printed in all uppercase.

#### Scenario: Shout flag present
- WHEN the user runs `greet Alice --shout`
- THEN the output is `HELLO, ALICE!`