# D127 independent protected review command results

## Central receipt consumed

- Existing request `app-D127-leaf-retention-author-1606-targeted-1025160952-28551` was not resubmitted.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-D127-leaf-retention-author-1606-targeted-1025160952-28551` — pass, exact snapshot tree `4fc171c1639d52df2fe0996f34311fa43ae42654`, `23 passed in 3.46s`.
- Receipt command: `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_p2_commit_phase_capture.py`.

## Own targeted/offline checks

- `/home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_p2_commit_phase_capture.py -k 'not mounted_http_commit_route_and_provider_are_observed and not live_watchdog_uses_real_handler_and_private_faulthandler_output'` — `21 passed, 2 deselected`.
- `ruff check tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — passed. The requested `/home/user/work/venv-runtime/bin/ruff` path does not exist; `/root/.local/bin/ruff` was used.
- `TMPDIR=/tmp/w-3e9a8cb144/d127-mypy mypy --cache-dir /tmp/w-3e9a8cb144/d127-mypy/cache --follow-imports=skip tests/helpers/p2_commit_phase_capture.py` — passed, no issues.
- `PYTHONPYCACHEPREFIX=/tmp/w-3e9a8cb144/d127-pyc /home/user/work/venv-runtime/bin/python -m py_compile tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — passed.
- `git diff --check b81c0ab^ b81c0ab -- tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — passed.
- Independent AST script over parent/candidate test files — 19 parent test functions retained by name; parent has 160 `ast.Assert` nodes, candidate has 181 total, and retained-parent assertion AST equality is false (163 retained assertion nodes after additions/edits).

## Not run

- No browser, native, original tour, new collector, activation, full suite, or duplicate central request.
- No App source was changed. App validator compatibility was source-inspected only.
