Goal

Repair the B-only expectation in `src/integrations/runtime/shotCompositionRuntime.test.ts` identified by `diag-cdelta-0910`. The recovery draft now correctly contains authored shot-local ids and metadata after B's projection sanitization; the test must assert that authored form while retaining the recovery and canonical-head guarantees.

Files

- `src/integrations/runtime/shotCompositionRuntime.test.ts`

Exact acceptance tests

- `npx vitest run src/integrations/runtime/shotCompositionRuntime.test.ts`
- Request the central targeted lane for the changed test file and report the exact result.
- `git diff --check`.

Do not remove, weaken, skip, or xfail assertions. Keep the recovery and canonical-head assertions; only update the expectation that is stale relative to the decided shot-local authored-data boundary. Compare against pristine `staging/timeline-v2.1` if useful to confirm this is B-only.

Out of scope

- No product implementation changes unless the test exposes a genuine B regression rather than the classified stale expectation.
- No C-owned files, full suite, browser suite, or render.

Evidence

Put evidence files in `$ORCH/workers/B-reopen-runtime-recovery-11/evidence/`, never inside the worktree. Finish with `DONE` and a conventional commit message as usual.
