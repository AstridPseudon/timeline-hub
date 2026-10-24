# R2r/P4 Assembly Security Review

## Result: FAIL

Reviewed exact candidate:

- Commit: `bad9ce1d18885a23b42b89342ec99f6e3013b548`
- Tree: `e00c46b6e1abb02067a6d927c361866e01d8eb1f`
- Base: `732c48c6f5a9441a65c61b24595d454a1cd3e180`
- Product blobs:
  - `timeline_commit_store.py`: `4fbac66e...e78bfe5`
  - `test_timeline_history_assembly.py`: `30cf84df...5d3849f0`

Only the expected two files differ; canonical/schema content is unchanged.

## Blocking finding

Deferred replay is not fresh after a queued node’s live checks.

`_verify_accepted_record()` computes replay inputs, then `_accepted_replay()` defers validation until graph traversal completes. A callback mutated an already-checked ancestor’s `timeline_commit_history.metadata_json` to `{}` before deferred replay. The actual `RequestCommitPort.history_entry()` provider path still returned the descendant entry instead of refusing.

A later independent lookup refuses, but the current request has already received stale authenticated history. This violates the required same-request callback/concurrent freshness boundary.

Evidence: `callback-attack-provider.xml` and `.log` — witness test passed because the unsafe return was reproduced.

## Tests

Required command:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=<review worktree>:/home/user/work/agent:/home/user/work/venv-agent/lib/python3.13/site-packages /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider --junitxml=<evidence>/security.xml tests/test_timeline_history_assembly.py tests/test_timeline_request_verification.py tests/test_timeline_lock_placement_limits.py tests/test_timeline_history_authenticated_read.py tests/test_timeline_inverse_stage_authentication.py
```

Result: **193 passed, 0 failures, 0 errors, 0 skipped**.

Focused neighbors: **192 passed, 0 failures, 0 errors, 0 skipped**.

Compile and `git diff --check`: passed.

Ruff/Pyright reproduced the author’s baseline findings with zero new findings per the persisted comparison; direct candidate runs reported 11 Ruff and 74 Pyright existing diagnostics.

Original P4 timing, full suites, and merge were not run. No source fix was made.