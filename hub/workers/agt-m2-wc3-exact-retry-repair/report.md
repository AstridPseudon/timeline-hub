Implemented WC3 exact retry repair.

- Pending swaps now require exact owner, clip, source object, head/publication, and old/new five-field media pins.
- Unrelated, ambiguous, stale, or multiple pending intents visibly refuse with no flush, POST, or outbox mutation.
- Omitted keys replay the persisted flight key/body; opaque command data is preserved.
- Added adversarial and restart/lost-ACK tests.

Validation:

- Central targeted: **165 passed**
- Replacement tests: **13 passed**
- Sync: **61 passed**
- Native frontends: **10 passed**
- Media recipes: **81 passed**
- `git diff --check`: passed
- Ruff on changed adapter/tests: passed

Real private Runtime parent-provider qualification remains for the orchestrator’s approved private-runtime lane; no public13 or fake-provider qualification was claimed.

Commit message and `DONE` marker written.