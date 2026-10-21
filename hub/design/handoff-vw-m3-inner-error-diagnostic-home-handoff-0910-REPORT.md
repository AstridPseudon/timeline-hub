# AggregateError diagnostic HOME handoff

Verdict: **APPROVED — minimal and correct.**

Reviewed the actual one-parent diff `832384e9071d95feae1cd1f2425dffe015d5264f` against `e2267a418a89d659c1a70524b17dde631f12fd16`.

- Exact scope: two test files, 28 net insertions / 3 deletions:
  - `tests/e2e/timeline/viewing-parity/harness.ts` — adds `safeFailureReason` and `aggregateFixtureFailures`; both existing teardown aggregate sites now use it.
  - `tests/e2e/timeline/viewing-parity/harness.test.ts` — adds one direct control with two visible inner messages, identity checks, nested-cause preservation, and sanitization.
- The formatter exposes only numbered direct `Error.message` values (or fixed fallbacks), while `new AggregateError(failures, ...)` retains the original `Error`/`AggregateError` objects and their causes in `errors`.
- Cleanup and diagnostics remain intact: existing `harness.stop`, `browser.close`, `assertRunBoundary`, and `assertSourceVersionsUnchanged` checks are unchanged; the thrown value remains an `AggregateError`, preserving the existing error type/location reporting path.
- No assertions were deleted or converted, and no frozen d00 or gate packet was touched.

## Source/current-HOME checks

- Donor commit: `832384e9071d95feae1cd1f2425dffe015d5264f`
- Donor tree: `1ceb1f339b31555b524833724a10b980c8d2f3e8`
- Parent/base: `e2267a418a89d659c1a70524b17dde631f12fd16`
- Current HOME source: `/home/user/work/app` `tl/integration` at commit `9cd604f37b5826a36fc7ac449c8baa51c8174f92`, tree `aa659245db3e58c2cf592e4437316aeb1454f38f`
- Current HOME does not contain the donor; both target files are unchanged from e226.
- The exact patch byte-compares with `git diff e226..832` and applies cleanly to current HOME (`git apply --check`).

## Evidence reused / not repeated

The donor worker already passed:

```text
node --import tsx -e "import assert from 'node:assert/strict'; import { aggregateFixtureFailures } from './tests/e2e/timeline/viewing-parity/harness.ts'; const cause = new Error('nested secret'); const first = new Error('first inner failure'); const second = new Error('second inner failure', { cause }); const aggregate = aggregateFixtureFailures('fixture failed', [first, second]); assert.ok(aggregate instanceof AggregateError); assert.match(aggregate.message, /1: first inner failure/); assert.match(aggregate.message, /2: second inner failure/); assert.doesNotMatch(aggregate.message, /nested secret/); assert.deepEqual([...aggregate.errors], [first, second]); assert.equal(second.cause, cause); console.log('aggregateFixtureFailures direct control: PASS');"  PASS
npx tsc --noEmit --pretty false                                                                                 PASS
npx eslint tests/e2e/timeline/viewing-parity/harness.ts tests/e2e/timeline/viewing-parity/harness.test.ts       PASS
node --import tsx --test --test-name-pattern='keeps both fixture failures visible' tests/e2e/timeline/viewing-parity/harness.test.ts  PASS
git diff --check                                                                                               PASS
```

Per the brief, unchanged tests were not rerun. No browser, renderer, helper, socket, central, full, render, or install run.

Recommended next step: merge the flat patch through the current HOME source, then let the existing central gate run consume the now-readable fixture failure messages.
