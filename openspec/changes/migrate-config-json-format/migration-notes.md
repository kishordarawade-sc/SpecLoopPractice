# Migration Notes: Config File Format Change (key=value -> JSON)

**Audience:** anyone deploying or operating this system with an existing config file.
**Breaking change — action required before upgrading.**

## What's changing

The config file's internal format is changing from flat `key=value` lines to a single
JSON object. This is **not** backward compatible: an old-format file will fail to parse
once this change ships (see `specs/config/spec.md`'s "Old-format file present" scenario).

## Why

The old format can't express structured settings (e.g. a Slack webhook URL nested under
a channel's own settings) without encoding multiple values into one string. JSON removes
that limitation.

## Timeline

| Stage                     | What happens                                             |
|----------------------------|-----------------------------------------------------------|
| Now (proposal)              | Change proposed, not yet merged to main                  |
| Deprecation window (2 weeks after merge) | Old-format files still present will fail at startup with a clear error pointing to this doc — no silent fallback |
| Removal (end of window)     | Old-format support is not reintroduced; JSON is the only supported format going forward |

## Migration steps for an existing deployment

1. Locate your existing config file (fixed, well-known path — see "Config file location"
   requirement, unchanged by this migration).
2. Convert each `key=value` line to a JSON field:
   - `log_level=minimal` -> `{"log_level": "minimal"}`
   - Channel-related keys become nested objects under `"notification"` (see design.md
     for the exact shape).
3. Validate the new file is valid JSON before restarting the system.
4. Restart. If the file is still in the old format, the system will refuse to start
   with a config parse error rather than silently using defaults.

## Who is affected

- Operators with an existing config file in the old format: **must migrate manually**
  (no automated migration script is provided — see design.md "Out of scope").
- New deployments with no existing config file: unaffected, start directly with JSON.