Implemented test-only D40 migration.

- Added Runtime f320 owner-custody helper: Git-backed temp checkout, exact owner grant, `OwnerSourceCapture`, `TrustedLocalHostLaunchVerifier` one-use claim, non-serializable handle, retained preparation binding, cleanup.
- Updated only the target test setup; pack/manifests/module bytes, constructor/admit/invoke arguments, and three assertions remain unchanged.
- Assertion hashes:
  - `result.ok`: `b4f3b4e0c25822f1496ae2376a46fa3e09465457352d99ab44f5c5d30c2a2492`
  - `result.returncode == 0`: `edbec4f2e72bcfa33bd21ab2529219e617758a78f344e31b3363e7c5a5cb04b7`
  - imported path assertion: `a48a5e83de765d65ead63b3541f64c84681dad7bb26a7b1ef43136da7432a5d2`

Checks passed:

- Helper authority/admission control with Runtime `f3208b26b53c4d7053e5464eaa7c5e15b1505812`: PASS
- `ruff check tests/helpers/external_orchestrator_owner.py`: PASS
- `py_compile`: PASS
- `git diff --check`: PASS

The original positive test body was intentionally not executed in this preparation worker. Central command:

```bash
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-f3208b26 PYTHONPATH=.:/home/user/work/wt/rt-pin-f3208b26 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/stage1/test_zero_shim_execution_pack_deletion.py::test_generic_host_runs_external_python_orchestrator_from_admitted_pack
```

Commit message and `DONE` marker are written.