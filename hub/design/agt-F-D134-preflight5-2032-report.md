## Report

- Updated only [test_occurrence_fork_source_baseline.py](/home/user/work/wt/agt-F-D134-preflight5-2032/tests/editing_conformance/test_occurrence_fork_source_baseline.py).
- Restored genuine Runtime daemon/provider plumbing and a real `AstridClient` for the fork fixture.
- Left ordinary-sheet fixture unchanged: exact UNAPPLIED dependency remains because its raw ingest lacks the verified catalog selection and mirrored shot item required by supported occurrence-media plumbing.

Validation:

- `py_compile` — passed
- Ruff — passed
- mypy — passed
- Pure tests — 16 passed, 1 integration deselected
- `git diff --check` — passed
- Central integration targeted lanes deselected all five nodes; live integration remains unverified.

Commit message and evidence files were written. `BLOCKED` marker created with the dependency explanation.