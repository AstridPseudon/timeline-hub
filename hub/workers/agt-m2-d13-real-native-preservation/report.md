Implemented and qualified D13/RT07 native preservation.

- Removed both unauthorized xfails while retaining legacy refusal/artifact-preservation coverage.
- Added real registered native assembly → commit lost-ACK/restart retry → revision-pinned render → decodable MP4 → undo coverage.
- Added minimal Runtime epoch propagation and existing WorkspaceClient read facades.
- Final named suite: `2 passed in 227.61s`.
- Local targeted suite: `78 passed in 27.59s`.
- `git diff --check`: clean.

Reports:

- [Design report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-d13-real-native-preservation.md)
- [Worker notes](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-d13-real-native-preservation/notes/report.md)
- Commit message and `DONE` marker written.

Remaining gate: manager review and merge; no public activation claim made.