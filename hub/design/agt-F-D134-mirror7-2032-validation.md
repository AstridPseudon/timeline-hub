# Validation

- `git diff --check` — passed.
- Python 3.11 AST parse and `py_compile` for both changed files with a private `PYTHONPYCACHEPREFIX` — passed.
- `ruff check tests/editing_conformance/test_native_word_anchor.py tests/editing_conformance/test_word_binding_recipe.py --output-format concise` — passed.
- `make PY=/home/user/work/venv-agent/bin/python mypy` — blocked by the existing environment baseline: 13 missing `types-PyYAML` stubs plus NumPy stubs using Python 3.12 `type` syntax; no changed-file error was reported before checking stopped.

The generic central `targeted` suite omitted `-m integration` and deselected all tests. The available named integration suites had stale or missing Runtime path configuration. Final node validation used the qualified local integration environment with `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime` and the normal Runtime service provider.
