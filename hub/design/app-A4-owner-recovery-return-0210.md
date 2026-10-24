## Report

Implemented the narrow A4 fix in `localSaveSession.ownerRecovery.test.ts` only.

- Replaced the in-memory owner-set illusion with a stateful `exclusiveLock` at the real `createCommitOutbox` boundary.
- Uses durable IndexedDB fixture persistence.
- Proves A holds the lock, B’s explicit recovery is refused while held, and recovery succeeds only after A disposes/releases.
- Preserved existing recovery bytes, keys, dependent B guards/display basis, canonical/raw preservation, and zero legacy-route assertions.
- Source tree: `8f92a51e3a4b5ccc27e1a5b83a3ca5dc73b63179`
- Diff: 1 file, 39 insertions / 20 deletions.
- Commit message written; `DONE` marker created.

Validation:

- Owner recovery test: 2/2 passed.
- Exact six-file lane: 6 files, 105/105 passed.
- Root/App/Node TypeScript checks: passed with `--noEmit --incremental false`.
- Scoped ESLint: passed with `--max-warnings 0`.
- `git diff --check`: passed.
- Scope/title/assertion census: passed; helper, production files, and `commitSession.test.ts` unchanged.

No full, browser, backend, service, or live-suite tests were run.