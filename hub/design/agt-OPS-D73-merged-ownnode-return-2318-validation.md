# D73/D139 validation

Available bytes before controls: `5,199,777,792` (required admission >= 5,000,000,000; source floor 4,600,000,000; stop 4,000,000,000).

Passed:

- `/home/user/work/venv-agent/bin/python -m unittest discover -s ops-d73-exact-nodes -p test_recipe.py` — 7 tests passed; both named rows positive exit 17 with one call, and five refusal cases per row with zero additional calls/artifacts.
- `./ops-d73-exact-nodes/dry-check.sh --controls` — 7 tests passed.
- `/home/user/work/venv-agent/bin/ruff check ops-d73-exact-nodes` — all checks passed.
- Python compile of `check.py`, `pre-dispatch.py`, and `test_recipe.py` with `PYTHONPYCACHEPREFIX` in private `$TMPDIR` — passed.
- `bash -n ops-d73-exact-nodes/dry-check.sh` — passed.
- `bash -n ops-d73-exact-nodes/suites.conf` — passed.
- `git diff --check` — passed.

The controls used the actual extracted `test-run` parser and rendered named rows. No product imports, real launcher preflight, product body, service, request-test, central request, install, registry, or full suite ran.
