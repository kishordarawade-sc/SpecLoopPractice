# Tasks: Greet CLI

**Input**: Design documents from `/specs/001-greet-cli/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-contract.md,
quickstart.md

**Tests**: Requested explicitly (pytest) — included per user story, written before implementation.

**Organization**: Tasks are grouped by user story (US1 = P1, US2 = P2) for independent testing.

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup

- [X] T001 Create `greet.py` at repo root: argparse CLI with one optional positional `name`
      argument, calling `build_greeting(name)` and printing the result; `build_greeting` raises
      `NotImplementedError` for now.
- [X] T002 [P] Create `tests/test_greet.py` importing `build_greeting` from `greet.py`.

## Phase 2: Foundational

- [X] T003 Add a minimal `pytest.ini` (or `[tool:pytest]` section) at repo root so `pytest` from
      repo root discovers `tests/` without extra flags.

**Checkpoint**: Project skeleton runs (`python greet.py` exits, tests are collectible) before any
story logic exists.

---

## Phase 3: User Story 1 - Greet a named user (Priority: P1) 🎯 MVP

**Goal**: Running `greet <name>` prints `Hello, <name>!`.

**Independent Test**: Run `python greet.py Alice` and confirm the output is `Hello, Alice!`.

### Tests for User Story 1 ⚠️ write first, confirm they FAIL

- [X] T004 [P] [US1] Add `test_greet_with_name`: `build_greeting("Alice") == "Hello, Alice!"` in
      `tests/test_greet.py`.
- [X] T005 [P] [US1] Add `test_greet_with_multiword_name`:
      `build_greeting("Alice Smith") == "Hello, Alice Smith!"` in `tests/test_greet.py`.
- [X] T006 [P] [US1] Add `test_greet_trims_whitespace`:
      `build_greeting("  Alice  ") == "Hello, Alice!"` in `tests/test_greet.py` (FR-004).

### Implementation for User Story 1

- [X] T007 [US1] Implement `build_greeting(name)` in `greet.py`: strip whitespace; if the result
      is non-empty, return `f"Hello, {name}!"` (depends on T004-T006 existing and failing first).

**Checkpoint**: User Story 1 fully functional and independently testable/demoable.

---

## Phase 4: User Story 2 - Greet with no name provided (Priority: P2)

**Goal**: Running `greet` with no argument (or a blank one) prints `Hello, World!` instead of
erroring.

**Independent Test**: Run `python greet.py` with no arguments and confirm the output is
`Hello, World!`.

### Tests for User Story 2 ⚠️ write first, confirm they FAIL

- [X] T008 [P] [US2] Add `test_greet_default`: `build_greeting(None) == "Hello, World!"` in
      `tests/test_greet.py`.
- [X] T009 [P] [US2] Add `test_greet_whitespace_only_defaults`:
      `build_greeting("   ") == "Hello, World!"` in `tests/test_greet.py`.

### Implementation for User Story 2

- [X] T010 [US2] Extend `build_greeting(name)` in `greet.py` to return `"Hello, World!"` when
      `name` is `None` or blank after stripping (depends on T007, T008, T009).

**Checkpoint**: Both user stories pass independently and together.

---

## Phase 5: Polish & Cross-Cutting Concerns

- [X] T011 Confirm `greet.py`'s `main()` exits with status code 0 after printing in all cases
      (FR-005).
- [X] T012 [P] Run `quickstart.md` validation manually: `python greet.py Alice` and
      `python greet.py` both produce the documented output.
- [X] T013 [P] Confirm `python greet.py --help` prints usage text (argparse default) without
      error.

---

## Dependencies & Execution Order

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup — blocks both user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational. No dependency on US2.
- **User Story 2 (Phase 4)**: Depends on Foundational. Extends the same function as US1 (T010
  depends on T007), so in practice run after US1, though its tests (T008-T009) can be written in
  parallel with US1's.
- **Polish (Phase 5)**: Depends on both user stories being complete.

### Parallel Opportunities

- T001 and T002 can run in parallel (different files).
- T004, T005, T006 can run in parallel (same file, but independent test functions — write all
  three, then implement once).
- T008, T009 can run in parallel with each other, and can be drafted alongside T004-T006 even
  though T010 must wait for T007.
- T012, T013 can run in parallel.

## Implementation Strategy

### MVP First (User Story 1 only)

1. Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1).
2. **STOP and VALIDATE**: `python greet.py Alice` → `Hello, Alice!`; `pytest` passes T004-T006.
3. This alone is a demoable MVP.

### Incremental Delivery

1. Setup + Foundational → skeleton runs.
2. Add US1 → validate independently → demo.
3. Add US2 → validate independently (and that US1 still passes) → demo.
4. Polish.

## Notes

- Only one implementation file (`greet.py`) and one test file (`tests/test_greet.py`) — "parallel"
  here mostly means "can be drafted together", not "no merge conflicts across files".
- Commit after each phase checkpoint, not after every single task.
