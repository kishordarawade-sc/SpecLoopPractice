# Data Model: Greet CLI

No persisted entities. The feature's only data is a transient, in-memory value for the duration
of one invocation:

- **name** (string, optional): raw CLI argument, trimmed of leading/trailing whitespace before
  use. An empty value after trimming is treated as "absent" (see FR-003, FR-004).

There is no storage, no relationships, and no state transitions to document.
