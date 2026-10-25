# Commands and results

All App commands used `/opt/node20/bin/node` or the repository's existing shared `node_modules`; no install or generated build was performed. Node compile caches and Python caches were private under `/tmp/w-d127-combined-Ntc0E0`.

| Command | Result |
|---|---|
| `NODE_COMPILE_CACHE=... /opt/node20/bin/node --import tsx --test --test-name-pattern='D127 reviewed-new validator|D105 launch ownership' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` | PASS: 2 passed, 2 skipped |
| `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python /opt/node20/bin/node --import tsx --test --test-name-pattern='D78 bootstrap' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` | PASS: 1 passed, 3 skipped |
| Normal harness P2 control with qualified Runtime, `ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-070dfc5e`, external helper `4ee0424b…`, and `D66_P2_COMMIT_PHASE_CAPTURE_HELPER*` hash hook | PASS: 1 passed, 3 skipped; accepted endpoint commit and capture validation |
| `/opt/node20/bin/node --import tsx --test --test-name-pattern='P2 Runtime observer bootstrap' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` with the same qualified source/helper environment | PASS: 1 passed, 3 skipped in 14.59s |
| `./node_modules/.bin/eslint tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts --report-unused-disable-directives --max-warnings 0` | PASS |
| `./node_modules/.bin/tsc -p tsconfig.app.json --noEmit` | PASS |
| `./node_modules/.bin/tsc -p tsconfig.node.json --noEmit` | PASS |
| `/opt/node20/bin/npm run typecheck:strict-islands` | FAIL baseline/environment: missing `@astrid/packs/*`, `virtual:astrid-element-admissions`, and existing implicit-any errors; no touched-file diagnostic |
| `/root/.local/bin/ruff check /tmp/w-d127-combined-Ntc0E0/p2_commit_phase_capture.py` | PASS |
| `/root/.local/bin/mypy --cache-dir /tmp/w-d127-combined-Ntc0E0/mypy-cache --follow-imports=skip /tmp/w-d127-combined-Ntc0E0/p2_commit_phase_capture.py` | PASS |
| `PYTHONPYCACHEPREFIX=/tmp/w-d127-combined-Ntc0E0/py311-cache /usr/bin/python3.11 -m py_compile /tmp/w-d127-combined-Ntc0E0/p2_commit_phase_capture.py` | PASS |
| Qualified Runtime `pytest ... tests/test_p2_commit_phase_capture.py -k test_observer_avoids_line_events_and_unrelated_request_lookups` | PASS: 1 passed, 18 deselected in 2.17s |
| `git diff --check f9fa634aa9a547ade4ae545129dce8e75f1afe06^ f9fa634aa9a547ade4ae545129dce8e75f1afe06 -- tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` | PASS |
| Reused central request `app-D127-leaf-retention-author-1606-targeted-1025160952-28551` | PASS: 23 passed in 3.46s; not resubmitted |

Not run: full suite, browser/original tour, native, collector, activation, SWAP, unrelated profiles, or service replay.
