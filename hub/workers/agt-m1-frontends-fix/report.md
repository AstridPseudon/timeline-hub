Implemented public-client commit/history calls, unlocked network reads/sends, durable flight fencing, and strict ACK identity checks. Concurrent suffixes, original guards, exact bodies/keys, and preview intent remain preserved. Commit message written.

Validation: **190 passed**, using real core and bridge source through a temporary import overlay; generated transport was faked.

```bash
PYTHONPATH=$PWD:/tmp/agt-m1-frontends-fix-overlay /home/user/work/venv-agent/bin/python -m pytest -q -p core_overlay tests/sdk/test_timeline_sync.py tests/packs/timeline/test_cli_commit_move.py tests/sdk/test_timeline_publish_connection.py tests/sdk/test_timeline_journal.py tests/packs/timeline/test_cli_edit_flags.py tests/packs/timeline/test_cli_history.py tests/packs/timeline/test_cli_status_publish.py tests/packs/timeline/test_cli_parity.py tests/packs/timeline/test_edit_verbs.py --basetemp=/tmp/agt-m1-frontends-fix-pytest-final
```

Checks passed:

```bash
/home/user/work/venv-agent/bin/ruff check --no-cache astrid/sdk/timeline/sync.py astrid/sdk/timeline/outbox.py tests/sdk/test_timeline_sync.py tests/packs/timeline/test_cli_commit_move.py
/home/user/work/venv-agent/bin/mypy --cache-dir=/tmp/agt-m1-frontends-fix-mypy astrid/sdk/timeline/sync.py astrid/sdk/timeline/outbox.py
git diff --check
```

CLI Ruff findings remain unchanged at 15. Temporary overlay and caches were removed.

Used existing receipt/command validators plus narrow acceptance-identity checks because Agent lacks the packaged Runtime response schema. No contract decisions changed.

Full, real-Runtime restart/socket, and browser journeys remain unverified. Next: integrate core and bridge dependencies, then run those checks centrally.