# G5 local-save independent review

Verdict: **PASS** for the bounded correctness, security, and behavior-fidelity review. This is a draft-only review; it does not grant P1 GO and no integration merge or G5 deletion is approved by this report.

## Scope and origins

- Reviewed cumulative `tl/agt-G5-local-save-1137` tree at Agent `7f4edd3277084c2d85675c33735cb6b0e5ddcd05`, against `d1fa6c1332011e4c6f6e075ca458c7dff6bf130c`.
- Exactly three paths differ: `astrid/sdk/timeline/_doc_patch.py`, `astrid/sdk/timeline/checkout.py`, and `tests/sdk/test_timeline_checkout.py`.
- Runtime was read from the pinned checkout `/home/user/work/wt/rt-pin-3b926efa` at `3b926efab2eed122d374540baee297d4cdcec62a` (clean; tree `b794170504544b259781e50d7ca4d61b6729e67c`). `/home/user/work/runtime` was not used or modified.
- Frozen origin refs observed read-only: Runtime `31c7ac3a00f7a205f507bf5bd4d4625628d429bd`, Agent `11caf1d9de291d76f491cf69f7942606b7471d7a`, App `8f0c2484463e9b666d184a744d52e252984e551a`, Composition `c82eb7c459d0a41263954bf007071a6a0e8e0a6a`.

## Static review

- AST/source comparison: all 64 original `test_` function bodies are source-identical; 69 current functions means 5 additions, no original removal/change.
- AST comparison of the extracted `_doc_patch.apply_change` effect segment against the original provider `patch` segment before `verify_media`, allocations, reads, installation, bindings, materialization, and effects: equal, 7 statements on both sides.
- Production local save now routes through `_merge_local_draft`, the existing emitter `_diff` and the existing `apply_change` primitive; no copied/renamed `three_way` executor and no Runtime writer was added.
- `store.three_way` remains unchanged and is not called by production `checkout` save. The live monkeypatch test passed.
- `git diff --quiet` checks passed for unchanged provider/public support files (`store.py`, `publish.py`, `cli_working.py`, `sync.py`, `commit_session.py`, `commit.py`, `commands.py`, `_commit_patch.py`) and for pins/artifacts. No HTTP/D17 rerun was used; these surfaces were checked by blob/diff preservation.
- Existing explicit local `save(force=True)` remains the only force path exercised here; no new film-force route exists. Closure membership, provenance, owner links, collection/order changes, and unknown/free/mixed edits remain conservative/refused. Source mapping, physical source-bound images, legacy owner guards, absent/null/raw/opaque values, mirrors, and full-bundle landing history are retained.

## Test evidence

All commands ran from `/home/user/work/wt/agt-G5-local-review-1204`, with `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa`, `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa`, `/home/user/work/venv-agent/bin/python`, `--timeout=35`, `-p no:cacheprovider`, and private basetemps under `/tmp/w-68c6c0d3ae`.

1. Save/history/original disjoint + overlap/two-writer + all new local cases and relevant neighbors:

   `python -m pytest -q -o addopts= -p no:cacheprovider --timeout=35 --basetemp=/tmp/w-68c6c0d3ae/review-save --maxfail=1 tests/sdk/test_timeline_checkout.py::test_first_draft_pins_the_fetched_bundle_for_edit_diffs tests/sdk/test_timeline_checkout.py::test_replace_asset_repoints_all_clips_and_undo_restores_registry tests/sdk/test_timeline_checkout.py::test_save_load_round_trip_shows_both_clocks_and_honours_timeline_edits tests/sdk/test_timeline_checkout.py::test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones tests/sdk/test_timeline_checkout.py::test_two_writers_on_one_working_copy_merge_and_never_drop_each_others_edits tests/sdk/test_timeline_checkout.py::test_local_patch_replay_preserves_the_whole_bundle_and_landing_history tests/sdk/test_timeline_checkout.py::test_local_patch_replay_preserves_explicit_absence_null_and_opaque_array_order tests/sdk/test_timeline_checkout.py::test_local_patch_replay_failed_replacement_keeps_pending_intent_for_retry tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_unknown_reads_and_collection_order_conservative tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_source_bound_children_and_raw_parent_mirrors tests/sdk/test_timeline_transaction.py tests/sdk/test_timeline_noop.py tests/sdk/test_timeline_checkout_history_boundaries.py tests/sdk/test_undo_a1_legacy_open.py tests/sdk/test_timeline_store_fixes.py`

   Result: `61 passed in 4.83s`.

2. Seven-process persistence, atomic replacement/lock/retry and concurrent writer cases:

   `python -m pytest -q -o addopts= -p no:cacheprovider --timeout=35 --basetemp=/tmp/w-68c6c0d3ae/review-persistence tests/sdk/test_timeline_persistence.py::test_restart_a_fresh_process_sees_every_edit_and_the_undo_history tests/sdk/test_timeline_persistence.py::test_a_writer_that_dies_holding_the_lock_does_not_block_the_next_writer tests/sdk/test_timeline_persistence.py::test_a_failed_working_copy_write_leaves_no_undo_step_for_the_edit_it_did_not_save tests/sdk/test_timeline_persistence.py::test_a_live_holder_that_never_exits_is_waited_for_then_refused_by_name tests/sdk/test_timeline_persistence.py::test_a_truncated_temp_file_is_never_read_as_the_working_copy tests/sdk/test_timeline_persistence.py::test_two_writers_in_separate_processes_merge_different_clips_and_refuse_the_same_param tests/sdk/test_timeline_persistence.py::test_a_discard_in_one_process_leaves_the_next_process_with_no_working_copy`

   Result: `7 passed in 16.13s`.

3. Existing document-patch emitter, previous/order/read negatives, provider and mirror/inverse coverage:

   `python -m pytest -q -o addopts= -p no:cacheprovider --timeout=35 --basetemp=/tmp/w-68c6c0d3ae/review-emitter tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_document_patch_emitter_v2.py tests/editing_conformance/test_doc_patch_v2.py::test_bad_operands_refuse_atomically tests/editing_conformance/test_doc_patch_mirrors.py::test_sequential_clip_mirrors_execute_provider_history_and_inverse`

   Result: `55 passed in 4.98s`.

4. Quality and integrity:

   - `make ruff PY=/home/user/work/venv-agent/bin/python` with private `RUFF_CACHE_DIR`: `Ruff findings: current=2149 baseline=2149`; pass.
   - Private mypy comparison with `/home/user/work/venv-agent-typecheck-v2/bin/python`: `Mypy findings: current=1912 baseline=1912`; pass.
   - `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004`: `ok runtime.lock.json (matches producer manifest)`.
   - `scripts/artifact_manifest.py --check`: `artifacts.json is current`.
   - `git diff --check`: pass.
   - Scoped Ruff against the three changed files, current versus base by `(file, rule, message)` counts: total `47` versus `47`; checkout `1→1`, `_doc_patch.py` `0→0`, test file `46→46`; no count differences.

The first attempted pytest invocation used the worker `tmpdir` marker file itself as `--basetemp` and produced only pytest setup `NotADirectoryError`; it was not a product failure. The corrected runs above used the marker's resolved private directory `/tmp/w-68c6c0d3ae` and all passed.

## Disposition

PASS for this independent bounded review. Keep the three-file change unmerged until the plan's P1 GO. Do not delete `store.three_way` or other legacy writers as part of this draft; the joined G5 owner must handle those after the required integrated proof.
