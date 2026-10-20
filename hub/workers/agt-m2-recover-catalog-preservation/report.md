Implemented the catalog-preserving recover fix.

- No-version/current-version recover now unarchives via the existing Runtime operation.
- Non-current flat-version recover visibly refuses with `TimelineSession.restore` guidance.
- Restored canonical timeline scoping and closed client dispatch.
- Added idempotency, visibility, head/document preservation, CLI success, and historical refusal tests.
- Explicit `timeline.restore` path and unsafe content writer removal remain intact.

Tests:

- Targeted recovery/CLI suite: **189 passed, 2 skipped**
- Restore/workspace neighbors: **64 passed**
- `git diff --check`: **passed**
- Ruff: baseline failure unrelated to this change.

HTTP positive qualification remains unverified: public Runtime server `2c4ac180c2220bdad966bc01e95ad230e99ce26a` predates catalog visibility restoration.

Tree: `4507ab16813085eaae848a3f9c278c8754cdf8b1`

Commit message and `DONE` marker written; harness should commit the worktree.