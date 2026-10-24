Implemented F-WC6 fixture/helper correction.

Changes:
- Bound `coordinator.saved` to the active lookup frame’s coordinator local, preserving exception type/object ID, ordering, privacy, and call behavior.
- Updated source attachment blob expectation:
  - Before: `e55be12f...`
  - After: `62c30a6d...`
  - AST assertion count remains 59.

Tests/checks:

- Targeted pytest: `13 passed`
- Ruff: passed
- Mypy: passed
- Compileall: passed
- `git diff --check`: passed
- No full suite or upstream source-body run.

Only assigned files changed:

- [wc6_completion_capture.py](/home/user/work/wt/agt-F-wc6-return-2323/tests/helpers/wc6_completion_capture.py)
- [test_wc6_completion_capture.py](/home/user/work/wt/agt-F-wc6-return-2323/tests/sdk/test_wc6_completion_capture.py)

Commit message recorded; `DONE` created. Independent protected review and merge remain for the orchestrator.