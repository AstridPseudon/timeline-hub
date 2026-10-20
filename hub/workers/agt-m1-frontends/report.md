Implemented CLI/Python move, durable exact-request retries, suffix retention, conflict preservation, and publication-based undo. Accepted results include revision/publication IDs and an immutable show command. Product diff: **313 added, 4 removed lines**.

Validation:

```bash
PYTHONPATH=$PWD:/tmp/agt-m1-frontends-test-overlay /home/user/work/venv-agent/bin/python -m pytest -q -p core_overlay tests/sdk/test_timeline_sync.py tests/packs/timeline/test_cli_commit_move.py tests/sdk/test_timeline_publish_connection.py tests/sdk/test_timeline_journal.py tests/packs/timeline/test_cli_edit_flags.py tests/packs/timeline/test_cli_history.py tests/packs/timeline/test_cli_status_publish.py tests/packs/timeline/test_cli_parity.py tests/packs/timeline/test_edit_verbs.py --basetemp=/tmp/agt-m1-frontends-pytest-final
```

**139 passed.** The temporary overlay imported the parallel owner’s real core read-only; generated transport was faked. Temporary files were removed.

Ruff passed for new modules, parser, and tests; mypy passed for both new modules; `git diff --check` passed. Existing CLI lint counts were unchanged; the parser’s existing mypy override error was reproduced from HEAD.

Used the connected generated client directly because its workspace allowlist is outside this task’s ownership. No fallback writer, renderer call, or accepted-history journal was added.

Seam updated and commit message written. Next: integrate core and regenerated Runtime client, then run the combined full/live suite centrally. Those integration checks remain unverified.