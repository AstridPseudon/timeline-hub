Automatic placement now records every read it consumes as a guard, and the targeted suite is green. The scratch files are outside the worktree, which `rm-own` refused to touch, so I left them. The worktree itself has only the intended edits.

## Changes
- **Guards:** `placement.create` and `occurrence.add-media` take an optional closed arg `consumed` (raw clip IDs). The op reads each row inside the recorder, so every consumed value is a recorded guard.
  - A moved or changed clip now conflicts at replay (`dependency_changed`); a rebuild re-reads the new values.
  - A deleted or reordered clip still refuses through the existing membership guard.
  - An exact retry on the same head replays to identical records.
  - Completion consumes the anchor, or every clip for a lane end. Shared placement consumes every clip of the shot (extent, occupied starts, anchor lane).
- **Exclusive owner:** `occurrence.add-media` now checks the exclusive owner on every branch. A retargeted head refuses at replay with `selection_changed`, from the recorded `placement.owners` selection. A fresh capture still refuses `unsupported_ownership`.
- **Saved intent:** `auto_place_completion` takes `preferred_track`, `fallback_at` (global seconds) and `fallback_track`, and uses them as saved. Lane end and home lane are recomputed only when nothing was saved.
  - A saved `fallback_at` consumes nothing, so a sibling moving does not change the approved start.
  - A deleted saved track refuses (`dependency_changed`); it does not move to another lane.
  - Durations are unchanged: image 5 s, video 5 s when none is supplied, shared 4 s.
- **Goldens and docs:** the two auto-placement goldens are republished, and `docs/design/m2-auto-placement.md` is updated (still-open list included). The goldens for occurrence-media `add` and placement-create `create` also changed, because their records now carry the `placement.owners` selection.

## Tests
- The old tests "replay keeps the recorded start after the anchor/shot moved" (completion and shared) are now "replay conflicts, and a rebuild resolves the new position". The 330→360 anchor case is covered.
- New cases:
  - **Completion:** lane-end 450→480, a clip moving onto the lane, saved fallback and preferred lane, deleted saved track.
  - **Shared:** append 510→540, collision shift 391→392, anchor-lane change, exact retry.
  - **Both:** retarget, so a birth cannot appear through both occurrences.
- `bin/request-test agt-m2-auto-placement-guards targeted --files "tests/editing_conformance tests/timeline"` passed: 1911 passed, 4 skipped, 6 xfailed. `ruff check` on the changed files is clean.
- A wider run that added `tests/sdk` had 6 failures. Four were my retarget assertions (fixed to `selection_changed` and covered by the passing run). The other two are `test_timeline_occurrence_delete_provider::..._refuse_stale_delete[False/True]`, which fail identically on untouched `/home/user/work/agent` at 931d7ec5, so they are pre-existing and not touched by this change. I did not re-run `tests/sdk` after the fix.

## Decisions and caveats
- **Schema change:** the handler cannot read what the builder consumed unless the command says so, and `execute` rejects reads the handler did not make itself. So `consumed` is a schema addition, and the vendored `astrid_runtime_client` types and Runtime artifacts need their normal regeneration (I did not touch them).
- **Whole-row guards:** conflicts can fire on unrelated edits to a consumed clip, for example its volume. That is conservative and acceptable for a conflict.
- **Short media:** a source shorter than 5 s still refuses `unsupported_timing`, which is a newly visible refusal versus the old behaviour. This needs a policy call.
- **Old completion add:** the opacity, volume and manual-track defaults are still omitted and not tested for rendering equivalence.
- **Still open:** parent births, append growth past the occurrence window, video unplace.

Commit message is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-auto-placement-guards/commit-msg`, and the DONE file is created. I did not commit.
