Implemented bounded `clip.set` with source-hold edits, explicit asset/transition clears, guarded replay, and generic undo/redo. Added the exact App-row golden.

- **476 targeted tests passed**
- **1 direct Runtime integration test passed**
- Ruff and whitespace checks passed

Transition SET remains unsupported; the report flags the existing outgoing-transition validator mismatch. M2 remains held.

[Report with exact commands and handoff details](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-clip-scalar-fields/notes/report.md). Contract and both commit-message files are written for harness pickup.