## Done

- Fixed draft labels to use the draft’s own base revision.
- Added honest loading/unavailable surface UI without mounting a fake Player.
- Decoupled unavailable recovery from delivered pixel identity.
- Preserved unknown metadata when no pinned head exists.
- Added surface and mailbox tests for canonical head advances, recovery, atomic delivery, stale labels, and no-cache failure.

## Verification

- PreviewPanel tests: **7 files, 68 passed**
- Targeted ESLint: **passed**
- `npm run typecheck:strict-islands`: **passed**
- `npx tsc --noEmit`: **passed**
- `git diff --check`: **passed**
- Full/browser suites: **not run**, per orchestrator rule.

Commit message written to the requested path. No blockers.