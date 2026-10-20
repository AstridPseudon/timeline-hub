**Recommendation:** retain one full-composition frame count before native layer filtering; carry it in the existing `RenderRequest.metadata` string map; forward it through the normal runner as one optional internal Root prop. Keep the native absolute window and every selected original clip unchanged. A Root metadata change is necessary: no existing unmodified Root input expresses this fact. Do not merge/qualify the generalized layer route on the existing tests alone. No product changes were made by this worker.

Read PLAN.md, COMMON.md, the native-window-resume-r1 report and empty-layer probe, and the actual final implementation. This worktree's source is `/home/user/work/wt/vw-m3-empty-layer-duration-seam`, HEAD **abd41eb2a6a8fe9224028018ac65225018e490bd** (the harness-committed normal PCM implementation, rather than an earlier draft). All Agent line references below are relative to that absolute directory and commit. Other source inspected read-only: Composition `/home/user/work/composition` at `46bd700b2b46ae1cab1e8a1502ed6504e81aa8d8`; App `/home/user/work/app` at `18becfbede00038830b97e63345445eeef54fa42`; frozen Agent R4 ref `origin/codex/handover-timeline-r4-20261019-candidate-sdk` at `11caf1d9de291d76f491cf69f7942606b7471d7a` (git show only).

**Executable findings.** The original reproducer exits 0 and confirms the reported problem. The additional direct Python probe alongside this report exercises actual `_segment_request`, shared render serialization, existing duration helpers and native guard, with no substitutions, renderer, listener or media processing. Its JSON output covers:

| Original source / window | Original render extent | Native selected extent | Current result | Legacy result |
| --- | ---: | ---: | --- | --- |
| 10s bottom, empty top; [150,180), 30fps | 300 | 1 | bounds refusal | 30-frame local empty fill contract |
| Same, 30000/1001fps | 300 | 1 | bounds refusal | 30-frame local empty fill contract |
| 10s bottom, early top clip; same two rates | 300 | 31 / 30 | bounds refusal | 30-frame local empty fill contract |
| Empty top plus 20s source-role reference; same two rates | 300 | 1 | bounds refusal | 30-frame local empty fill contract |

The legacy column verifies null native window, empty clips, existing alpha stamp and window-duration metadata; it does not claim pixel output. Source file bytes remain unchanged. Deliberately authored `metadata.duration_seconds=999` does not extend the current native clock. Original [150,301) remains refused. A further information-loss check shows that 10s and 20s originals yield **identical filtered layer props**, despite different original frame counts (300 and 600). Neither those props, the unchanged window [150,180), nor a format profile can recover the lost full extent. Using `window.end_frame` would retain only 180, not the original 300/600.

**Exact existing path and why it loses duration.**

| Source location | Actual data/use |
| --- | --- |
| `astrid/packs/rendering/actions/render/run.py:413,472` | Existing facade constructs `RenderRequest` with timeline path, optional profile and window. It does not supply a full duration. This facade needs no new argument. |
| `astrid/core/rendering/contracts.py:348,379,412,735` | `FrameWindow` is half-open; `duration_frames=end-start`. `RenderProfile` has FPS/format/tolerance, **no composition length**. `RenderRequest.metadata` already is `dict[str,str]`. |
| `astrid/core/rendering/service.py:1410` | The plan loop replaces request.window with `segment.window` before calling `_segment_request`; the input timeline path still names the full source. This is the last existing service point with the full source and segment FPS together. |
| `service.py:1092` | Native layer branch copies top-level fields, filters tracks/clips to the layer, copies metadata. It keeps all selected-track original clips, including out-of-window/overlap peers. No original extent is retained. |
| `service.py:1112,1125` | Adds only `metadata.astrid_layer={z,alpha}`, writes invocation-private JSON and its existing materialized-timeline digest, replaces timeline path and preserves native request.window. |
| `contracts.py:794,866`; `service.py:795,1023,1965` | `to_dict`, `for_backend`, support/render projection and subprocess JSON transport already preserve request.metadata. `for_backend` filters backend_config, **not metadata**. No protocol/schema/Runtime DTO addition is needed to carry another string entry. |
| `astrid/packs/rendering/rendering/renderers/remotion/run.py:1788` | `_load_request` parses RenderRequest and projects it for this backend. Existing metadata reaches the actual normal service renderer. |
| `astrid/packs/rendering/shared/rendering_backend/__init__.py:52` | `_serialize_timeline` calls `Timeline.load(...).for_render(...).to_json_data()`. Source-role tracks disappear here, not in the raw service read. |
| `astrid/core/timeline/banodoco_composer.py:127,172,268` | Render serialization validates, preserves placement precision, filters source-role tracks and defaults theme; `to_config` deep-copies. Measuring raw source JSON instead would incorrectly count long reference clips. |
| `astrid/core/timeline/duration.py:173,265` | Existing frame extent helper mirrors Composition: independently rounded start plus minimum-one-frame rounded duration; maximum over clips, minimum one. Optional explicit media-tail clock has separate validation. Reuse this helper, not a new extent algorithm. |
| `remotion/run.py:1494,1602,1639` | support checks native bounds; `_protocol_render` calls support again. A fix solely inside execution is too late. |
| `remotion/run.py:888,1040` | `_native_window_argument` rejects sliced metadata, source_range, nonunit speed, FPS mismatch, then a window beyond the recomputed **filtered** extent. Locked execution calls it before runtime allocation. These checks must remain. |
| `remotion/run.py:1720,915,945,985` | Protocol render -> `_execute_remotion` -> `_execute_remotion_locked`, with two forwarding branches for staging paths. All need the same optional retained duration parameter if request.metadata is used. |
| `remotion/run.py:1105,1167,1181,1210,1236` | Actual Root props contain timeline/assets/theme/review; normal PCM preparation deep-copies them, then JSON is written and passed with absolute `--frames=start-(end-1)`. Request metadata is **not automatically a Root prop**. |
| `remotion/normal_audio.py:74,113` | Both no-audio and prepared-audio paths deep-copy the entire props mapping. An additional internal top-level prop survives without changing this module or WAV clocks. |
| `remotion/src/Root.tsx:124,139,151,160,168` | Root selects canvas FPS, then duration from legacy local-window metadata, explicit render-clock duration, or package `getTimelineDurationInFrames` on the filtered clips. Both registered compositions share `getMetadata`. No request/window/profile object is available there. |

Composition's `typescript/src/lib/duration.ts:34` uses the same clip-only maximum. `typescript/src/types.ts:72,100` has no full-duration prop. `compiledTransitions` is an optional canonical transition result; its type at `typescript/src/lib/transition-spans.ts:15` contains FPS and track transition vectors, not total extent. Do not manufacture or extend it for this purpose.

**Smallest recommended implementation grant (not implemented).**

1. In `astrid/core/rendering/service.py::_segment_request`, only for the native filtered-layer branch, obtain the full **render view** from the already-read timeline using the existing `Timeline.from_json_data(...).for_render().to_json_data()`. At `segment.window.fps_rational[0]/[1]`, call existing `timeline_render_duration_frames`. Validate the original segment end against that total **before filtering**. Preserve the full original extent even when the selected layer ends earlier or is empty. Source-role reference material must not count. Keep the existing materialized digest and alpha handling.
2. Carry that integer as one reserved internal string entry, suggested name `request.metadata['astrid_composition_duration_frames'] = str(total)`, using `replace(request, metadata={**request.metadata, key: str(total)}, ...)`. The service computes/overwrites this value; it must never adopt an authored/caller claim as the original bound. Strip an incoming reserved key on other paths, including the unlayered early return, so an unlayered/direct request cannot enlarge its bound by supplying metadata. The backend must scope consumption to the service's native isolated-layer handoff, not general user metadata. This is internal execution plumbing within the existing trusted service/backend boundary, not a new authenticated source protocol. Treat it only as an invocation render fact, never as timeline/revision/source certification. No authored timeline duration/origin stamp, new request member, schema version, Runtime field or endpoint. The existing native window binds the FPS; the backend still requires exact equality to the canonical profile FPS. The optional request.profile must not become the duration authority.
3. In `astrid/packs/rendering/rendering/renderers/remotion/run.py`, parse the optional reserved string into a strictly positive safe integer (reject malformed/boolean/fractional/nonfinite/oversized values), in the native isolated-layer path. Use it in **both** support and locked execution via an optional keyword `composition_duration_frames: int | None = None` on `_native_window_argument`, `_execute_remotion`, and `_execute_remotion_locked`. Forward it through `_protocol_render` and both `_execute_remotion` branches. Preserve existing local timing/clock validation, require retained duration >= filtered clip extent, and require window.end <= retained duration. With no retained value the old full-composition bound remains. Do not use `max(window.end_frame, local_extent)`, clamp the window, or remove checks. The normal source path must reject a forged overlong request against the original source before a retained value can enlarge the filtered bound.
4. In that same normal runner, add only the validated retained value to merged props, suggested `astridCompositionDurationInFrames`. In `remotion/src/Root.tsx` define a local host intersection type, e.g. `type HostCompositionProps = TimelineCompositionProps & {astridCompositionDurationInFrames?: number}`, and use it in the metadata callback/component prop typing. Validate a supplied value as a positive safe integer at least the local clip extent. For native isolated layers it selects the full composition duration; the CLI still selects the 30 absolute output frames. The value must never accompany the legacy rebased-window duration (reject conflicting clocks rather than guess). Absent prop preserves current window/clock/clip selection and the one-frame empty default. Public package props/types need no change.

The genuinely new information is just that one frame count. A new **internal Root input** is unavoidable. A top-level prop is not mathematically the only encoding: one could invent a new timeline metadata field and read it in Root. That would be a new stamp/contract too, with worse separation from authored fields. Under the task's no-authoring-stamp constraint, the optional host prop is the clean minimal recommendation. Existing request.metadata is transport, not a second compiler; the service copies an existing extent result and does not rewrite clip timing.

Reusing `metadata.duration_seconds` is not equivalent: Root currently honors it only with `source_window_start_seconds`, and the native guard explicitly refuses that combination. Broadening it would give arbitrary authored duration metadata new power and change full-render behavior. Reusing `app.astrid_render_clock` is also wrong: `duration.py:213` requires a matching authored extent and a real tail source/interval/policy; `Root.tsx:55` actually paints that tail. Neither is an empty transparent duration extension.

**Other callers / limits that must stay explicit.**

- `astrid/packs/rendering/rendering/renderers/threejs/run.py:232,468,512,565` still rebases its windows with the existing service slicer, writes a private timeline, and calls the shared executor **without a native window**. It must omit the new prop and continue to use Root's local window length. Sharing the executor is not evidence that Three.js uses original clocks. Migrating that policy is separate work.
- `remotion/run.py:1383` selected-PNG capture must keep its existing absent window/absent retained-prop call. Full, unlayered native-window and direct executor callers retain optional defaults. No extra duration prop is required for App Player or the public Composition package.
- The alpha path already neutralizes the per-run theme background to transparent at `remotion/run.py:1148`, chooses alpha-capable output, and retains `metadata.astrid_layer`. Duration retention must not manufacture media to fill the layer. Pixel transparency remains unverified here.
- **Existing explicit media tails are a separate coupled limit, not solved by a scalar.** The probe verifies a valid full `app.astrid_render_clock` becomes invalid after filtering away its authored extent: `render clock authored_duration_frames must match the authored clip extent`. Root's tail component additionally recomputes its start from filtered clips (`Root.tsx:65`), so ignoring that Python error can paint the original tail in the wrong span/layer. Keep validation intact. Do not describe the scalar fix as qualification for layered media-tail films; grant a separate tail-ownership review if these inputs must be supported. Ordinary full-tail rendering remains on its existing route. This finding does not justify silently removing/rewriting its tests.
- Storage admission already measures the original canonical snapshot (`astrid/core/rendering/storage.py:294,394`) before service layer materialization; the normal renderer support path does not call that estimator. Do not teach the generic duration helper or storage admission to trust a render metadata override.

**Submillisecond serialization review.** The change in `TimelineRenderView.to_json_data` (`banodoco_composer.py:172`) is data-compatible: same validated shape, `from_` -> `from` conversion, passthrough fields, source-track exclusion, theme default and nested copy independence. Its timing is intentionally different. Previously it called persisted `Timeline.to_json_data`, which rounds floating `at` to three decimal places (`:48,271`); now it uses the precise config. Persistence/dump still round.

The probe demonstrates `at=0.016682` at 30000/1001fps: precise render starts at frame **0**, old rounded render/persisted reload at frame **1** (`at=0.017`). At 30fps this particular value starts at frame 1 in both paths; the change is boundary-dependent. This affects **all callers of shared `_serialize_timeline`**, including normal full/window renders, support bounds, selected PNG capture and the Three.js path, rather than only normal PCM. It can also change last-frame extent and acceptance of a boundary window. FFmpeg's direct JSON readers (`renderers/ffmpeg/run.py:125,252`) are outside this serialization change and already see the original precision. Visualize's inspection model uses original assembly values and the duration helpers directly (`actions/timeline_visualize/model.py:513,563,568,595`). Composition rounds seconds directly at `typescript/src/lib/duration.ts:3`; the inspected App shot Sequence also does `Math.round(clip.at*fps)` (`src/tools/video-editor/compositions/TimelineRenderer.tsx:248`). These source reads support removing an accidental second quantization, but do not prove cross-product pixel/audio parity.

This serializer is not a new timing compiler: it stops altering placement on a render copy. Nevertheless, **unchanged raw file versus dump/reload can now render a frame apart**. Calling the persistence rounding a formatting-only convention is false for these inputs. Existing projection retains floating placements (`shot_composition_projection.py:103,308,327`); render props should consume that result without inventing another quantizer. The R4 compiler exists only on the inspected frozen ref at `astrid/sdk/timeline/compiler.py`; this worktree does not contain that module. Do not claim its convergence or the one-compiler migration is proven by these serializer tests.

**Decision needed:** the orchestrator should explicitly classify/approve retirement of millisecond placement quantization for render consumers and record the owner-visible one-frame placement/extent difference for the hard-stop film review. PLAN's approved gain/curve/theme differences do not explicitly settle this distinct behavior. I recommend precise compiled placement as the single viewing input, while leaving persistence policy to its owner; if “save/reload never changes timing” is required for submillisecond authored values, rounding in the authoring/persistence path needs a separate decision/grant. Do not restore consistency by rounding only the PCM input or relaxing parity/bounds expectations.

**Exact tests recommended for the implementation worker.** Extend the existing main-suite files, preserving their passing behavior assertions:

- `tests/packs/rendering/test_normal_audio_run.py`: actual service-produced empty/sparse layer -> actual normal locked props/CLI; original full extent=300, native `--frames=150-179`, empty top has no clips and alpha true, sparse clips retain exact at/from/to/speed/fades/overlap peers; prop survives normal preparation. Existing scalar gain, source validation, cleanup/lifetime tests stay.
- `tests/packs/rendering/test_remotion_native_window.py`: support and locked calls receive the same retained bound; original [150,301) still refused before allocation, end=300 accepted, absent prop unchanged, malformed/smaller/unsafe duration rejected, mismatched FPS/source_range/speed/sliced metadata/frame-capture conflict still refused. Check both `_execute_remotion` forwarding branches and Three.js/PNG defaults.
- `tests/core/rendering/test_service.py`: original-source measurement before filtering, original request/file unchanged, metadata merge, selected source-role track exclusion for measurement, integer/rational FPS, unrelated authored duration ignored, reserved caller duration overwritten by actual source fact, legacy supports_windows:false unchanged. Existing empty allowlisted-track and alpha tests must keep their expectations.
- `remotion/tests/bounds.test.cjs` supplies the existing source-transpile/stub pattern at line 180. Add a focused `remotion/tests/root-metadata.test.cjs` that captures each registered Composition's real `calculateMetadata` callback and invokes it: empty/sparse native props retain 300 (not 30 or 180), no override remains 1, legacy window remains 30, ordinary clip/explicit-tail/default canvas behavior unchanged, invalid/conflicting values fail. Stub runtime imports, not the metadata implementation or duration arithmetic; no browser required.
- `tests/timeline/test_timeline_characterization.py`, `tests/core/timeline/test_source_role_tracks.py`, and `tests/editing_conformance/test_compile_contracts.py`: keep source exclusion/persistence/deep-copy guarantees; add precise placement boundary vectors through actual projection -> shared render serializer -> public timing helper, plus explicit dump/reload characterization. The two existing prepared-audio xfails execute projection, not normal preparation; do not relabel them as duration regressions or weaken/remove them.
- After implementation and scope decisions, central qualification needs empty/sparse alpha MP4/MOV output, layered/window frame comparison, PCM parity and a planted mismatch. None was requested/run here. Shared dependency graphs remain read-only; their qualification status is outside this report.

**Commands and results (cwd = the assigned Agent worktree).**

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-native-window-resume-r1-empty-layer.py
# exit 0: original counterexample and legacy metadata reproduced.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-empty-layer-duration-seam-probe.py \
  > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-empty-layer-duration-seam-probe.json
# exit 0: six source/layer cases, bounds, identical filtered inputs with unequal
# original extents, source exclusion, precision/dump/reload, explicit-tail limit.

env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
  tests/timeline/test_timeline_characterization.py \
  tests/core/timeline/test_source_role_tracks.py \
  tests/editing_conformance/test_compile_contracts.py \
  tests/packs/rendering/test_remotion_native_window.py \
  tests/packs/rendering/test_normal_audio_run.py::test_native_layer_retains_exact_clips_window_and_materialized_hash \
  tests/packs/rendering/test_normal_audio_run.py::test_legacy_layer_still_rebases_its_window \
  tests/packs/rendering/test_normal_audio_run.py::test_render_serialization_preserves_submillisecond_source_placement
# exit 0: 82 passed, 2 existing xfailed, 161 subtests passed in 4.07s.

git diff --check
git status --short
# both exit 0; clean product worktree, no generated output.
```

Tests above are existing targeted suites and a diagnostic probe, not tests of an implemented duration fix. No full suite, make check, browser, sockets, render, install, shared-dependency write, git mutation, push or repository documentation edit. No Root/package changes or assertions were modified. Design work is complete; implementation awaits a bounded service/runner/Root grant and the noted compatibility decision.

Source SHA256 at review (to disambiguate subsequent branch movement):

```text
930f7d6914bc4cb36d65e266e7fbaf83e625e6ed9466ce6426551631f477ec22  astrid/core/rendering/service.py
5cf8139312e813143adaf84c5a9a9e45d9ad6ce6be9a5dabd667df0048203a4f  astrid/core/timeline/banodoco_composer.py
cbdb18bffebc6c9d5a07a3d144fcbfa558ba6249fda5c2a8dd8016b87a3fd3db  astrid/core/timeline/duration.py
37a43a6bfcc2806d09f0b9149c9301c2c833cd6a807c624c77e19076151b284a  astrid/packs/rendering/rendering/renderers/remotion/run.py
f5b7474e19fa282c55ab6b56d4ee7a74db9b78b8dbc0e2b8891a2e88e8a5bf76  remotion/src/Root.tsx
```
