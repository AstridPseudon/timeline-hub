## Done

Updated only:

- `tests/sdk/test_wc6_completion_capture.py`
- `tests/helpers/run_wc6_completion_capture.py`

Changes align the current cleanup protocol, wrapper/source guards, offline caller seam, and reviewed helper digest. Original `not_ready` behavior is restored; no Runtime product code changed.

## Tests

- Targeted pytest: `15 passed`
- Ruff: passed
- Mypy: passed
- Py_compile: passed
- `git diff --check`: passed
- AST/source/hash conservation: passed
- Original protected function retains 59 assertions.
- No full/service/browser/P4 runs performed.

## Decisions / blockers

- Added genuine `clear_replay_memo` and `history_read_scope` test-double behavior.
- Added the current `revision_closure` offline seam, preserving the existing primary exception and no-write behavior.
- Helper digest updated from reviewed normal receipt `f17c…`.
- Independent protected review is still required before merge; source-only tests do not establish functional GREEN.

Commit message and empty `DONE` marker recorded.