Added [the integration test](tests/editing_conformance/test_commit_runtime_m1.py) covering real CLI/SDK commits, lost ACK, restart, exact retry, dependent edits, conflict retention, undo, and published readback.

- Focused lint and syntax: passed.
- `python -m pytest -q tests/editing_conformance/test_commit_runtime_m1.py tests/editing_conformance/test_runner_selftest.py -p no:cacheprovider`: **28 passed, 2 deselected**.
- Real fixture/capture/compiler offline smoke: passed.
- Required `agent commit-integration` lane: **not run**, pending product merges and the corrected Runtime schema/client pin. M1 remains unverified.

Commit message written for the harness. Exact commands, source tuple, blockers, and manager next steps are in [the report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m1-cli-runtime-journey/report.md).