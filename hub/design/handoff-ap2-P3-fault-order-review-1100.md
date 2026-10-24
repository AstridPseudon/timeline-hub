# P3 independent review: FAIL

The source preserves the original Gate5 body, reset, tail, mounted helper, product paths, and assertions byte-for-byte, but the fault helper weakens the protected `attempts === 1` guard.

At `three-products.spec.ts:811–818`, the exact automatic A retry is recorded in `stagedRetries` and returns before `route.fetch()`. It is therefore absent from both `attempts` and `posts`, while the original assertion at `1366` still checks `wire.attempts === 1`. This counts forwarded Runtime requests, not observed browser POST attempts, allowing the known second A browser request to pass invisibly.

The offline controls pass, but the “fast/slow” cases execute identical states—the schedule value is only an assertion message—and do not exercise B staging, page lifecycle, or stale-route behavior. The staged `Route` is not retained for explicit release/abort, so same-page retry and old-page route races remain unproved.

The P1 comparison is stronger: it retains `heldRetry`, records raw body/key/status, explicitly fetches/releases the retry, and verifies the exact retry reply. The candidate has no equivalent staged-route release or response correlation.

Protected hashes:

- Full spec: `26c1ae…` → `b3bc5d…`
- Gate5 block, marker-bounded: unchanged `d47d5526…`
- Reset-to-next-test tail: unchanged `db3b8aff…`
- Mounted-document helper: unchanged `d2174781…`
- Reset-precondition controls unchanged.
- Reverse-removal check passed.
- Only the three authorized paths differ.

Tests:

- Node controls + reset preconditions: 23 passed.
- Repo-pinned serialized TypeScript checks: all 3 passed.
- Scoped ESLint: passed.
- Playwright list-only: 15 tests discovered.
- `git diff --check`: passed.
- No browser/backend/full/live suite run.
- Original actual run `3896` remains a Gate5 NO-GO.

Minimal proposal: retain a complete observed-request sequence and explicit staged-route lifecycle, then assert exact `[A, A]` browser identities before recovery, zero B identity before A recovery, and forwarded Runtime sequence `[A]`; the protected `attempts === 1` contract must be resolved by the orchestrator before editing. No source changes made.