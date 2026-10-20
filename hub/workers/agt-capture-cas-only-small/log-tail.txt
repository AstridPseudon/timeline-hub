**Blocked.** The candidate-less working-copy fix can't be extracted onto `tl/integration` (4a75f68f) without porting the capture chain, so I reverted my attempt. The worktree is clean and there is no commit-msg. I wrote the dependency list to `BLOCKED`.

- **What applied:** 95e770b5 (`prepare_filmstrip` stops enriching the registry, plus the overview fixture fix) applies cleanly.
- **What didn't:** b30b164c doesn't apply to `astrid/sdk/invocation.py`.
- **Why it can't be adapted:** On integration, `rendering.timeline_visualize` never produces `authority_context.capture_snapshot_ref`. Its whole authority goes into one managed object (`authority_object`, around `invocation.py` 4262-4300). The snapshot-ref publishing path only serves `rendering.render`.
- **What I tried anyway:** I put the "no candidate → exact 4-key cas ref" edit into that path. The two new tests failed with `KeyError: 'capture_snapshot_ref'`, and the other 17 tests in the two files passed. The edit is dead code for visualize captures, so I reverted it.
- **Runtime side:** Runtime b2a1d9f reads `capture_snapshot_ref` in `runtime_protocol/capture_validation.py` and `store.py`, so the Agent side must emit that shape.

**Dependency:** the producer is on `tl/agt-m3-capture-test-rebase`, in commits above 4a75f68f:
- **435357ae:** the Viewing composition.
- **3c382f4d:** the capture projector in `astrid/sdk/timeline/commit.py`, the `managed_timeline.py` changes, and the `runtime_capture` branch with candidate forwarding in `invocation.py`.
- **f8bbdf70:** the Runtime qualification tests.

The earlier part of that branch, with 3c382f4d and whatever of 435357ae it depends on, has to land on integration before b30b164c and 95e770b5 will apply.

I did not run the paired `request-test commit-integration` check, since there was no change to test. I also did not move vendor locks or request a full suite.

**Recommended next step:** decide whether to bring in 3c382f4d (and the part of 435357ae it needs) as a gated unit. I can then redo this extraction on top of it.
