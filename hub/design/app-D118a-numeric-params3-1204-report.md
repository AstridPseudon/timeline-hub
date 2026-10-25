## Report

No source changes were made; the assigned test remains byte/AST-identical to base.

Exact pinned run:

```bash
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-42aad0e9 \
PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-42aad0e9 \
/home/user/work/venv-agent/bin/python -m pytest -q -m integration [three exact nodes]
```

Result: `3 failed in 13.30s`.

All failures occur during redo inverse in Runtime:

- `runtime_protocol/service.py:2524`
- `runtime_protocol/timeline_commit_auth.py:1755`
- `inverse stage native writes do not cover its authenticated effect image`

Accepted save, reload, and first inverse assertions pass. This is an out-of-scope Runtime validation/custody defect; no faithful test-only correction was proven.

Checks passed:

- Ruff
- Mypy `--follow-imports=skip`
- `py_compile`
- `git diff --check`
- Byte/AST conservation
- Assigned file absent at pristine `08e6b905`

Runtime receipt verified clean: `42aad0e9…`, tree `085a5be7…`.

Evidence is in the worker evidence directory. `BLOCKED` and commit message were written. Recommended next step: Runtime owner repair the inverse-stage authentication boundary, then rerun these exact three nodes.