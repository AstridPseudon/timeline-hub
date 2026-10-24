PASS_SOURCE

Changed only [test_native_sheet_current_runtime.py](/home/user/work/wt/agt-F-current-sheet-2344/tests/editing_conformance/test_native_sheet_current_runtime.py).

- Replaced synthetic trusted setup with authenticated Runtime v2 semantic/authoring commits.
- Preserved all 17 requested selectors; AST conservation passed.
- Compile, scoped Ruff, scoped mypy, and `git diff --check` passed.
- Ruff baseline: `2143 == 2143`.
- Full mypy baseline comparison blocked by missing PyYAML stubs and NumPy/Python-version incompatibility.
- No pytest, service, body, build, or browser runs performed.

Hashes: file `8d979fff…917ca`; diff `e95a4a06…c9df`; base `efa0504f…1d81e`.

Commit message and `DONE` marker created. Proposed log entry: `F-D85 | PASS_SOURCE | NativeSheet setup migrated to Runtime v2; 17 selectors AST-conserved`.