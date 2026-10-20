## Done

Migrated literal numeric parent-clip CLI moves (`timelines edit --on`) to the registered `clip.move` command via `TimelineSession`. Symbolic moments, occurrence-scoped edits, drafts, and unsupported flags retain the legacy path.

Tests:

- 104 targeted pytest tests passed.
- Ruff passed on changed adapter/tests.
- `git diff --check` passed.
- Full suite and `make check` not run.

WC7/WC8 global helpers remain held for unsupported Checkout, narration, and whole-document consumers; AG02 remains `in-progress` in the ledger.

Created `DONE` and the conventional commit message at the requested path.