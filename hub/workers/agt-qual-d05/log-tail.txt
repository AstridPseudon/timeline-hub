## D05 qualification: `inverses.py` deletion (agt-qual-d05)

**Verdict: the deletion is safe, but the replacement is only partly proven. I did not mark D05 DELETED. The ledger row stays `held`.**

### What is proven
- **No production caller.** A repo-wide grep on the synced tree finds no `plan_inverse`, `plan_inverses`, `InverseRequest` or `timeline.inverses` import outside `inverses.py` and `tests/timeline/test_inverses.py`. The only other hit is a stale line in `tests/.test_durations`, a tracked timing cache, which I left alone.
- **Integration does not touch the deleted files.** `git diff fc324e83 tl/integration` is empty for `inverses.py`, `tests/timeline/test_inverses.py`, `events/schema/types.py` and `giant-file-split-candidates.json`.
- **Supported command-level inverses pass on the synced tree.** `test_exact_authored_move_inverse_redo`, `test_undo_detects_aba_and_unchanged_write_publications` and the other named replacements all run and pass.

### How I merged, since I could not run `git merge`
- I exported the integration delta with `git diff --binary fc324e83 tl/integration` and applied it to the worktree with `git apply`. The dry run was clean.
- The worktree now holds the tree that `git merge tl/integration` would produce. It is uncommitted: the harness will commit it on exit, as a plain commit rather than a merge. Three `tests/editing_conformance/test_commit_runtime_*.py` files arrive as untracked.
- The commit message says this. The orchestrator can review it.

### Commands and results
Run from the worktree root on the synced tree:

| Command | Result |
|---|---|
| `pytest -q -p no:cacheprovider tests/timeline tests/editing_conformance tests/sdk -k "timeline or commit or inverse or undo or history or restore"` | 1168 passed, 2 skipped, 173 subtests passed |
| `pytest -q -p no:cacheprovider tests/timeline/test_mixed_mode_cut.py tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py` | 106 passed. Run from the worktree root; the first combined run failed 3 cwd-dependent tests. |
| `request-test agt-qual-d05 commit-integration`, then `wait-test` | pass, 2 passed (`tests/editing_conformance/test_commit_runtime_m1.py`) |
| `pytest -q -p no:cacheprovider tests/test_structure_contracts.py` | 32 passed, 1 failed |

The failure is `test_giant_file_inventory_matches_rationale`: `generic_host.py` is 13798 lines but the rationale doc says 13598. `generic_host.py` is byte-identical to `tl/integration`, and D05 does not touch it or the rationale doc. So this is drift on integration itself, not caused by D05. I did not run it on integration directly.

### Gap that blocks DELETED
- **Lost legacy behaviour, no replacement.** `test_inverses.py` covered 24 legacy event kinds (clip retime, swap, text, annotation, effect tune, theme, pool, arrangement, config), the non-reversible fallback to `timeline.reverted`, erased-payload handling, and purity. None of these has a replacement test. The current registry's commands are essentially `clip.move` v1 and `track.create`, and nothing in the product emits the legacy kinds for undo. PLAN's rule to keep every distinct behaviour therefore still needs a judgment call.
- **Review citation error.** The retirement review cites `test_inverse_rebases_only_over_proven_disjoint_new_writes` under `editing_conformance`. It actually lives in `tests/sdk/test_timeline_commit_provider.py:579`. It passes.

### Decisions I made
- Did not flip the ledger row. The brief allowed it only if proven, and the legacy-kind gap is not closed.
- Did not restore the deleted tests as `xfail`. They import a module that no longer exists, so xfail does not apply cleanly. This is a decision for the orchestrator: accept the legacy-kind cut as settled, or restore the tests as xfail with a requirement comment.

### Cleanup
- The `rm -rf` cleanup of the four ignored `__pycache__` dirs in the worktree was denied. They are gitignored. My temp patch `integ-delta.patch` is in my scratchpad, not the worktree.
- Commit message written to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-qual-d05/commit-msg`. `DONE` created.

### Recommended next steps
1. Orchestrator decides the legacy-kind question above.
2. If accepted, flip D05 to DELETED with the replacement tests named in the review, and fix the `editing_conformance` citation.
3. Separately, fix the `generic_host.py` line count in `docs/giant-file-rationale.md` on integration.
