# F-D86 source-only report

No product or test changes. Evidence: [f-d86-video-owned-source-disposition.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-video-owned-remainder-0352/evidence/f-d86-video-owned-source-disposition.md).

Video packet: source `9c149b0201f6cbca096064f5b516a673e8eb0a59`, receipt `27c68177c1f587acec0d2b615d1b8bb95c4a4fde`.

- Four item-correspondence findings:
  - `test_capture_commit_reload_undo_redo_and_restart_safe_retry[image-False]`
  - `[image-True]`
  - `[video-False]`
  - `[video-True]`
- First exception: `_command_state.py:154`, missing/ambiguous `occ-a`.
- Trace: `unplace_shared → capture_placement_unplace → commands.execute → placement_unplace → State.entity/occurrence → one`.
- Minimal seam: `State.shot_item_map/_item_ids` plus `native_occurrence_shared.install_shared_source`; owner R1/G3/R2.
- Actual intermediate item/materialization correspondence is unavailable. UNKNOWN; required safe fields are existing placements, shot/internal revision IDs, `item_id_map`, and materialization bindings.

The eight recipe cases remain separate: four `test_raw_media_golden...` and four `test_provider_round_trip...`, terminating at D90 `_validate_materializations` (`inverse.py:1021`) and `commit.py:1467`. Current `inverse.py` differs from captured `cef8` only via the D90 verifier change; no repair was inferred.

Owned packet: source `73998ac446ea2e4bceed1e0df2c5e2c68c558e82`, receipt `6386c700ee56264aebe12da4558ac74dda0d60ca`.

- `test_http_original_sdk_move_publish_disjoint_rebase_reload_undo`: line 174 expects `rebased`. Trace: `TimelineSession.publish → sync._flush → Runtime commit_timeline → coordinator → registered RuntimeCommitService`. Current v2 contract uses `merged` for new disjoint landings and preserves `rebased` historically. Agent source/test equal captured `cef8`; exact receipt status remains UNKNOWN without existing safe receipt fields.
- `test_prepared_video_public_preview_accept_retry_undo_and_no_write`: line 249 fails before behavior because expected Runtime `8ea0766f...`/tree `6047ac...`, while current read-only Runtime is `6634a17f...`/tree `47b376...`. This is a pin mismatch, not product evidence.

The six shared M1 bootstrap errors remain separate and were not attributed to these two assertions.

Static checks:

- AST/in-memory compile: 12 files PASS.
- Ruff: PASS.
- Mypy `astrid/sdk/timeline/inverse.py`: PASS.
- `git diff --check`: PASS.
- No pytest, collection, helper execution, probe, service, browser, render, install, or repair performed.

Commit message and `DONE` marker created.