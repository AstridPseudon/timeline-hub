**PASS — merge-ready for the bounded pure compiler port.** Source review found no blocker; product code is unchanged.

Moved the API doc to `docs/design/agent-timing-kernel-current.md`, copied it to `$ORCH/design/agent-timing-kernel-current.md`, and removed root `design/`.

Fresh checks:

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timing_compiler.py tests/sdk/test_timing_cycles.py --tb=short` — **51 passed**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python scripts/reshape/check_repo_hygiene.py` — **passed**.
- `git diff --check` — **passed**.

Prior 201-neighbor, 97 + 2-word/version and 93-D07 proofs remain unchanged; they were not rerun. No full suite or Runtime/default-activation qualification claimed.

[Detailed report]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-timing-kernel-gate/notes/report.md) records the exact safe quartet and source/cohort deltas. Commit message and `DONE` are written. No blockers; next step is the harness commit and orchestrator integration.