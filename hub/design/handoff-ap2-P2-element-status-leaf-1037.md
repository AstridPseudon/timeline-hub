# Handoff: ap2-P2-element-status-leaf-1037

The P2 element/asset spec has one bounded contract spelling correction at `assertAcceptedReply` line 209: the accepted-status allow-list now uses `rebased` instead of `historicalrebased`. This is test-only and preserves every other byte-level assertion and route guard.

Starting identity: `HEAD` and `tl/ap2-P2-element-eof-review-port-1034` both resolve to `f2fd916061f73d02b1c6c9803350af880b7bf2e5`.

Working target blob: `836d144bc0e3bbd8f1677d23e96385bcd8127daa`.

Evidence:

- `git diff --check f2fd916061f73d02b1c6c9803350af880b7bf2e5 --` passed.
- Base-to-working diff is one file, one insertion and one deletion, only the `historicalrebased` → `rebased` token.
- Scoped ESLint passed.
- Playwright `--list` passed and listed exactly the three P2 tests; no browser/test body was run.
- No typecheck, HTTP/body/service, build, or full suite was run per the bounded brief.

No blocker. The harness can perform the required commit and next independent review.
