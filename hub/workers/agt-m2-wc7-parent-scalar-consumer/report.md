## Done

- Extended `AttachedCheckout.publish()` to admit one explicit parent `clip.set` source-HOLD command.
- Preserved source-unit semantics, exact capture, outbox/session retry identity, undo, and legacy refusal for mixed, occurrence, source-window, or unsupported edits.
- `sync.py` unchanged; no legacy writer/public method/schema added.
- Added SDK and HTTP regression coverage.

## Tests

- SDK: `26 passed`
- Central HTTP integration: `14 passed`
- `git diff --check`: passed
- No full suite run.

Commit message written to `commit-msg`; `DONE` marker created. No blockers.