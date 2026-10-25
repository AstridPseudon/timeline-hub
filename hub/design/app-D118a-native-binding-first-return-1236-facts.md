# D118a first-return evidence

- The overbroad media-pin refusal was removed without restoring stale authority.
- Complete Runtime authority is retained only when the requested text descriptor exactly matches the existing media pin.
- A changed-text rebind emits no `binding_id`, `head`, or `event_stream_id`; the registered Runtime provider remains the authority that derives the new identity.
- Incomplete authority still refuses as `unsupported_shape` before writes.
- Production source contains no `_runtime_document` or `source_mapping`.
- Only the permitted production module and additive authority test changed.

## Exact checks

- `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-42aad0e9 PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-42aad0e9 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -m integration tests/sdk/test_timeline_script.py::test_runtime_pin_flow_returns_old_script_after_binding_rebind` → `1 passed in 1.96s`.
- Parent comparison loaded from `cf7b8d7c2b4cb980de1d873f0498784d5210d508` under the same Runtime checkout → `1 passed in 1.93s`.
- Focused native/script units → `56 passed, 2 deselected in 4.15s`.
- Ruff, mypy `--follow-imports=skip`, `py_compile` with a temporary cache, and `git diff --check` → pass.
- Original relevant source/test hashes and AST counts matched base; changed-path allowlist and privacy/source containment → pass.

The first post-edit integration retry without `ASTRID_RUNTIME_CHECKOUT` errored during dependency setup; it was immediately rerun with the prescribed variable and passed.
