# D103 source-only validation

Candidate source: `tests/editing_conformance/test_cli_trim_runtime.py`.

- In-memory `ast.parse` and `compile` candidate: PASS.
- In-memory `ast.parse` and `compile` parent (`tl/integration`): PASS.
- Candidate `/home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_cli_trim_runtime.py`: PASS.
- Parent Ruff through stdin with the same filename: PASS.
- Candidate `/home/user/work/venv-agent/bin/python -m mypy tests/editing_conformance/test_cli_trim_runtime.py`: PASS, no issues.
- Parent Mypy on the extracted parent source: PASS, no issues.
- `git diff --check`: PASS.
- Static AST inventory: the two test function names are identical; assertion count
  is 38 in both parent and candidate; the `relevant_peer` parameter values and
  ids are identical.
- Changed paths: exactly the authorized test file.

Per the worker brief, no pytest collection, test/helper/fixture execution,
media probe, ffmpeg, service, browser, render, build, or package installation
was run.
