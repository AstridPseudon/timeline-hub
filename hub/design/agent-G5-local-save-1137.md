# G5 concurrent local draft saves — bounded draft

Base: `d1fa6c133`; worktree `/home/user/work/wt/agt-G5-local-save-1137`.
**Gap 2's local save caller no longer depends on `store.three_way`. Draft only; no integration merge or deletion is requested before P1 GO.**

## Changes and scope

Only three product/test paths changed:

- `astrid/sdk/timeline/checkout.py`: production `save → _save_locked → _merge_writer` now plans local payload patches with the existing emitter and replays them with the existing patch application primitive. The file lock, history staging, redo retirement, and atomic replacement ordering remain. On a failed file write/replacement, pending scalar intent remains usable for retry.
- `astrid/sdk/timeline/_doc_patch.py`: the additional narrow command helper was announced before editing. Extracted the existing value/order/identity/mirror/managed-edge operations into `apply_change`; the provider calls that same helper. An AST comparison against HEAD confirms the extracted operations are identical, including submitted alias error references. Closure resolution, previous values, physical bindings, media verification, allocation recording, installation, and effects stay in the existing provider path. No semantic or provider policy change was made.
- `tests/sdk/test_timeline_checkout.py`: added counterexamples for same-child disjoint edits, derived duration preservation, complete bundle equality, landing-head undo/redo, absent/null/opaque ordered values, failed replacement plus retry, conservative unknown edits, collection order changes, and canonical source-bound parent/child saves. A live monkeypatch makes any local `store.three_way` call fail. All 64 original test functions are source-identical, including both tests named in 1122 and the original explicit local-force assertion.

This is neither a renamed three-way executor nor a copied old file: diff generation and actual value application are shared with the existing emitter/command machinery. No Runtime write is added; these writes are local working-copy JSON only. `store.three_way` and its live `publish_bundle` caller remain unchanged for the separate joined G5 retirement.

## Decisions within the brief

- Independently merge bounded `Clip.nudge` / `Clip.set` scalar edits only when the captured before/after chain exactly covers the draft. Guard complete clip items, collection membership/order, supporting payload/parent settings, and relevant placement inputs. Generic step labels do not establish known reads, and mixed direct edits cannot acquire scalar permission merely by calling a helper afterward.
- Uncaptured transforms retain whole touched-payload guards. Changed closure membership, order, base/provenance, or owner links are refused, including under explicit local force. Existing explicit local scalar force still re-emits at the conflicting scope and passes normal previous-value application checks; it is never an automatic conflict fallback.
- Preserve authored placement rows as a guarded occurrence payload. Preserve the other writer's derived duration and allow the existing final length synchronization to run on the combined result; duration is not substituted for owner/start provenance.
- Source-bound local files now preserve the complete source mapping, including `_runtime_document`, across serialization/reload. The ordinary editable-document reader previously stripped that image. Full images use the existing emitter's physical alias checks. Legacy files without an image use the existing native `State`/`guard` owner checks and unchanged provenance, without manufacturing a canonical image or fetching a head.

The 68a scaffold refused every concurrent save. It was read as reference and not transplanted. The original successful saves remain successful in the original tests and in the separate-process persistence test.

## Final targeted evidence

All commands ran from the assigned worktree with private scratch/caches, no dependency installation, no full-suite request, and no live socket/browser/renderer suite. Runtime pair: `/home/user/work/wt/rt-pin-3b926efa`.

**save-history-complete: 61 passed**, exit 0. Log: `/tmp/w-c4fb881684/save-history-complete.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-c4fb881684/save-history-complete \
  tests/sdk/test_timeline_checkout.py::test_first_draft_pins_the_fetched_bundle_for_edit_diffs \
  tests/sdk/test_timeline_checkout.py::test_replace_asset_repoints_all_clips_and_undo_restores_registry \
  tests/sdk/test_timeline_checkout.py::test_save_load_round_trip_shows_both_clocks_and_honours_timeline_edits \
  tests/sdk/test_timeline_checkout.py::test_three_way_merges_disjoint_edits_and_refuses_overlapping_ones \
  tests/sdk/test_timeline_checkout.py::test_two_writers_on_one_working_copy_merge_and_never_drop_each_others_edits \
  tests/sdk/test_timeline_checkout.py::test_local_patch_replay_preserves_the_whole_bundle_and_landing_history \
  tests/sdk/test_timeline_checkout.py::test_local_patch_replay_preserves_explicit_absence_null_and_opaque_array_order \
  tests/sdk/test_timeline_checkout.py::test_local_patch_replay_failed_replacement_keeps_pending_intent_for_retry \
  tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_unknown_reads_and_collection_order_conservative \
  tests/sdk/test_timeline_checkout.py::test_local_patch_replay_keeps_source_bound_children_and_raw_parent_mirrors \
  tests/sdk/test_timeline_transaction.py \
  tests/sdk/test_timeline_noop.py \
  tests/sdk/test_timeline_checkout_history_boundaries.py \
  tests/sdk/test_undo_a1_legacy_open.py \
  tests/sdk/test_timeline_store_fixes.py
```

**persistence-complete: 7 passed**, exit 0. Log: `/tmp/w-c4fb881684/persistence-complete.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-c4fb881684/persistence-complete \
  tests/sdk/test_timeline_persistence.py::test_restart_a_fresh_process_sees_every_edit_and_the_undo_history \
  tests/sdk/test_timeline_persistence.py::test_a_writer_that_dies_holding_the_lock_does_not_block_the_next_writer \
  tests/sdk/test_timeline_persistence.py::test_a_failed_working_copy_write_leaves_no_undo_step_for_the_edit_it_did_not_save \
  tests/sdk/test_timeline_persistence.py::test_a_live_holder_that_never_exits_is_waited_for_then_refused_by_name \
  tests/sdk/test_timeline_persistence.py::test_a_truncated_temp_file_is_never_read_as_the_working_copy \
  tests/sdk/test_timeline_persistence.py::test_two_writers_in_separate_processes_merge_different_clips_and_refuse_the_same_param \
  tests/sdk/test_timeline_persistence.py::test_a_discard_in_one_process_leaves_the_next_process_with_no_working_copy
```

**emitter-complete: 55 passed**, exit 0. Log: `/tmp/w-c4fb881684/emitter-complete.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --basetemp=/tmp/w-c4fb881684/emitter-complete \
  tests/editing_conformance/test_document_patch_emitter_engine.py \
  tests/editing_conformance/test_document_patch_emitter_v2.py \
  tests/editing_conformance/test_doc_patch_v2.py::test_bad_operands_refuse_atomically \
  tests/editing_conformance/test_doc_patch_mirrors.py::test_sequential_clip_mirrors_execute_provider_history_and_inverse
```

**123 targeted cases passed, with no skips or expected failures.** These are bounded suites, not full-project qualification. The emitter/guard selection includes malformed previous values, identity writes, list operations, mirror handling, conservative dependencies, provider history, and inverse behavior.

The initial child-source probe exposed the stripped closure image; a separate-process probe exposed the legacy no-image shape. Both are covered by the final passing selections. Early new-fixture mistakes (the parent sentinel and frame quantization/derived length expectations) were corrected; no original assertion or guard was changed to accommodate them.

## Quality, preservation, and exact commands

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa RUFF_CACHE_DIR=/tmp/w-c4fb881684/ruff-complete make ruff PY=/home/user/work/venv-agent/bin/python
```

Exit 0; log `/tmp/w-c4fb881684/ruff-complete.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa MYPY_CACHE_DIR=/tmp/w-c4fb881684/mypy /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline
```

Exit 0; log `/tmp/w-c4fb881684/mypy-complete.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004
```

Exit 0; log `/tmp/w-c4fb881684/vendor-complete.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
```

Exit 0; log `/tmp/w-c4fb881684/artifact-complete.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa git diff --check
```

Exit 0; log `/tmp/w-c4fb881684/diff-complete.log`.

Normal Ruff **2149/2149**, private mypy **1912/1912**; no baseline change or increase. Scoped Ruff identities/counts against HEAD are unchanged: checkout 1→1, command helper 0→0, allowed test file 46→46. No new or removed diagnostic identities; `/tmp/w-c4fb881684/scoped-ruff.json`. Helper extraction AST evidence: `/tmp/w-c4fb881684/helper-ast.txt`. Vendor lock, artifact manifest, and diff checks pass.

The preservation diff over store.py, publish.py, cli_working.py, sync.py, commit_session.py, commit.py, commands.py, _commit_patch.py, generated Runtime client, schemas, pins, and Composition artifact paths is empty. All other tests are untouched.

The full v2 request remains byte-for-byte unchanged: base revision/publication pair, commands, label, steps with patch/reads/ordinals, merge, key, dry_run, source, rationale, group_id. Reply code remains unchanged: data+receipt accepted/merged, full canonical closure, records/dependencies/effects/steps/history/undo_steps, preview would_status, conflict reason+head, and invalid code+path+hint+suggested command. This is preservation by scope/audit plus the targeted in-process command/provider tests, not a claim of a new HTTP or P1 qualification.

No Git commit/merge/rebase/checkout/push, branch/ref deletion, daemon, shared dependency/cache mutation, safety denial, new dependency, test skip/xfail, renderer/browser/full/P1/P4 HTTP/native14/original58/D17 run occurred. The worker tmpdir marker resolves to private `/tmp/w-c4fb881684`; it was not replaced.

## Remaining scope and next step

No blocker to this bounded draft. Unknown/free transforms and structural changes remain conservative; this does not promise arbitrary automatic concurrent rebasing of every checkout helper. No film writer or remaining publisher has been retired here. Review the three-file draft independently, keep it unmerged until P1 GO, and let the joined G5 owner migrate the remaining publisher before deleting `store.three_way`.
