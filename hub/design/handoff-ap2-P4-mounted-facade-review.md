# P4 independent review — FAIL

Reviewed candidate `d143e3029afc176f91159c79eaf720b5ffb1f0d5`.

The candidate changes unauthorized repository paths `harnessreport.md` and `design/handoff-ap2-P4-mounted-facade-cases.md`; the original brief allowlist permits only `tests/sdk/test_p4_commit_v2.py`. Its author report also names base SHA `131561e2...` rather than candidate SHA `d143e302...`.

The new tests provide bounded, passing public-Python/provider-seam evidence. The parent-only fixture construction is valid and minimal, but uses `clip-a.at == 1`, so it does not assert the original P4 `0 -> 5` case. The ten-note test hand-builds `doc.patch` commands through ten `tl.command()` calls and therefore bypasses G3 emission. The existing `Generated` transport invokes the real command executor/compiler, with no persisted `sys.modules` stub, alternate executor, or schema override, but it is a fake transport and does not validate v2 schemas or authoritative reply/history data.

Unverified: full v2 request/reply DTOs, merged/conflict/invalid/preview/idempotency behavior, authoritative receipt/attribution/history, show, guarded undo, ten-note conflict/rerun, CLI, sheet, and Runtime HTTP/coordinator acceptance. Do not promote this to real Runtime/provider/service/HTTP, CLI, sheet, undo/history/conflict/rerun, or full P4/H3 qualification.

Checks: the required pytest command passed 4 tests with one pre-existing unknown-`timeout` warning; Ruff passed; mypy passed; `git diff --check` passed.

**Verdict: FAIL.** Smallest first-return correction: remove the two unauthorized repository report files and keep the report external; then narrow or extend the test claims so ten-note G3 coverage and the original `0 -> 5` fixture are actually covered.
