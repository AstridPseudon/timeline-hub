# Validation

- `PYTHONPYCACHEPREFIX=/tmp/w-agt-F-D134-preflight5-2032/pycache python3 -m py_compile tests/editing_conformance/test_native_sheet_ordinary_runtime.py tests/editing_conformance/test_occurrence_fork_source_baseline.py` — passed.
- `/home/user/work/venv-agent/bin/python -m ruff check tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_native_sheet_ordinary_runtime.py` — passed.
- `/home/user/work/venv-agent/bin/python -m mypy --config-file pyproject.toml tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_native_sheet_ordinary_runtime.py` — passed.
- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m 'not integration' tests/editing_conformance/test_occurrence_fork_source_baseline.py` — 16 passed, 1 integration deselected.
- `git diff --check` — passed.

The two central targeted requests selected the default lane and the
`integration:agent` lane respectively, but both lanes deselected all five
integration nodes and exited 5; no live-runtime node executed.
