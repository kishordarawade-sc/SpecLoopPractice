# End-to-End Beginner Workflow Log (Module 4)

This log traces one complete pass of the beginner Spec Kit workflow —
**specify → CI lint → plan → task → implement → test → archive** — using the
003-greet-log feature as the running example, with commit hashes and a real
CI run as evidence.

## 1. Specify

A spec was drafted for a greeting-log feature, simulating "ask Claude to draft
a spec from a one-line prompt":

- Prompt used: "Draft a Spec-Kit feature specification, matching the existing
  spec.md format in this repo, for a feature that logs every greeting to a
  file with a timestamp."
- `specs/003-greet-log/spec.md` created — commit `f644327`.

## 2. CI Lint (red)

Ran the structural lint against the fresh draft:
