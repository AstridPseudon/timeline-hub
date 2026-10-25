# Commands and results

- `/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_recorded_graph_roots.py` — PASS.
- `MYPY_CACHE_DIR=/tmp/w-b167ce7fde/app-D132a-created-claim/mypy-cache /home/user/work/venv-agent/bin/mypy --cache-dir /tmp/w-b167ce7fde/app-D132a-created-claim/mypy-cache tests/editing_conformance/test_recorded_graph_roots.py tests/sdk/test_timeline_commit_graph_roots.py` — PASS, no issues in 2 source files.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/w-b167ce7fde/app-D132a-created-claim/pycache /usr/bin/python3.11 -m py_compile tests/editing_conformance/test_recorded_graph_roots.py tests/sdk/test_timeline_commit_graph_roots.py tests/sdk/test_timeline_semantic_reservations.py tests/sdk/test_timeline_created_root_stage_redo.py` — PASS.
- `git diff --check` — PASS.
- `PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-5e9ad1c6 ... pytest ... tests/editing_conformance/test_recorded_graph_roots.py` — PASS, 47 passed in 4.55s.
- Authorized nine-node protected proof against Runtime `5e9ad1c6`/tree `de2954a`: 8 passed, 1 failed in 14.36s. The original missing-created-claim refusal is cleared. The remaining child-staging node reaches a later Runtime refusal: `provider occurrence alias is outside its boundary`.

No full, family, browser, native, recovery, SWAP, collector, profile, or unrelated case suite was run.
