## Report

- Ported the exact 3-file `65c87dd5..46f2b9e2` delta: 67 insertions, 2 deletions.
- Retained exact pidfd `poll(POLLIN)` exit proof; live or mismatched incarnations still fail closed.
- Existing strict tests unchanged; reused-PID negative coverage already existed.
- Added requested delivery note: [agent-main-infrastructure-touched.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-main-infrastructure-touched.md).

Tests:

`targeted --files "tests/core/execution/test_process_group.py tests/core/execution/test_custody_broker.py"` — **627 passed, 16 deselected**.

No full suite or merge request performed. Pending separate security review and current D13 integration. `DONE` and commit message were written.