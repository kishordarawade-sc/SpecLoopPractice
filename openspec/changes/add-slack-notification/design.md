# Design: Add Slack Notification Channel

## Approach

Add a `send_slack(webhook_url: str, message: str) -> bool` function to `greet.py`. For this
exercise it does not make a real network call — it simulates posting by returning `True` when
given a non-empty `webhook_url`, and `False` when `webhook_url` is empty/`None` (standing in for
"channel not configured").

## Integration point

`build_greeting()` stays unchanged. A new function, `notify(greeting: str, webhook_url: str | None) -> bool`,
wraps the decision of whether to attempt a Slack post, matching the two scenarios in the delta spec:
- Slack channel configured -> attempt post, return the post result.
- Slack channel not configured -> skip posting, return `False`, no error raised.

## Out of scope

Real HTTP calls, retries, error handling for network failures — a real implementation would use
e.g. `requests.post`, but that's beyond what this exercise needs to practice the Feature Loop.