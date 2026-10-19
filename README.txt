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

------------------------------------------------------------------------
4. OPENSPEC MODULE (brownfield systems, delta specs, change management)
------------------------------------------------------------------------
Same repo, new tool: OpenSpec (github.com/Fission-AI/OpenSpec). Where Spec
Kit organizes work by FEATURE (specs/<NNN>-<slug>/, a one-time build),
OpenSpec organizes work by CAPABILITY (openspec/specs/<capability>/, an
ongoing area of system behavior) plus a separate queue of in-progress
CHANGES (openspec/changes/<change-id>/) that get folded into the live
specs once approved.

4.1 The brownfield baseline
-------------------------------
Scaffolded 5 capability specs under openspec/specs/ to act as an
"existing system" (the assignment's "given a 5-spec system"):
  - greeting      (ported from the archived greet-cli spec)
  - user-profile  (new: stores a default name)
  - notification  (new: delivers the greeting via stdout/email)
  - audit-log     (new: records every greeting generated)
  - config        (new: flat key=value settings file - deliberately
                    picked as the target for the later BREAKING change)
Each uses OpenSpec's requirement format: "### Requirement: <name>" with
SHALL-language, and "#### Scenario: <name>" with WHEN/THEN bullets -
different from Spec Kit's "**FR-00X**" + Given/When/Then style, same
underlying idea (a testable, traceable requirement).

4.2 Delta specs without rewriting the whole spec
----------------------------------------------------
For the additive change (Slack notification channel), the delta lived in
its OWN file - openspec/changes/add-slack-notification/specs/notification/
spec.md - containing ONLY an "## ADDED Requirements" section with the new
Slack requirement. The existing stdout/email requirements were never
touched or restated.
This is the core brownfield idea: in Spec Kit, "what changed" is a
question you answer AFTER the fact via `git diff <tag1> <tag2>`. In
OpenSpec, "what changed" is a document you write BEFORE the change is
even approved - the delta file IS the diff, not something reconstructed
from git history later.

4.3 Second Feature Loop iteration (real implementation, not just specs)
----------------------------------------------------------------------------
Ran a full mini Feature Loop for the Slack addition, matching OpenSpec's
file set to Spec Kit's equivalents:
  proposal.md -> (why/what, like Spec Kit's spec.md Input/Why section)
  design.md   -> (technical approach, like Spec Kit's plan.md)
  specs/notification/spec.md (delta) -> (like a spec.md diff)
  tasks.md    -> (like Spec Kit's tasks.md, same T001/T002... numbering
                  and TDD red/green task-pairing convention)
Then actually implemented it for real: wrote two failing tests for a new
notify()/send_slack() pair in greet.py, confirmed the RED failure was an
ImportError (missing function, not a wrong assertion - same discipline as
the greet-cli module), implemented notify()/send_slack(), reran pytest
and got 8/8 GREEN, checked off all 4 tasks, committed.

4.4 Merge and fold-in (OpenSpec's extra step vs Spec Kit)
---------------------------------------------------------------
Spec Kit: edit spec.md directly, bump its version, done.
OpenSpec: merge the change branch to main, THEN manually copy the
"ADDED Requirements" block out of the change's delta spec INTO the real
openspec/specs/notification/spec.md - a distinct, explicit "apply the
delta" step that doesn't exist in Spec Kit (Spec Kit never separates "the
proposed change" from "the live spec" as two different files).
We also added our own version header to the capability spec (OpenSpec has
no built-in semver policy either, just like Spec Kit's constitution never
defined "archive" - we had to invent the convention again here).

4.5 Archiving a completed change
-------------------------------------
Same WHAT/WHEN/WHERE/HOW discipline as Spec Kit's archive convention, just
a different path: openspec/changes/<change-id>/ moves to
openspec/changes/archive/<date>-<change-id>/ once its delta has been
folded into the live spec and no further iteration is planned.

4.6 The BREAKING change (config file format migration)
-----------------------------------------------------------
Ran a second change through the same OpenSpec structure, this time deliberately
BREAKING: config's storage format moved from flat key=value to a single JSON
object (change-id migrate-config-json-format). Kept spec-only this time (no
code implementation) - the point was to practice the artifacts a breaking
change needs that an additive one doesn't:

  - delta spec.md used BOTH "## REMOVED Requirements" (old flat-format
    requirement, named only - no need to restate its scenarios since it's
    being retired) AND "## ADDED Requirements" (new JSON-format requirement,
    full scenarios) in the same file. The additive Slack change only ever
    needed ADDED.
  - impact-map.md: traced config's downstream dependents (notification reads
    channel settings, audit-log reads log_level) and explicitly noted a
    capability that LOOKS related but isn't actually wired up (user-profile
    mentions "default name" like config's Purpose does, but no requirement in
    either spec actually connects them) - flagged as a pre-existing spec
    inconsistency worth remembering for later (spec debt).
  - migration-notes.md: a stakeholder-facing doc with a deprecation timeline
    (deprecation window, then removal) and concrete migration steps - this
    has no equivalent artifact in the additive change at all, because nobody
    needs migration instructions for a change that breaks nothing.
  - openspec/semver-decisions.md: a single log (not per-change) covering BOTH
    changes made in this module - Slack = MINOR (1.0.0 -> 1.1.0, purely
    additive), config format = MAJOR (1.0.0 -> 2.0.0, a requirement was
    REMOVED, not just extended).

Fold-in looked different too: the additive change's fold-in only APPENDED a
new requirement to notification/spec.md. This one REPLACED the old
"Flat key-value file format" requirement with "Structured JSON file format" -
proof that OpenSpec's delta mechanism handles replacement, not just addition.

------------------------------------------------------------------------
5. OPENSPEC MODULE - ISSUES FACED AND HOW WE OVERCAME THEM
------------------------------------------------------------------------

- Several files (user-profile/spec.md, notification's folder, design.md,
  tasks.md) were repeatedly created in the WRONG place - nested one level
  too deep inside an existing capability's own folder/subfolder (e.g.
  openspec/specs/greeting/specs/user-profile/spec.md instead of
  openspec/specs/user-profile/spec.md), or inside specs/notification/
  instead of the change folder's own top level.
  Fix: git mv to the correct path each time (creating the destination
  parent directory first when needed), then re-verified with git status
  and a direct file Read before committing.

- A folder name typo (notificaiton instead of notification) caused
  `git add` to fail with "No such file or directory".
  Fix: git mv the misspelled folder to the correct name.

- Repeated an EARLIER issue from the Spec Kit module: a file (greeting/
  spec.md, later also design.md) was committed with "0 insertions(+), 0
  deletions(-)" - meaning the file was staged and committed EMPTY even
  though it had real content on disk moments later. This happened because
  `git add` ran before the file's content was actually saved to disk.
  Fix: always check the insertions/deletions count in commit output - "0
  insertions" on a new file is a hard signal something is wrong, even if
  the create mode line looks normal. Re-added and re-committed once the
  real content was confirmed on disk via Read.

- A careless `Remove-Item -Recurse -Force` aimed at cleaning up a stray
  leftover folder accidentally deleted a FILE WE NEEDED (the delta
  spec.md) because it was sitting inside the same folder being removed.
  Fix: git restore --staged + git checkout -- to bring the deleted file
  back from the last commit, then re-verified it existed on disk before
  proceeding.

- The archive step for the Slack change silently went wrong: the
  intended `git mv` to openspec/changes/archive/2026-10-18-add-slack-
  notification never actually happened (instead an empty, oddly-named
  folder "archive-add-slack-notification" was created), and a `git add -A`
  swept up an unrelated, long-untracked README.txt into the same commit,
  under a misleading commit message.
  Fix: caught by checking `git show --stat <commit>` on the archive
  commit and noticing it only touched README.txt, not any openspec/
  folder - then re-ran the Remove-Item/New-Item/git mv sequence correctly.

- Multiple times, "done" was reported before a commit had actually
  happened (git add succeeded but git commit was never run, or ran but
  produced "nothing to commit"), or a commit's message claimed a step
  (like "mark tasks complete") while the diff showed a totally different
  file had changed.
  Fix: same discipline as the Spec Kit module - always independently ran
  git status --short, git log --oneline, and git show --stat <hash> to
  confirm the ACTUAL diff matched the CLAIMED step, before moving to the
  next one.

- The breaking config change's tasks.md hit the EMPTY-COMMIT bug a third
  time (0 insertions(+), 0 deletions(-), no rename involved - so not the
  benign case). It was also toggled/committed inconsistently across two
  separate commits (checkboxes appeared checked, then the same commit's
  diff showed them going from unchecked to checked again), suggesting a
  stale on-disk copy was edited and saved on top of an already-committed
  version.
  Fix: same as before - git show --stat on the suspicious commit, Read the
  current file, and re-commit once the live file content matched reality.

- A standing, cross-change artifact (semver-decisions.md, meant to live at
  the top-level openspec/ folder because it logs decisions for ALL changes,
  not just one) was first created INSIDE the single change's own folder.
  Fix: Move-Item to the correct top-level path (not git mv, since the file
  was still untracked at that point), then git add + commit from the right
  location.

------------------------------------------------------------------------
6. OPENSPEC MODULE - KEY TAKEAWAY (SO FAR)
------------------------------------------------------------------------
OpenSpec's directory split - specs/ as "current truth" vs changes/ as "a
queue of proposed diffs" - makes the delta-writing discipline explicit and
mechanical (write only ADDED/MODIFIED/REMOVED, never restate the whole
capability), whereas Spec Kit achieves the same end result (a reviewable
diff) implicitly, via git diff between two tagged versions. Neither tool
defines semver or archiving policy for you - in both cases that discipline
has to be invented and written down by the team using the tool, not
assumed from the tool's existence.

Both OpenSpec changes practiced in this module (the additive Slack change and
the breaking config format change, see 4.6) are now complete: specified,
folded into their live capability specs, and archived.

------------------------------------------------------------------------
7. CI INTEGRATION + AI-DRAFTED SPEC MODULE (Module 4)
------------------------------------------------------------------------
Same repo, new focus: making the spec conventions MACHINE-ENFORCED instead
of just hand-followed, and practicing AI-assisted spec drafting with a
mandatory critical-review step.

7.1 Structural spec lint, enforced in CI
---------------------------------------------
Wrote scripts/spec_lint.py: checks every specs/**/spec.md (including
archived ones) for the structural conventions this repo had only
informally followed so far - a **Status** field and a Change Log section.
Wired it into .github/workflows/spec-lint.yml, triggered on every pull
request into main, so a spec missing these fields fails CI before it can
be merged, not just at review time.

7.2 AI-drafted spec, then critical review (003-greet-log)
----------------------------------------------------------------
Had Claude draft specs/003-greet-log/spec.md from a one-line prompt
("log every greeting to a file with a timestamp"), matching the existing
spec.md format. Ran the lint against it immediately: FAIL (missing Status
field and Change Log section) - the lint tool doing exactly its job on a
fresh AI draft.
Then wrote specs/003-greet-log/ai-review-notes.md as a SEPARATE critical-
review step, documenting not just the lint-caught structural gaps but
content-quality gaps lint cannot catch: an inconsistent SHOULD requirement
(should be MUST), an unspecified timestamp format, an unmeasurable success
criterion, and missing edge cases (unwritable log path, concurrent writes,
unbounded log growth). Applied all of these fixes directly to the spec,
re-ran the lint: PASS. The key lesson: a passing lint only proves the
SHAPE is right, not that the content is unambiguous - that still needs a
human (or a deliberate separate review pass) reading it critically.

7.3 Real TDD cycle tied to the spec's own acceptance scenario
--------------------------------------------------------------------
Took the fixed spec's one GIVEN-WHEN-THEN scenario literally as the test to
write: wrote test_log_greeting_appends_timestamped_line with no
implementation behind it, ran pytest, confirmed RED (ImportError: cannot
import name 'log_greeting' - the right kind of failure). Implemented
log_greeting() in greet.py, reran pytest, confirmed GREEN (9/9 passed).
Committed test + implementation together.

7.4 A real pull request, not a simulated one
--------------------------------------------------
Pushed main (it had drifted 33 commits ahead of origin/main, since earlier
module work was only ever committed locally - had to push that first),
then pushed the feature branch and opened PR #1 against main through the
GitHub web UI (no gh CLI installed). Watched GitHub Actions actually run
spec-lint.yml on the real PR: "spec-lint succeeded in 7s". Squash-merged
into main. This was the first time in the whole project that CI ran
somewhere other than a local terminal.

7.5 workflow-log.md: narrating the whole loop end to end
----------------------------------------------------------------
Wrote workflow-log.md at the repo root, tracing this entire module's pass
through specify -> CI lint (red) -> critical review -> plan/revise -> CI
lint (green) -> task/implement/test -> push + real CI run -> archive, with
the actual commit hashes and CI result as evidence for each stage (see
workflow-log.md for the full table).

------------------------------------------------------------------------
8. MODULE 4 - ISSUES FACED AND HOW WE OVERCAME THEM
------------------------------------------------------------------------

- A pytest run right after adding the new log_greeting test showed only
  the original 8 tests passing, no error, no mention of the 9th test at
  all - the test FILE hadn't actually been saved to disk yet when pytest
  ran (an editor/save-race, the same family of bug as the earlier
  empty-commit issue, just hitting a test run instead of a commit).
  Fix: re-read the file to confirm its real on-disk content, then reran
  pytest - this time it correctly showed the true RED state
  (ImportError), proving the first "pass" was never real.

- `gh pr create` failed with CommandNotFoundException - the GitHub CLI
  wasn't installed.
  Fix: opened the pull request manually through the GitHub web UI instead.

- The repo's own "Approve" button was disabled on the PR.
  Not a bug: GitHub does not allow a PR's author to approve their own PR -
  a platform rule, not something broken in this repo's setup.

- Local main had drifted 33 commits ahead of origin/main (all of an
  earlier module's work had only ever been committed, never pushed).
  Fix: pushed main first, THEN pushed the feature branch and opened the
  PR, so the PR only showed this module's actual diff instead of the
  entire unpushed backlog.

- workflow-log.md was committed twice in a row at only ~20 lines, cut off
  mid-sentence, even though the full intended content was much longer.
  Root cause: the message delivering the file's content wrapped the WHOLE
  thing in one outer ```markdown fence, but the content itself contained
  two INNER ``` fenced examples - a renderer/clipboard closed the outer
  fence at the first inner one, silently truncating everything after it.
  Confirmed by noticing the cutoff landed at the exact same line both
  times.
  Fix: delivered the file content via a PowerShell here-string
  (@'...'@ | Set-Content -Encoding utf8 workflow-log.md) with indented
  (not fenced) code examples instead, which has no inner ``` markers to
  collide with an outer one. Verified the full line count before
  committing.

------------------------------------------------------------------------
9. MODULE 4 - KEY TAKEAWAY
------------------------------------------------------------------------
Turning a written convention (Status field, Change Log section) into a
LINTED, CI-enforced rule is what actually makes it stick across an entire
team or a long project - a convention that only lives in a human's memory
gets forgotten the moment attention moves elsewhere. Equally important:
an AI-drafted spec still needs a deliberate, separate critical-review pass
- lint catches missing STRUCTURE, but only a human (or a dedicated review
step) catches missing or ambiguous CONTENT, and those are different kinds
of gaps that need different kinds of checks.

------------------------------------------------------------------------
10. ADVANCED CI / OPENSPEC CLI / TRACEABILITY MODULE (Module 5 - IN PROGRESS)
------------------------------------------------------------------------
Same repo, scaling up the CI integration from Module 4: a real OpenSpec
CLI in the pipeline (not a hand-simulated one), a spec-to-test coverage
gate, and AI-generated test stubs at scale across multiple specs.

10.1 Installing the REAL OpenSpec CLI (not a namesquat)
----------------------------------------------------------------
Before adding any package as a dependency, verified it directly against
the npm and PyPI registries rather than trusting the name alone: plain
"openspec" on both npm and PyPI turned out to be unrelated placeholder /
hardware-parts-API packages (a namesquat risk), while @fission-ai/openspec
(v1.14.3, github.com/Fission-AI/OpenSpec - the same tool already used in
Module 2) was confirmed as the real CLI. Installed it as a devDependency
via `npm.cmd install --save-dev @fission-ai/openspec`.

10.2 Confirming the CLI recognizes existing OpenSpec work
----------------------------------------------------------------
Ran `npx.cmd openspec validate --all --no-interactive` against the
openspec/ folder built back in Module 2's brownfield exercise, with no
`openspec init` needed first: all 5 existing capability specs (audit-log,
config, greeting, notification, user-profile) validated cleanly -
"Totals: 5 passed, 0 failed (5 items)". Confirms the real CLI reads this
project's existing structure correctly, not just a freshly scaffolded one.

10.3 A spec-to-test traceability convention, enforced by a coverage gate
------------------------------------------------------------------------------
Invented a lightweight, two-sided linking convention (neither Spec Kit nor
OpenSpec prescribe one):
  - each GIVEN-WHEN-THEN acceptance scenario in a spec.md gets an inline
    HTML anchor right before its **Given**, e.g.
    <a id="US1-S1"></a>**Given** ... (invisible when the spec renders, but
    a real clickable GitHub anchor link).
  - each test covering that scenario carries a comment directly above it:
    # spec: specs/<slug>/spec.md#US1-S1
Wrote scripts/spec_test_coverage.py to parse both sides, compute the
percentage of scenarios with a matching test-side comment, and gate at an
80% threshold (FAIL below it). Confirmed the gate: 002-farewell-cli (no
tests yet) and 003-greet-log (1 scenario, already tested) together
produced exactly 1/3 scenarios linked (33.3%) -> FAIL, as expected before
any stubs existed for 002.

10.4 AI-generated test stubs for every scenario, logged
----------------------------------------------------------------
Used Claude to generate pytest stubs directly from each spec's GWT
scenarios, one scenario at a time (not the whole spec in one shot), using
@pytest.mark.skip plus a deferred (in-body) import so a not-yet-written
function doesn't crash collection of the whole test file. Generated two
stubs for 002-farewell-cli's two scenarios; 003-greet-log's one scenario
already had a real passing test from Module 4, so it was documented as
"already implemented" in the log rather than being re-stubbed. Logged the
exact prompt pattern and generated output in
specs/test-stub-generation-log.md. Afterwards the coverage gate reported
3/3 scenarios linked (100.0%) -> PASS, since the gate only checks for the
linking comment, not whether the test passes or is skipped.

10.5 Expanding CI to three parallel gates (a fourth still pending)
------------------------------------------------------------------------
Expanded .github/workflows/spec-lint.yml (renamed in display only to
"Spec CI") from one job to three, all triggered on every PR into main and
running in parallel: spec-lint (Module 4's structural check),
openspec-validate (`npx openspec validate --all --strict --no-interactive`,
via a Node setup + `npm ci` step), and coverage-gate (this module's 80%
threshold script). A fourth stage - auto-archiving a spec's folder
automatically on merge - is deliberately NOT yet wired in: it would mean a
CI job pushing commits back to main on its own, which needs an explicit,
separate go-ahead before being automated (same standing caution as any
other hard-to-reverse, repo-wide action in this project).

------------------------------------------------------------------------
11. MODULE 5 - ISSUES FACED SO FAR (module still in progress)
------------------------------------------------------------------------

- `npm init` / `npx` failed under PowerShell with "npm.ps1 cannot be
  loaded ... is not digitally signed ... UnauthorizedAccess" - npm/npx
  resolve to .ps1 wrapper scripts blocked by the shell's execution policy.
  Fix: called npm.cmd / npx.cmd directly instead, bypassing the blocked
  wrapper with zero system or global policy changes - a narrower fix than
  touching Set-ExecutionPolicy.

- The coverage script reported "0/0 scenarios linked (100.0%) - PASS" on
  its first real run, instead of the expected 1/3 (33%) FAIL. Root cause:
  the HTML anchor edits meant to be added to both gated spec.md files
  hadn't actually been saved on disk yet at the time the script ran - one
  spec had no anchors applied at all, the other's edit had only been
  applied AFTER that run, not before.
  Fix: independently re-read both spec files' actual on-disk content
  before trusting the reported "done", found the missing anchor, had it
  applied, and reran - this time getting the correct 1/3 (33.3%) FAIL.
  This also surfaced a latent design gap in the script itself: treating
  total == 0 as "100% PASS" silently hides the case where NO scenarios
  were instrumented at all, rather than distinguishing that from genuine
  full coverage - noted as a known rough edge, not yet fixed.

- A file meant to hold a rendered markdown log (test-stub-generation-log.md)
  instead ended up containing the LITERAL PowerShell here-string command
  text (the `@'` ... `'@ | Set-Content ...` wrapper) as its actual file
  content - the command block had been pasted into an editor as file
  content instead of being run in the terminal.
  Fix: wrote the file's real content directly instead of relying on a
  copy-pasted terminal command, then had the coverage/pytest run confirm
  the file was now real, readable markdown.

------------------------------------------------------------------------
12. MODULE 5 - KEY TAKEAWAY (SO FAR)
------------------------------------------------------------------------
Scaling a convention from "one spec, checked by hand" (Module 4) to "every
gated spec, checked by a script in CI" (Module 5) surfaces failure modes
that don't show up at small scale: a silent "0 instrumented == 100%
covered" edge case, and a save/paste step that silently produces the wrong
artifact (command text instead of its output) are both the kind of bug
that is invisible until something downstream (a coverage number, a file
read) is checked independently rather than trusted at face value. The
project's running discipline - verify the actual file/commit state before
advancing, not just the claim that a step was done - caught both.