## F-D86 report — SOURCE_EXACT

- Reviewed authentic XML, prior pool fixture/reviews, and current source.
- All six errors share `GenuineTimeline.create()` → `_create_fixture()`.
- Merged helper `095177db79` already fixes the exact missing `occ-a` path by submitting semantic birth, reloading canonical state, then applying guarded patches.
- No change made to the allowed test file; worktree remains clean.
- Evidence: `.../workers/agt-F-pool6-actual-0223/evidence/source-exact.md`
- `DONE` marker created; no commit required.

Checks passed:

- Ruff baseline/candidate: pass.
- Mypy baseline/candidate: pass.
- In-memory compile: pass.
- AST/predicate/input/topology review: pass.
- `git diff --check`: pass.

No pytest, collection, service, build, browser, render, or product execution was run. Functional confirmation remains for the later MAIN exact-six batch.