# Capability: Audit Log

## Purpose

Records every greeting that was generated, for later review.

## Requirements

### Requirement: Log every greeting
The system SHALL record an entry each time a greeting is generated.

#### Scenario: Greeting generated
- WHEN a greeting is generated for any name
- THEN an audit entry is recorded containing the name and timestamp

### Requirement: Configurable log level
The system SHALL support a configurable log level controlling how much detail is recorded.

#### Scenario: Log level set to minimal
- WHEN the log level is set to "minimal" AND a greeting is generated
- THEN only the timestamp is recorded, without the name