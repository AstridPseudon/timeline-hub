Implemented the normal PCM join on exact base `2019d7e69ceb9b10f18cc311e570d635b16c15d8`, with a confirmed blocker for general native layers. Changes remain uncommitted for the harness. No git mutation, install, full suite, browser, socket, HTTP request or video render was performed.

The four product changes are confined to the granted files:

- `service._segment_request` retains original clips/tracks for the selected layer, the canonical native window, existing alpha stamp, and existing materialized-timeline digest. It keeps all selected-track clips, including overlap peers. Explicit `supports_windows: false` still uses the original rebasing implementation.
- `TimelineRenderView.to_json_data` preserves the actual source placement precision. Its previous millisecond rounding moves the tested placement `0.016682` from frame 0 to frame 1 at 30000/1001. Persistence still rounds as before, source tracks still disappear from render props, validation still runs, and output nested data remains independent of authored data.
- Normal `run.py` calls `prepare_normal_audio_sources` on its final serialized Root props, within the existing ExitStack and asset-server lifetime. A private TemporaryDirectory under the materializer's serving root retains WAVs through consumption and removes them on every exit. Selected PNG capture keeps its existing path.
- `normal_audio.py` accepts the existing canonical profile's explicit internal FPS, without inventing compiledTransitions props. It retains existing managed-registry comparison and selected-byte digest checks, then uses the unchanged public12 trim/rate/apply/WAV kernel. Clip/track scalar gain and mute data remain in props; envelope WAV samples do not bake those gains.

No R4 custody/factory, source certificate, DTO, projector/compiler, authority inferred from app metadata, ID parsing, feature flag, alignment or fallback was added. The pin, package/lock files, three MJS kernels, and both compiler xfails are byte-identical to base. The compiler xfails remain appropriate: their test executes projection before render preparation, rather than the intended active render path.

The new socket-free tests execute the actual normal locked renderer through final props serialization. Only unrelated registry/effect setup, port selection, the HTTP server, and renderer consumption are substituted. AssetMaterializer, original timeline validation/serialization, source integrity, Python-to-Node helper launch, public12 preparation and native FFmpeg decoding run for real. Full, unlayered-window and layered-window cases check original submillisecond placement, rational public trim/rate, nonlinear fade, overlapping clips, opaque app data, clip gain 3, clip silence 0, track gain 0.5, full stereo WAV clock/content, retention through consumption, cleanup after success/error/cancellation/timeout, partial-batch failure, digest failure and native decode failure. This proves preparation/retention, not HTTP delivery, MP4 output, Player behavior or audio parity.

Exact commands ran from `/home/user/work/wt/vw-m3-pcm-native-window-resume-r1`. `test-targeted.sh` is copied alongside this report and expands to `env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node ASTRID_REMOTION_PROJECT_DIR="$TASK_WORKER/audio-project" PATH="/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short "$@"`. Ambient unsupported Node loader overrides were removed for the process, with no production validation change.

```bash
TASK_WORKER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-native-window-resume-r1

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$TASK_WORKER/prepare-overlay.py"
# Private real @scope directories and readonly package leaf links; own extracted public12 artifact.
# SHA256 0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3.

bash "$TASK_WORKER/test-targeted.sh" \
  tests/packs/rendering/test_normal_audio_run.py \
  tests/packs/rendering/test_normal_audio_sources.py \
  tests/packs/rendering/test_remotion_native_window.py
# FINAL: 67 passed in 11.80s, exit 0. See -green.log.

bash "$TASK_WORKER/test-targeted.sh" \
  tests/timeline/test_timeline_characterization.py \
  tests/core/timeline/test_source_role_tracks.py \
  tests/editing_conformance/test_compile_contracts.py \
  tests/core/rendering/test_service.py::test_window_timeline_allowlist_slices_to_layer_tracks \
  tests/core/rendering/test_service.py::test_window_timeline_without_allowlist_keeps_existing_pruning \
  tests/core/rendering/test_service.py::test_window_timeline_allowlist_track_without_window_clips_stays_present \
  tests/core/rendering/test_service.py::test_segment_request_stamps_astrid_layer_metadata_merged \
  tests/core/rendering/test_service.py::test_segment_request_z0_stamps_alpha_false
# 59 passed, 2 existing xfailed, 161 subtests passed in 3.31s; exit 0. See -neighbors.log.

env -u NODE_OPTIONS -u NODE_PATH /tmp/vw-m3-agent-gate-node20.19.4/bin/node \
  "$TASK_WORKER/audio-project/tests/normal-audio-sources.test.mjs"
# 8 passed, 0 failed/skipped, exit 0. See -public12-direct.log.

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$TASK_WORKER/capture-red.py"
# Final new tests on exact original base product bytes: 20 failed, 4 passed in 4.53s.
# Test subprocess exits 1 as expected; capture script restores all edited source in finally.
# See -red.log. No test expectation/xfail/skip was weakened.

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python "$TASK_WORKER/compare-static.py"
# Exact Ruff/mypy commands are in the script and -{ruff,mypy}-{base,current}.log.
# Ruff: 13 existing findings on base and current; zero additions.
# Targeted mypy with --follow-imports=skip: base 19, current 17; zero additions.
# These are baseline comparisons, not clean whole-repository lint/typecheck passes.

git diff --check
# exit 0. Complete patch also passes git apply --reverse --check.
```

Blocking executable counterexample to the preferred layer approach: a valid 10-second bottom plate plus an empty top track, rendered at window [150,180) / 30fps. The original timeline accepts `--frames=150-179`. Filtering to the original empty top layer retains the correct canonical window and alpha stamp, but its authored extent becomes one frame, and the existing native guard refuses `Remotion window extends beyond the full composition`. Legacy rebasing retains `duration_seconds: 1` and a null native window, so Root can render the empty transparent fill. Layers whose last selected clip ends before the window have the same problem. No authored duration/origin stamp was fabricated to bypass it, and no test was rewritten to accept lost fill behavior.

Reproduce without sockets or a renderer:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-native-window-resume-r1-empty-layer.py
# exit 0: reproducer asserts and prints the limitation; saved as -empty-layer.json.
```

Recommendation: do not qualify/merge the generalized native layer change until the orchestrator grants a minimal original-composition duration seam shared by service and Root, with empty/sparse-layer behavior tests. Root is outside this worker's grant. The PCM join and precision preservation are implemented and tested; the whole task is marked BLOCKED rather than DONE because the specified layer strategy has this demonstrated contract violation. After that correction, HTTP/MP4/preview parity must be qualified centrally on a repaired dependency graph.

Transferable evidence shares this absolute flat prefix:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-native-window-resume-r1-`
Files include REPORT.md, implementation.patch (all five changed/new paths), test_normal_audio_run.py, test-targeted.sh, prepare-overlay.py, compare-static.py, source.json, red.log, green.log, neighbors.log, public12-direct.log, static-delta.json, empty-layer.py/json, and shared-before/after/delta.json. Copied worker scripts retain their original worker-directory assumption; place them in the named worker directory when replaying. The source JSON binds exact changed bytes, unchanged kernels/pins and base revision.

Before/after lstat inventories show zero added/removed/changed entries in App node_modules (35,618 entries), borrowed scene-host Remotion node_modules (23,132), and venv-agent (16,267). This demonstrates no drift during this worker's run, not repair or qualification of either previously disqualified graph. The private overlay remains under the worker directory for replay; no build output or temporary files remain in the repo. No full suite or make check was requested/run.
