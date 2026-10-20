**Verdict: APPROVE, for the inactive seam only.** No blocking defect found. The branch does not satisfy the D09 source-identity join and does not activate anything. Both remain open Agent-owner work.

Review written to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-live-scene-join-r2.md`. `DONE` is created. No repo changes and no commit-msg.

## What I checked
- **Diff:** merge-base `86d7cf9b1f…` against `tl/vw-m3-live-scene-join-r2`. It is 3 files, +351/−5. The files are `composed_frame.py`, `overlays/labels.py` and the new `tests/packs/rendering/test_capture_scene_labels.py`.
- **Save path:** no scene evaluation there. The only new `host_frames_at` call is inside `CaptureSceneLabels.observe`, which nothing calls.
- **Authority:** no source, provider, compiler or pin change in product code. The public12 artifact appears only in test env defaults.
- **Inactive:** no production caller. `overlay_labels_frame` is called without `capture=` at `fast_lane.py:742` and `layers/builtin.py:507`, so those keep the legacy path.
- **Advisory unknowns:** unknown visibility, opacity or bounds go to the legend as text. Query unavailability raises by design, so no stale facts are shown.
- **Legacy behaviour:** the old `Visible` items have no `visible` attribute, so the `getattr` default keeps the legacy boxed/legend split unchanged.
- **Identifiers:** no colon parsing and no second projector. Addresses come from the owner-supplied map, and `observe` requires exact ID-set equality with it.
- **Tests:** the 20 named cases exist. `grep` finds no skip, xfail or fails markers.

## Gaps (not blocking)
- **D09 identity is not met by this seam, and it does not claim to be.** `props`, `basis` and `source_identity` are accepted as the caller gives them. `source_identity` is an opaque string. The join stays held.
- **Failed first `observe` leaves the adapter "already used".** `_frames` is set before validation, so a retry reports the wrong cause.
- **Malformed props raise `KeyError`** rather than `SceneQueryUnavailable`.
- **`retain` checks keys and file existence only.** The report already accepts this as an owner-attested limit.

## Wiring still needed (Agent-owned)
1. Bind the source in `prepare_filmstrip` and `RemotionFrameProvider` (`filmstrip_execution.py` ~1771). Use the same retained revision, candidate and closure, plus the projector's exact address map.
2. Derive the basis from `_canonical_profile` on the same frozen inputs.
3. `tl/integration` already has `on_scene_props` in `run.py` at lines 1035, 1169, 1387 and 1425, called as `(merged_props, frame_numbers)`. That matches `observe`. The callback must validate the final props, and it must pass sorted, unique frames.
4. Create a new adapter per invocation in both renderer capture paths. Call `retain` only with the complete fresh map.

Public12 adoption is a separate owner prerequisite, since production still pins public10.

## Unverified
I did not run the tests. The branch is not checked out in my worktree, and this was a read-only review. Viewing's claimed results (53 passed, lint, `git diff --check`) are unverified here. The central targeted lane should confirm them.
