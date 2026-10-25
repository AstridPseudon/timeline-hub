# D118d commands and results

- `PYTHONPYCACHEPREFIX=$TMPDIR/pycache /home/user/work/venv-agent/bin/python -m py_compile tests/sdk/test_timeline_capture_projection.py` — PASS.
- `/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_capture_projection.py` — PASS (`All checks passed!`).
- `/home/user/work/venv-agent/bin/mypy --cache-dir $TMPDIR/mypy --follow-imports=skip tests/sdk/test_timeline_capture_projection.py` — PASS (`Success: no issues found in 1 source file`).
- `git diff --check` — PASS.
- AST conservation script — PASS: non-fixture functions equal, original saved-closure tail equal, original assertions preserved, parameters/decorators preserved.
- Own retained-node command — NOTRUN: free space was `4821417984` bytes, below the required `5000000000`-byte floor. No `own-nodes.xml` or `own-nodes.log` was created because the run was not permitted.
