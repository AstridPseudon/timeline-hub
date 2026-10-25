PASS — reviewed author commit `f0c47759b9`, tree `73b0a07be3`.

- Exact 3-file delta: 56 additions, 8 deletions; all blob hashes match.
- Placement alone uses explicit 14s fixture; 17 other calls retain default 12s, including element/registerAsset and popup.
- Placement body, assertions, request/reply, history, reload, undo, and waits preserved.
- All 21 native seed assertions preserved.

Tests:

- Node20 placement/receipt controls: 3/3 passed.
- D66 Node22 controls: 24/24 passed; Node24 unavailable.
- Python AST/compile: passed.
- Locked App/Node TypeScript: passed.
- Scoped ESLint `--max-warnings 0`: passed.
- `git diff --check`: passed.
- Protected callback comparison: passed.

The initial intermediate commit failed its caller-count control; the author corrected this with a separate `placementTest`, then committed `f0c47759b9`.

Applied the exact reviewed blobs to this worktree. Created `DONE` and the required commit message. Recommended next step: manager normal-merge the author commit, then submit the single placement journey.