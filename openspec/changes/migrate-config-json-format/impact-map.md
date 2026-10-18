# Impact Map: Migrate Config File Format to JSON

## Diagram

    config (BREAKING: key=value -> JSON)
      |
      |-- read by --> notification   (email recipient, Slack webhook URL)
      |-- read by --> audit-log      (log_level)
      |
      `-- NOT read by --> user-profile
            (user-profile has its own separate storage for default name;
             config's Purpose section mentions "default name" but no
             requirement in either spec actually wires them together —
             flagged here as a pre-existing spec inconsistency, not
             something this change introduces or needs to fix)

## Upstream

- None. `config` has no dependencies of its own — it's the root of this
  change.

## Downstream (must change when config's format changes)

| Capability   | What it reads from config      | Action required                                   |
|--------------|---------------------------------|----------------------------------------------------|
| notification | email recipient, Slack webhook  | Update parsing from `key=value` lookup to JSON path |
| audit-log    | log_level                        | Update parsing from `key=value` lookup to JSON path |

## Not impacted

- `greeting` — does not read config at all.
- `user-profile` — has its own storage, does not read config (see note above).

## Risk if downstream capabilities are not updated in lockstep

If `notification` or `audit-log` are not updated to read the new JSON format in the
same release as `config`, they will silently read nothing (fail to find expected keys)
rather than erroring clearly — a secondary risk worth calling out in the migration
notes.