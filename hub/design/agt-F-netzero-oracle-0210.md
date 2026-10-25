## Report

- Corrected only `tests/sdk/test_timeline_commit_provider_add_delete_runtime.py`.
- Net-zero inverse oracle now requires the complete sequential writes:
  - absent → present(full row)
  - present(row) → absent
  - retained `created` restoration fact
- All other parameters, branches, inputs, guards, retry/history predicates, and replace-existing behavior remain unchanged.
- Added predicate map/evidence: `.../workers/agt-F-netzero-oracle-0210/evidence/predicate-map.md`.
- Commit message written; `DONE` marker created.

Checks:

- `py_compile`: passed.
- Scoped Ruff: passed.
- Mypy baseline/candidate: identical pre-existing NumPy Python-version diagnostic; no target difference.
- `git diff --check`: passed.
- No pytest, collection, helper/fixture execution, service, build, browser, render, socket, or probe run.

Functional acceptance remains unverified; replace-existing remains a separate Runtime authentication seam requiring later MAIN/D90 qualification.