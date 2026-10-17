# CLI Contract: `greet`

## Invocation

```text
python greet.py [name]
```

- `name` (positional, optional, string): the name to greet.

## Behavior

| Input                         | stdout                | Exit code |
|--------------------------------|------------------------|-----------|
| `greet Alice`                   | `Hello, Alice!`        | 0         |
| `greet "Alice Smith"`            | `Hello, Alice Smith!`  | 0         |
| `greet "  Alice  "`              | `Hello, Alice!`        | 0         |
| `greet` (no argument)            | `Hello, World!`        | 0         |
| `greet "   "` (whitespace only)  | `Hello, World!`        | 0         |

Maps to spec.md: FR-001 (command shape), FR-002/FR-003 (greeting selection), FR-004 (trimming),
FR-005 (exit code). No other flags, output streams, or exit codes are part of this contract.
