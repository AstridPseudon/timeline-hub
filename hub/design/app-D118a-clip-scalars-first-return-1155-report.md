# D118a report

- Moved genuine provider registration before project/timeline bootstrap.
- Restored `request(calls)` byte-for-byte, removing only added metadata.
- Changed only [test_commit_runtime_clip_scalar_fields.py](/home/user/work/wt/app-D118a-clip-scalars-first-return-1155/tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py).

Checks passed:

- Ruff
- mypy `--follow-imports=skip`
- `py_compile`
- `git diff --check`
- Assertion AST and request-wrapper conservation

Runtime receipt: `42aad0e9...`, tree `085a5be7...`, clean.

Exact retained nodes: `3 failed in 14.26s`. All passed bootstrap and reached Runtime authorization, then failed at `timeline_commit_auth.py:2267` with `provider intermediate image lacks an authenticated physical promotion`. No full-case GREEN claim; remaining defect is outside this assigned file.

Evidence, commit message, and `DONE` marker are present.