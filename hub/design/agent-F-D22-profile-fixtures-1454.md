# F-D22 profile-fixtures-1454 handoff

Status: **qualified with a test-support correction; six failures preserved and classified**.

Base Agent: `58316fd6e0ce8a1fb3b2b3826ec71906d29080de`.

Profile: Runtime `3b926efab2eed122d374540baee297d4cdcec62a`, Node `v20.19.4`,
Composition `0.0.14`, archive `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

## Correction

Updated only existing profile-related test support:

1. backend fixture package assertion 0.0.13 → 0.0.14;
2. layer-tail duration module old chunk `SE4TPVLW` → current archive chunk
   `A6LVBEHN`;
3. typecheck mapping parser ignores fixed Composition imports and validates
   the current public registry when no hashed host imports exist;
4. AM plate host fixture uses the locked 0.0.14 archive SHA
   `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` and
   80-file body.

Product source, contract, lock, archive, generated files, pins, dependencies,
and environment were untouched.

## Exact qualification

Command prefix:

```text
env PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/bin:/bin /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider
```

It was followed by the exact 40 inventory nodes below:

```text
tests/packs/rendering/test_remotion_backend.py::test_manifest_command_runs_from_owning_pack_root
tests/packs/rendering/test_remotion_backend.py::RemotionBackendRegistryGenerationTest::test_registry_generation_regenerates_when_generated_output_is_missing
tests/packs/rendering/test_remotion_backend.py::RemotionBackendRegistryGenerationTest::test_registry_generation_regenerates_when_state_hash_differs
tests/packs/rendering/test_remotion_backend.py::RemotionBackendRegistryGenerationTest::test_registry_generation_uses_pack_registry_and_composition_env
tests/packs/rendering/test_remotion_backend.py::RemotionBackendRegistryGenerationTest::test_remotion_render_env_is_explicit_not_host_inherited
tests/packs/rendering/test_remotion_backend.py::RemotionBackendRegistryGenerationTest::test_render_provenance_matches_registry_and_local_overlay_discovery
tests/packs/rendering/test_remotion_backend.py::RemotionBackendRegistryGenerationTest::test_render_regenerates_registries_before_remotion_and_writes_props
tests/packs/rendering/test_remotion_backend.py::RemotionBackendRegistryGenerationTest::test_render_registry_cache_tracks_element_edits_and_missing_outputs
tests/packs/rendering/test_remotion_backend.py::RemotionBackendRegistryGenerationTest::test_render_removes_staged_assets_and_props_after_remotion_failure
tests/packs/rendering/test_remotion_backend.py::RemotionBackendRegistryGenerationTest::test_render_stages_only_used_effect_assets_and_removes_them_after_success
tests/packs/rendering/test_remotion_layer_tail_compat.py::test_fully_covered_pre_tail_layer_window_keeps_legacy_native_positive
tests/packs/rendering/test_remotion_layer_tail_compat.py::test_fully_covered_pre_tail_root_callback_accepts_native_extent
tests/packs/rendering/test_remotion_layer_tail_compat.py::test_ordinary_full_tail_and_no_clock_controls_remain_distinct
tests/packs/rendering/test_remotion_layer_tail_compat.py::test_legacy_service_keeps_covered_pre_tail_output[0-30]
tests/packs/rendering/test_remotion_layer_tail_compat.py::test_legacy_service_keeps_covered_pre_tail_output[150-165]
tests/packs/rendering/test_remotion_layer_tail_compat.py::test_middle_pre_tail_window_keeps_absolute_clips_and_tail_outside_output
tests/packs/rendering/test_remotion_layer_tail_compat.py::test_unlayered_original_clock_native_windows_unchanged[0-30]
tests/packs/rendering/test_remotion_layer_tail_compat.py::test_unlayered_original_clock_native_windows_unchanged[150-165]
tests/packs/rendering/test_remotion_layer_tail_compat.py::test_unlayered_original_clock_native_windows_unchanged[300-330]
tests/packs/rendering/test_remotion_layer_tail_compat.py::test_support_and_locked_props_keep_pre_tail_positive[0-30]
tests/packs/rendering/test_remotion_layer_tail_compat.py::test_support_and_locked_props_keep_pre_tail_positive[150-165]
tests/packs/rendering/test_remotion_layer_tail_compat.py::test_remotion_typecheck_mappings.py::test_every_scope_the_generator_emits_is_declared_and_mapped[effects]
tests/packs/rendering/test_remotion_typecheck_mappings.py::test_every_scope_the_generator_emits_is_declared_and_mapped[animations]
tests/packs/rendering/test_remotion_typecheck_mappings.py::test_every_scope_the_generator_emits_is_declared_and_mapped[transitions]
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_prepared_real_plate_background_picture_and_gap[False]
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_prepared_real_plate_background_picture_and_gap[True]
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_prepared_empty_raw_plate_stays_unknown
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_registered_plate_ssr_preserves_existing_draw_and_default_theme
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_managed_transparent_image_has_opaque_backing_without_media_alpha_proof
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_real_plate_fade_dip_and_translucent_gap
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_real_plate_wipe_mosaic_pan_and_tint_keep_the_painted_backing
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_unproven_backing_cannot_claim_opaque_coverage[params0]
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_unproven_backing_cannot_claim_opaque_coverage[params1]
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_unproven_backing_cannot_claim_opaque_coverage[params2]
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_unproven_backing_cannot_claim_opaque_coverage[params3]
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_public12_outer_geometry_gap_does_not_erase_original_positive[outer0]
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_public12_outer_geometry_gap_does_not_erase_original_positive[outer1]
tests/packs/rendering/test_am_snap_plate_scene_capability.py::test_public12_outer_geometry_gap_does_not_erase_original_positive[outer2]
tests/editing_conformance/test_compile_contracts.py::test_audio_vector[fade-in-needs-prepared-envelope-source]
tests/editing_conformance/test_compile_contracts.py::test_audio_vector[fade-out-needs-prepared-envelope-source]
```

Result: **34 passed, 6 failed, 1:50.75**.

Preserved failures and owners:

- backend raw-manifest node: sanitized child cannot import `runtime_protocol`;
  D18 invocation/child-environment owner;
- three `public12_outer_geometry_gap_does_not_erase_original_positive` nodes:
  current 0.0.14 source returns `GAP` for evaluated crop/entrance geometry;
  Composition/profile owner;
- fade-in and fade-out compile vectors: projection has no
  `audio.render_source`; trusted-host prepared-envelope owner.

The original SSR/painted-backing positives and negative controls pass under
the current profile. Assertions were not weakened, skipped, or xfailed.

## Checks

`git diff --check`, changed-test `compileall`, and the repository Ruff baseline
passed. Ruff baseline stayed exactly `2149`. Mypy baseline could not execute
in the shared venv because `types-PyYAML` is absent and one NumPy stub requires
Python 3.12+; expected baseline is `1912`. No dependencies were installed.

Changed test body hashes are recorded in `report.md`; lock/archive hashes are
unchanged and equal to the profile values.
