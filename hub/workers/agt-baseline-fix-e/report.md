## Group E (34 nodes): fixed, all 34 pass

All 34 group E nodes now pass under the `remotion-env-nodes` suite. The fix was the module path only. No assertions were weakened, and nothing was skipped or xfailed.

**Before/after counts**
- **Before (my local run, same venv-agent, pre-change):** 34 failed, 7 passed across the three files (41 nodes). Every failure was `ModuleNotFoundError: astrid.packs.runpod.executors` (or the `FileNotFoundError` in the source-scan test). I did not run the remotion-env suite on the pre-change tree, so the remotion-env "before" figure is the cutlist's 34.
- **After, remotion-env suite:** `bin/request-test agt-baseline-fix-e remotion-env-nodes --files "<34 ids>"` → request `agt-baseline-fix-e-remotion-env-nodes-1020065547-13032`, result **34 passed in 7.63s, exit 0**. I also ran a one-node probe first (`...-1020065506-11582`, passed).
- **After, local targeted run:** `pytest tests/packs/runpod/test_pack_executors.py test_ensure_storage.py test_provision_ports.py` → **41 passed**.

**Changes (3 test files, +31/−31)**
- `test_pack_executors.py`: `from astrid.packs.runpod.executors import _common` → `from astrid.packs.runpod.shared import common as _common`. The `executors.provision.run` imports → `shared.common`.
- `test_ensure_storage.py`: the source-scan test now reads `astrid/packs/runpod/shared/common.py`. Its assertions are unchanged. `common.py` contains no `ensure_storage` or `create_storage`, so the "provision never auto-creates storage" check still holds. I also updated its comment.
- `test_provision_ports.py`: import from `shared.common`.

**Environment split: none.** The cutlist said `runpod_lifecycle` is not installed in venv-agent. That is no longer true: `runpod_lifecycle` resolves to `venv-agent/.../site-packages/runpod_lifecycle`, and all 34 pass with it. So no node in group E stays red for an environment reason. The cutlist's ENV note for E is stale.

**Out-of-scope reds I saw in the same directory (not group E, not touched):**
- F/G/M from the cutlist: 5 failed and 15 errors in `test_worker_process.py` and `test_worker_staging.py`.
- `test_worker_preparation.py::test_runtime_activation_checkpoints_restore_only_the_exact_process` also fails. I did not check whether it is in the 109-node set.

**Other notes**
- Not run: `ruff` (the command was refused by the approval gate, so the lint check is unverified). The diff is import and path only.
- Not run: any full* suite, per the brief.
- Cleanup: I could not remove `astrid/__pycache__` and `tests/__pycache__` from my runs. The removal was denied. They are gitignored, so they will not be committed, but they are on disk in the worktree.
- Scratchpad: the node list is at `/tmp/claude-0/-home-user-work-wt-agt-baseline-fix-e/b40fba4e-3261-4bbd-b715-63c58a974f46/scratchpad/group-e-nodes.txt`.
- Also written: `commit-msg` and `DONE` under `orch/workers/agt-baseline-fix-e/`. Nothing was committed, pushed, or merged.

**Suggested next steps**
- Correct the cutlist's group E environment note.
- Check whether the `test_worker_preparation` red is in the 109-node set.
