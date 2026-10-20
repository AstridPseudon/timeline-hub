Implemented the M0 audit artifacts:

- Reworked [port-manifest.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/port-manifest.md) with separate experiment status vs. M1/M2 recommendations, main-schema rules, renderer-free commit requirements, deferred authoring, playback preservation, and full M1 scope.
- Added [port-failure-index.tsv](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/port-failure-index.tsv): 140 exact node-level rows, with zero missing/extra/duplicate nodes per indexed run.
- Wrote [commit-msg](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m0-port-audit/commit-msg).

Tests:

- Import walk: `58 candidates, 0 failures`.
- Focused compiler/cycle/curve lane including freshness: `104 passed, 5 failed`.
- Clean `tl/integration` baseline: `196 passed, 17 deselected`.
- `git diff --check`: clean.
- Worktree: clean; no product source or integration worktree modified.

The five focused failures remain indexed as evidence: four runner-guard incompatibilities and one missing motion-curve generator. No environment (`c`) failures were found. Older `targeted.log` output was pre-final/pre-shim and was not included in the final index.