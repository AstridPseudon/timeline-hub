Implemented the exact D118 sheet15 caller correction in [test_native_sheet_current_runtime.py](/home/user/work/wt/app-D118-sheet15-verified-caller-return-1050/tests/editing_conformance/test_native_sheet_current_runtime.py):

- Changed two `verified['object_id']` reads to `verified['selection']['object_id']`.
- Preserved all fixture values, IDs, guards, predicates, and 248 AST assertions.
- Runtime shape and production Agent caller confirm the nested field.

Checks passed:

- Ruff
- Mypy
- Py_compile
- `git diff --check`
- AST conservation: 248 assertions identical

No functional/service suite was run; the two other retained failures remain open. The independent reviewer captured matching source checks but terminated before emitting a formal verdict. Remote merge request was not issued because its required path is outside this sandbox; manager action remains needed.