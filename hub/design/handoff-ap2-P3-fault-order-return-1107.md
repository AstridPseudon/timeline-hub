## Report

Implemented helper-only P3 repairs in the three authorized files:

- Records bounded raw browser POST identities; `attempts` counts all observations.
- Separates observed traffic from forwarded Runtime receipts.
- Adds staged-route release/abort lifecycle and stale-page handling.
- Rejects early/mismatched B traffic and duplicate A.
- Replaced message-only fast/slow controls with real callback/timer ordering.

Tests passed:

- Node controls + reset preconditions: 23/23.
- Serialized TypeScript checks: all 3 passed.
- Scoped ESLint: passed.
- Playwright list-only: 15 tests.
- `git diff --check`: passed.
- Reverse-removal dry run: passed.

Protected Gate5 body/reset/tail hashes remain unchanged:

- Body: `d47d5526…`
- Reset: `62c28b0b…`
- Tail: `6bfdd99d…`

Full spec hash: `b3bc5d03…` → `01049584…`.

The original assertion was not edited. Review-only proposal is recorded in `/tmp/w-6c48e25706/ap2-P3-fault-order-proposal.patch`; it asserts observed `[A,A]`, forwarded `[A]`, exact identity, and no distinct B before recovery.

Original live run 3896 remains NO-GO; no browser/backend/full run was performed. Orchestrator approval is still required before applying the assertion correction.