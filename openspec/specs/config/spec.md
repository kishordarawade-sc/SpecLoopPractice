# Capability: Config

## Purpose

Stores settings that other capabilities read to control their behavior (default name, notification channels, log level).

## Requirements

### Requirement: Flat key-value file format
The system SHALL store configuration as a flat `key=value` text file, one setting per line.

#### Scenario: Reading a setting
- WHEN the config file contains the line `log_level=minimal`
- THEN the system reads `log_level` as `minimal`

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