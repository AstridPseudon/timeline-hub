Review `tl/B-reopen-runtime-recovery-11` against `tl/shotlayer-integration` in the App repo.

Check that the change is limited to the B-only stale recovery expectation in `src/integrations/runtime/shotCompositionRuntime.test.ts`: authored IDs/metadata are expected, while recovery and canonical-head assertions remain. Confirm no assertion was removed, weakened, skipped, or xfailed and no product behavior was changed unnecessarily.

Run the relevant central targeted lane through `$ORCH/bin/request-test B-reopen-runtime-recovery-11 targeted --files "src/integrations/runtime/shotCompositionRuntime.test.ts"`, then wait for it. Also run `git diff --check` on the task diff. Verdict PASS/FAIL with reasons and exact results. Put the review note in `$ORCH/workers/B-review-reopen-runtime-recovery-11/evidence/`, never in the worktree.
