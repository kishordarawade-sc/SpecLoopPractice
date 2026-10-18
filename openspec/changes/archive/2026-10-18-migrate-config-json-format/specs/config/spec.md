## REMOVED Requirements

### Requirement: Flat key-value file format
Removed in favor of structured JSON storage — see "Structured JSON file format" below.

## ADDED Requirements

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