## Done

- Updated only `tests/editing_conformance/test_native_sheet_current_runtime.py`.
- Corrected both remaining `role_media` consumers to read `['selection']['object_id']`.
- Preserved all 248 Assert AST nodes and 10 tests.

Checks passed:

- Ruff
- Mypy
- Py compile
- `git diff --check`
- AST conservation

No functional/service tests run. The known `CommitConflict` and `AssertionError` remain open and unchanged. Commit message and `DONE` marker created; independent protected review remains the next step.