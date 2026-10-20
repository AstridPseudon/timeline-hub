Implemented on base `78ff61d5`:

- Numeric `Clip.on(number)` captures `clip.move` before mutation with explicit parent/occurrence identity and guards.
- Existing session/outbox now carries and publishes the original command with rationale, durable retry, peer rebase, restart, and undo.
- Unsupported/mixed edits remain held; no donor recognizer or schema changes.
- Added regression coverage with zero legacy-writer traffic.

Tests:

- Publication retry: 3 passed.
- Native checkout: 20 passed.
- Producer/native sync: 48 passed.
- Broader checkout: 86 passed, 1 unrelated failure due missing fonttools/WOFF2 dependency.

`git diff --check` passes. No full/live integration suite was run. Commit message and `DONE` marker written.