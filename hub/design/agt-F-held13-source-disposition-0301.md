# F-D86 report

Completed readonly disposition for all 13 canonical held selectors on base `562ee30b6e` / tree `b4a181a9`.

- Eligible for next MAIN body: **0**
- Failure seam unchanged / owner needed: **10** — IDs 1–10
- Retired D87 CLI surface: **3** — IDs 11–13
- D87 mapping used: exact entries **1, 2, 7, 8, 24**, with current replacement tests recorded.

The shared word fixture correction is applicable to the nine word rows’ setup path, but restores the same final rational-FPS/source closure; none of the nine first failing calls changes. No unchanged retry is authorized.

Evidence:

- [Disposition JSON](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-held13-source-disposition-0301/evidence/f-d86-disposition.json)
- [Per-selector TSV](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-held13-source-disposition-0301/evidence/f-d86-selectors.tsv)

Author brief for IDs 11–13:

> Update only `tests/editing_conformance/test_native_sheet_current_runtime.py` so the two semantic-batch CLI parameters use the current ordinary `commit --file`/`NativeSheet.apply` route and the lost-ack parameter uses the current persisted outbox retry plus `TimelineSession.undo`, preserving every original assertion and refusal predicate. Allowed file: `tests/editing_conformance/test_native_sheet_current_runtime.py`; predicate map: `[cli]` and `[sheet-cli]` retain one commit, reload, inverse, redo, and exact pin/base assertions via current commit routes, while `test_http_sheet_lost_ack_restart_exact_retry_original_guards_and_aba` retains exact request/key replay, immutable changed-key refusal, draft preservation, ABA/intervening-write refusal, and no-recapture.

Verification:

- Static JSON/TSV exact-set validation: **PASS**
- AST parsing of 8 scoped source files: **PASS**
- `git diff --check`: **PASS**
- Repository worktree: **clean**
- No pytest, collection, helper/fixture execution, service, build, browser, render, or probe run.

C0 sections 1–5 retained unchanged; hash recorded in evidence. Commit message and `DONE` marker created.