Implemented the approved AM snap-plate unit after sprite source `ded9b0c9`.

- Ported exact plate source/direct tests from `48f3eef4b`.
- Refreshed and verified `catalog.ts` and `artifacts.json`.
- Preserved sprite revision/digest and protected bytes.
- Tests:
  - `test_am_snap_plate_fill.py`: 2 passed
  - `test_am_snap_plate_scene_capability.py`: 14 passed
  - Catalog/manifest checks and `git diff --check`: passed
- No full suites or broader integration changes run.
- Report: [agent-plate-current-artifact-gate.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-plate-current-artifact-gate.md)
- Commit message and `DONE` marker written.