# D118a captured redo1 facts

- Exact retained node baseline: failed at `runtime_protocol/timeline_commit_store.py:251` with `AttributeError` because the synthetic store lacked the supported `db_path` field. Baseline failure SHA: `333037e7106e70fc1317c19f1baa44ad26fa5139226ccac18c3274e83166d49d`.
- Minimal permitted correction: use `tmp_path / 'realm.sqlite3'` for the SQLite connection and expose the same path as `store.db_path`. Captured SQL, CAS source bytes, request, IDs, authored inputs, assertions, no-write check, and negative tests were untouched.
- Candidate exact node: `1 passed in 1.98s` on Runtime `42aad0e92f6da8ea83dd0a382a87e3acd12651b0` with the genuine Agent provider.
- Conservation: only `tests/editing_conformance/test_captured_redo_media_closure.py` changed; seven assertion ASTs and six authored-input assignment ASTs remain equal to HEAD; fixture SHA remains `a20636115ffb6e986ad7731d57bc90dd7ed98a2330b65d3dc71b83a3707ddb37`; Agent and qualified Runtime production source hashes are unchanged.
- Static checks passed: Ruff, `mypy --follow-imports=skip`, temporary-cache `py_compile`, and `git diff --check`.
- Frozen R4 candidate SDK did not contain the retained test, so no upstream exact behavior was available for adaptation.
