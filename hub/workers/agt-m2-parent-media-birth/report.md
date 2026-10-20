`clip.add-media` v1 is in and `auto_place_completion` now supports `ownership='parent'`. One `replace` semantic differs from the brief (see Decisions). The targeted run has two failures, which also fail on an untouched checkout. The commit message and `DONE` are written. I could not run lint: `ruff` isn't installed here.

## What I built
- **`clip.add-media` v1** (`astrid/sdk/timeline/native_parent_media_commands.py`): select `parent`, intent `{}`, closed args `{id, track, at, hold, media, from?, to?, speed?, replace?}`.
  - `at` is seconds, quantized once to a frame at the pinned rational fps. Hold is in source seconds, and a video window `[from, to)` must equal it and fit the verified media.
  - The track must be an active visual output track. A track that any occurrence names as its lane refuses with `unsupported_ownership`.
  - The registry alias is created as a recorded write when absent, and must match the exact binding when present.
- **`replace`** names a populated clip on the same track. It is removed under the same relation guards as `clip.delete`, and the new clip is appended.
- **Schema (additive):** a new `ClipAddMediaArgs` def and a `clip.add-media` branch in `EditCommand`. The Runtime artifact needs regenerating for these two additions; that is the follow-up you mentioned. `commit.py` now verifies the pin for this op too.
- **`auto_place_completion(..., ownership='parent', track=...)`** uses the same anchor-after rule on that track from frame 0. A missing anchor falls back to the track end, and an empty track starts at 0. It emits `clip.add-media` (image 5 s hold, video window `0..d`).
- **Supporting changes:**
  - Inverse (`inverse.py`): the removed parent clip leaves the config mirror before the alias-dependents check.
  - Parent registry address (`_command_state.py`): the parent asset address follows the real registry location, `parent.registry` when present, else `parent.config.registry`. Both present refuses. Real parent documents keep a direct registry, so the old fixed `config` address would not have worked.
  - `_ordinary_create` (`_collections.py`): accepts a removal beside the create.
  - `delete` (`_delete_commands.py`): split into a `removable` guard plus the clear, so `replace` can reuse it.
- **Tests:** `tests/editing_conformance/test_recipe_m2_parent_media.py` has 39 cases: image and video, replay, inverse and redo, the golden, create-or-require, 22 refusals, replace, ABA and dependents, rebase, provider reload and retired ids, and the builder. The golden is `fixtures/recipe_m2_parent_media.json`. I also added a "Parent media birth" section to `docs/design/m2-auto-placement.md`.

## Test evidence
- `bin/request-test agt-m2-parent-media-birth targeted --files "tests/editing_conformance tests/timeline tests/sdk"` gave 3892 passed, 2 failed, 6 skipped, 15 xfailed.
- The 2 failures are `tests/sdk/test_timeline_occurrence_delete_provider.py::test_provider_equal_state_and_aba_child_publications_refuse_stale_delete[False/True]`. They fail the same way with all my edits to existing files reverted to HEAD, so they are not mine.
- After restoring my edits, a local run of the new parent-media, auto-placement, occurrence-media and clip-delete files gave 177 passed. The first two have already been in the central run above.

## Decisions
- **`replace` appends instead of keeping the slot.** I first tried creating the new clip right after the target and then removing the target, so the new clip would take its position. The inverse re-runs the recorded create-after selection against a state where that target is gone, and it errors. Undo still restores the removed clip at its original position. If clip-array order matters for z-order, this needs a deeper inverse change. I did not do it, so this is a gap against "keeping ordered ids".
- **`replace` is in the args, not the command's `intent`.** Intent must equal the operation's fixed intent, so args made it replayable without changing that.

## Not done or unverified
- The occurrence video birth still has no exclusive-owner re-check at replay, as the earlier report noted.
- I did not check the `_ordinary_create` loosening against Runtime or App; it is covered only by the suites above.
- I left the shared-occurrence builder (`auto_place_shared`) alone; it is still occurrence-only.
