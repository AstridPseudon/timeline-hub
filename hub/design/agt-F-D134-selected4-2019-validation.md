# Validation

- `python3` AST parse of `tests/sdk/test_timeline_selected_schema_runtime.py`: PASS.
- `python3 -m py_compile -q tests/sdk/test_timeline_selected_schema_runtime.py`: PASS.
- `/home/user/work/venv-agent/bin/python -m ruff check tests/sdk/test_timeline_selected_schema_runtime.py`: PASS (`All checks passed!`).
- `/home/user/work/venv-agent/bin/python -m mypy --config-file pyproject.toml tests/sdk/test_timeline_selected_schema_runtime.py`: baseline-only failure, missing `yaml` stubs (`types-PyYAML`); no source type errors reported.
- `git diff --check`: PASS.
- `pytest --collect-only` for the three v2 nodeids: 3 collected.
- Direct targeted integration command with the shared Runtime checkout, selecting the exact three v2 nodeids: `3 passed in 5.12s`.
- Central HTTP attempt `agt-F-D134-selected4-2019-targeted-1025202016-9453`: not executed; generic targeted lane deselected the integration-marked node.
- Central HTTP attempt `agt-F-D134-selected4-2019-commit-integration-1025202110-19610`: not executed; suite environment failed collection with `ModuleNotFoundError: runtime_protocol`.
- Central HTTP attempt `agt-F-D134-selected4-2019-document-diff-null-track-http-integration-1025202309-32315`: not executed; suite's pre-existing appended test node was not found, so pytest ran no tests.
