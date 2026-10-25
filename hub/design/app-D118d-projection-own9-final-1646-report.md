# D118d report

- Capacity admission passed: 5,094,088,704 bytes free; post-run 5,092,470,784 bytes.
- Source and Runtime custody passed; reviewed source hash matched exactly, Runtime pin clean.
- Ran the exact recorded own9 command. Result: **exit 1**, 9 tests, 9 setup errors, 0 failures, 0 skipped, 16.26s.
- First failure: `astrid/sdk/timeline/_command_state.py:369`, `CommandError(kind="identity_conflict")`: `shot item correspondence changed`, surfaced from fixture setup at `tests/sdk/test_timeline_capture_projection.py:311`.
- No fixes, retries, additional suites, or SWAP inspection performed.

Evidence: [verdict.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-projection-own9-final-1646/evidence/verdict.md), [own9.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-projection-own9-final-1646/evidence/own9.xml). Commit message and `DONE` were written.