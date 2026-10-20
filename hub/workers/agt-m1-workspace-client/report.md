## Done

- Added `WorkspaceClient.commit_timeline` and `list_timeline_commits` via `_call_generated`.
- Added actionable `503 not_ready` errors when generated Runtime methods are unavailable.
- Added scoped `RemoteTimelines.commit` and immutable `history` adapters.
- Added focused SDK tests and published signatures in coordination docs.
- Wrote commit message to the requested path.

## Tests

- Targeted SDK/remote tests: **48 passed**
- Existing remote neighbors: **110 passed, 1 skipped**
- `ruff` focused checks, `py_compile`, and `git diff --check`: **passed**
- Full/socket suite: **not run** per instructions.
- Broad Ruff still reports 122 pre-existing `remote.py` violations.

Runtime-generated client integration remains unverified until the Runtime pin lands.