# Validation

- Central targeted service: `python -m pytest -q tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — **26 passed in 3.22s**, exit 0.
- Offline local focused lane: `PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_p2_commit_phase_capture.py -k 'not mounted_http_commit_route_and_provider_are_observed and not live_watchdog_uses_real_handler_and_private_faulthandler_output'` — **24 passed, 2 deselected**, exit 0.
- Python 3.11 compile: `python3.11 -m py_compile -q tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — passed.
- Ruff: `/root/.local/bin/ruff check tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — all checks passed.
- Diff check: `git diff --check` — passed.
- A direct local run of the full touched file hit the sandbox socket restriction on the two existing localhost tests (`PermissionError: [Errno 1] Operation not permitted`); the central targeted service subsequently ran the exact file suite successfully.

No full suite was requested. No product or generated source was changed.
