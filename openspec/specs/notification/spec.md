# Capability: Notification

## Purpose

Delivers the generated greeting to a destination channel, in addition to printing it to stdout.

## Requirements

### Requirement: Print to stdout
The system SHALL always print the greeting to stdout, regardless of any other configured channel.

#### Scenario: Default behavior
- WHEN a greeting is generated
- THEN it is printed to stdout

### Requirement: Email channel
The system SHALL support sending the greeting via email when an email channel is configured.

#### Scenario: Email channel configured
- WHEN the email channel is configured with a recipient address AND a greeting is generated
- THEN the greeting is also sent to that email address