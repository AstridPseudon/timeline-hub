# Agent outbox Runtime-lock custody review

**APPROVE** exact target commit `a6eec98d31a4715bb807f85fd8646789612af506`,
tree `c146abab53cbf83c8c9e1f8af7be10326e037fbc` (parent
`de36e302e3ee6e950e22aed5c02c02163f7cf5c8`).

The full committed diff is limited to `astrid/sdk/timeline/outbox.py` and the
raising-body regression in `tests/sdk/test_timeline_sync.py`. The production
change preserves the existing `.lock` path and changes only the native lock
calls to the existing Runtime `platform.lock_file` / `platform.unlock_file`
ABI. `lock_file` retains exclusive blocking defaults; its cancellation-aware
wait is entered before the body. The file context owns the descriptor,
unlocking is in one `finally` after successful acquisition, and the outer file
context closes the descriptor afterward. Thus body exceptions release once,
acquisition errors do not unlock an unacquired descriptor, and the body error
is preserved when unlock succeeds. No double-unlock path was found.

The Runtime backend fits this use: POSIX maps to `flock`; Windows regular
files map to `LockFileEx` / `UnlockFileEx` with the same exclusive/blocking
semantics. Windows execution was not available in this Linux review
environment; this is a source-level backend-fit result, not Windows runtime
qualification.

`request_bytes`, `Outbox.write` atomic temp-file/fsync/replace cleanup, and all
sync retry/idempotency logic are unchanged. No API, schema, authority,
lock-path, or test weakening was introduced.

## Evidence

- Exact-target inline custody control, loading `outbox.py` directly from
  `git show a6eec98d31a4715bb807f85fd8646789612af506:astrid/sdk/timeline/outbox.py`:
  **PASS** — raising body releases exactly once; descriptor is closed;
  contender blocks until release; failed acquisition does not unlock.
- Focused unchanged serialization/atomic/retry/idempotency controls:

  ```text
  PYTHONPATH=/home/user/work/runtime:. /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
    tests/sdk/test_timeline_sync.py::test_capture_and_same_value_write_are_sent_even_without_a_diff \
    tests/sdk/test_timeline_sync.py::test_restore_lost_ack_retries_exact_request_after_reload \
    tests/sdk/test_timeline_sync.py::test_lost_ack_reload_retries_exact_request_before_sending_suffix \
    tests/sdk/test_timeline_sync.py::test_failed_fsync_prevents_send_and_atomic_replace_preserves_unsent_intent \
    tests/sdk/test_timeline_sync.py::test_changed_intent_key_and_dry_run_cannot_replace_an_ambiguous_request \
    tests/sdk/test_timeline_sync.py::test_restart_preserves_parsed_body_source_and_optional_presence \
    tests/sdk/test_timeline_sync.py::test_blocked_read_does_not_hold_outbox_lock_or_overwrite_concurrent_work
  ```

  Result: **10 passed in 1.39s**.

The requested shorthand suites `smallestnewfailure-release` and
`serializationcontrol` are not present in the current central
`suites.conf`; no substitute central suite or HTTP/full suite was requested.
The supplied baseline evidence (66 sync + 46 focused and the exception-release
regression) was not repeated per brief. No browser, HTTP, Windows, or full
suite claim is made.
