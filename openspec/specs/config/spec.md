# Capability: Config
**Spec Version**: 2.0.0 (MAJOR bump — flat key=value format removed, replaced with structured JSON; see openspec/semver-decisions.md)

## Purpose

Stores settings that other capabilities read to control their behavior (default name, notification channels, log level).

## Requirements

### Requirement: Structured JSON file format
The system SHALL store configuration as a single JSON object in the config file.

#### Scenario: Reading a setting
- WHEN the config file contains `{"log_level": "minimal"}`
- THEN the system reads `log_level` as `minimal`

#### Scenario: Reading a nested setting
- WHEN the config file contains `{"notification": {"slack": {"webhook_url": "https://hooks.slack.test/abc123"}}}`
- THEN the system reads the Slack webhook URL from the nested `notification.slack.webhook_url` path

#### Scenario: Old-format file present
- WHEN the config file is still in the old flat `key=value` format
- THEN the system fails to parse it and raises a config error (no automatic fallback to the old format)

### Requirement: Config file location
The system SHALL read configuration from a single file at a fixed, well-known path.

#### Scenario: Config file present
- WHEN a config file exists at the well-known path
- THEN its settings are loaded before any capability reads them

### Requirement: Missing settings use defaults
The system SHALL fall back to a built-in default value for any setting not present in the config file.

#### Scenario: Setting absent from file
- WHEN the config file does not contain a `log_level` line
- THEN the system uses the built-in default log level