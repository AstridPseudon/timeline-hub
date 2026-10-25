# D127 first return command results

- `/home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_p2_commit_phase_capture.py -k test_observer_avoids_line_events_and_unrelated_request_lookups` — **1 passed, 22 deselected** in 1.84s.
- `ruff check tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — **passed**.
- `TMPDIR=/tmp/w-738c23d321 PYTHONPYCACHEPREFIX=/tmp/w-738c23d321/pycache mypy --cache-dir /tmp/w-738c23d321/mypy --follow-imports=skip --ignore-missing-imports tests/helpers/p2_commit_phase_capture.py` — **passed**.
- `TMPDIR=/tmp/w-738c23d321 PYTHONPYCACHEPREFIX=/tmp/w-738c23d321/pycache /home/user/work/venv-runtime/bin/python -m py_compile tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py` — **passed**.
- `git diff --check` — **passed**.

Reused central receipt: `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_p2_commit_phase_capture.py` — **23 passed in 3.46s**, request `app-D127-leaf-retention-author-1606-targeted-1025160952-28551`, exact helper candidate tree `4fc171c1639d52df2fe0996f34311fa43ae42654`. No duplicate 23-test run because helper source/hash stayed byte-exact.

No full suite, browser journey, live service rerun, App edit, product edit, activation, or new collector was run.
