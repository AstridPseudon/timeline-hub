# D127c first-return validation

## Source and static checks

- `git diff --check`: PASS.
- `/root/.local/bin/ruff check tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py`: PASS.
- `PYTHONPYCACHEPREFIX=/tmp/w-829cc351d6/pycache /home/user/work/venv-runtime/bin/python -m py_compile tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py`: PASS.
- `/root/.local/bin/pyright tests/helpers/p2_commit_phase_capture.py`: PASS, 0 errors.
- `/root/.local/bin/pyright tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py`: two pre-existing test-file diagnostics remain (`pytest` unresolved and optional `stop` at line 78); no helper diagnostics.
- `/root/.local/bin/mypy tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py`: PASS, no output.
- Changed-path audit against `e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9`: exactly the two permitted test files.

## Tests

- Local focused command using the qualified Runtime environment, with the two socket tests excluded: `PYTHONPATH=. /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_p2_commit_phase_capture.py -k 'not mounted_http_commit_route_and_provider_are_observed and not live_watchdog_uses_real_handler_and_private_faulthandler_output'` — 29 passed, 2 deselected, exit 0. This run occurred while free space was below the genuine 5 GB unit-body admission floor and is therefore retained as informational, not qualified acceptance evidence.
- Central required route: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-D127c-cProfile-first-return-1921 targeted --files 'tests/test_p2_commit_phase_capture.py'` — queued as `app-D127c-cProfile-first-return-1921-targeted-1025192227-20838`, not started because the central service reported 4,984,758,272 bytes free against its 5,000,000,000-byte floor. No resubmission was made.
- Exact system-Python command `python3.11 -m pytest -q -o addopts= -p no:cacheprovider tests/test_p2_commit_phase_capture.py` was not run because the system interpreter has no pytest module; the qualified Runtime interpreter was used for the informational local run above.

No full, browser, service body, native, SWAP, WAL, recovery, or full-tour suite was run.
