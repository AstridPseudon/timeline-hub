Implemented the four-file M1 harness: real mouse gestures, lost ACK/restart recovery, original B guards, disjoint C, UI inverse, immutable readback, and zero legacy-save assertions.

Validation passed: file lint, isolated spec/support TypeScript, `git diff --check`, and discovery of both M1 cases. Exact commands, results, and observed source heads are in the [report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m1-real-journey/report.md).

**Browser/full/rendering tests remain unrun.** App’s machine handover blocked the reviewed source composition; Runtime owns the final integrated `e2e-m1-gesture` run. No M1 gate pass claimed.

Commit message and transferable patch are written. Next: transfer/integrate this branch, then run the central browser lane.