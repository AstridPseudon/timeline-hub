Implemented the bounded `NativeSheet` adapter: scoped-ID bindings, pinned basis, native move/label captures, local preview, and session/outbox commits. Existing read output is preserved; unsupported edits refuse explicitly.

Verification: **323 targeted tests passed**. Lint checks and `git diff --check` passed; no new lint findings. No full/socket suite was run.

[Report with exact commands, API decisions, limitations, and remaining writer consumers](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-sheet-commands/notes/report.md). Both commit-message files are written.

No implementation blocker. **HELD pending M1 record**; CLI wiring remains with its owner.