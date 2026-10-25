# D118d report

- No repository changes; existing setup fix `7d85895ba` already changes the archive lookup causally and preserves all assertions/inputs.
- AST: all test functions conserved; only reader fixture setup differs.
- Static checks: py_compile, Ruff, mypy, and `git diff --check` passed.
- Own 16-node pytest run: **NOT RUN**; free disk was 4,832,747,520 bytes, below the 5,000,000,000-byte floor.
- Frozen upstream924 tip: `92443771676ef2bbb547d0a103d708fa8bec4c63`; assigned file absent. Requested `d11417a59` unavailable.
- Worktree clean. Evidence and commit message are written at the required absolute paths; `DONE` created.

Recommended next step: run the exact retained nodes once disk is above the required floor.