# Runtime startup-stop final review

## Verdict

**APPROVE** `94a7a2d` (`fix(runtime): treat startup stop as orderly`) against
current integration `b88a56f`. No correction is required.

## Review findings

- `astrid_runtime/cli.py:398-415` keeps the existing
  `cancellation.startup_scope(stopped)` and changes only the foreground
  exception classification. A `StartupCancelled` is suppressed only when the
  stop event is set. Genuine bootstrap/readiness exceptions still set
  `failure`, print `Runtime failed`, and return nonzero. The `finally` block is
  unchanged, so a shutdown/cleanup failure still sets `failure` and returns
  nonzero.
- The cancellation exception is not a generic `RuntimeError`: it is the
  dedicated `runtime_protocol.cancellation.StartupCancelled`, raised by
  `cancellation.check()` only when the scoped stop event is requested. This
  does not swallow unrelated startup errors.
- Cleanup remains outside the cancellation scope after the exception unwinds.
  The existing `ForegroundRuntimeBoundary.stop()` path therefore still owns
  daemon shutdown and any retained-custody/cleanup-uncertainty result.
- The candidate diff touches only `astrid_runtime/cli.py`,
  `tests/test_foreground.py`, `tests/test_portable_lifecycle.py`, and
  `tests/conftest.py`. It does not touch owner-token handling, runtime epoch,
  authentication, custody/retained-controller code, or commit/history code.
- `tests/test_foreground.py:216-235` directly proves a stop raised during
  bootstrap skips readiness continuation, calls `boundary.stop()`, emits no
  failure, and returns zero. Existing parameterized startup/shutdown failure
  assertions remain intact.
- `tests/test_portable_lifecycle.py:224-235` waits for the installed
  foreground process's own `door_endpoint` ready log after the door health and
  realm checks. Because `_emit_ready()` runs only after `_wait_for_door()` and
  the log is line-buffered, `_stop_foreground()` now exercises stopping a
  ready foreground Runtime rather than racing its startup.
- `tests/conftest.py:158-161` removes only the obsolete
  `SETUPTOOLS_USE_DISTUTILS=stdlib` override from the private wheel-build
  fixture. No package pin, assertion, or install behavior was changed; this
  permits the classified Python 3.13 fixture to use setuptools' available
  distutils implementation.

## Evidence

Recorded targeted evidence on the candidate tree (not rerun here, per task):

```text
python -m pytest -q tests/test_foreground.py::test_run_foreground_treats_stop_during_startup_as_orderly tests/test_foreground.py::test_run_foreground_reports_failure_log_and_stops_owner_in_same_process tests/test_foreground.py::test_run_foreground_stops_only_when_handler_event_is_set tests/test_foreground.py::test_run_command_routes_to_in_process_foreground_owner
5 passed

/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_portable_lifecycle.py::test_installed_foreground_runtime_owns_discovery_door_and_stops_cleanly tests/test_portable_lifecycle.py::test_installed_up_wait_and_down_stop_the_exact_discovered_owner tests/test_portable_lifecycle.py::test_installed_up_reports_occupied_browser_door_without_claiming_owner
3 passed in 14.60s

git diff --check
passed
```

The worker's recorded pre-fix reproduction failed as expected with return 1
and `Runtime startup cancelled by a stop request`; the corrected foreground
run passed. No full suite, browser/live-socket suite, install, pin change, or
test rerun was performed for this review.

## Disposition

Merge the candidate as-is through the Runtime integration queue. Later full
qualification remains subject to the orchestrator's central-suite schedule.
