Implemented the AG01 consumer migration.

- Authenticated sheet-basis reads now use `RuntimeRevisions` and exact retained revisions; legacy local draft history remains unchanged.
- Added regression coverage for Runtime-first lookup and explicit `/home/user/work/runtime` test resolution.
- Preserved native outbox/retry/undo/redo behavior and existing assertions.

Tests:

- History: 5 passed
- Journal/revisions: 46 passed
- Sheet/native: 73 passed
- Central Runtime lane: 27 passed, 2 deselected
- `git diff --check`: passed

Ruff reports only inherited diagnostics outside this change. AG01 remains in progress until integration; no full suite or integration cut was run. Report, shared note, commit message, and `DONE` marker are written.