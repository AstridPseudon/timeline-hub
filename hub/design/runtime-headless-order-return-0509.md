## Report

- Updated only [tests/test_timeline_headless_overwrite_refused.py](/home/user/work/wt/rt-R5-headless-order-return-0509/tests/test_timeline_headless_overwrite_refused.py:335), changing expected allocation order to `track`, `asset`, `clip`.
- Agent archive verified: commit `9cd3dbe…`, tree `57f0231d…`; module origins resolved from `/tmp/r5-agent-archive.2UR77r`.
- Exact family result: **FAIL — 12 passed, 1 failed, 3.52s**. Failure is the retained retry’s `idempotency_mismatch` because it omits `declare_track=True`. No retry or additional fix made.
- Static checks: compile/AST 84 asserts and topology PASS; Ruff PASS; Pyright 0 errors; one-hunk diff and `git diff --check` PASS.
- No product/source changes, deletions, full suites, HTTP/browser runs, or provider workarounds.
- Commit message written: `test(runtime): fix R5 headless exact allocation expectation`
- `DONE` marker created.