## PASS

- Head: `45cecae7b`; includes ancestor `998492dea`.
- Fixture blob: exact `cfa5dbf0…`; parent blob `9f9622ad…`.
- Merge delta: one JSON symbol replacement only. Original test function and all outside files preserved.
- Tests:

```bash
PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f \
ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-8ea0766f \
PYTHONDONTWRITEBYTECODE=1 \
timeout 30s /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider \
tests/sdk/test_p4_commit_cases.py::test_p4_sources_are_real_and_parseable \
tests/packs/timeline/test_cli_commit_move.py::test_ordinary_edit_literal_move_uses_commit_outbox
```

Result: `2 passed in 2.79s`.

No broad suites, HTTP/P4 journey, browser, benchmark, provisioning, daemon, or shared-environment mutation run. Prior independent Ruff/mypy/producer evidence was reused unchanged. Worktree remains clean. Required `DONE` marker and commit message were written.