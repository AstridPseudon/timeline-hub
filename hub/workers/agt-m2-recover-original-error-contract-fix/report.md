## Report

Implemented AG-RECOVER repair on base `53af5383802e995f78b3693a22d54b3e86062eff`.

- Ported catalog recovery and native `TimelineSession.restore`.
- Removed restore-only `WorkspaceClientError` → `ConnectionError` wrapping.
- Preserved WC7 `_flush(..., prepare=...)` and `_explicit_outbox`.
- Added/updated recovery, retry, CLI, and native facade tests.
- `DONE` and commit messages written.

Tests:

- Focused SDK/facade/CLI: **190 passed, 1 skipped**
- Exact retry + refusal neighbors: **2 passed**
- `git diff --check`: passed
- Ruff: existing baseline failures; no new targeted validation claimed.
- Live HTTP case: attempted centrally but remained unverified due test-service marker/allow-list limitations. No full suite run.

Patch digest: `586ce7f80e1e7dc31e98562faa68a32980b02af2c0e80dca0a3df2cfe5a6455f`.