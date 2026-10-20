# Viewing size and remaining deletion cuts

Base: Composition `tl/integration` `2ac77f4` (public 0.0.9 source integrated). Counts are nonblank physical lines in tracked source files, from `git ls-tree` + `git show`; tests, fixtures, `dist`, locks, tarballs, and `*.generated.*` are excluded. Composition includes authored TS/TSX/JSON under `typescript/src`; App/Agent rows use the named implementation roots and exclude test files. Duplicate rows intentionally count only the duplicate tree, not canonical source again.

| scope | integration | reviewed candidate |
|---|---:|---:|
| Composition canonical `typescript/src` | **4,086** (80 files) | **4,086** (`2ac77f4`) |
| Agent full rendering package | **54,219** (151) | **54,545** (D2 `94e86ec1`) |
| Agent visualize `timeline_visualize` | **25,350** (57) | **25,671** (D2 `94e86ec1`) |
| Agent Remotion `remotion/src` | **1,490** (14) | **1,514** (15) |
| Agent core evaluator | **375** `onscreen.py` | **491**: 375 `onscreen.py` + 116 `scene_answers.py` (D2 still retains both) |
| App preview/player/render | **7,249** (31) | **7,501** (32) at `83ac7b63`; flat-source in flight: **7,503** |
| Duplicate Agent reference copy | **1,473** (`docs/reference/timeline-composition-v0.0.6`) | unchanged |
| Duplicate App Composition vendor | **1,416** (17) | unchanged |
| Duplicate App default/theme vendor copies | **1,091** (64) | unchanged |

Adoption of the central package can delete the App’s 1,416-line Composition source copy and 1,091-line static default/theme copies after the App manager’s root/package/vendor adoption. It does not delete the 7,249–7,503 lines of App host/preview/player/render source, the 85-line fallback source, Agent host wrappers, Agent’s old reference copy without a separate docs decision, `vendor/astrid-build-inputs`, fonts, custom media, or RenderClockTail handling. Do not sum canonical and duplicate rows as two savings claims.

Next bounded cuts (not applied here):

1. **Agent D09 consumer retirement:** after the in-flight scene-compose candidate is independently reviewed, migrate `sdk/timeline/check.py`, `sdk/timeline/reflow.py`, and `timeline_visualize/overlays/labels.py`; then remove only `core/timeline/onscreen.py` and its old tests. Current imports/calls are real (`check.py:48,84,210`; `reflow.py:1015`; `labels.py:28`). Preserve `fast_lane`, `sweep`, and `_timing_evaluators`. Required replacement evidence: `test_scene_answers.py`, `test_host_scene.py`, `test_native_scene_inputs.py`, plus named check/label caller tests; D2’s `test_motion_diagnostics_public.py` is not by itself sufficient.

2. **Agent D2 region slice:** once every supplied-scene caller has public facts, remove only the `model.boxes_at`/face-region path still reached by `motion/lint.py:136`; retain the no-facts fallback until fonts, custom media, and unsupported modifiers have equivalent public facts. Existing originals are `test_timeline_visualize_motion_views.py` (`test_lint_flags_face_frame_small_and_sync`, `test_declared_face_zone_on_real_footage_is_linted`, `test_presenter_face_box_follows_zoom_and_focus`); replacements are D2’s 22 public diagnostics tests. No whole `motion/model.py` deletion.

3. **App D08 adapter cleanup:** after App adoption, delete only proven-replaced branches in `playerEvaluation.ts`, `VisualClip.tsx`, and `TimelineRenderer.tsx`. Keep custom/typed components, unsupported media/fonts, native audio, and host timing. Candidate tests already name the boundary: “canonical 0.0.9 compiled preview and public draw”, “retains unsupported custom tracks…”, “retains host path for video transitions…”, and the half-open/trim/speed/audio tests.

No owned helper or asset is called truly unreferenced on name alone. M3 remains open; frame/audio parity, owner film, and macOS are unrun.
