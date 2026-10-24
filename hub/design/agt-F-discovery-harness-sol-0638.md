Repaired the runner and added its wrapper. Independent whole-path static review: **PASS**.

- Separated the snapshot from the approved `bb50`/`f320` source carriers; removed `--child` and the caller-written approval gate.
- Added normal Store/maker custody checks, bytecode validation, production import checks, fixed profile/Composition binding, durable failure artifacts, and nonzero failed postchecks.
- Preserved **9 assertions, 10 support calls, transition invocation 6, and the 45-second watchdog**.

Checks passed:

```bash
PYTHONPYCACHEPREFIX="$TMPDIR/compile-cache" python3 -m py_compile tools/run-discovery-original-0603.py
/home/user/work/venv-agent/bin/ruff check --no-cache tools/run-discovery-original-0603.py
/home/user/work/venv-agent/bin/ruff format --check tools/run-discovery-original-0603.py
bash -n tools/run-discovery-original-0603.sh
git diff --check
```

Targeted mypy: **current 0 diagnostics; parent 4; zero new**. Row shell syntax also passed.

The single handoff is [discovery-original-0638.row](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-discovery-harness-sol-0638/evidence/discovery-original-0638.row). Commit message and `DONE` are written.

No tests, body, Node, preflight, provisioning, or installation ran. Execution remains unverified. Next: complete dependency route 0628, obtain the genuine candidate, then have the manager install the reviewed row and enqueue it normally.