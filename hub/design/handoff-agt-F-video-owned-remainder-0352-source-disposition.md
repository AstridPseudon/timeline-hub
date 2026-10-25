# F-D86 source-only disposition

Base: Agent `f518440837`; actual packet: `handoff-rt-D86-9211-outcomes-0303-*`; video source review: `rt-D86-video12-review-0328-report.md`.

## Video item-correspondence findings (4)

- `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[image-False]`
- `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[image-True]`
- `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[video-False]`
- `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[video-True]`

Packet first exception: `astrid/sdk/timeline/_command_state.py:154`, `missing or ambiguous identity 'occ-a'`.
Static path: `unplace_shared` → `capture_placement_unplace` → `commands.execute` → `placement_unplace` → `State.entity`/`State.occurrence` → `one`; the item-correspondence sub-seam is `State.shot_item_map`/`_item_ids` (`_command_state.py:320-369`), with shared physical installation in `native_occurrence_shared.install_shared_source`.
Owner: Agent R1/G3/R2; no cure inferred. The final video fixture preserves shared `chapter-shot`/`shot-1`, opaque fields, inputs, predicates and IDs, but actual intermediate item correspondence/materialization fields are not published. UNKNOWN pending only existing safe fields: accepted setup/inverse `placements`, `shot_revision_id`/`internal_timeline_revision_id`, `source_mapping.shots[*].item_id_map`, and `commit.materialization` bindings.

## Owned-move findings (2)

- `tests/editing_conformance/test_owned_move_publish_runtime.py::test_http_original_sdk_move_publish_disjoint_rebase_reload_undo` — line 174, assertion of `data.status == 'rebased'`. Static caller: `TimelineSession.publish` → `sync._flush` → generated `timelines.commit` → Runtime `commit_timeline` → coordinator → registered `RuntimeCommitService.commit`; `sync._ack` accepts `accepted|merged|rebased`. The v2 contract names a new disjoint landing `merged` and preserves `rebased` only for historical receipts. Agent source and test are equal to captured `cef8`; the assertion is not caused by the current Agent delta. UNKNOWN until the existing safe receipt fields (`status`, `rebased_onto`, base/previous pins, tuple) are read.
- `tests/editing_conformance/test_prepared_video_birth.py::test_prepared_video_public_preview_accept_retry_undo_and_no_write` — line 249, exact Runtime commit assertion. Test expects Runtime `8ea0766f5e9fb23cea26c7398770a8aaac06b258` / tree `6047ac3033c3594b8f83db3afd8bb2c47cafa6d6`; current read-only Runtime worktree is `6634a17f3ffd885567ba3c91b6c7a560df7375a4` / tree `47b376717ce7a919a697c62133de3e74dc9f6d3a`. This is a tuple/pin mismatch before the behavior body, not evidence of a product failure. Minimum safe evidence is the existing exact-pinned Runtime identity; no rerun requested.

## Source equality / checks

Current Agent equals captured `cef8a5be53f68a7cd3b5403c362171c5633a5ae9` for `_command_state.py`, `commit.py`, `emitter.py`, `sync.py`, and both owned test files. Only `inverse.py` differs (`cef8`: `0702cda4...`; current: `06bd41f4...`), matching the D90 materialization verifier and relevant only to the eight recipe cases, which remain separate/unverified.

Static-only checks: AST/in-memory compile 12 files PASS; scoped Ruff PASS; scoped mypy on `inverse.py` PASS; `git diff --check` PASS. No pytest, collection, helper/fixture execution, probe, service, package install, browser, render, or source repair was performed.
