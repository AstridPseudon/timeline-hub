Implemented original-slot replacement with guarded SDK undo/redo/replay and equal-z-order coverage.

- Central targeted: **3908 passed, 3 failed**—two inherited occurrence-delete reds and one new provider undo blocker.
- The required `commit.py` fix is outside allowed scope. Its proposed patch passed **103 tests** in a private probe and remains unapplied.
- Integration’s file delta is present; merge ancestry still needs the harness.
- Runtime schema regeneration remains required.

Wrote `commit-msg`, `BLOCKED`, and the [report with exact commands, schema hashes, op list, and separate parent-builder delta](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-parent-media-order/report.md). No `DONE`.