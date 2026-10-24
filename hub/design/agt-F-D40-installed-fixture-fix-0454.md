## Report

Implemented test-only D40 fixture support in `tests/helpers/external_orchestrator_owner.py`.

- Loads exact f320 Runtime fixtures from the authenticated child source snapshot.
- Verifies fixture hashes, direct URL metadata, f320 source marker, and installed production origins before/after setup.
- Uses only `tests.__path__`; no Runtime production source overlay.
- Original stage1 test remains untouched.

Tests:

```text
Installed isolated:
1 passed in 3.24s

Source mode:
1 passed in 3.93s

Ruff: passed
py_compile: passed
git diff --check: passed
```

The default pytest import mode fails closed before authority setup because it resolves Agent production modules from the worktree; the supported installed command uses `--import-mode=importlib`.

Actual fixture origin: child retained Runtime snapshot `/.../.child-venv-source-venv-agent-child-d40-ba8f-f320/runtime/tests`.

Commit message written and `DONE` marker created.