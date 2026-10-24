## Completed

Restored byte-exact blobs from `602f8b1f58593302829fb449d0ded62a91462a22`:

- Five session tests and `commitSession.ts`
- `trackLabelGesture.ts` and its test, because `commitSession.ts` and restored tests still depend on them

All eight hashes match the source revision. Final expected tree: `a38844975865110cd2c026dc10fd7aa1ea488e71`. Worker base: `080db52e6bb9095b3116afd7a076772cf2475d0f`; parent: `602f8b1f58593302829fb449d0ded62a91462a22`. Commit SHA remains pending harness commit.

The two gesture files could not remain deleted: caller scan found production type usage plus restored session-test imports. Remaining deletion inventory: none.

Review census: 58 declarations / 515 assertions. Direct restored counts: 515 `expect(...)` total; five named session tests account for 499, gesture test 16.

Tests/checks passed:

- Pinned Node 20 Vitest, serialized, expanded union: 34 files, 627 tests passed
- Locked `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`: passed
- Scoped ESLint on all eight restored paths: passed
- `git diff --check`: passed
- Protected generic-patch, session environment, track-label capture, and D31 transcript blobs: identical
- D31 transcript: 397 lines / 40 assertions

Live coverage restored includes scalar guards, lost-ACK/restart recovery, placement/task fencing, duplicate inverse/undo, shot-set commits, label conflicts, explicit resolution, request/reply assertions, and frozen gesture capture behavior.

Ledger disposition:

- `APP-A4-D37-SESSION-CHAIN`: retained required behavior
- `APP-A4-D37-NATIVE-LABEL`: no bounded deletion; required gesture dependency restored

No full, browser, service, backend, or original journey suite was run. `DONE` and the commit message were written.