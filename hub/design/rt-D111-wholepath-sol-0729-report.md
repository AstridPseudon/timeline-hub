**FAIL — D111 acceptance remains unestablished; candidate stays held.** Read-only investigation is complete.

The [review](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D111-wholepath-sol-0729/evidence/D111-wholepath-review.md>) records exact source paths, commands, results and limitations.

- **Mounted lifetime:** HTTP requests share one Runtime service, store and registered Agent provider. Each request gets a fresh port and verification scope; successful scope exit preserves process proofs.
- **D94 already covers replay:** verified records return at `timeline_commit_store.py:539–543`, before historical replay. The separate replay memo guards `_verify_accepted_replay` at `:611`; `_historical_sequential` is downstream at `:798`. New candidate validation remains separate.
- **App29218’s exact miss remains unresolved:** a cold/new row, restart, unrelated write, refusal/error or D97 fallback can require replay. The raw correlated stack/phase/lifecycle artifacts are absent locally, so the specific trigger cannot be identified.
- **0706 deliberately reset reuse to expose historical validation.** Its forced timings measure altered cache behavior and cannot establish a non-flat **production** curve. The final profiler source is also absent, limiting audit of its exact hook.
- **Ordinary controls still matter:** retained ordinary runs show one historical sequential call across eight replay checks, yet N=8 takes roughly 10–11 seconds. Repeated historical validation cannot explain all that growth. History, document size and reads grew together.
- **Before/after wall improvement is unproved:** author0653’s profiled request was 2754 ms before and 2995 ms after. Aggregate inclusive CPU totals span acceptance and replay; they do not isolate Recorder dominance within historical replay.

Validation on baseline Runtime **c91626f5**:

- Existing lifecycle controls: **17 passed in 3.79 s**; complete command is recorded in the review.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" ASTRID_CHECKOUT=/home/user/work/agent PYTHON_BIN=/home/user/work/venv-runtime/bin/python bash scripts/check-before-push --native-provider-smoke`: **2 passed in 2.74 s**, genuine provider origin verified.
- `git diff --check`: passed; worktree unchanged.
- Retained current P1 reports **2/2 PASS**, with matching immutable spec hash. Its raw XML/manifest are unavailable locally and were not independently re-certified here.

**One next step:** obtain the existing App29218 artifacts and exact 0706 harness/profiler sources, then use the existing native harness without forced resets on the demonstrated request/lifecycle sequence. No new cache or D94 shortcut is justified by this evidence.

No product, test, schema, pin or authority changes; no full suite/browser run. Evidence totals about 36 KB. Commit message and `DONE` written.