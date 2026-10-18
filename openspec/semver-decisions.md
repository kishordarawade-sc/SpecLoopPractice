# Semver Decision Log

OpenSpec has no built-in semver policy (same gap as Spec Kit's constitution before we
added one). This log records the bump decision for every change as it's folded into a
live capability spec, following the same MAJOR/MINOR/PATCH rule we defined for Spec Kit:

    MAJOR - a requirement changes in a way that breaks existing behavior/expectations
    MINOR - a new requirement/capability added, backward-compatible
    PATCH - wording/clarification only, no behavior change

## add-slack-notification -> notification capability

- **Bump:** MINOR (1.0.0 -> 1.1.0, already applied in notification/spec.md's version header)
- **Reasoning:** purely additive. The new "Slack channel" requirement doesn't touch the
  existing "Print to stdout" or "Email channel" requirements — nothing that previously
  worked stops working, and Slack is opt-in via config.

## migrate-config-json-format -> config capability

- **Bump:** MAJOR (1.0.0 -> 2.0.0, to be applied to config/spec.md's version header once
  this change is folded in)
- **Reasoning:** breaking. The "Flat key-value file format" requirement is REMOVED, not
  just extended — any existing config file in the old format stops working with no
  automatic fallback (see migrate-config-json-format/specs/config/spec.md's "Old-format
  file present" scenario). This fits the MAJOR definition exactly: a requirement changes
  in a way that breaks existing behavior/expectations.