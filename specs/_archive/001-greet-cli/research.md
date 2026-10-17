# Research: Greet CLI

No `[NEEDS CLARIFICATION]` markers remained in the Technical Context, so this is a short record of
the small technology decisions made while filling it in, rather than open-ended research.

## Decision: argparse over click/typer

- **Decision**: Use the standard library `argparse` module.
- **Rationale**: Zero external dependencies, matches Constitution Principle IV (Simplicity Over
  Completeness), and the interface is a single optional positional argument — too small to
  benefit from a third-party CLI framework.
- **Alternatives considered**: `click` and `typer` — both add a dependency for no behavioral gain
  at this scope; rejected.

## Decision: whitespace handling

- **Decision**: Call `.strip()` on the provided name; treat an empty result as "no name given".
- **Rationale**: Directly satisfies FR-004 and the edge case in spec.md (whitespace-only name
  falls back to the default greeting).
- **Alternatives considered**: Rejecting whitespace-only input with an error — rejected, spec
  explicitly calls for graceful fallback, not an error.

## Decision: exit code

- **Decision**: Always exit 0 after printing a greeting (argparse itself exits non-zero on
  malformed invocation, e.g. too many arguments, which is standard argparse behavior and out of
  spec's scope).
- **Rationale**: Satisfies FR-005; there is no failure mode within the feature's own logic.
- **Alternatives considered**: None needed — single success path.
