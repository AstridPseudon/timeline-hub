# G5 bounded local-save test migration

Worker: `agt-G5-threeway-tests-1222`  
Repo: Agent worktree `/home/user/work/wt/agt-G5-threeway-tests-1222`  
Base: `tl/agt-G5-local-save-1137` / `7f4edd327`  
Result: **PASS for this test-only migration; G5/P1 integration gates remain unchanged.**

## Scope and origins

Only these two assigned test files changed:

- `tests/sdk/test_timeline_checkout.py`
- `tests/sdk/test_timeline_store_fixes.py`

No production, Runtime, generated, pin, contract, facade, or shared dependency
file changed. The removed legacy imports were:

- `astrid.sdk.timeline_checkout.three_way` in `test_timeline_checkout.py`;
- `astrid.sdk.timeline.store.three_way` in `test_timeline_store_fixes.py`.

There were three affected legacy test functions and four direct legacy calls:
the checkout function called `three_way` twice; the store parent-config
success function called it once; and the store parent-theme function called it
twice (ordinary refusal and force). The migrated tests use the real local
boundary: `Checkout.save()` → `_file_lock()` → `_save_locked()` →
`_merge_writer()` → `_merge_local_draft()` → the existing emitter diff and
`_doc_patch.apply_change()` path. They use real `Checkout.load()` reloads and
temporary working-copy files; no copied or renamed test merger was added.

## Exact assertion mapping

| Original case and source | Local-save migration and retained property |
|---|---|
| `test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones`, old checkout test: base bundle; `R.nudge(+0.5)` versus `b-type.set(text="LIVE!")`; assert merged `R == 1.5`, `text == "LIVE!"` | Two stale `Checkout` handles save through the file lock and reload the landing file; the same exact input/output is asserted. A second base file applies the original overlap input (`R.nudge(+0.5)` versus head `b-type="LIVE!"` plus `R.nudge(-0.5)`), asserts refusal, preserves head `R == 0.5`, then asserts explicit LOCAL `force=True` lands `R == 1.5`. |
| `test_publish_merge_keeps_candidate_parent_config_changes_next_to_head_changes`, old store test: child edit in the head plus candidate `parent.config.chapters = [{"name": "01 OPEN", "from": "c1"}]`; assert no conflict, chapters retained, head shots retained | Head and candidate are stale local checkouts saved to the same file. The candidate save succeeds through local replay; reload asserts the exact chapters value through `intent.chapters()` and exact head shot bundle preservation. |
| `test_publish_merge_flags_a_parent_config_key_changed_differently_and_force_wins`, old store test: head theme canvas FPS `24`, candidate FPS `60`; assert `theme_overrides (parent-config)` conflict and force candidate output `60` | Local save refuses the same parent payload and leaves the disk head at `24`; the assertion preserves the exact local conflict detail (`both changed 1 of the same thing(s): parent.`), which is the LOCAL boundary's conservative parent-root wording rather than the retired publication unit label. Explicit `candidate.save(force=True)` then reloads and asserts the exact candidate value `60`. |

The existing local-save raw/absence/null/media/order/source-bound and
concurrency guard assertions were left unchanged. The 13-case guard selection
was run without skip, xfail, or weakened expectations.

## Evidence

Environment: `/home/user/work/venv-agent/bin/python`,
`PYTHONPATH=.:/home/user/work/runtime`,
`ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`; all pytest basetemps were
private under `/tmp/agt-G5-threeway-tests-1222-*`.

```text
Affected three cases: 3 passed in 1.01s
Local-save guard selection: 13 passed in 1.45s
Full two target files: 119 passed, 4 warnings in 44.03s
```

The four warnings are the pre-existing Pillow `Image.getdata` deprecation
warnings in the checkout test file. No full project, browser, HTTP, native14,
P1, P4, or D17 suite was requested or run.

Quality checks:

- private mypy on both changed files: `Success: no issues found in 2 source files`;
- scoped Ruff comparison: checkout diagnostics unchanged from baseline; store
  improved from one baseline import diagnostic to clean;
- `git diff --check`: passed.

No safety denial, dependency installation, daemon, Git mutation, or shared
install/cache mutation occurred.
