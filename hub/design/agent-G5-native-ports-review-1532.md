# G5 independent native CLI port review

**DRAFT; no merge.** Reviewed `3996822a0` against current `58316fd6e` and the
1450 current-base design. Only the four assigned test files are in scope.

## Verdict

- Test-port fidelity: **FAIL** for one concrete substitution. The new
  `test_normal_commit_conflict_keeps_head_and_has_no_force_overwrite` uses
  `Checkout.open` / `open_timeline` / `Checkout.publish` directly at
  `tests/packs/timeline/test_verbs_working_copy.py:524`, not the normal CLI
  caller required for this review. It is a real Runtime fixture and retains
  conflict, no-write/history, and force-refusal assertions, so the author
  should re-express the same checks through the normal CLI.
- Actual scoped behavior: **FAIL, 7 reds**. The author’s final run was 87
  collected, 80 passed, 7 failed. This is not an all-G5-PASS claim.

## Seven reds

1. `test_cli_commit_move.py:162` accepted undo: missing product
   `undo --commit` front door; current `cli.py:3785-3791` only accepts numeric
   steps and `:3529-3531` calls detached `_edit_checkout`. Owner: Product
   Sol/CLI.
2. `test_cli_commit_move.py:195` accepted redo: fixture history/read-pair
   lacks the complete canonical publication pin for reopening the second
   normal edit. The adapter is `:18-41`; the normal session requires the
   exact pair at `sync.py:199-205`. Owner: author first return, repair the
   existing fake history/receipt ancestry without inventing pins.
3. `test_cli_commit_trim.py:56` lost-ack undo: same missing product
   `--commit` front door. Owner: Product Sol/CLI.
4. `test_cli_native_sheet.py:94` export/apply/undo: normal apply and exact
   request assertions pass, then `undo --commit` hits the same parser gap.
   Owner: Product Sol/CLI.
5. `test_cli_native_sheet.py:123` detached duration: normal apply reaches
   `_apply_parsed` at `timeline_sheet.py:884-906`, tripping the retained
   legacy-writer guard at test line 133. Owner: Product Sol/sheet apply.
6. `test_cli_native_sheet.py:250` row omission/delete: delete and sibling
   preservation pass, final `undo --commit` hits the parser gap. Owner:
   Product Sol/CLI.
7. `test_cli_native_sheet.py:306` trim/clear/params: captured batch and
   resulting bundle pass, final `undo --commit` hits the parser gap. Owner:
   Product Sol/CLI.

## Evidence

The author’s unchanged-source bounded result is `80 passed, 7 failed in
42.79s`; no known red was replayed here. This review independently collected
87 tests, ran three representative normal-path tests (`3 passed in 8.81s`),
compileall, scoped Ruff, scoped mypy, and diff-check; all passed. No tests were
weakened, skipped, xfailed, or deleted; no product code changed.

Exact source identities and commands are in the worker report:

[`report.md`](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-native-ports-review-1532/report.md)

Required next step is the same 87-node bounded rerun after author fixture/CLI
fidelity repair and Product Sol’s `--commit` plus detached-duration changes.
