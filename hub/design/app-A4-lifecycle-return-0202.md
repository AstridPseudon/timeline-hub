## Report

Implemented A4 in `localSaveSession.lifecycle.test.ts` only.

- Replaced no-op outbox locking with a stateful production `createCommitOutbox` + IndexedDB fixture.
- Lock ownership is derived from acquisition/hold/release state.
- Added early-contender refusal and post-dispose contender success controls.
- Preserved all six lifecycle cases and existing assertions: 35 baseline assertions, 39 total including four lock controls.
- Created `DONE` and commit message (`A4: prove local save claim lifecycle`).

Tests:

- Target lifecycle: 6/6 passed.
- Exact five-file lane: 105/105 passed.
- Root/App/Node TypeScript checks: passed with `--noEmit --incremental false`.
- Scoped ESLint: passed with `--max-warnings 0`.
- `git diff --check`: passed.

No full/browser/service suites run.