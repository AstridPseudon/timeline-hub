# Commands and results

- Pure pre-edit census: `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python` with an in-memory frozen-schema registry loaded from Runtime commit `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, constructing `bundle_from_document(document_fixture())`, `commands.execute(bundle, [create_command()])`, and `document_from_bundle(plan.bundle)`. PASS: complete prepared candidate, 2 roots, 2 writes, exactly 1 error at `$.canonical_document.shot_revisions[1].payload.metadata` (`NoneType` versus object).
- Pure post-edit census: same construction and immutable schema registry. PASS: complete prepared candidate, 2 roots, 2 writes, zero schema errors.
- `ruff check tests/editing_conformance/test_recorded_graph_roots.py tests/sdk/test_timeline_commit_graph_roots.py` — PASS (`All checks passed!`).
- `MYPY_CACHE_DIR=/tmp/w-e65e9e8325/app-D132a-graph-schema-enumerate-1653/mypy-cache /home/user/work/venv-agent/bin/mypy --cache-dir /tmp/w-e65e9e8325/app-D132a-graph-schema-enumerate-1653/mypy-cache --follow-imports=skip tests/editing_conformance/test_recorded_graph_roots.py tests/sdk/test_timeline_commit_graph_roots.py` — PASS (`Success: no issues found in 2 source files`).
- `PYTHONPYCACHEPREFIX=/tmp/w-e65e9e8325/app-D132a-graph-schema-enumerate-1653/pycache /usr/bin/python3.11 -m py_compile tests/editing_conformance/test_recorded_graph_roots.py tests/sdk/test_timeline_commit_graph_roots.py` — PASS.
- `git diff --check` — PASS.
- AST/predicate census — PASS: fixture 22 test bodies/90 assertions/6 parametrizations; graph consumer 11/33/7; shared consumers checked; changed-slot predicates absent; only one authored slot changed.
- JSON evidence parse check over `evidence/*.json` — PASS.

Per task scope, no pytest, Runtime/provider, own9, full/family/P2/P4/browser/native/service suite, ZIP, build, or packaging command was run.
