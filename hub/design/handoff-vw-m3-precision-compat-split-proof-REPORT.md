PCM activation can preserve the existing Agent render quantization. Split the held abd41eb2 unit: retain its native-clock PCM preparation and complete the retained-duration fix, but hold its TimelineRenderView precision hunk and the assertions that specifically require that new precision. No product or repository test was changed in this task.

Evidence files share the absolute prefix `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-precision-compat-split-proof-`.

Sources and actual current compiler

- Assigned Agent worktree `/home/user/work/wt/vw-m3-precision-compat-split-proof`: abd41eb2a6a8fe9224028018ac65225018e490bd. This is the held public12/native-PCM candidate, not current Agent integration.
- Current Agent integration was read and snapshotted at 931d7ec56dadffc2efdc893fec80b4c4aadf8a8e. Its package pin is still 0.0.10; using its M2 compiler/projector does not claim public12 has landed there. Its `banodoco_composer.py`, `shot_composition_projection.py`, and service match the pre-abd versions at the inspected seams. Its runner also has the newer `on_scene_props` capture callback, which a forward port must preserve.
- Current M2 publication compilation is `astrid/core/timeline/authoring_bundle.py:778`, not a presumed `astrid/sdk/timeline/compiler.py`. The latter does not exist here. It copies supported authored fields without implicit quantization, generates immutable revisions/pins, and validates changed placement capabilities (`:717,909,991`). Source-offset/playback-rate placement edits without projection semantics refuse; do not invent inheritance to bypass this.
- The actual canonical renderer projector is `astrid/core/timeline/shot_composition_projection.py:454`. `_project_clip` at :291 applies occurrence placement, namespaces IDs, caps the visible child at the occurrence end in source units, preserves child speed, and applies occurrence gain/mute. `project_runtime_parent_composition` namespaces selected assets at :615. These are the source of the compiled originals; raw child rows are not interchangeable.
- Current saved capture uses that projector in `astrid/sdk/timeline/commit.py:730`; candidate preview uses the same projector in `astrid/sdk/authoring_render_preview.py:184`. The preview adapter recompiles a supplied frozen publication for validation at :107; this task does not claim all upstream open/preview/verification operations globally compile once. No additional compiler/projector is needed for PCM.
- `-compile.py` executes the current real publication compiler once, the current real runtime-parent projector once, then the existing `_render_compatible_projection`. It counts both calls, checks candidate immutability, and writes `-compiled.json`. It uses a real existing authoring-bundle fixture and supported ordinary candidate edits, with no Runtime calls/publication, fabricated authority, or replacement compilation algorithm.
- Public audio evidence uses the exact 0.0.12 tarball tracked in the assigned worktree, privately extracted. Helpers and tests are copies of tracked candidate files. Dependency scopes are real private directories with links only to existing dependency package leaves. No shared package, venv, cache, lockfile, or generated artifact was modified.

What the concrete vector proves

The actual M2 compiler/projector emits `occ-1:voice-1` from child `voice-1`, selecting `occ-1:voice`. Child at=0.016682, from=0.051, to=3.051, speed=1.5, volume=3; occurrence duration=1.2 seconds and gain=0.5. Its projected `to` is 1.8259769999999997 and volume is 1.5. These changes came from the real projector, not diagnostic arithmetic substituted for it.

The private probe runs the actual held `_execute_remotion_locked` and actual `prepare_normal_audio_sources`, using the existing socket-free normal-run fixture. It covers full, absolute native window [15,45), and actual service-produced isolated native layer inputs. Admission/runtime/registry generation/render consumption are stubbed exactly as in that fixture; actual AssetMaterializer integrity checking, local ffprobe/ffmpeg decoding, preparation, serialization, CLI argument construction, and cleanup execute. No socket or Remotion/video render executes. Canonical profile resolution is fixture-supplied at 30000/1001; end-to-end profile resolution and Root metadata are not qualified by this probe.

For each route the probe runs both candidate precision and the exact current M2 `TimelineRenderView.to_json_data` method, loaded from its source snapshot. This restores the existing serializer, rather than introducing a quantizer or manually rounding/repositioning clips.

| Quantity | Candidate precise serialization | Existing serialized compatibility |
| --- | --- | --- |
| Root clip `at` | 0.016682 | 0.017 |
| Existing frame helper start | 0 | 1 |
| Projected local duration | 35 frames | 35 frames |
| Public `compiledAudioSourceClock` | source_from=2/fps=0.06673333333333334, rate=1.5 | identical |
| Native WAV | 90000 stereo frames, 30000 Hz, IEEE float32; 720044 bytes | identical |
| WAV SHA256, all three routes | abcc7088475c77c7443a5e72db2be8e6066b214ae476c80d6ee890f044b2e2a6 | identical |

Each actual WAV is byte-equal to the public `compileAudioEnvelope` + `applyAudioEnvelope` + `audioEnvelopeWav` reference from that route's final serialized original. Scalar clip/track gain remains in props; it is not baked again. Sample 5000 is (0.12481120228767395,-0.062405601143836975), sample 30000 is (0.25,-0.125), and sample 70000 is zero. The raw child's public-reference WAV differs by up to 0.25, because its uncapped exit fade belongs to a different duration. Its hash is defbb61dffd7886a99e3b7b3c638c12782425d247f356adeb2107e6eb9588072. This is a vertical current-M2-to-PCM distinction that the older hand-built “compiled clip” tests alone did not establish.

The probe additionally sends each final serialized original through the real host slicer on A1, then the existing public normal-audio adapter with that retained original. The sliced public source clock is 23/fps=0.7674333333333333, rate=1.5. The resulting full-source WAV differs from the native original by exactly zero in this vector (checked with the existing 1e-7 tolerance, not a widened tolerance). Omitting the original restarts the envelope and differs by up to 0.25. `-vectors.json` contains all six results, clocks, envelopes and sample values.

Why the split works, and its limits

`remotion/compiled-audio-source-clock.mjs:9` uses public `computeMediaTrim` and `getSanitizedPlaybackRate`. Public trim reads `from`/`to`; it does not read `at`. Public `compileAudioEnvelope` reads the local duration, fade lengths/curves, or an existing compiled envelope; it also does not read absolute `at`. Restoring millisecond placement serialization changes the Sequence start and possibly composition extent, but does not require changing this media clock or PCM sample phase. This is why PCM activation does not require retiring render placement quantization.

The relevant route is actual serialized Root props, not `Timeline.to_config()`, raw authored children, or a pre-serialization projector result. The runner's `_serialize_timeline` calls happen at the native guard, effect validation, and final Root construction (`remotion/run.py:1044,1052,1106`). They serialize an already compiled/projected flat input; they do not invoke the publication compiler or canonical projector. Capture the retained original from the final serialized props before adding `audio.render_source`. Native full/window paths do not transform that clip; native layer filtering retains every selected original clip and overlap peer (`service.py:1092`). Consequently their final serialized clip itself suffices; the current helper can keep `original_clips=None`. There is no reason to reconstruct a raw original or add a second compiler call. For a caller that does slice, capture a detached original map from the unsliced serialized Root payload before that transform, using the existing internal seam. Do not read `app.astrid_slice_origin` as authority.

A genuine limitation remains once only a sliced payload survives: `test_slice_records_original_phase_that_the_cut_clip_cannot_recover` already proves two different originals yield the same cut clip but different gains. The final *sliced* Root props cannot recover an erased original. This is information loss, not a reason to change serialization or fit samples. The native normal route avoids that loss.

The shared runner is also used by Three.js. Its `_protocol_render` serializes, slices, writes a temporary file, and invokes `_execute_remotion` without a native window (`threejs/run.py:466,468,512,565`). New activation inside the shared executor therefore reaches this caller too. Do not call it phase-qualified just because native normal tests pass: its original must be retained before slicing through the existing seam, or its separate source-owner work must remain held. No timing rewrite, broad acceptance change, or original reconstruction from sliced/app fields is justified. Likewise, WAV equality is not proof that every historical rebased segment's displayed frames or media selection equals native full-clock selection.

Minimal implementation recommendation to the Viewing manager

1. Forward-port the approved native normal preparation onto current M2; preserve the current capture callback. Keep normal full/window/layer data on their existing final serialized renderer clock. Remove only abd's broad `TimelineRenderView.to_json_data` precision hunk from this activation unit: retain the pre-existing `self._timeline.to_json_data()` serialization, source-role exclusion, theme default, and independent copies. Do not introduce a PCM-only rounding path, quantizer, clip realignment, or new authored stamp.
2. Complete the separately granted duration seam exactly along the empty-layer report: measure full composition duration with existing `timeline_render_duration_frames` on the full render-serialized view before native layer filtering; transport the trusted invocation fact in existing request.metadata, validate in both support and execution, and pass the bounded internal Root prop to both metadata callbacks. Use the compatibility-serialized extent, not raw projector/raw-source extent. Keep original bound checks, FPS, half-open window, selected original clips, alpha, source-track exclusion, and legacy no-override behavior. No second projection/compilation is required for that measurement. This is an implementation recommendation, not implementation or evidence that the duration defect is fixed.
3. Do not generalize the scalar to explicit media-tail ownership. The cited empty-layer report proves authored-tail validation and Root tail-start depend on the original full clip extent. Those cases remain a separate held contract question. Empty/sparse layer output still needs the authorized duration implementation and subsequent targeted/central qualification.
4. Hold precision retirement as a distinct change with its precise boundary tests and persistence decision. at=0.016682 / 30000/1001 must continue to be reported as old renderer frame 1 versus proposed frame 0; dump/reload still rounds it back to 0.017. Restoring the old serializer preserves the existing Agent renderer policy; it does not settle future cross-product viewing parity. Authoring/compiler/persistence changes belong to the Agent manager. Route cross-manager semantics through the Viewing manager; do not modify persistence, App clocks, or threshold policy here. Graph repair remains held.
5. Keep behavior tests intact. The held candidate introduced `test_render_serialization_preserves_submillisecond_source_placement`, and its actual-normal-props test also asserts raw at equals serialized at. An isolated diagnostic restoration of the exact existing serializer makes those four cases fail specifically on 0.017 versus 0.016682. They are precision-retirement requirements coupled into the held PCM unit, not evidence that PCM needs raw precision. Separate their feature scope explicitly with manager approval; never silently rewrite them, mute them, or turn behavior into a refusal expectation. Add final-serialized-original PCM cases to main's suite during the authorized implementation.

Existing tests that distinguish representations

- `tests/timeline/test_shot_composition_projection.py::test_projection_preserves_frames_trim_audio_and_occurrence_placement`: actual projection caps source-to, applies mute, and preserves source offset/occurrence speed as metadata. `::test_projection_caps_visible_time_without_applying_speed_twice_or_mutating_source` checks both fast and slow capped holds. These reject confusing raw children with projected originals.
- `tests/core/timeline/test_shot_composition_projection_volume.py`: absent child volume/unity, existing volume, occurrence gain and mute distinguish projected scalar semantics without unmuting footage.
- `tests/editing_conformance/test_compile_contracts.py::test_audio_vector`: named vectors include occurrence gain/mute, source-offset-is-metadata-only, occurrence-speed-not-inherited, child-speed-wins, and preserved fade curves. Visual overhang/clamp and half-open vectors also distinguish output from raw children. The two existing strict prepared-source xfails execute projection, not preparation; they remain unchanged and do not establish a duration regression.
- `tests/timeline/test_authoring_bundle.py::test_full_authored_field_edits_compile_without_normalizing_opaque_fields` and placement-capability refusal tests protect current M2's lossless authored behavior. `::test_publish_uses_one_compilation_and_returns_complete_mapping` checks one writer call and mapping, despite its name; it does not instrument compiler invocation count. This task's private compile probe does instrument that count.
- `tests/packs/rendering/test_normal_audio_sources.py::test_full_stereo_wav_and_exact_compiler_clock_without_authored_writes` checks public trim/rate at 30 and 30000/1001, but its “compiled” props are manually constructed. `::test_internal_original_clip_seam_preserves_phase_without_trusting_app`, `::test_actual_slice_needs_original_compiled_clip_transport`, and `test_normal_audio_source_phase.py` distinguish a retained original from a sliced clip and reject relying on forged app origin metadata. They do not run current M2 compilation.
- `remotion/tests/normal-audio-sources.test.mjs` checks public source-clock/original-phase vectors at integer and rational FPS, speed, source offsets, recursive envelope translation and source-byte identity; again, its compiled inputs are hand-built. Native-source and long-source tests remain valuable decoder-origin/retention coverage, not proof of M2 compilation; they were read, not run here.
- `tests/timeline/test_timeline_characterization.py::TimelineFromConfigToJsonDataTest::test_from_config_to_json_data_rounds_at_to_three_decimal_places` protects authoring dump rounding; `tests/core/timeline/test_source_role_tracks.py::test_source_track_is_stored_but_not_rendered` protects final render filtering. The held candidate's precision and actual-normal-props tests are the explicit old-serialized-versus-new-precise discriminators described above.

Commands and results

Let `ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`, `TASK=$ORCH/workers/vw-m3-precision-compat-split-proof`, `OUT=$ORCH/design/handoff-vw-m3-precision-compat-split-proof`, `WT=/home/user/work/wt/vw-m3-precision-compat-split-proof`, `PY=/home/user/work/venv-agent/bin/python`, `NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node`. These variables stand for the absolute arguments used in the executed commands.

```sh
# Actual current M2 source snapshot; one compiler call + one canonical projector call.
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TASK/current" "$PY" -B "$OUT-compile.py" > "$OUT-compile.log"
# exit 0; -compiled.json is the reusable compiled output.

# Common prefix for the following candidate Python runs (cwd=$WT):
run_candidate() {
  env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$WT" \
    ASTRID_NODE_EXECUTABLE="$NODE" ASTRID_REMOTION_PROJECT_DIR="$TASK/audio-project" \
    PATH="$(dirname "$NODE"):$PATH" "$PY" -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short "$@"
}
run_candidate "$OUT-probe.py"
# 6 passed in 7.21s, exit 0; -probe.log, -vectors.json.
run_candidate tests/packs/rendering/test_normal_audio_run.py \
  tests/packs/rendering/test_normal_audio_sources.py \
  tests/packs/rendering/test_normal_audio_source_phase.py \
  tests/packs/rendering/test_remotion_native_window.py
# 73 passed in 13.67s, exit 0; -candidate-targeted.log.

# cwd=$TASK/current, exact current M2 snapshot tests:
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TASK/current" "$PY" -B -m pytest -q \
  -o addopts= -p no:cacheprovider --tb=short \
  tests/editing_conformance/test_compile_contracts.py \
  tests/timeline/test_shot_composition_projection.py \
  tests/core/timeline/test_shot_composition_projection_volume.py \
  tests/timeline/test_authoring_bundle.py::test_full_authored_field_edits_compile_without_normalizing_opaque_fields \
  tests/timeline/test_authoring_bundle.py::test_placement_edits_without_shared_projection_semantics_fail_before_publish \
  tests/timeline/test_authoring_bundle.py::test_publish_uses_one_compilation_and_returns_complete_mapping \
  tests/timeline/test_authoring_bundle.py::test_independent_unique_shot_reuses_untouched_revision_and_direct_edits_compile_identically
# 54 passed, 2 xfailed in 0.43s, exit 0; -current-targeted.log.

env -u NODE_OPTIONS -u NODE_PATH "$NODE" "$TASK/audio-project/tests/normal-audio-sources.test.mjs"
# 8 passed, exit 0; -public-node.log.

# Explicit counterexample run, cwd=$WT: same candidate environment as run_candidate,
# but PYTHONPATH="$TASK:$WT", adding -p compat_serializer_restore:
# selected tests below are unchanged; the private plugin restores the exact current serializer.
env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TASK:$WT" \
  ASTRID_NODE_EXECUTABLE="$NODE" ASTRID_REMOTION_PROJECT_DIR="$TASK/audio-project" \
  PATH="$(dirname "$NODE"):$PATH" "$PY" -B -m pytest -q -o addopts= -p no:cacheprovider \
  -p compat_serializer_restore --tb=short \
  tests/packs/rendering/test_normal_audio_run.py::test_render_serialization_preserves_submillisecond_source_placement \
  tests/packs/rendering/test_normal_audio_run.py::test_actual_normal_props_prepare_native_source_without_baking_scalar_gain
# 4 failed in 3.93s, exit 1, specifically precise-placement assertions; -precision-expectations.log.

git -C "$WT" diff --check
# exit 0; git status --short is empty.
```

The first private probe version failed six cases because it imported non-exported public helper names; the first slice extension failed six cases because the fixture's unrelated hold-only media row is unsupported by the legacy slicer. The final probe uses exported public audio functions and the actual A1 track allowlist for its audio-only slice experiment. Both diagnostic setup logs are retained as `-probe-initial.log` and `-probe-slice-initial.log`. No product fix, product-test edit or relaxed tolerance resulted.

No full suite, browser, socket, live server, network, install, normal render/MP4, Root metadata execution, complete rational-profile resolution, App Player parity, media-tail/layer pixel parity, or Gate 6 qualification was run or claimed. Duration propagation remains unimplemented; it does not block this read-only proof. Recommended next action: Viewing manager requests/implements the compatibility-scoped forward port and retained-duration seam, holds precision retirement for the Agent/cross-manager decision, and obtains the separately required output qualification afterward.
