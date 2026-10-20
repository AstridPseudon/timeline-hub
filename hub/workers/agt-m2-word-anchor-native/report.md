Implemented native `clip.anchor` v1 with authored stable choices, exact transcript hydration, bounded timing compilation, clear, rebase, inverse and revision restore.

Checks passed:

- Real Runtime: **50 passed**
- Portable captures/schema: **12 passed**
- Command/provider neighbors: **441 passed**
- Ruff, `git diff --check`, normal Runtime generation and `--check`: passed

Exact commands, results, decisions and limitations are in [notes/report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-word-anchor-native/notes/report.md).

No bounded-task blocker remains. Manager must compose the current kernel and complete S1 schema union before freezing. No full suite ran. Commit message and `DONE` are written; private test copies were cleaned up.