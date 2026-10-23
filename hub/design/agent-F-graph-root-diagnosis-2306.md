## Report

Diagnosis complete on c36; no product/test changes. Worktree is clean. Commit message written to the assigned path.

Five exact failures:

1. `test_authenticated_created_child_stages_reload_inverse_redo_exact_closure`
   - Observed: call phase rejects redo with `history_unavailable: restored root differs from accepted source`.
   - Stack reaches `commit.py:1082` → `inverse.py:889` → `_root_inverse.py:217`.
   - Cause: R2 staged-root restoration guard rejects the reloaded child-created root during authenticated redo. This is a provider accepted-source/stage-binding seam, not a fixture failure. The combined predicate’s exact subcondition is not observable without rerunning the forbidden body.
   - Next control: R2 owner needs an exact stage-boundary observer and a fix preserving the authenticated child root’s source→successor provenance through redo. Do not weaken the guard or trust snapshots.

2–5. `test_provider_root_child_aliases_guard_equal_state_publications`, all `first_scope=child` variants:
   - `[False-False-child]`
   - `[False-True-child]`
   - `[True-False-child]`
   - `[True-True-child]`
   - Observed: expected `intervening_write`, received `inverse_conflict`.
   - Root-scope variants all passed.
   - Inferred source-backed cause: authenticated child alias normalization omits the materialization successor from later-history guards; `check_later_steps` then classifies the later root publication as a surviving consumer instead of an intervening write. The pending R2 owner output-guard change directly targets this seam. These four are one shared R2 cause and should be combined with that owner’s work.

C0 mapping:

- §2 requires alias normalization to one verified physical closure image, distinct source/successor bindings, exact digests/pins, owner/effect attribution, and authenticated provenance.
- §5 requires current-value guards plus scanning every later publication, including equal-state/A→B→A history. Later writes must not be hidden by equal bytes or shared-source reachability.
- Caller-supplied inverse writes, roots, digests, or pins cannot authorize restoration; only accepted records and verified source→successor bindings can do so.

Evidence used: retained full-run inventory/longrepr and c36 source audit of `tests/sdk/test_timeline_commit_graph_roots.py`, `_root_inverse.py`, `inverse.py`, `_step_undo.py`, and `commit-v2.md`. No original failing test body was rerun.

The authorized full run `agent-full-post-g5-2225-1023222822-25691` remains active at 97%; repeated `wait-test ... 1` calls returned 124. Terminal counts and after-origin comparisons are unavailable. Resume with:

```bash
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test agent-full-post-g5-2225-1023222822-25691 1
```

No `DONE` marker was created while that run remains active.