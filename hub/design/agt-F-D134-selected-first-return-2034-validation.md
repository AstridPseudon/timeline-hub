# Validation

- `PYTHONPYCACHEPREFIX=/tmp/d134-pycache-2034 python3.11 -m py_compile tests/sdk/test_timeline_selected_schema_runtime.py`: PASS.
- `/home/user/work/venv-agent/bin/python -m ruff check tests/sdk/test_timeline_selected_schema_runtime.py`: PASS.
- `/home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/d134-mypy-2034 --config-file pyproject.toml tests/sdk/test_timeline_selected_schema_runtime.py`: known baseline failure only: missing `types-PyYAML` stubs for `yaml`.
- `git diff --check a30e74e901a28b39c28facba3deb00d76f186e23 -- tests/sdk/test_timeline_selected_schema_runtime.py`: PASS.
- `git diff --name-status a30e74e901a28b39c28facba3deb00d76f186e23 -- tests/sdk/test_timeline_selected_schema_runtime.py`: only the assigned test file.
- Source conservation AST/hash check: PASS; all seven UNKNOWN cases unchanged.
- Three local ABI-1 nodes: FAIL against current Runtime because each returned `data.status == "merged"` while the preserved C0-compatible assertion is `"rebased"`.
- Central HTTP node request: not run; targeted service deselected it as `run by CI job lanes-integration` (exit 5, one deselected). No retry was submitted.
