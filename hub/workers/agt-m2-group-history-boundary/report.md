**Runtime owns the blocker.** Its trusted helper records raw parent payloads as a `parent` root replacement. Both verified boundaries differ from authored `State.parent` only at `occurrences`; the existing `timeline` RootPins match exactly. Agent projection preserves the complete closures, so no Agent guard change is warranted.

Results:

- Official-pin Runtime nine cases: **7 passed, 2 failed** before migration acceptance.
- Focused migration/root/inverse/reservation suites: **313 passed**.
- Existing restore/ABA controls: **6 passed, 99 deselected**.
- Read-only boundary probe and `git diff --check`: passed.

[Report with exact commands and source proof](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-group-history-boundary/notes/report.md). Shared coordination and both commit-message files are written. Agent worktree is clean.

Next: Runtime corrects the original helper capture before fresh acceptance, then rerun the unchanged nine cases. **M2 remains held; actual migration/undo/redo remains unverified.**