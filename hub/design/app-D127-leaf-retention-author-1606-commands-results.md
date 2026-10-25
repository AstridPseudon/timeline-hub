# D127 command results

## Passed

- `/home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_p2_commit_phase_capture.py -k 'not mounted_http_commit_route_and_provider_are_observed and not live_watchdog_uses_real_handler_and_private_faulthandler_output'` — `21 passed, 2 deselected`.
- `ruff check tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — passed.
- `TMPDIR=/tmp/w-2c01717184 mypy --cache-dir "$TMPDIR/mypy" --follow-imports=skip tests/helpers/p2_commit_phase_capture.py` — passed.
- Private `py_compile` for both authorized files with `PYTHONPYCACHEPREFIX=/tmp/w-2c01717184/pyc` — passed.
- `git diff --check` — passed.

## Sandbox limitation

- Exact required command `/home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_p2_commit_phase_capture.py` — `21 passed, 2 failed`; both failures occur before test execution when the sandbox denies `socket.socket` with `PermissionError: [Errno 1] Operation not permitted` in the two socket-backed tests.

## Central targeted request

- Requested `targeted --files "tests/test_p2_commit_phase_capture.py"` through the central test service.
- It remained queued because available disk was `4,859,318,272` bytes, below the service floor of `5,000,000,000` bytes. No central result is claimed.
