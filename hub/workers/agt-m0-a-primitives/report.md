## Completed

Updated [design/extensions.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/extensions.md) only:

- Limited pre-M4 marker/signal work to bounded resolver seams and fixtures.
- Made missing-marker republication fail closed and atomic.
- Removed orphan/last-known fallback language.
- Labeled registration, reconciliation, generalized signal binding, editable hosting, query growth, policies, personas, and merge overrides as M5/later.
- Added Runtime-owned immutable transcript/config snapshot retention rules.
- Preserved legacy film read/playback semantics and clarified source-word behavior.
- Wrote [commit-msg](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m0-a-primitives/commit-msg).

Checks:

- Contradictory orphan/fallback scan: passed.
- Conditional marker/signal scope scan: passed.
- Trailing-whitespace scan: passed.
- Agent worktree `git status --short`: clean.
- No product tests or probe run; docs-only change, so behavioral integration remains unverified.