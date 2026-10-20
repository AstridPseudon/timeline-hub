`auto_place_shared` is done for placed media, but two pieces of shared placement are blocked because no existing op can write them. Pooled placement, `keepAsPooled` and promotion are not built. Appending past the occurrence window always refuses. I created `DONE` and left the commit message in place.

## What I built
- **Builder:** `auto_place_shared` and `unplace_shared` in `astrid/sdk/timeline/native_auto_placement.py`, next to the step 1 completion builder. Both are pure and use only `placement.create`, `placement.unplace` and `occurrence.add-media`.
- **Owner:** the occurrence that exclusively owns its shot, per option A. A shot used by two occurrences, a display ID, `ownership='shared'` or a non-empty `pinnedShotGroups` all refuse. The last one refuses with `migration_needed`, so ownership is never inferred.
- **Hold:** 4 s for image and video. Completion stays at 5 s. Video authors the source window 0..4.
- **Append:** a `frame=None` call starts after the greatest end frame over all clips in the shot, on any lane. An empty shot starts at the occurrence start.
- **Explicit frame:** clamped at 0, then shifted +1 while a clip's start frame in the shot is equal. Overlapping intervals are allowed.
- **Lane:** the anchor's lane if the anchor is in the shot, otherwise the occurrence lane. The anchor never moves the start.
- **Captures:** each one records the resolution, lane, extent or skipped frames, and the start frame. The exact completed variant stays bound, never the gallery primary or the latest.

## Tests
- **New file:** `tests/editing_conformance/test_recipe_m2_shared_auto_placement.py`, with golden `fixtures/recipe_m2_shared_auto_placement.json`. It has 30 passing tests and 2 strict xfails.
- **Coverage:** append, lane inheritance, shift, isolation, refusals, replay when the anchor moved or a clip was deleted, guarded undo/redo, and the provider round trip.
- **Command:** `bin/request-test agt-m2-auto-placement-step2 targeted --files "tests/editing_conformance"` gave 1335 passed, 4 skipped, 7 xfailed. The 7 xfails include my 2.
- **Lint:** `ruff check` passes on the changed files. I did not run `make check` or request a full suite.

**App RED parity:** the Agent-side expectations match: video append lands at frame 120 at 30 fps, the group lane is inherited, and a duplicate start shifts 30 → 31 with overlap allowed. The pooled-membership test and the `keepAsPooled` test in that patch are not met.

## BLOCKED
Both entries are also in `design/m2-auto-placement.md`. I invented no writers.
1. **Pool membership** (null frame, `keepAsPooled`, promote):
   - The canonical model has no pool representation. Group migration keeps `poolGenerationIds` only inside opaque provenance.
   - Proposed op `shot.pool` v1, select `occurrence:<id>`, args `{"action": "add"|"remove", "media": <five-field pin>}`.
   - Promote would be a birth command plus `shot.pool remove` in one batch.
   - `pooled=True` and `keep_as_pooled=True` refuse with `unsupported_pool`. Two strict xfails keep the legacy expectation.
2. **Appending past the occurrence window:**
   - Group migration sets `duration_ms` to the member span, so every real append refuses with `occurrence_boundary`.
   - Proposed op `occurrence.set-extent` v1, select `occurrence:<id>`, args `{"duration_ms": <positive number>}`, guarded on the old value.
   - My tests widen the window to get around this.

## Decisions and caveats
- **Short video:** the legacy 4 s video hold ignored media length. A native row authors a 0..4 window, so media shorter than 4 s now refuses. This is a deliberate difference.
- **Image on a non-home lane:** `placement.create` always uses the occurrence lane, so an image anchored on another lane goes through `occurrence.add-media`.
- **`unplace_shared`:** it only removes the image expression and keeps the registry binding. It does not remove registry membership, and video is not covered because `placement.unplace` v1 is image-only.
- **Group migration not in this base:** `timeline.migrate-groups` is on the `tl/agt-m2-group-*` branches. My fixtures use the canonical occurrence/shot shape directly, so the migration-to-placement path is untested end to end until that branch merges.
- **Not verified:** I did not run the Runtime schema/provider pair or any App test. `placement.create` is missing from Runtime's schema, as the gap doc says.
