# Proposal: Migrate Config File Format to JSON

## Why

The flat `key=value` format can only express single-level string settings. Downstream
capabilities increasingly need structured values (e.g. notification channel settings
that have both a type and credentials) and are already forced into ad-hoc workarounds
like encoding sub-fields into a single string. A structured JSON format removes that
workaround.

## What Changes

- `config` capability's storage format changes from flat `key=value` lines to a single
  JSON object.
- **This is breaking**: every existing config file written in the old format will fail
  to parse under the new format. There is no backward-compatible read path in this
  change.
- The "Config file location" and "Missing settings use defaults" requirements are
  unaffected — only the file's internal format changes.

  ## Impact

- Affects: `config` capability directly.
- Downstream dependents that read config settings must update how they parse it:
  `notification` (channel settings), `audit-log` (log level).
- Existing config files in the old format must be migrated (see migration-notes.md)
  before upgrading.