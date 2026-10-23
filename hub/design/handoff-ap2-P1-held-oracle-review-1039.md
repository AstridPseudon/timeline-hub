# P1 held-duration oracle review handoff

Independent review **PASS** for the exact one-line test-only correction in
`116b6514137343668fb24bff6b53f8b89d2ae2e0` against current
`0cdc76782833d594776452e07706acb406c51553`.

The numeric-held seed is authored with `hold: 8`; split at 2 creates the right
clip with `hold: 6`. Source In changes only `from: 0 -> 3`, preserving explicit
`hold: 6`, `to: 8`, and `at: 2`. The assertion now uses
`originalClip.hold - SPLIT_AT`, preserving the original source-of-truth
boundary. Exact diff custody confirms one own commit, one file, one line,
clean outside identity, and no product/API/fixture/port changes. All other
guards, raw/canonical/opaque/null/absence/order/new-ID/dependency/lost-ACK/
restart/retry/undo assertions and the complete second case are unchanged.

Checks passed: scoped ESLint; original Playwright list with exactly 2 tests;
root, App, and Node TypeScript checks; and `git diff --check`. No browser,
HTTP/body, full, build, service, or request-test run was performed.

This is not overall P1 credit: the second case remains unresolved because the
missing second App dispatch prevented observing the intended Runtime refusal.
Recover the retained trace/error context before changing or retrying that case.
