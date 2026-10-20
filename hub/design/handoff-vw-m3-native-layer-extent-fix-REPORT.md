Implemented the bounded original-extent handoff on **abd41eb2a6a8fe9224028018ac65225018e490bd**. The narrow task is complete; the generalized candidate is **still held**, pending the existing precision/tail decisions, current consumer adoption, independent Root metadata tests, and later qualification. No MP4 output, pixel/alpha output, audio parity, or Gate 6 claim.

Read PLAN.md, COMMON.md, the 09:03 grant in managers/viewing/INBOX.md, the empty-layer seam report/probe, and the PCM window final DEFECT review. No settled policy was changed.

The narrow delta changes three product files and two Python test files:

- `service._segment_request` removes caller `astrid_composition_duration_frames` before every path, including the unlayered early return and legacy slicing. For native layers it measures the original `Timeline.from_json_data(...).for_render().to_json_data()` with the existing `timeline_render_duration_frames` at the segment's rational FPS, checks the original bound before filtering, then overwrites the reserved request metadata with the computed frame count. Source-role reference clips do not count. It preserves the original native window, all original selected clips, alpha stamp and existing materialized hash.
- Normal Remotion support and locked execution use the same native-window validator. The request parser accepts canonical positive decimal safe integers only. The validator requires the native isolated-layer context, retains exact canonical FPS equality and existing speed/source-range restrictions, rejects a retained extent below selected clips or a window above it, and refuses concurrent legacy/render-tail clocks. Full/no-window and unlayered executor requests refuse a supplied extent. Both executor staging branches forward the value. Only the validated optional fact becomes `astridCompositionDurationInFrames`; normal preparation preserves it by copying existing props.
- Root reads that optional host prop, checks a positive safe integer covering local clips, rejects clock collisions, and uses it for composition metadata duration. The CLI still selects absolute `--frames=150-179`. Root's scene, tail rendering, canvas selection, package inputs, and no-override duration behavior are unchanged. This worker did not edit `remotion/tests/root-metadata.test.cjs`.
- Added `test_native_layer_extent.py` and strengthened the existing actual normal-props/PCM test to pass the retained fact through preparation and assert the same rational FPS in props. No behavior assertion was muted, deleted, or changed to expect loss.

The backend consumes metadata as an internal invocation fact within the existing trusted service/backend boundary. This is not a source certificate or authentication protocol for callers that bypass the service and fabricate a complete isolated-layer invocation. Service adaptation ignores incoming reserved values; authored metadata never supplies the retained count. No DTO, schema, authored stamp, second projector, authority check, new tail policy, or public Composition package change was introduced.

Evidence establishes empty/sparse [150,180) layers retain 300 frames; identical filtered empty inputs retain distinct 300/600 originals; 30 and 30000/1001 FPS work; longer source-role references do not enlarge the bound; selected clips, source bytes and opaque fields remain unchanged. Negative cases cover original overrun, malformed/huge/boolean/fractional/nonfinite values, short retained extent, FPS mismatch, speed/source_range, full/unlayered injection, legacy clock and an otherwise valid tail clock. Existing no-override, PNG and Three.js seams remain covered by the targeted native-window suite. Empty/sparse normal command assembly exercises both z=0 and alpha z=1 through real serialization/materialization and the no-audio preparation path; it checks props and codec/window flags, not pixels.

Real normal PCM tests execute managed asset digest checks, native FFmpeg decode and the extracted public12 audio helpers. Runtime/project/effect setup, port selection, HTTP serving and renderer consumption are substituted. They preserve clip/track gain, trim/rate, overlap, nonlinear envelope samples and rational source clocks, and verify success/error/KeyboardInterrupt/timeout/partial preparation cleanup. Canonical profile/theme resolution is substituted consistently; no end-to-end profile-resolution claim.

Exact commands, from `/home/user/work/wt/vw-m3-native-layer-extent-fix`:

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
PY=/home/user/work/venv-agent/bin/python
NODEBIN=/tmp/vw-m3-agent-gate-node20.19.4/bin
PROJECT=$ORCH/workers/vw-m3-native-layer-extent-fix/audio-project

# Before product edits, initial nine behavior regressions on base abd41eb2:
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" "$PY" -B -m pytest -q   -o addopts= -p no:cacheprovider --tb=short   tests/packs/rendering/test_native_layer_extent.py   -k 'keeps_original_extent or distinct_original_extents or enlarge_original_layer_bounds'
# exit 1: 9 failed, 34 deselected; -red.log.

# Final tree, after the last test edit:
env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD"   ASTRID_NODE_EXECUTABLE="$NODEBIN/node" ASTRID_REMOTION_PROJECT_DIR="$PROJECT"   PATH="$NODEBIN:$PATH" "$PY" -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short   tests/packs/rendering/test_native_layer_extent.py   tests/packs/rendering/test_remotion_native_window.py   tests/packs/rendering/test_normal_audio_run.py   tests/packs/rendering/test_normal_audio_sources.py   tests/packs/rendering/test_normal_audio_source_phase.py
# exit 0: 127 passed in 13.87s; -targeted-final.log.

# Unchanged neighboring timeline/service lanes:
env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD"   "$PY" -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short   tests/timeline/test_timeline_characterization.py   tests/core/timeline/test_source_role_tracks.py   tests/editing_conformance/test_compile_contracts.py   tests/core/rendering/test_service.py::test_window_timeline_allowlist_slices_to_layer_tracks   tests/core/rendering/test_service.py::test_window_timeline_without_allowlist_keeps_existing_pruning   tests/core/rendering/test_service.py::test_window_timeline_allowlist_track_without_window_clips_stays_present   tests/core/rendering/test_service.py::test_segment_request_stamps_astrid_layer_metadata_merged   tests/core/rendering/test_service.py::test_segment_request_z0_stamps_alpha_false
# exit 0: 59 passed, 2 existing strict xfailed, 161 subtests passed in 3.30s; -neighbors.log.

# Changed tests' name/import checks:
env PYTHONDONTWRITEBYTECODE=1 "$PY" -B -m ruff check --no-cache --isolated --select F   tests/packs/rendering/test_native_layer_extent.py tests/packs/rendering/test_normal_audio_run.py
# exit 0: All checks passed.

env PYTHONDONTWRITEBYTECODE=1 "$PY" -B -m ruff check --no-cache   astrid/core/rendering/service.py   astrid/packs/rendering/rendering/renderers/remotion/run.py --output-format concise
# exit 1: 13 pre-existing diagnostics; -ruff.log.
# Each file was also checked from stdin against git show abd41eb2:<path> with
# --output-format=json --stdin-filename <path> -; all diagnostic codes/messages
# match exactly (6 service + 7 runner); -ruff-comparison.json.

git diff --check
git diff --check abd41eb2
# both exit 0.
```

The first all-case extent run exposed test setup mistakes (an unbounded legacy media fixture, an empty string already refused by the request DTO, and missing registry files). Those fixtures were corrected; no product behavior was relaxed. Intermediate logs remain, and `-targeted-final.log` is the final-tree result.

Private overlay: real `audio-project/node_modules/@banodoco` directory, one leaf link to its own privately extracted public12 package, and the three unchanged MJS helper files copied from this worktree. It needs **zero shared node_modules links**. Archive SHA256 is `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; see `-overlay.json`. The shared venv and Node executable were read only. No dependency installation, cache mutation, network, browser, socket, render, full suite, make check, git mutation or push was performed. No repository report/build output was created. The existing shared graph repair/qualification hold remains.

Exact deliverables, all under the absolute prefix shown below:

- `-narrow.patch`: abd41eb2 -> this worktree, including the new test file.
- `-whole-candidate.patch`: 2019d7e69ceb9b10f18cc311e570d635b16c15d8 -> this worktree, including the new test file. This includes the inherited normal PCM join and precision serializer; it is not a merge-ready claim.
- `-source-state.json`: exact modified file hashes and byte-equality checks for the inherited precision serializer, normal_audio.py, helper kernels and pin/lock files against abd41eb2. Those inherited files are unchanged by this task.
- `-red.log`, `-green.log`, `-boundary.log`, `-targeted.log`, `-targeted-final.log`, `-neighbors.log`, `-ruff.log`, `-ruff-comparison.json`, `-overlay.json`.

Absolute prefix: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-native-layer-extent-fix`.

No bounded implementation blocker remains. Recommended next step: combine this exact delta with the parallel independent Root metadata tests for review, retain the precision/tail/current-consumer holds, then seek the orchestrator's separate qualification grant after graph repair. Actual empty/sparse alpha output, current public consumer adoption and planted frame/audio mismatches remain unverified here.
