# Validation

No live pytest or central suite was run, per the D134 live-boundary rule and the
published route's exact-missing-input refusal.

- `PYTHONPYCACHEPREFIX=/tmp/w-76397cd4aa/d134-source/pycache python3.11 -m py_compile tests/editing_conformance/test_fork_abi1_binding_set.py tests/editing_conformance/test_recipe_occurrence_fork.py` — PASS.
- `python3.11` in-memory AST parse plus `compile()` for both assigned files — PASS (1624 and 1547 AST nodes).
- `/home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_fork_abi1_binding_set.py tests/editing_conformance/test_recipe_occurrence_fork.py` — PASS (`All checks passed!`).
- `make PY=/home/user/work/venv-agent/bin/python mypy` — BLOCKED by the existing environment baseline: 14 errors in unrelated files, chiefly missing `yaml` stubs and the installed NumPy stub requiring Python 3.12; no assigned-file error was reported before checking stopped.
- `git diff --check` — PASS (clean).
- `git status --short` — target files unchanged; no worktree product diff was produced.

The exact source and review hashes are in `source-manifest.json`. The mypy
failure was not repaired by installing into the shared read-only environment.
