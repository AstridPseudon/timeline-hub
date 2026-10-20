Implemented `track.delete` v1 with closed args, recorded dependency guards, exact ordered undo/redo, and a portable golden.

- Targeted regression: **436 passed, 1 strict xfailed**.
- Changed-file Ruff and `git diff --check`: **passed**.
- Both commit-message files written; generated caches removed.

**Blocked:** bootstrap track IDs can still be reused after deletion. The strict xfail preserves the required refusal. The manager should port the existing clip-delete reservation fix before integration. M2 remains **HELD**.

[Full report with exact test commands and next steps](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-track-delete/notes/report.md)