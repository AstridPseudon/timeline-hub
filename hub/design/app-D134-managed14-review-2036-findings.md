# D134 managed14 independent source findings

## Verdict

`PASS_UNAPPLIED`: the completed source finding is independently supported. The
three authorized files are unchanged; no source merge is recommended.

## Exact finite findings

All 14 selected nodes have the same finite setup seam (`S1`): the source starts
from an empty semantic birth, then attempts to restore the authored shot root
containing `item-1` through a generic whole-root patch. The current registered
semantic routes can preserve that item only when an authenticated item-bearing
source already exists; they do not create it from the empty birth.

1. `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[image-False]` — `S1`.
2. `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[image-True]` — `S1`.
3. `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[video-False]` — `S1`.
4. `tests/editing_conformance/test_commit_runtime_video_unplace.py::test_capture_commit_reload_undo_redo_and_restart_safe_retry[video-True]` — `S1`.
5. `tests/editing_conformance/test_recipe_m2_auto_placement.py::test_exact_capture_replay_inverse_and_redo[image-absent]` — `S1`.
6. `tests/editing_conformance/test_recipe_m2_auto_placement.py::test_exact_capture_replay_inverse_and_redo[image-anchor]` — `S1`.
7. `tests/editing_conformance/test_recipe_m2_auto_placement.py::test_exact_capture_replay_inverse_and_redo[video-absent]` — `S1`.
8. `tests/editing_conformance/test_recipe_m2_auto_placement.py::test_exact_capture_replay_inverse_and_redo[video-anchor]` — `S1`.
9. `tests/editing_conformance/test_recipe_m2_auto_placement.py::test_provider_accepts_completion_placement_with_exact_undo_and_redo[image]` — `S1`.
10. `tests/editing_conformance/test_recipe_m2_auto_placement.py::test_provider_accepts_completion_placement_with_exact_undo_and_redo[video]` — `S1`.
11. `tests/editing_conformance/test_recipe_m2_placement_create_unplace.py::test_exact_capture_replay_inverse_and_redo[create]` — `S1`.
12. `tests/editing_conformance/test_recipe_m2_placement_create_unplace.py::test_exact_capture_replay_inverse_and_redo[unplace]` — `S1`.
13. `tests/editing_conformance/test_recipe_m2_placement_create_unplace.py::test_provider_accepts_create_with_exact_undo_and_redo` — `S1`.
14. `tests/editing_conformance/test_recipe_m2_placement_create_unplace.py::test_provider_accepts_unplace_with_exact_undo_and_redo` — `S1`.

## Route audit

- Registration is finite in `astrid/sdk/timeline/commands.py:29-115`. It includes
  `occurrence.create`, `shot.set`, occurrence media, placement, duplicate,
  fork, shared placement, `timeline.duplicate`, `timeline.restructure`, and
  generic `doc.patch`.
- `occurrence.create` creates `payload.items: []` and an empty internal timeline
  (`astrid/sdk/timeline/native_occurrence_create.py:40-50`). Its args contain
  occurrence/shot identity, name, track, time, and duration only.
- `shot.set` writes only `payload.name` and bounded `payload.settings`
  (`astrid/sdk/timeline/_shot_commands.py:12-41`); there is no item insertion.
- `occurrence.add-media` creates an occurrence clip and asset binding
  (`astrid/sdk/timeline/native_occurrence_media_commands.py:207-222`). Its
  payload-media helper only replaces `media_id` on an existing item whose
  identity is already present (`:69-82`). `placement.create` delegates to that
  path (`astrid/sdk/timeline/native_placement_commands.py:81-100`), while
  `placement.unplace` removes a clip (`:102-119`). Neither creates shot items.
- `doc.patch` allocation records cover parent/internal tracks, clips, and asset
  aliases, not shot payload items (`astrid/sdk/timeline/_doc_patch.py:303-328`).
  The item map requires the exact pre-authenticated item identity set and
  rejects correspondence changes (`astrid/sdk/timeline/_command_state.py:341-369`).
  This is the missing semantic record, not merely a blanket membership refusal.
- `occurrence.duplicate` and `occurrence.fork` copy an existing occurrence's
  authenticated shot payload (`native_occurrence_duplicate.py:17-29,48-61`;
  `native_occurrence_fork.py:21-36`). `occurrence.place-shared` reopens an
  existing source (`native_occurrence_shared.py:304-325`). These are faithful
  only after an item-bearing source is already present.
- `timeline.duplicate` requires a Runtime-authenticated foreign source closure
  and an empty destination (`native_timeline_duplicate.py:23-65`); the exact
  caller supplies no such source reference. Using one would introduce a new
  cross-timeline source/history, which is outside this setup-only review.
- `timeline.restructure` requires the authenticated current closure and derives
  child roots from that closure; it explicitly does not accept caller-supplied
  child payloads (`native_restructure.py:15-44`). It cannot manufacture the
  missing item from an empty birth.

## Passing source comparator

The existing occurrence-media comparator is the faithful positive boundary:
`tests/editing_conformance/test_recipe_occurrence_media.py:90-116` applies the
registered media-swap path to a document that already contains `item-1` and
asserts that the item remains while only its media binding changes; the scoped
birth/replay comparator is at `:128-149`. This demonstrates the supported
preservation case and its precondition. It does not prove item creation from an
empty shot. The comparator was inspected only; no test body was run under this
brief.

## Missing capability and records

The smallest missing source capability is a registered semantic birth/restore
that consumes an authenticated item-bearing closure or equivalent authored
child source, allocates `item-1`, and records the source/item map, media pin,
and managed occurrence/shot edges. The current source has no such command or
accepted record. The owner is `unknown_unproved`; this review does not assign
implementation ownership or propose a schema/product change.
