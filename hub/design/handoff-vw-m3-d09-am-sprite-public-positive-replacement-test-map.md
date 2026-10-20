# AMsprite replacement proof map

| Requirement / existing positive | New direct public12 evidence | Remaining caller work |
|---|---|---|
| Raw x4212/y20/width16/scale8 audit | test_compiled_sprite_bounds_keep_logical_units_and_source; test_compiled_sprite_editor_units_snap_once | Original raw private bbox was not rendered geometry; do not reproduce it |
| SDK OFFCANVAS / deliberate runner | test_public_sprite_offcanvas_run_in_mixedscale_and_integrity_addresses, plus actual registered SSR positions | Agent owner joins exact prepared occurrence rows; original SDK test stays unchanged |
| SDK MIXED-SCALE | Same test: simultaneous scale8 size128 vs scale6 size96 on same 16px art | Agent owner retains existing address/duration formatting |
| SDK DAMAGED-ART source .70/.56 | Same test: explicit source_clip_id + occurrence + selected asset provenance | Source integrity is data, not alpha; Agent owner retains .10 outline-free style rule |
| True unknowns | test_known_sprite_bounds_do_not_invent_media_alpha; test_sprite_missing_dimensions_and_decorations_stay_unknown; test_sprite_unsupported_outer_geometry_stays_unknown | No fabricated presence/opacity/support |
| Registered rendering and source selection | test_sprite_registered_ssr_preserves_drawing; test_sprite_renderer_selected_source_wins_over_static_fallback; test_sprite_stepped_strip_and_hidden_frames_use_the_draw_clock | SSR is not browser/pixel parity |
| Actual package and type seam | test_sprite_public12_declarations_and_installed_bytes; reused host_project audit | Public12 archive unchanged, no public types/package change |

Existing tests/packs/rendering/test_scene_host.py and tests/sdk/test_timeline_checkout.py::test_check_flags_offcanvas_mixed_scale_and_damaged_sprite_by_address run unchanged. No tests are removed, skipped, xfailed or rewritten to expect lost behavior. No SDK caller is activated in this patch.
