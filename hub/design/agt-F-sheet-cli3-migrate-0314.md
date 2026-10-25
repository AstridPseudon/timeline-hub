## F-D86 report

- Migrated `[cli]` to `commit --file` with exact base pins.
- Migrated `[sheet-cli]` and lost-ack flows to current `NativeSheet`/persisted outbox APIs.
- Replaced retired publication undo with `TimelineSession.undo`.
- Preserved commit count, reload, inverse/redo, exact retry/key immutability, pending-draft, ABA/intervening-write, and no-recapture assertions.
- Only the assigned test file changed.

Validation:

- In-memory compile: PASS
- Ruff candidate and parent baseline: PASS
- Mypy candidate and parent baseline: PASS
- `git diff --check`: PASS
- Behavioral tests/full suites: intentionally not run per source-only brief.

Commit message and `DONE` marker created.