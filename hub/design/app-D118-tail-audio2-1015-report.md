Implemented D118 compile audio2 in `tests/editing_conformance/test_compile_contracts.py`.

- Preserved both audio vectors and all assertions.
- Cleans strict probe-rejected environment overrides via pytest `monkeypatch`.
- Current/original070dfc/retained source hash before edit: `519a2aa5…37b4a`.
- Static checks passed: Ruff, mypy, py_compile, diff check, AST assertion conservation.
- Targeted selectors remain unverified: sandbox denied localhost socket creation (`PermissionError`). Agent core service should rerun both exact fade selectors.
- Commit message and `DONE` marker created.