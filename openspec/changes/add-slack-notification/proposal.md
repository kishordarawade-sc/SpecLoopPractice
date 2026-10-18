# Proposal: Add Slack Notification Channel

## Why

Users currently only get the greeting via stdout or email. Several users have asked for a
Slack channel option so greetings can be posted into a team channel during demos.

## What Changes

- `notification` capability gains a new Slack channel, configurable with a webhook URL.
- Existing stdout and email channels are unaffected — this is purely additive.

## Impact

- Affects: `notification` capability only.
- No existing requirement is modified or removed.
- No migration needed for existing users; Slack is opt-in via config.