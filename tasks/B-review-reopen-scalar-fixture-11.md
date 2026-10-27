Review `tl/B-reopen-scalar-fixture-11` against `tl/shotlayer-integration` in the App repo.

Check that the change only gives `src/tools/video-editor/commands/commitSession.clipScalar.test.ts` a local transform-free placement setup, leaves the canonical shared fixture bytes/digest untouched, and preserves all 34 scalar-contract assertions. Reject any bypass of projection validation or weakened/skipped/xfail assertion.

Run the relevant central targeted lane through `$ORCH/bin/request-test B-reopen-scalar-fixture-11 targeted --files "src/tools/video-editor/commands/commitSession.clipScalar.test.ts"`, then wait for it. Also run `git diff --check` on the task diff. Verdict PASS/FAIL with reasons and exact results. Put the review note in `$ORCH/workers/B-review-reopen-scalar-fixture-11/evidence/`, never in the worktree.
