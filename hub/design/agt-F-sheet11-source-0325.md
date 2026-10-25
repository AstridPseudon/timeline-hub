Implemented the one-line F-D86 fix in [test_native_sheet_ordinary_runtime.py](/home/user/work/wt/agt-F-sheet11-source-0325/tests/editing_conformance/test_native_sheet_ordinary_runtime.py:274): `test-bootstrap` → `python`.

Verification:

- AST/input/predicate conservation: passed.
- Ruff baseline/candidate: passed.
- Mypy baseline/candidate: passed.
- `git diff --check`: passed.
- Exact `ordinarysheet11` membership: 11 IDs confirmed.
- No pytest or fixture execution, per source-only requirements.

Commit message written and `DONE` created. Protected review and MAIN11 behavioral proof remain external follow-ups.