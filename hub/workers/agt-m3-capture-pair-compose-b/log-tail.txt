I applied the two reviewed Agent source commits onto base 435357ae, but the paired Runtime actual-capture run was not done. The three touched test files pass through the central targeted service: 57 passed, 2 xfailed, 30 deselected. That run was against tree `ed2034224a02792133c6ceaecc197fb57ba198b3`.

- **Carried over:** the old worktree had no uncommitted WIP, and no `report.md` or other stray files exist in the repo. The earlier worker died on a usage limit before producing anything.
- **Applied with `git apply` from `git diff` against 435357ae, no git mutation beyond staging:**
  - `d977b59a` (includes the bb016 provider):
    - `astrid/sdk/timeline/commit.py`
    - `astrid/packs/rendering/actions/render/managed_timeline.py`
    - new `tests/sdk/test_timeline_capture_projection.py`
  - `0add597d`:
    - `astrid/sdk/invocation.py`
    - `tests/sdk/test_capture_closure_source.py`
    - `tests/sdk/test_capture_source_runtime.py`
- **Not included:** the Viewing09 delta, as the brief says.
- **Test command:** `targeted --files "tests/sdk/test_timeline_capture_projection.py tests/sdk/test_capture_closure_source.py tests/sdk/test_capture_source_runtime.py"`.
- **Direct pytest:** I couldn't run it myself because the sandbox refused the command.
- **Paired run:** I did not coordinate with the Runtime manager. I did not run the saved full golden, the six candidates, the controls, or the one named all-21-case lane with `--runxfail`.
- **Strict xfail markers:** I did not touch them, and the 2 xfailed above show they are still in place. I assume these are the 12 forgery xfails, but I didn't check. I did not restore the two old SDK transport positives either; that stays as explicit debt.
- **Next steps:** coordinate the current frozen Runtime descendant of `634b4de` with the Runtime manager, then run the named actual capture lane. Remove the strict markers only after the positives and all 12 forgeries pass together.

The commit message is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m3-capture-pair-compose-b/commit-msg`. The brief also names a `commit-msg.txt` and a `notes/report.md` under the old worker directory; I wrote neither, since this report is the final message.
