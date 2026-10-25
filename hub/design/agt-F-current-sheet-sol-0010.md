F-D85 fixture correction is ready for independent protected review.

Changed only [test_native_sheet_current_runtime.py](/home/user/work/wt/agt-F-current-sheet-sol-0010/tests/editing_conformance/test_native_sheet_current_runtime.py:376): both emitter inputs retain the exact Runtime parent and occurrence edges; the candidate overlays only authored fields. Shared shot, audio/text bindings, and pins remain intact.

Verification:

- All 10 original test ASTs conserved, including assertions, raises, decorators, parameters, and branches.
- All [17 requested selectors](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-current-sheet-sol-0010/evidence/selectors.txt), plus two additional original cases, retained.
- In-memory compile, scoped Ruff/mypy on original/return/candidate, and `git diff --check`: PASS. [Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-current-sheet-sol-0010/evidence/static-checks.json).
- No pytest, service, build, render, or product/test-body execution.

Candidate file SHA256: `6e8b187f8a3bcef57056462974002e7bf27f9d5c04d98e278cbbbfee9c632d8d`. [Exact baseline, return, blob, AST, and diff hashes](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-current-sheet-sol-0010/evidence/hashes.json).

Source discrepancy: review 0005’s claimed rejection was not established by the source: detached parents already omit occurrences, and `_outside` excludes the parent. The correction explicitly preserves physical edges on both inputs; details are in [source notes](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-current-sheet-sol-0010/evidence/source-notes.txt).

Proposed existing log entry:

`F-D85 | PASS_SOURCE (author checks; independent review pending) | current-sheet17 destination preserves Runtime occurrence edges and shared source; functional qualification pending`

Commit message and `DONE` written. Next: independent review before merge, then the single authorized MAIN qualification batch. Runtime behavior remains unverified.