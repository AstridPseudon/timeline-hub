## A — F-D86/D95

Verdict: `PASS_SOURCE` only; no behavior credit.

Reviewed commit `33be39334ddac2ee54091a58ec1f96bcb0249092`, parent `b8a48a9`, blobs `d77d9e1` → `0f83aae`.

- Exact D95 disposition confirmed for legacy IDs 99/101.
- Original body hashes verified against the parent blob.
- All other function ASTs conserved exactly.
- One approved parametrized refusal/no-write test added:
  - `...test_bound_main_descriptor_invalidating_set_and_clear_refuse_without_writes[rebind]`
  - `...test_bound_main_descriptor_invalidating_set_and_clear_refuse_without_writes[clear]`
- Real registered provider, strict refusal predicate, history/head, closure, live-row, original-CAS, and replacement-CAS guards verified statically.

Checks: AST compile PASS; Ruff PASS; mypy on six scoped files PASS; `git diff --check` PASS.

## B — F-D86/R2

Verdict: `FAIL_SOURCE`; no behavior credit.

Reviewed commit `99f2d183`, parent/product commit `72a5e533`, new-file blob `8bf6c08`.

FIRST MAIN selector:

`tests/sdk/test_timeline_restore_effect_order_runtime.py::test_id5_public_undo_of_restore_preserves_authenticated_effect_order`

Static call trace finds the fixture cannot reach restore/undo: fresh `timeline.open()` calls `TimelineSession.open()` → `RemoteTimelines.history()` → `WorkspaceClient.list_timeline_commits()`, but the test transport defines only `generated.commit_timeline`; `generated.list_timeline_commits` is absent. The path therefore returns `not_ready` before the first commit.

The product branch and effect-order claims were otherwise reviewed, but this fixture defect prevents qualification. Historical ID5 old-RED applicability is also only partial because the fixture uses an opaque track rather than the original word-binding fixture.

Checks: AST compile PASS; Ruff PASS; `git diff --check` PASS. Author-reported candidate mypy PASS. No tests, services, fixtures, or full suites were executed.

Evidence written separately under:

- `/tmp/.../evidence/A-F-D86-D95.md`
- `/tmp/.../evidence/B-R2.md`

Worktree remains unchanged. Commit message written and `DONE` created.