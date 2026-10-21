# D09 current assertion map

This is the revised one-to-one map for the 14 tests in
`tests/core/timeline/test_onscreen.py` (3) and
`tests/core/timeline/test_onscreen_more.py` (11). It is an assertion
disposition, not deletion approval. The Agent base inspected here is
`5c5173dcb57669a9d43e5add2674543333f1c6d2`.

Evidence labels:

- **CURRENT** means the test is on the Agent base above and exercises the
  current active surface.
- **DONOR** means a committed test/source branch was inspected, but is not an
  ancestor of this base. It must not be described as integrated.
- **SOURCE14** means the approved Composition14 source review only; it is not
  a published package or a current Agent public proof.
- **HELD** means the candidate is source-owner evidence with an unresolved
  qualification boundary.
- **MISSING** means the old assertion still has no current-base replacement.

| Old test and assertion | Exact named evidence | Current disposition and remaining assertion |
| --- | --- | --- |
| `test_visible_at_lists_layers_top_first_with_role_and_opacity_product`: three-layer top-first order, roles, and clip × track opacity (`0.4`, `0.5`) | **CURRENT:** `tests/packs/rendering/test_scene_host.py::test_native_host_preserves_root_painter_order_and_current_roles`; `tests/packs/rendering/test_scene_answers.py::test_resolved_painter_order_and_compiled_payload_are_preserved`. **DONOR:** public13 join `0b08c6847` adds the `0.5 × 0.8 = 0.4` assertion. | **PARTIAL.** Current public order is canonical bottom-to-top (`picture`, `content`), not the private top-first projection. The current base does not assert the opacity product; the donor does, but is not integrated. A three-layer top-first private projection and the remaining opacity assertions are **MISSING**. Do not invert public order. |
| `test_a_cropped_plate_and_an_inset_are_not_full_frame_but_a_default_plate_is`: default full-frame, cropped plate non-full-frame, AM-footage inset non-full-frame | **CURRENT:** `tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_prepared_real_plate_background_picture_and_gap`; `tests/packs/rendering/test_scene_host.py::test_native_host_uses_exact_assets_and_runtime_theme`. **SOURCE14:** `typescript/tests/scene-evaluation.test.ts::scene clip-look uses render crop and builtin entrance geometry with half-open clocks`. **HELD:** corrected AM-footage source `2e9fb6e26`. | **PARTIAL.** The default positive is covered. Composition14 crop is source-only, not a current Agent/public13 proof. The corrected AM-footage candidate uses the valid declared `params.inset` shape, but its owner packet is held for normal resource refresh and Root qualification; it is not a public replacement. Exact crop/inset positives remain **MISSING**. |
| `test_coverage_run_length_encodes_covered_gap_and_covered_but_empty`: `COVERED/CONTENT`, `GAP`, `COVERED/EMPTY`, half-open boundaries, and exact `(0,30)`, `(30,45)`, `(45,90)` spans | **CURRENT:** `tests/packs/rendering/test_scene_answers.py::test_cut_fractional_fps_and_empty_scene_are_answers`; current AM per-frame coverage evidence in `tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_prepared_real_plate_background_picture_and_gap`. | **PARTIAL.** Per-frame classes/content and half-open behavior are evidenced, but no current public carrier asserts the exact consumer-used RLE spans or merge boundaries. The public summary/RLE replacement is **MISSING**. Keep the private consumer assertion live. |
| `test_a_cross_fade_of_two_full_plates_is_covered_not_dip`: independently authored fade-out/fade-in overlap | **CURRENT:** `tests/packs/rendering/test_scene_host.py::test_native_host_passes_public12_compiled_transitions_unchanged`; approved incoming-transition positive `test_actual_am_public_incoming_crossfade_stays_covered` is external evidence. | **INTENTIONAL DIFFERENCE.** Independent element fades are the approved DIP behavior in the retained pixel verification. The incoming-transition `COVERED` positive is a different authored representation and remains required evidence; it is not a replacement for the old independent-fade assertion. |
| `test_a_one_sided_fade_is_a_dip_during_the_ramp_then_covered`: DIP/content, midpoint opacity, then COVERED and half-open GAP, including exact continuous spans | **CURRENT:** `tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_real_plate_fade_dip_and_translucent_gap`; approved external `test_actual_am_one_sided_fade_has_dip_frames_then_coverage`. | **PARTIAL.** Per-frame DIP/COVERED/content behavior is covered, but no current public summary proves the old continuous `(0,15)` / `(15,60)` spans while retaining detailed membership/findings. Exact public RLE remains **MISSING**. |
| `test_a_none_element_is_not_listed`: declared `coverage: none` is omitted from visible layers | **CURRENT:** `tests/packs/rendering/test_scene_answers.py::test_unknown_custom_modifier_and_unresolved_media_stay_unknown`; `tests/packs/rendering/test_scene_host.py::test_unknown_animation_diagnostics_and_root_tail_are_preserved`. **DONOR:** `test_native_host_absent_element_is_not_visual_but_unknown_custom_stays_unknown` in `0b08c6847`. | **MISSING.** The donor distinguishes an actually absent registered component from an unsupported custom element, but retains an invisible diagnostic row. Neither it nor current tests proves declared-`none` omission. Keep the private omission assertion. |
| `test_an_inset_with_layout_is_declared_and_not_full_frame`: declared bounds and exact `(1200,600,1776,924)` | **HELD:** corrected AM-footage direct source tests at `2e9fb6e26` use the valid declared inset shape; Root typecheck remains blocked by unrelated generated `text-card` typing. **SOURCE14:** known clip-look geometry is covered only in the unreleased Composition source test. | **MISSING on the current active surface.** The old raw `{x,y,scale}` fixture is not a valid replacement for the actual AM-footage component. No refusal/`UNKNOWN` substitution is allowed. A public declared-inset proof still requires resource adoption, public-host qualification, and the exact bounds assertion. |
| `test_a_scale_in_entrance_is_not_full_frame_during_its_duration_but_keeps_its_opacity`: early non-full-frame, opacity `1.0`, late full-frame | **SOURCE14:** `typescript/tests/scene-evaluation.test.ts::scene clip-look uses render crop and builtin entrance geometry with half-open clocks`, reviewed at `2f98befde04021a631566e908b639dbc92685e4f`. | **MISSING on current base.** Composition14 is approved source-only. Its known scale-in geometry does not establish the old opacity contract, and no package/public Agent proof is integrated. Keep the private positive and `_timing_evaluators` unchanged. |
| `test_a_fade_up_entrance_ramps_opacity_and_keeps_full_frame`: first-frame opacity `0.0` and full-frame geometry | **SOURCE14:** the same approved Composition14 clip-look test and off-center crop/entrance review. | **MISSING on current base.** The source-only proof covers known fade-up transform geometry, not the old exact full-frame assertion through the current public Agent surface. |
| `test_audio_clips_and_audio_tracks_are_ignored`: audio-only clip produces no visual layers and `GAP` | **DONOR:** `test_native_host_audio_only_track_is_gap_without_visual_layers` in public13 join `0b08c6847` (originating at `a1d659b6b`). | **MISSING on current base; exact donor candidate.** The donor asserts `layers == []`, `coverage == GAP`, and `content is None`, but the test and public13 artifact are not integrated into this base. Do not count it as a current replacement until merged and requalified. |
| `test_element_coverage_reads_metadata_coverage_from_element_yaml`: declared metadata affects role/content; bare and missing declarations return `{}` | **CURRENT:** `tests/packs/rendering/test_scene_host.py::test_declared_background_has_known_empty_content`. **DONOR/source seam:** static role extraction qualification at `4a4725e7e` and its 75-test public-host lane. | **PARTIAL.** Current semantic background/empty behavior is covered. Bare/missing `{}` are private loader details and are retirement candidates only after `onscreen.py` has zero callers; they are not a new public test obligation. |
| `test_the_real_elements_declare_the_picture_roles_coverage_needs`: exact map for `am-snap-plate`, `am-footage`, `am-presenter` | **CURRENT:** `tests/packs/rendering/test_scene_host.py::test_native_host_preserves_root_painter_order_and_current_roles` proves exercised public roles. **DONOR:** static-role extraction qualification at `4a4725e7e`; **HELD:** AM-footage source `2e9fb6e26`. | **PARTIAL.** Current/donor evidence proves role outputs for exercised cases, not the exact three-ID declaration map. AM-footage remains held and has no qualified public-host proof. The exact declaration lookup remains **MISSING**. |
| `test_large_coverage_processes_each_clip_boundary_once`: 300-clip class/content boundaries, exact large RLE, and one call per boundary | **CURRENT:** `tests/packs/rendering/test_scene_host.py::test_large_native_batch_is_not_truncated`; current private `coverage()` remains the source of the exact boundary behavior. | **PARTIAL.** No current public test proves the large class/content interval result or exact RLE. Exact Python boundary call counts are private-only retirement candidates after zero callers, not a public replacement. The large public RLE assertion is **MISSING**. |
| `test_a_declared_non_fade_entrance_on_the_picture_is_a_dip_not_a_gap`: DIP `(0,6)`, then COVERED `(6,30)` | **SOURCE14:** the approved Composition14 clip-look source test covers known entrance geometry only. **CURRENT:** public12 unknown-animation diagnostic remains the nearest current behavior. | **MISSING on current base.** `UNKNOWN`/`unknown-animation-geometry` is an honest refusal, not the old DIP/COVERED positive. Exact public coverage-class spans require a published/adopted capability and a current public test. |

## Disposition and retirement boundary

On the current Agent base: **0/14 complete replacements**, **7/14 partial**
(rows 1, 2, 3, 5, 11, 12, 13), **1/14 intentional difference** (row 4),
and **6/14 missing** (rows 6, 7, 8, 9, 10, 14). The donor-only public13
audio/none and alpha assertions do not change these counts.

The old module and all 14 tests remain live. Current callers remain in Scene
answer preparation, SDK checking/reflow, and visualization labels; no module or
test deletion is authorized. Preserve pixel verification and
`_timing_evaluators.py`. The approved Composition14 source and corrected
AM-footage source are not integrated public proofs.

Mouth and PCM evidence is outside this D09 map and remains unqualified:

- the approved four-still mouth packet is capture preparation, not a completed
  physical/browser certification;
- the PCM/audio physical experiment was explicitly not run and the original
  5/6 result remains red.

Neither may be used to retire a D09 assertion or to claim Gate 6 completion.
