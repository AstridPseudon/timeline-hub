# Validation

- `PYTHONPYCACHEPREFIX=<private /tmp dir> python3 -m py_compile tests/sdk/test_timeline_selected_schema_runtime.py`: PASS.
- `/home/user/work/venv-agent/bin/python -m ruff check tests/sdk/test_timeline_selected_schema_runtime.py`: PASS (`All checks passed!`).
- `/home/user/work/venv-agent/bin/python -m mypy --cache-dir=<private /tmp dir> --config-file pyproject.toml tests/sdk/test_timeline_selected_schema_runtime.py`: known baseline failure only, missing `types-PyYAML` stubs for `yaml`; no source type error reported.
- `git diff --check a30e74e901a28b39c28facba3deb00d76f186e23..HEAD`: PASS.
- `git diff --name-status a30e74e901a28b39c28facba3deb00d76f186e23..HEAD`: only the assigned test file.
- No pytest/body run: source verdict failed, and the task explicitly requires no body after source failure. The author's three direct v2 passes are not credited because the request bodies were changed.
- HTTP lost-ACK node: unverified after central precollection failure; no hidden retry, fixture workaround, or competing heavy run.
