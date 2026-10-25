# D118c occurrence-create2 facts

- Changed only `tests/editing_conformance/test_commit_runtime_occurrence_create.py`.
- The edit is confined to the local `body()` request wrapper. It aligns the retained fixture with the supported current caller by supplying the C0 envelope metadata: label, one ordered semantic step with empty submitted patch and reads, `merge: fields`, request reads, `dry_run: false`, Python source, rationale, and group ID.
- No semantic command, physical/opaque value, timing, authored ID, media input, assertion, history check, inverse/redo/retry check, or no-write check changed.
- Before source SHA-256: `26ecb3e8da202dc9a1113f942cf9c1a7384600d8662cb9c1e8d983caf17afe6f`.
- After source SHA-256: `91b0d3e7f5815892e58cb0256640a08173fe3e7703cff0a4caa480d0e9bcf855`.
- AST assertion count stayed 29; assertion AST and test-function AST were conserved.

Static checks passed:

- `/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_commit_runtime_occurrence_create.py`
- `/home/user/work/venv-agent/bin/mypy --follow-imports=skip tests/editing_conformance/test_commit_runtime_occurrence_create.py`
- `PYTHONPYCACHEPREFIX=$TMPDIR/pycache python -m py_compile tests/editing_conformance/test_commit_runtime_occurrence_create.py`
- `git diff --check`
- Parent source through Ruff stdin also passed.

Behavioral/service/full/browser tests were not run, as required. This is a source-only caller alignment and does not claim functional closure of the retained RED nodes.
