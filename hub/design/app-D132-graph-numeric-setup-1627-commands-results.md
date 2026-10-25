# D132 commands and results

- `git diff --check` — PASS.
- `ruff check tests/editing_conformance/test_recorded_graph_roots.py` — PASS (`All checks passed!`).
- `MYPY_CACHE_DIR=/tmp/w-3202c4f371/app-D132-graph-numeric-setup-1627/mypy-cache /home/user/work/venv-agent/bin/mypy --cache-dir /tmp/w-3202c4f371/app-D132-graph-numeric-setup-1627/mypy-cache tests/editing_conformance/test_recorded_graph_roots.py` — PASS (`Success: no issues found in 1 source file`).
- `PYTHONPYCACHEPREFIX=/tmp/w-3202c4f371/app-D132-graph-numeric-setup-1627/pycache /usr/bin/python3.11 -m py_compile tests/editing_conformance/test_recorded_graph_roots.py` — PASS.
- AST/source/history census — PASS: exact one-field migration; all non-gain inputs equal; fixture assertion AST unchanged; graph consumer remains 11 tests/33 assertions/7 parametrizations with identical AST/assertion hashes.
- `git diff --stat 20177e66564f9f91735ed1a11bac821682d60edf -- tests/editing_conformance/test_recorded_graph_roots.py tests/sdk/test_timeline_commit_graph_roots.py` — PASS: 2 files, 7 insertions, 1 deletion.

Per task scope, no pytest, Runtime/socket, browser, native/full/family, or own9
suite was run. Own9 remains for the independent protected reviewer after this
SOURCE PASS.
