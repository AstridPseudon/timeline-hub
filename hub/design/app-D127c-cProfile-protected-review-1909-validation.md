# Validation

- Disk admission at review start: 5,122,207,744 bytes available on `/tmp`
  (5 GB decimal floor met; below 5 GiB).
- Required exact interpreter command:
  `python3.11 -m pytest -q -o addopts= -p no:cacheprovider tests/test_p2_commit_phase_capture.py`
  — **NOTRUN/blocked before collection**, because system Python 3.11 has no
  pytest module.
- Existing qualified Runtime environment, exact pytest arguments with only the
  two socket tests excluded as required offline:
  `PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_p2_commit_phase_capture.py -k 'not mounted_http_commit_route_and_provider_are_observed and not live_watchdog_uses_real_handler_and_private_faulthandler_output'`
  — **24 passed, 2 deselected**, exit 0.
- Same qualified environment with the complete touched file — **24 passed, 2
  failed**, exit 1; both failures are the pre-existing localhost socket tests
  blocked by sandbox `PermissionError: [Errno 1] Operation not permitted`.
- `python3.11 -m py_compile -q tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — PASS.
- `/root/.local/bin/ruff check tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — PASS.
- `git diff --check e319fdb..HEAD` — PASS.
- Scoped Pyright reports two candidate `Stats.stats` attribute errors plus
  pre-existing test-environment diagnostics; direct mypy reports the same two
  candidate errors plus repository baseline errors.
- No full, socket, browser, service, native, production-body, SWAP, WAL,
  recovery, or full-tour suite was requested by this reviewer.
