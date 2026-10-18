# Design: Migrate Config File Format to JSON

## Old format (flat key=value)

    log_level=minimal
    email_recipient=team@example.com

## New format (JSON)

    {
      "log_level": "minimal",
      "notification": {
        "email": { "recipient": "team@example.com" },
        "slack": { "webhook_url": "https://hooks.slack.test/abc123" }
      }
    }

Structured settings (like notification channels) become nested objects instead of
being encoded into a single string value.

## Scope of this change

This change is spec-only — no code migration or parser implementation is done as part
of this exercise. The purpose here is to practice writing a BREAKING delta spec, an
impact map, migration notes, and the semver decision, not to re-run the TDD loop a
second time (already practiced for real with the Slack addition).

## Out of scope

- An actual JSON parser/writer in `greet.py`.
- A migration script to convert existing `key=value` files to JSON.
- Backward-compatible dual-format reading.