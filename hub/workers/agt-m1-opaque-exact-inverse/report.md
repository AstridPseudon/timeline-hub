Implemented authenticated historical-image reuse in `commit.py`: **44 net product lines**. All six opaque-item tests pass with exact closure restoration and no xfails.

- Focused tests: **187 passed, 1 deselected**.
- Central Runtime9f tests: **19 passed**.
- Ruff and `git diff --check`: passed.

Kept M1 guards unchanged. Two M2 shared redo journeys remain incompatible and were not ported; handle those separately.

[Report with exact commands, provenance, and limits](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m1-opaque-exact-inverse/notes/report.md). Coordination updated; both commit-message files are ready for the harness. No in-scope blockers.