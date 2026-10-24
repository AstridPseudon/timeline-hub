## Report

- Updated only [tests/sdk/test_timeline_persistence.py](/home/user/work/wt/rt-F-SDK-persistence-fixture-0708/tests/sdk/test_timeline_persistence.py).
- Added truthful revision/publication history pairs, full history response fields, and exact `open_bundle(..., publication_id=...)` validation/hydration.
- Preserved all test bodies and assertions: 10/10 AST body hashes and assertion hashes unchanged.

Test command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider 'tests/sdk/test_timeline_persistence.py::test_restart_a_fresh_process_sees_every_edit_and_the_undo_history' 'tests/sdk/test_timeline_persistence.py::test_two_writers_in_separate_processes_merge_different_clips_and_refuse_the_same_param' --junitxml="$TMPDIR/persistence-fixture.xml"
```

Result: **2 passed in 4.19s**, JUnit reports 0 failures/errors.

Additional checks:

- In-memory compile: passed.
- `git diff --check`: passed.
- Ruff: only pre-existing `BLE001`.
- Mypy: only the same five pre-existing subprocess-stream errors; zero new diagnostics.
- Old result: both tests failed with `_FakeTimelines.history` missing.
- Commit message written to the assigned path.
- `DONE` marker created; no blockers.