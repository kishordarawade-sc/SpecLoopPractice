SpecLoopPractice - Learning Log
================================

This file records what was practiced in this repo, how it was done, and the
issues hit along the way (and how they were fixed). It's a companion to
README.md, which just describes the project.

------------------------------------------------------------------------
1. WHAT WE LEARNED
------------------------------------------------------------------------

1.1 The Feature Loop (end-to-end cycle)
----------------------------------------
Every feature goes through, in order:

    specify -> plan -> tasks -> implement -> review -> merge -> archive

- specify  : /speckit-specify writes specs/<slug>/spec.md (user stories,
             functional requirements, success criteria).
- plan     : /speckit-plan writes plan.md, research.md, data-model.md,
             contracts/, quickstart.md - the technical approach, checked
             against the project constitution.
- tasks    : /speckit-tasks writes tasks.md - an ordered, numbered
             checklist (T001, T002, ...) grouped by user story, written
             TDD-style (failing test task, then implementation task).
- implement: work through tasks.md top to bottom. For each test/impl pair:
             write the test -> run it -> confirm it fails for the RIGHT
             reason (NotImplementedError, not a wrong assertion) -> write
             the implementation -> run it -> confirm it passes -> check
             the task off in tasks.md -> commit.
- review   : a human (or reviewer agent) reads the diff against the spec
             and constitution before it ships.
- merge    : fold the feature branch into main.
- archive  : once a feature is closed (merged, no further iteration
             planned), move its whole specs/<slug>/ folder into
             specs/_archive/<slug>/ and mark its Status as Archived.

It only really becomes a "loop" (not a one-way waterfall) because of two
loop-back paths:
  a) within one feature: if implement/review finds the spec or plan was
     wrong or incomplete, you go back and amend spec.md/plan.md rather
     than pushing forward with a known defect.
  b) across features: once one feature reaches archive, the whole
     sequence starts over for the next feature.

Example from this repo: the "greet-cli" feature went through this whole
loop once for v1.0.0 (named + default greeting), then again in miniature
for v1.1.0 (adding the --shout flag as a spec change).

1.2 TDD red/green loop (nested inside "implement")
----------------------------------------------------
This is a SMALLER loop, not the same thing as the Feature Loop:

    write failing test (red) -> implement until it passes (green)
    -> check off task -> next task

tasks.md decides the order of this loop in advance (during the "tasks"
stage) - you are not deciding what to test next on the fly, you're
executing a pre-written sequence.

Interesting real case we hit: writing the US2 tests (T008-T009) did NOT
produce a red phase - they passed immediately, because the US1
implementation (T007) had already been written generally enough to cover
blank/None names too. That's a legitimate TDD outcome: an earlier task's
implementation can subsume a later one. The tests still proved the
behavior was correct; there was just no code diff left for T010.

1.3 Versioning specs in Git (branch naming, tagging, semver)
---------------------------------------------------------------
- Branch naming: <NNN>-<slug>, e.g. 001-greet-cli. For a follow-up spec
  change on the same feature, a new scoped branch: 001-greet-cli-shout.
- Tagging: tags are scoped to the feature, not global, because a repo
  will have many features each with their own version:
      <feature-slug>-v<version>   e.g. greet-cli-v1.0.0, greet-cli-v1.1.0
  (the one global tag, v0.0.0, was reserved for the whole-project
  scaffold baseline, not a feature).
  Tags were created as ANNOTATED tags (git tag -a ... -m "...") so they
  carry a message/author/date as a real object, not just a pointer.
- Semver rule for a spec (mirrored in the constitution):
      MAJOR - a requirement changes in a way that breaks existing
              behavior/expectations
      MINOR - a new requirement/capability added, backward-compatible
      PATCH - wording/clarification only, no behavior change
  Example: adding FR-006 (--shout flag) was purely additive, so it was a
  MINOR bump, 1.0.0 -> 1.1.0.
- The same MAJOR/MINOR/PATCH policy was also applied to the project
  CONSTITUTION itself when we added the archiving rule to it (1.0.0 ->
  1.1.0, since adding a governance rule is "materially expanding
  guidance").

1.4 Spec change management
------------------------------
When a spec changes, three things must happen together, not just a code
edit:
  1. bump the Spec Version header,
  2. add the new requirement/scenario,
  3. record WHY in a Change Log section at the bottom of spec.md
     (version, date, what changed, why).
This Change Log convention isn't built into the Spec Kit template - we
added it ourselves as part of practicing change management.
The change itself goes on its own branch (see 1.3), gets reviewed, and
then merges/tags like any other feature work.

1.5 Delta spec (reading and applying a diff between versions)
------------------------------------------------------------------
Reading a delta spec is just a git diff between two anchored points
(tags, in our case):

    git diff <old-tag> <new-ref> -- specs/<slug>/spec.md

This shows exactly what changed between two released spec versions,
without needing to re-read the whole document.

Applying a delta spec elsewhere uses git's patch mechanism:

    git format-patch <old-tag>..<new-ref> -- specs/<slug>/spec.md -o .
    (creates a portable, shareable .patch file)

    git am <file>.patch
    (on a DIFFERENT checkout, applies the patch and recreates the
    commit with its original message/author)

We generated the patch file to see the mechanism, then deleted it since
it was only a demo artifact, not something to keep committed.

1.6 Spec archive (what / when / where)
------------------------------------------
Spec Kit's own constitution template NAMES "archive" as the last stage of
the Feature Loop but does not define it - that's left for the project to
decide. We defined and recorded this convention in the constitution:

  WHAT:  the entire specs/<slug>/ directory (spec, plan, tasks, research,
         contracts, quickstart - everything), moved as a whole.
  WHEN:  once a feature is merged to main AND no further iteration is
         planned (not after every single merge - we archived greet-cli
         only after BOTH v1.0.0 and v1.1.0 had shipped).
  WHERE: specs/_archive/<slug>/ - a sibling namespace, kept separate from
         the live specs/ folder so in-flight work stays easy to find.
  HOW:   git mv specs/<slug> specs/_archive/<slug>  (preserves file
         history through the rename), then set the spec's Status field
         to "Archived".
Note: archiving is about keeping the WORKING TREE organized, not about
data safety - git history and the version tags already preserve every
past version permanently regardless of whether the folder is archived.

1.7 Full Spec-Kit cycle for a small feature
------------------------------------------------
Done in practice for "greet-cli": specify -> plan -> tasks -> implement,
producing spec.md, plan.md, research.md, data-model.md,
contracts/cli-contract.md, quickstart.md, tasks.md, checklists/
requirements.md, and the working code (greet.py, tests/test_greet.py,
pytest.ini). The checklists/requirements.md "quality gate" was confirmed
to pass (all items checked) before /speckit-implement was allowed to
proceed - this is the mechanism that would have stopped implementation
if the spec had been incomplete.

------------------------------------------------------------------------
2. ISSUES WE FACED AND HOW WE OVERCAME THEM
------------------------------------------------------------------------

- specify init failed with "Agent Detection Error: claude not found"
  even though we were running inside Claude Code.
  Fix: re-ran with --ignore-agent-tools.

- Calling the speckit-* skills immediately after specify init failed
  with "Unknown skill" because the skill list had already been loaded
  for the session before the skills were scaffolded onto disk.
  Fix: manually read and followed the relevant SKILL.md files' documented
  procedure by hand until a fresh session picked up the new skills.

- pytest wasn't installed in the project's .venv, so `python -m pytest`
  failed with "No module named pytest".
  Fix: pip install pytest.

- A hand-written test (test_greet_without_name) asserted the WRONG
  expected value ("Hello, !") which contradicted the spec's documented
  behavior for blank names ("Hello, World!").
  Fix: caught this by comparing the test against spec.md's FR before
  implementing - fixed the test to match the spec (the spec was right).
  This was a concrete example of implementation-time review catching
  drift between a test and its spec.

- Several times, commit messages claimed to "mark tasks complete" or
  "implement X" but the actual file edit / git add never happened, so
  tasks.md checkboxes stayed unchecked and greet.py's real implementation
  sat uncommitted for a while.
  Fix: regularly cross-checked `git status --short` and
  `git log --oneline` against what was claimed to be done, and did the
  missed edit + commit as soon as the gap was found, before moving on.

- `git log` (and other commands) opened in a pager, which was confusing
  in the terminal (output looked "stuck" at a ":" or "(END)" prompt).
  Fix: press q to exit the pager, or avoid it entirely with
  `git --no-pager log ...` or piping to `| cat`.

- Several small typos crept into spec.md edits done by hand: a missing
  space after a comma, a doubled dash in "FR--006", a stray trailing
  period after "optional.".
  Fix: always ran `git diff` (or `git --no-pager diff`) BEFORE
  committing, and reviewed the exact diff line by line to catch wording
  issues before they became permanent commit history.

- `git mv specs/001-greet-cli specs/_archive/001-greet-cli` failed with
  "No such file or directory" because the destination parent folder
  (specs/_archive/) didn't exist yet - git mv doesn't create intermediate
  directories.
  Fix: create the destination directory first
  (New-Item -ItemType Directory -Force specs/_archive), then retry the
  git mv.

- Ran a bare `git merge` with no branch argument while sitting on the
  feature branch itself, which failed with "fatal: No remote for the
  current branch" (no upstream configured to merge from).
  Fix: `git merge <branch>` needs an explicit branch name when there's no
  tracked upstream, AND you must `git checkout` onto the TARGET branch
  (main) first - merge always applies into whatever branch is currently
  checked out.

------------------------------------------------------------------------
3. KEY TAKEAWAY
------------------------------------------------------------------------
Spec Kit's skills give you the specify/plan/tasks/implement mechanics,
but several important conventions (branch/tag naming, semver rules for
specs, change-log format, and the archive location/trigger) are NOT
prescribed by the tool - they were defined by us, written down in the
constitution, and then followed consistently. That act of writing the
rule down (in the constitution or in spec.md's Change Log) is what turned
an ad-hoc decision into a repeatable, reviewable process.
