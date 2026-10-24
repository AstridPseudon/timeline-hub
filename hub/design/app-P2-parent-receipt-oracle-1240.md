Implemented the strict receipt/publication oracle correction.

- Changed P2 reply validation to require distinct nonempty `txn-*` receipt IDs while preserving `Idempotency-Key`.
- Bound history, head, inverse, and undo assertions to `receipt.receipt_id`.
- Added actual-helper controls for wrong receipt, request key, head, history, inverse, and undo identities.
- Touched only:
  - `tests/e2e/local/three-products.p2-tour.spec.ts`
  - `tests/e2e/local/support/p2-parent-oracle.test.mjs`

Verification:

- Parent/document/transition controls: **12 passed**
- Scoped ESLint: **passed**
- `git diff --check`: **passed**
- Reverse removal check: **passed**
- Playwright list-only: **3 tests listed; browser not run**
- No full, browser, service, or admission suite run.

Contract citation: `commit-v2.md §4`, receipt publication identity is `receipt.receipt_id`; idempotency identity is `receipt.idempotency_key`.

Hashes:

- P2 spec before/after: `2e8fc72b...530a8d / 67662468...c9cd0e0`
- Parent control before/after: `a0bfad5d...7dfc5f / 225a4c43...47e90`
- `assertReplyShape` before/after: `eadab56b...6a1ca7 / 419085eb...41b49b1`

Current branch: `tl/app-P2-parent-receipt-oracle-1240`, uncommitted; harness commit message and `DONE` marker created.

Behavior ledger row: P2 receipt/publication oracle corrected on current branch; later merge proof must update status. No additional protected-shape gap found.