# AM snap plate replacement map

Repository root: /home/user/work/wt/vw-m3-d09-am-plate-public-positive
New direct file: tests/packs/rendering/test_am_snap_plate_scene_capability.py

All original tests remain unchanged and passed in the final targeted run. This is component capability qualification, not installation of a replacement in SDK check or another caller.

| Existing positive | New installed-public12 evidence | Status |
| --- | --- | --- |
| tests/core/timeline/test_onscreen.py::test_coverage_run_length_encodes_covered_gap_and_covered_but_empty | test_prepared_real_plate_background_picture_and_gap, both normal and owner-qualified dispatch: actual AM image and explicit #F7F4ED filled plate, CONTENT / GAP / EMPTY / half-open end, projected occurrence IDs | Qualified at final prepared Root props; no check caller deletion authorized |
| tests/sdk/test_coverage_empty_cut.py::test_a_cut_left_with_only_a_background_plate_is_not_valid | Same actual filled AM plate gives COVERED/EMPTY, not the custom rectangle probe | Component answer qualified; exact check formatting/cut duration and intentional hold remain in unchanged SDK tests, not replaced |
| tests/core/timeline/test_onscreen_more.py::test_a_one_sided_fade_is_a_dip_during_the_ramp_then_covered | test_real_plate_fade_dip_and_translucent_gap: actual AM plate gives DIP during fade_in, opacity .5 at its midpoint, then COVERED/CONTENT | Qualified at prepared Root props |
| tests/sdk/test_coverage_empty_cut.py::test_a_translucent_plate_does_not_cover_the_canvas | test_real_plate_fade_dip_and_translucent_gap: known AM support and .4 opacity yield GAP | Qualified at prepared Root props; diagnostic caller unchanged |
| tests/core/timeline/test_onscreen.py::test_a_cropped_plate_and_an_inset_are_not_full_frame_but_a_default_plate_is | Default AM backing is known/full-frame. test_public12_outer_geometry_gap_does_not_erase_original_positive retains the private cropped-plate positive alongside public12's explicit unknown-animation-geometry | Cropped element positive BLOCKED by immutable public12 evaluator; footage inset outside this grant |
| tests/core/timeline/test_onscreen_more.py::test_a_scale_in_entrance_is_not_full_frame_during_its_duration_but_keeps_its_opacity | Same direct gap test retains full_frame=False / opacity=1 private positive; actual prepared public12 answer stays UNKNOWN | Outer scale-in positive BLOCKED by package evaluator |
| tests/core/timeline/test_onscreen_more.py::test_a_fade_up_entrance_ramps_opacity_and_keeps_full_frame | Same direct gap test retains opacity=0 / full_frame=True private positive; actual prepared public12 answer stays UNKNOWN | Outer fade-up positive BLOCKED by package evaluator |
| Actual AM enter/exitWipe, mosaic, tint and pan backing | test_real_plate_wipe_mosaic_pan_and_tint_keep_the_painted_backing | Qualified; these component params do not qualify clip.entrance / clip.exit wrappers |
| Actual source with alpha | test_managed_transparent_image_has_opaque_backing_without_media_alpha_proof: materialized transparent PNG passed through the real source projector/materializer/final callback, URL server doubled | Qualified backing support only; no assertion that media pixels are opaque |
| Existing component/default theme drawing | test_registered_plate_ssr_preserves_existing_draw_and_default_theme: 10 variants × 9 frames, hashes captured before the product edit; immutable public DEFAULT_THEME equality | 90 SSR samples preserved; no decoded-pixel or browser claim |

Still required for D09: public package-owned crop and outer entrance/exit evaluation preserving the existing positives, then the separately owned exact SDK checkout/source/caller join. No private fallback was removed, no test was weakened, and there are no new skip/xfail markers.
