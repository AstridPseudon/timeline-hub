Items 1–3 are done and the capture tests now pass; item 4 (`test_commit_runtime_m1`) is unchanged and still fails on the schema-digest skew. In the central `commit-integration` run on the two capture files, 26 passed, 2 failed (both `test_commit_runtime_m1` cases) and 6 xfailed.

## What I did
1. **Stale xfail removed.** I dropped the strict xfail on `test_arbitrary_capture_cannot_acquire_canonical_source`. All 12 parametrised cases pass with the original assertions, so Runtime really does refuse each forgery.
2. **Candidate-less working copy.** The old test is replaced by two tests, each run inline and by reference:
   - `test_missing_candidate_working_copy_is_admitted_uncertified`: `create_task` succeeds, the task can be claimed, and no `authoring_preview` is forwarded.
   - `test_missing_candidate_certificate_without_authority_refuses_before_admission_writes`: the working-copy marker's candidate digest is forged so it contradicts the capture's own authority. Runtime refuses it, and the database dump and CAS/staging files are unchanged afterwards.
   - I added the deletion-ledger row `CT1` in `design/deletion-ledger.agent.md`, since the old expectation was relabelled.
3. **Missing `content_digest`.** I added `"content_digest": shot["content_digest"]` to the shot rows in `managed_timeline._project_exact_parent_head`. Both goldens now pass, and `test_real_saved_entire_expansion_golden` compares the whole result with no ignore list.
4. **Schema digest.** `test_commit_runtime_m1` still fails with `a4e1eebd…` against `89a396aa…`. I did not touch it.

## Why `content_digest` goes in the projection
I did not find a Runtime-side saved-head projection that includes it. Runtime's `validate_capture` calls the Agent's own `project_capture` provider and requires the capture's expansion to equal that output exactly. So `project_capture` is the authority, and it emits `content_digest`.

Runtime's shot-revision read rows carry `content_digest`, so the value was available. The xfailed saved-projection test also expects it to equal the Runtime shot revision's digest.

Adding it to `_project_exact_parent_head` fixes a real inconsistency. The alternative of removing it from `project_capture` would have changed what Runtime verifies.

## Test commands and results
- `request-test … commit-integration --files "tests/sdk/test_capture_source_runtime.py tests/sdk/test_timeline_capture_projection.py"` gave the result above.
- `request-test … targeted --files "tests/packs/rendering/test_timeline_visualize_overview.py tests/sdk/test_timeline_filmstrip.py tests/sdk/test_timeline_revision_diff_admission.py tests/sdk/test_capture_closure_source.py"` gave 84 passed, 9 xfailed. I ran this because other tests call `_project_exact_parent_head` or fake its output.
- I did not request a full suite.

## Not verified
The other xfails in `test_capture_source_runtime.py` and `test_capture_closure_source.py` still say "needs verified source 435357ae". They are still failing as expected, but the saved-projection ones could be re-examined later.

The commit message is in `workers/agt-capture-tests-post-runtime/commit-msg`, and I created `DONE` in the same folder. No temp files are left in the worktree.
