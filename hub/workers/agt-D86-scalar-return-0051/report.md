Implemented F-D86 scalar first-return fix in [test_commit_runtime_clip_scalar_fields.py](/home/user/work/wt/agt-D86-scalar-return-0051/tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py:36), passing the resolved physical ref to `value_at`.

Checks passed:

- In-memory compile
- Candidate/baseline Ruff
- Candidate/baseline mypy
- AST/API conservation
- `git diff --check`

No pytest, service, browser, build, or full-suite execution was performed. Behavioral acceptance remains unverified.

Commit message and `DONE` marker created.