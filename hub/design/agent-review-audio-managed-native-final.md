# Agent native audio / WC5 dependency review

## Verdict

**APPROVE bounded native managed-audio authoring and the pure trim helper
semantics at candidate `ddaaf0d6de36bcc9c3305c5051a393bd424950fe`, tree
`99aec595603c8016a780bacc81ea2263ca3edb67`.** This is not approval that WC5
is fully restored, and it is not approval of the old publisher cut as complete.

The candidate preserves the existing five-field `MediaSelection` carrier.
Runtime `selected_media` remains the authority: it requires the exact declared
pin, validates the complete five-field identity, checks project/realm scope and
the generation/variant/object binding, and reconstructs `VerifiedMedia` from
managed generation metadata and the managed object. Audio admission accepts
only positive `audio/*` metadata and intrinsic duration; native add/swap
requires an active explicit audio track, uses the existing `clipType: media`
carrier, requires source-window length to equal authored source-time hold and
fit the server duration, and preserves positive speed/boundary checks. Trim
requires the active raw audio track and audio registry asset, keeps source-time
hold distinct from playback speed, uses the existing interior rounding helper,
and records the exact verified input in the dependency when the registry lacks
duration. The original image/video paths and their guards are unchanged by the
candidate.

The pure fallback is not an authority shortcut. It only accepts one exact
matching object identity, refuses missing or unequal duplicate matches, checks
kind/size, and requires positive `duration_seconds`; it must not be exposed as
a way to trust forwarded metadata or choose a latest/ambiguous object. A real
provider path for this fallback must call server `selected_media` only for a
declared complete pin, verify the returned asset/object against the original
registry source, and record that exact server input.

## Evidence

- The candidate’s real provider case settles three normal managed `audio/wav`
  outputs with valid PCM WAV bytes, obtains the exact Runtime selections,
  admits `clip.add-media` on a parent `voiceover` audio track, reads the CAS
  bytes back as WAV, reloads, retries the same request, and completes guarded
  undo/redo. Prior candidate evidence: `1 passed, 36 deselected` for the
  actual case and `117 passed` for the trim semantics file.
- Review rerun, bounded only to the requested negative/trim/inverse cases:

  ```text
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py -k 'test_refusals_preserve_input' tests/editing_conformance/test_recipe_occurrence_media.py -k 'test_refusals_preserve_input or test_disjoint_edit_rebases_but_same_value_asset_write_blocks_undo' tests/editing_conformance/test_recipe_m2_clip_trim.py -k 'test_audio_trim or test_trim_hold_is_source_time or test_rational_fps_source_contact or test_replay_consumed_source_identity_bounds or test_source_metadata_is_required_and_maps_refused or test_bad_closed_bounds_is_atomic or test_unsupported_shapes_refuse_without_mutation'
  ```

  Result: `45 passed, 216 deselected`.
- Review rerun of the one actual WAV/provider case:

  ```text
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_commit_runtime_parent_media.py -k real_managed_audio -m integration
  ```

  Result: `1 passed, 36 deselected`.
- `ruff check` on all candidate-touched Agent/test files: `All checks passed!`.
- `git diff --check`: passed. No full, matrix, browser, live-socket, or extra
  golden suite was run.

## Remaining bounded constraints

1. **Actual producer child scope is not proven by the parent case.**
   `astrid/packs/video_editing/shared/draft_voiceover.py:345-357` creates or
   mutates a `draft-vo` audio track inside each shot’s internal child timeline,
   updates the child registry/clip, and the current branch still publishes the
   whole candidate through `bound.publish` at `:472-475`. The reviewed test
   creates a parent-level `voiceover` track with `capture_track_create`; it does
   not prove native `track.create` plus occurrence/child-scope ownership for the
   producer’s actual path. The sibling WC5 proposal-cut commit is not an
   ancestor of this candidate. Keep this as the minimum remaining voiceover
   constraint; do not claim WC5 fully restored or the old publisher cut
   complete.

2. **Historical legacy audio trim remains strict OPEN.** The pre-cut
   `music-bed` object is an old audio registry object without a managed
   generation/variant/object selection tuple. There is no valid complete
   `MediaSelection` for it, so do not invent catalog adoption and do not turn
   the old positive into a refusal assertion. A future legacy-trim completion
   needs the already-described exact declared carrier, server-only
   `selected_media` reconstruction, complete pin/asset/object guards, and the
   exact server input recorded through inverse/replay. Until then, only the
   managed-source positive and the pure helper fallback are approved.

