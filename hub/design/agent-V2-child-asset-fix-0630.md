# Agent V2 D12a child-asset fix

Status: **PASS**, with two environmental/policy notes recorded in the worker
report. The production seam in `astrid/core/timeline/authoring_bundle.py`
now preserves an unchanged legacy missing child selector only when the real
provider bundle carries `_runtime_document`; modified/new/invalidated media
declarations remain strict. Real-provider regression coverage is in
`tests/editing_conformance/test_commit_boundaries_d12.py`.

Evidence: targeted suite **83 passed**; scoped Ruff and private mypy **PASS**;
venv-backed `make ruff` **2149/2149**; vendor lock, artifact manifest, and
`git diff --check` **PASS**. Plain `make ruff` is unavailable because system
Python lacks Ruff. Mypy baseline comparator reports 1912 current vs locked
1914 and requests a baseline rewrite; no baseline was changed. Full suites
were not run.
