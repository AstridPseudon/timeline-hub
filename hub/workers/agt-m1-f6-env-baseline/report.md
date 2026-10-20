Completed the read-only f6 baseline.

- Verified clean `HEAD f6fbe741a256e2756a1d686350f8a38e37c015ee`.
- Ran the single central `remotion-env-nodes` request on all 109 exact manifest nodes.
- Result: **79 failed, 30 errors, 0 passed**.
- Current 4a comparison produced the identical 109-node status partition: **no current-only regressions**.
- Runtime/App/Composition refs recorded exactly.
- Owned RunPod extra is failed in both runs; root cause remains **UNKNOWN**.

Reports:

- [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m1-f6-env-baseline/notes/report.md)
- [comparison.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m1-f6-env-baseline/notes/comparison.json)

Full logs and request metadata are preserved under the report’s referenced central test directories.