## Completed

- Added real HTTP `WorkspaceClient`/`RuntimeHandler` proof for image and video parent-media replacement.
- Covered lost ACK, restart retry, exact body/key/receipt, later-head replay, reload, opaque/order/mirror preservation, guarded undo/redo, and strict invalid-outbox guards.
- No product code changed.

Tests:

- Named a0 service: `24 passed, 1 deselected`; both new parametrized cases passed.
- Two unrelated pre-existing publication-chain tests failed against pinned a0 API differences.
- `git diff --check` and AST parse passed.

Artifacts written:

- Commit message: `/tmp/.../workers/agt-m2-wc3-real-http-retry-final/commit-msg`
- Shared report: [handoff report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agt-m2-wc3-real-http-retry-final-REPORT.md)
- `DONE` marker created.