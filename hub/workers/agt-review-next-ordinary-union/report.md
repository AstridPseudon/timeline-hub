## Review result

**APPROVE bounded source-union joins.** No blocker defect found. Candidate: `ce3e647f`, tree `260f2615…`.

Evidence:

- Private normal Runtime generation/checks passed; 75 artifacts, identity `sha256:7e8fe2…`.
- Schema: 55 definitions / 29 operations; raw SHA256 `6ba7b51e…`; canonical SHA256 `63ac77b3…`.
- Source/schema lane: **184 passed**.
- Native Runtime lane: **57 passed**, including birth + text, grouped undo/redo, restart, retry, stale guards, and selected-schema checks.
- `git diff --check`: passed.
- Worktree remains clean; no source or shared dependency changes.

Required before public freeze:

1. Port F1 fix `8e310785` (`staged_records` inverse guard).
2. Port fixture migration `134f1c27`; two old fixture-import failures remain in this candidate.
3. Preserve four existing renderer xfails and complete normal Runtime/public qualification.

Reports:

- [Review report](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-next-ordinary-union.md>)
- [Detailed notes](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-next-ordinary-union/notes/report.md>)