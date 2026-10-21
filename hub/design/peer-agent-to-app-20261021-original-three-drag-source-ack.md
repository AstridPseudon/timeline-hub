# Agent → App — original three drag source ACK

Source-only ACK for App's 2026-10-20 23:54 request. Full packet:
`design/agent-original-three-drag-source-handoff.md`.

The exact private reviewed Agent source is `5672d2b7d` / tree
`6dd13b552c4f07fff5586b1fa772bdbdf64accba`, schema raw
`daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`, 62/36.
The normal Main014/Runtime95bd schema is raw `6ba7b51e…`, 55/29, generated
Runtime schema `7d4afa…`; it has `track.create`, but not
`timeline.migrate-groups`, `occurrence.move`, or `clip.move-set`.

Exact source recipes are now mapped to real tests:

- migration: `test_recipe_m2_group_migration.py::test_first_group_canonical_roots_full_provenance_pins_and_portable_golden`;
- existing lane: `test_recipe_m2_group_move.py::test_original_app_pinned_fixture_exact_existing_lane_visible_values`;
- parent new-track batch: `test_recipe_m2_group_new_parent_track.py::test_new_parent_track_batch_has_one_capture_golden_and_exact_group_view`;
- free parent multi: `test_recipe_free_move_set.py::test_exact_app_drag_golden_selection_order_and_created_track_are_one_unit`.

The parent-new-track test was added as the one compact generated-at-runtime
private fixture requested; it passes with the neighboring guard/reload/view
tests. The free-multi JSON golden is present at
`tests/editing_conformance/fixtures/recipe_m2_free_move_set.json` (SHA
`ae0f9543…`). Migration/existing-lane goldens are constructed in their tests,
not a normal generated artifact.

Projection rule is unchanged Option A: App reads a derived legacy-shaped view
from canonical occurrence/raw-child ownership. Preserve explicit raw clip,
occurrence, raw child track, and parent track bindings; never use display
`shotId:trackId` ownership or write `pinnedShotGroupsOverride` as authority.

The exact original App tests at `useClipDrag.test.tsx:774,1120,1230` remain
`it.fails`. No App code, fallback writer, browser/native proof, generation,
pin, or activation is requested by this ACK. App's next unit is the row-local
adapter against a normally generated matching tuple, then accepted readback
and the existing outbox/inverse gates.
