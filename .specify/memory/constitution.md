# SpecLoopPractice Constitution

## Core Principles

### I. Small, Demo-able Features
Every feature taken through the loop MUST be scoped so it can be specified, planned, built, and
demonstrated within a single session. Large or multi-concern features MUST be split before
`/speckit-specify` is run. Rationale: this repo exists to practice the process, not to ship a
large system; oversized features hide process mistakes inside implementation noise.

### II. Versioned, Criteria-Bound Specs
Every spec MUST declare an explicit semantic version (`MAJOR.MINOR.PATCH`) and a concrete,
testable list of acceptance criteria before `/speckit-plan` is run. A spec without acceptance
criteria is incomplete and MUST NOT be planned against. Rationale: planning against vague or
unversioned specs makes later delta review and archiving meaningless.

### III. No Implementation Without an Approved Spec and Task List (NON-NEGOTIABLE)
Code MUST NOT be written until the feature has a committed spec (via `/speckit-specify`, and
`/speckit-clarify` if ambiguity remains) and a committed task list (via `/speckit-tasks`).
`/speckit-implement` MUST only execute tasks that trace back to a spec requirement. Rationale:
this is the core discipline the Feature Loop is meant to teach.

### IV. Simplicity Over Completeness
When a choice exists between a simple solution that demonstrates the concept and a complete one
that covers every edge case, choose the simple one and note the deferred edge cases in the spec.
Rationale: this is a learning exercise; completeness is practiced on real projects, not here.

## Spec Workflow Requirements

Every feature spec lives at `specs/<NNN>-<slug>/spec.md` and MUST carry a version header. Version
bumps follow: MAJOR for a change in scope/intent, MINOR for added/changed requirements, PATCH for
wording/clarification only. A spec's version history MUST be reconstructable from git history on
its branch (see branch/tag conventions in project docs), so that a delta between any two versions
can be read as a diff.

## Development Workflow

The Feature Loop for every feature is, in order: `/speckit-specify` -> (optional)
`/speckit-clarify` -> `/speckit-plan` -> (optional) `/speckit-checklist` -> `/speckit-tasks` ->
(optional) `/speckit-analyze` -> `/speckit-implement` -> review -> merge -> archive. Steps MUST
NOT be skipped backward (e.g. editing code during `/speckit-plan`), though later steps MAY send a
feature back to an earlier one (e.g. `/speckit-tasks` revealing the spec was ambiguous).

## Governance

This constitution supersedes ad-hoc process decisions for this repo. Amendments are made via
`/speckit-constitution` and follow the same semver policy as specs: MAJOR for removing/redefining
a principle, MINOR for adding a principle or materially expanding guidance, PATCH for wording
fixes. Every spec and plan produced by Spec Kit MUST be checked against this constitution before
being approved; unjustified deviation MUST be rejected back to the author.

**Version**: 1.0.0 | **Ratified**: 2026-10-16 | **Last Amended**: 2026-10-16
