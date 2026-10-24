Implemented F-D85 in [test_native_sheet_ordinary_runtime.py](/home/user/work/wt/agt-F-sheet-return-2344/tests/editing_conformance/test_native_sheet_ordinary_runtime.py):

- Sequentially capture/apply each `track.create`.
- Correct internal registry `before` state to `ABSENT`.
- Preserved all test bodies, assertions, parameters, and decorators.

Checks:

- In-memory compile: PASS.
- AST conservation: PASS; normalized hash unchanged: `6f89d1b3…d9fa7`.
- Ruff: PASS, `2143 == 2143`.
- Mypy: PASS, `1902 == 1902`; no YAML/NumPy diagnostics.
- `git diff --check`: PASS.
- No pytest, service, build, or production execution performed.

Candidate file SHA-256: `4532a5d9…a8962b`.

Remaining seam: shared native-batch `commands-file` coverage remains outside this task.

Commit message written and `DONE` marker created.