Implemented the bounded current-base Scene dispatch continuation.

- Added private scene-only invocation, authority/capture binding, executor artifact ZIP, catalog pagination, and preservation/dispatch tests.
- Added real Runtime/pack-host proof for saved and frozen-candidate queries with cleanup guarantees.
- Published [handoff](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-scene-current-dispatch-handoff.md>).
- Wrote commit message and `DONE` sentinel.

Tests:

- Offline targeted: `224 passed, 2 skipped, 44 deselected`.
- Central managed proof `agt-m3-scene-dispatch-current-resume-targeted-1020213245-7374`: `1 passed`.
- `git diff --check`: passed.
- Focused Ruff found only four pre-existing F401s in `filmstrip_execution.py`; no new lint issue.

No full suite run. Ordinary activation remains held.