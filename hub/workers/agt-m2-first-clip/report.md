Implemented parent-only `clip.add` v1 with native capture, preallocated IDs, destination-track guards, lossless row preservation, portable goldens and exact inverse/redo.

Validation:

- Focused native/provider tests: **269 passed, 1 strict xfailed**.
- Central real Runtime/client integration: **3 passed, 1 strict xfailed**, including both unchanged M1 journeys.
- Ruff and `git diff --check`: passed.
- No full suite or merge requested.

Known limits: grouped new-track undo needs staged reversal; Runtime inspection rejects explicit null speed despite accepting/storing it. Both positive expectations remain strict xfails. Runtime’s official schema projection still needs updating before M2 merge.

[Report with exact commands, artifacts and findings](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-first-clip/report.md) · [Commit message](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-first-clip/commit-msg)