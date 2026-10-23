# F-D22 profile-fixtures-1454

## Result

Qualified the 38 profile-fixture nodes and 2 compile-fixture nodes against
Agent base `58316fd6e0ce8a1fb3b2b3826ec71906d29080de`, Runtime
`3b926efab2eed122d374540baee297d4cdcec62a`, the Node 20.19.4 recipe, and
profile archive `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.

The one PR-sized correction is test-support-only and updates the existing
oracles to the locked Composition 0.0.14 profile:

- backend fixture version `0.0.13` → `0.0.14`;
- layer-tail duration chunk `chunk-SE4TPVLW.js` → the current archive's
  `chunk-A6LVBEHN.js`;
- mapping support now distinguishes generated `?astrid=` host imports from
  Composition-owned imports, and checks the public registry when a kind has no
  generated host imports;
- AM plate fixture now uses the locked 0.0.14 archive and its 80-file body
  rather than the stale public12 77-file body.

No product source, contract, package-lock, archive, generated output, pin,
dependency, or environment installation was changed.

## Qualification commands

Representative six-node pre-repair run: 5 profile/control nodes passed and
the fade-in compile node failed with the original assertion that
`audio.render_source` is absent.

Final targeted command (explicit nodes; no xdist, cache, full suite, browser,
renderer journey, or live socket):

```text
env PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/bin:/bin /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider
```

Explicit node groups were:

- all 10 nodes in `tests/packs/rendering/test_remotion_backend.py` listed by
  the terminal inventory;
- all 12 nodes in `tests/packs/rendering/test_remotion_layer_tail_compat.py`
  listed by the terminal inventory;
- all 3 parametrized nodes in
  `test_remotion_typecheck_mappings.py`;
- all 13 nodes in `test_am_snap_plate_scene_capability.py` listed by the
  terminal inventory;
- `test_audio_vector[fade-in-needs-prepared-envelope-source]` and
  `test_audio_vector[fade-out-needs-prepared-envelope-source]`.
The exact 40 node IDs were:

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

Final result: **34 passed, 6 failed, 1:50.75**.

The six preserved failures are:

1. `test_manifest_command_runs_from_owning_pack_root`: the sanitized raw
   launcher child cannot import `runtime_protocol`; this is a D18 invocation /
   child-environment qualification issue, not a fixture oracle correction.
2. The three `public12_outer_geometry_gap_does_not_erase_original_positive`
   nodes: current Composition 0.0.14 evaluates these outer crop/entrance cases
   as `GAP`, while the unchanged legacy oracle expects `UNKNOWN`.
3. The two audio compile nodes: projection returns no `audio.render_source`
   for parameter fades; the fixture explicitly documents this as requiring a
   trusted-host prepared envelope source.

The 34 passing nodes include all 12 layer-tail nodes, all 3 mapping nodes, all
remaining backend fixture nodes, the real plate SSR/painted-backing positives,
opaque-support negatives, and the remaining compile vectors.

## Source and identity evidence

The profile lock and source archive are byte-identical:

```text
f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d  remotion/package-lock.json
f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d  /home/user/work/runtimes/agent-remotion-v3-819acf-1110/package-lock.json
819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234  remotion/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz
819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234  /home/user/work/runtimes/agent-remotion-v3-819acf-1110/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz
```

Current installed package reports version `0.0.14` and exports
`TimelineComposition`, `prepareCompositionScene`, `prepareScene`,
`querySceneFrame`, `resolveElementRegistries`, and the public theme/registry
surface. Its evaluation export includes `compileAudioEnvelope`,
`encodedEnvelopeSource`, `applyAudioEnvelope`, and the scene query APIs.
The frozen Composition source body hashes inspected were:

```text
typescript/src/index.ts c0cd486aa25b6fbc47def0041866858657e91416847fa2625501eead66cdb4fa
typescript/src/evaluation.ts f99d1c666eefc6a6aa880282ba8b5729de43877b4b439cc805e074522934ae80
typescript/src/scene-evaluation.ts f52f5f4b28cb89b335e8f09eb7befd617c1e53ec54df8224a669ceac7e28bd12
typescript/src/scene-capabilities.ts 286f7134591ea55902e96ccf4718484508b404255c9aa6bf490c867b7e28d756
typescript/src/lib/audio-envelope.ts edbf7f270a6291459a7951f0ffafe38d2e2757197ba900edf3be42b3af51fddc
```

Changed-file body hashes (`before` → `after`):

```text
tests/packs/rendering/test_remotion_backend.py 8e5d4d8cabe2715a3cab3ee1f99e228fd54884f013dc13ea01e88f2b4ad35384 -> d55004cd934bc3614f22bcb8fc223fb1f47e2da37282af8556fc821ac69d15bb
tests/packs/rendering/test_remotion_layer_tail_compat.py 28a7f53e922ae8f1e64a8238ab57f9cfcb9ae7b2f0de0178ef721b5bc9aefdd4 -> 9445ccfac8439bbf55febe53fa67ff252fa46b84b07550f7f0365b5d8f9a8abe
tests/packs/rendering/test_remotion_typecheck_mappings.py 67eea063cf72fbd7873e318b4a4fd8a77eda73c46f8c1920ca189bd26923c952 -> 28458ab0180a47210d5085d14bde5ffc8437cce96937d7b919174c9c7081488b
tests/packs/rendering/test_am_snap_plate_scene_capability.py cd09a35874293f42f2a2733f4f0d08f44d3f2b5ea0ab8445fac53a15ae846587 -> 88924d571a95959a2fe2309c4739b0ce2f25f5f95ee6d21eb52dd966b906cbb8
```

## Static checks

- `git diff --check`: passed.
- `compileall` on all four changed test files: passed.
- scoped Ruff on the four changed test files: failed on 6 pre-existing
  findings in these large test files; no new finding was added.
- `scripts.reshape.compare_ruff_baseline`: passed, current `2149` equals
  baseline `2149`.
- `scripts.reshape.compare_mypy_baseline`: blocked before checking by the
  shared venv: missing `types-PyYAML` and a Python-version stub syntax error;
  no dependency installation was attempted. The expected baseline count is
  `1912`.

## Ownership / next steps

- D18/raw launcher environment owner: qualify how the raw pack command obtains
  `runtime_protocol` under the sanitized transport; do not weaken the raw
  caller or test assertion.
- Composition/profile owner: decide whether the three public12 outer-geometry
  expectations remain a historical control requiring a separately qualified
  0.0.12 host, or whether the current 0.0.14 `GAP` result is the settled
  behavior. No expectation was changed here.
- Audio compile owner: restore the trusted-host prepared envelope transform
  that supplies `audio.render_source`; no xfail/skip/refusal conversion was
  made.
