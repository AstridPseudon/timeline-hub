# Validation

Source-only checks were run against the candidate ref’s extracted files in the private task TMPDIR.

- Python 3.11 AST parse and `compile`: PASS for both assigned files.
- Python 3.11 `py_compile` with a private `PYTHONPYCACHEPREFIX`: PASS for both assigned files.
- `/home/user/work/venv-agent/bin/ruff check --no-cache --stdin-filename tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py`: PASS.
- Scoped mypy using `/home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --no-incremental --cache-dir=<private> --follow-imports=skip --ignore-missing-imports <candidate manifest>`: PASS, no issues.
- Parent Ruff check: pre-existing `F811` at line 226 for duplicate unused `RemoteTimelines`; parent blob is unchanged.
- `git diff --check tl/integration tl/agt-F-D134-parent24-manifest2-2016`: PASS.
- AST conservation: manifest assertions `23 -> 23`, bytewise equal; parent blob equal.
- Branch scope: one changed path, candidate parent exactly current base.

Behavioral tests were not rerun. The brief explicitly identifies the unchanged shared managed-edge boundary and forbids a redundant own rerun/shared-writer change. The author-reported exact targeted results remain the only behavioral evidence: parent `1 passed, 24 errors` including the unchanged legacy writer checker; manifest `2 errors`; no behavior closure.

No full, family, core, P1–P5, browser, render, collector, Store, child, or D130 suite was run.
