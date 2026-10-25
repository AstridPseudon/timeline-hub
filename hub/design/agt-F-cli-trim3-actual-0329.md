## Report

- Updated only [test_cli_trim_runtime.py](/home/user/work/wt/agt-F-cli-trim3-actual-0329/tests/editing_conformance/test_cli_trim_runtime.py).
- Preserved original timing, opaque metadata, and CLI assertions by applying `app.astrid.for = 2.5` through supported guarded `doc.patch` after media creation.
- No production or Runtime changes.

Checks passed:

- Ruff current and parent baseline.
- Mypy current and parent baseline: no issues.
- In-memory compilation and AST conservation checks.
- `git diff --check`.

Pytest/service execution was intentionally not run per the source-only brief. Runtime behavior remains for protected review and MAIN3 verification. Commit message and `DONE` marker created.