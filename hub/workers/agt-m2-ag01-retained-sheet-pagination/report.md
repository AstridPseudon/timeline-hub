Implemented AG01 retained sheet-history pagination.

Changes:
- Added private verified cursor-chain traversal in `RuntimeRevisions`.
- Updated `find_version()` to resolve bases beyond 100 accepted edges.
- Added two-page page-2 regression coverage.
- Preserved bounded revision refs, publication ancestry, refusal/malformed handling, and local journal/outbox separation.

Tests:

- `32 passed, 2 deselected`
- `57 passed`
- `git diff --check` passed

No full/integration suite was run. Runtime integration remains unverified. Report, commit message, and `DONE` marker written.