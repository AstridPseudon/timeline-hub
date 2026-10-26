# D140 independent review validation

Candidate: `0634ea013b29ba2ab02f619a99328b1f5ca81c7a`.

| Command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q ops-d140-farm/test_recipe.py` | PASS — 69 passed in 145.63s |
| `/home/user/work/venv-agent/bin/ruff check --no-cache ops-d140-farm/test_recipe.py ops-d140-farm/receipts.py` | PASS — all checks passed |
| `bash -n ops-d140-farm/receive-farm.sh` | PASS |
| in-memory `compile`/`ast.parse` for receipts.py and test_recipe.py plus JSON parse | PASS |
| `git diff --check HEAD^ HEAD` | PASS |
| empty `D140_PHASE=pre-child ... receive-farm.sh --check-only` | PASS control — exit 1, JSON `status=NOT_READY`, 59 checks |

No typecheck is configured for this private Python-only surface; this is
explicitly unverified rather than treated as a pass.

No full suite, Farm venue, live socket/browser, child request, package
acquisition, Store, import census, D73 dry/core body or production service was
run. The passing tests use private synthetic custody fixtures and do not prove
the live Farm handoff.
