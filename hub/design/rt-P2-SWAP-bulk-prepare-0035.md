## Report

Prepared P2 MAIN SWAP/bulk handoff.

- Copied the qualified 0006 D66 profile byte-for-byte.
- Added exact pinned plans for `p2-popup-swap` (SWAP80a) and `p2-transition-none-bulk` (bulkNone).
- Verified all four exact checkout receipts and trees.
- No registry changes, submissions, browser/body/build runs, or product/test changes.

Tests:

- D66 focused controls: `22 passed`
- Profile syntax/import and selector checks: passed
- Evidence JSON parsing, stale-tuple scan, clean checkouts, `git diff --check`: passed
- Full suite: not run.

Plans: [SWAP]( /home/user/work/wt/rt-P2-SWAP-bulk-prepare-0035/evidence/p2-popup-swap/p2-popup-swap-submit-plan.json), [bulk]( /home/user/work/wt/rt-P2-SWAP-bulk-prepare-0035/evidence/p2-transition-none-bulk/p2-transition-none-bulk-submit-plan.json)

Normal/preflight result IDs remain intentionally null; submit after priority MAIN P4 finishes.