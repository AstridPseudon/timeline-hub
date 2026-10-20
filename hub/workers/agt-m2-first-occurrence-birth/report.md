Implemented `occurrence.create` and capture using the existing recorder and typed refs. Includes guarded grouped inverse/redo and the complete S2 schema superset.

Validation passed:

- Targeted native/neighbour tests: **574 passed**.
- Central command: `request-test agt-m2-first-occurrence-birth renderer-peers12-integration --files tests/editing_conformance/test_commit_runtime_occurrence_create.py` — **2 passed**.
- Ruff and `git diff --check` passed.

Runtime proof covers normal bootstrap, child media, exact undo/redo, occupied/retired IDs and restart retry. No typed-ref or port gap remains. Full suites, HTTP/SDK and App journeys were not run.

[Report with exact commands, results and limits](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-first-occurrence-birth/notes/report.md).

Next: coordinated Runtime generation and consumer pins, then App adoption before writer retirement. `commit-msg` and `DONE` are written.