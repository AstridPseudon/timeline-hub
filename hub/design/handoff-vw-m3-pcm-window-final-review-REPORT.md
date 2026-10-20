# DEFECT — native layer duration is lost

Independent final review of **abd41eb2a6a8fe9224028018ac65225018e490bd**, producer `vw-m3-pcm-native-window-resume-r1`, against **2019d7e69ceb9b10f18cc311e570d635b16c15d8**. Do not merge/qualify the generalized native-layer change yet. The PCM preparation join and placement-precision fix work in the exercised normal path; one blocking layer regression remains. No product or repository files were edited by this review.

## Blocking finding

**P1: filtering a native layer drops the original composition extent.** `astrid/core/rendering/service.py:1092` retains only selected tracks/clips and forwards the original absolute window, without retaining the composition duration. `astrid/packs/rendering/rendering/renderers/remotion/run.py:911` then checks that window against the filtered layer's shorter extent. A valid original timeline with a bottom clip [0,10), an empty top track, and window [150,180) at 30 fps accepts `--frames=150-179` before filtering, but refuses afterward: `Remotion window extends beyond the full composition`. A top clip ending at 2 seconds produces the same failure. The old non-window materialization preserves an explicit one-second fill span and a null native window. Root's unchanged metadata calculation also derives native duration from the filtered clips, so removing the Python guard alone would not restore the missing span.

Independent executable counterexamples preserve the intended success assertion; **2 failed, exit 1**, both at the native-window guard. Their original-window and legacy-fill assertions pass first. Source fixtures use bounded media clips with explicit `from`/`to`. See `handoff-vw-m3-pcm-window-final-review-layer-defect.log` and the flat `-test_review_layer_duration.py` artifact. The initial probe had an invalid legacy fixture in its second case; that fixture was corrected before the final recorded two-case result. No product test was weakened or marked to expect lost behavior.

Recommended next step: orchestrator grants a narrow original-composition duration handoff shared by the service and Root, with empty/trailing-layer regressions. Preserve the original clips/window/phase while restoring transparent or background fill for the requested extent. That correction crosses this grant's Root boundary; this review makes no implementation choice or edit. The producer independently reported the same blocker.

## Frozen source and scope

Read PLAN, COMMON, the producer brief, and the authoritative original 07:58 grant. Began static prerequisite review while the producer ran; no tests executed against its mutable tree. Its `workers/vw-m3-pcm-native-window-resume-r1/exit` contains `0`, `ended` is `2026-10-20T09:00:24Z`, and the harness branch tip is the SHA above. The harness uses an `exit` file containing `0`, rather than a literal `exit0` filename.

Recreated the entire frozen commit with read-only `git archive` under this reviewer's own worker directory. Tests import/run that snapshot, preserving repository-relative test/source paths. `-source-bindings.json` records all four reviewed product modules and the normal-path test module resolving inside the snapshot when launched from the runner's candidate cwd. Before and after testing, every **2,930 tracked blobs**, executable mode, and symlink payload matched `git ls-tree` object IDs; no unexpected files existed in the snapshot. Tree ID: **2c5af9074aeccfa7a49ce2aaad044a89e03c628f**. The initial review worktree stays on the original base and remains clean.

The private audio project has real scope directories and package leaf links, with its own extracted public12 package. Its 19 copied source/test files match the frozen snapshot; all 77 extracted package files match the committed archive. Archive SHA256: **0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3**. No shared dependency/cache writes, installation, network, git mutation, merge, or remote request occurred. Before/after lstat manifests of App node_modules, borrowed scene-host node_modules, and venv-agent are equal. This does **not** repair or qualify the previously polluted graph; that hold remains.

The candidate changes exactly four granted product files plus `test_normal_audio_run.py`. Pin/lock files, the three MJS kernels, Root, the compiler, request DTOs and the two compiler-xfail fixture entries are unchanged from base. No R4 source factory/custody, certificate, new DTO, projector, colon/ID parsing, shape heuristic, or inferred app-metadata authority was introduced.

## What the executable evidence establishes

- `_segment_request` preserves unlayered native requests, original selected-track clips (including overlap peers), the canonical window, opaque data and host alpha stamp; explicit legacy non-window requests still use the existing rebasing path. The existing original-input and materialized-timeline SHA bindings remain. Actual `_execute_planner` merges those hashes into normalized segment inputs; no new certification is claimed.
- Normal `run.py` supplies the final serialized Root props directly to `prepare_normal_audio_sources` inside the existing ExitStack. The active native route supplies no transformed/original pair: it retains original clip clocks. Real serialization, AssetMaterializer, registry comparison, managed digest checking, helper launch, native FFmpeg decoding, public12 trim/rate/envelope/WAV operations, and props writing execute in the tests. Profile/theme/registry/effect initialization, port selection, HTTP server and renderer consumption are substituted. These are actual normal-preparation tests, not just green helper calls.
- The caller derives explicit helper FPS from `_canonical_profile().fps_rational`, without fabricated `compiledTransitions` props. The normal fixture supplies 30000/1001 as that canonical profile; existing native-window tests cover frame-window rejection. Full, unlayered-window and layer cases preserve public rounded trim and child playback rate, nonlinear fades, overlap and opaque fields. Scalar clip gain 3, zero clip volume and track gain 0.5 stay in props; envelope-only WAV samples do not bake those scalar gains.
- Independent retry cases consume the same original timeline/registry twice: first consumer failure, then success. Attempts use distinct paths and identical PCM bytes; previous WAVs are removed and inputs remain byte-identical. Additional real materializer reuse cases verify successful and failed consumption remove derived attempt files from the reused root while preserving the original managed file. Producer tests cover success, error, KeyboardInterrupt, timeout, partial-batch failure, wrong registry/digest and verified-but-undecodable bytes.
- The precision fix is necessary, rather than a claim that millisecond normalization is harmless. An independent source-phase probe runs actual `Timeline.from_json_data(...).for_render()` at `at=0.016682`, fps=30000/1001. Base renders `at=0.017`, start frame 1 instead of original frame 0 (**exit 1**). Candidate preserves `0.016682`, start frame 0 (**exit 0**). Render serialization avoids that persistence rounding; persistence still retains its prior convention. This route performs no extra compiler pass, so compiler idempotence does not excuse or hide the source-phase change. No corpus-wide compiler-idempotence claim is made.
- Embedded-video audio remains on the unchanged public12 Video path: the Python preparer selects only audio-kind tracks, and the public visual-media Video branches retain trim/rate, effective volume, and `muted: effectiveVolume <= 0`. There is no new blanket video mute or stripping of visual media. This is source/props review, not an audible embedded-video playback proof.
- Both compiler xfails stay strict and unchanged: they execute pre-render projection, not the intended active preparation path. Neighbor tests confirm **2 xfailed**, with no XPASS or marker removal.

## Exact commands and results

All paths below are absolute definitions; the runner changes into the frozen candidate. Its command is `env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TASK/candidate" ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node ASTRID_REMOTION_PROJECT_DIR="$TASK/audio-project" PATH="/tmp/vw-m3-agent-gate-node20.19.4/bin:$PATH" /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short "$@"`.

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
TASK=$ORCH/workers/vw-m3-pcm-window-final-review
PY=/home/user/work/venv-agent/bin/python
NODE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node

env PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$TASK/freeze.py"
# exit 0; -freeze.log: exact frozen source + private overlay.

bash "$TASK/test-targeted.sh" \
  tests/packs/rendering/test_normal_audio_run.py \
  tests/packs/rendering/test_normal_audio_sources.py \
  tests/packs/rendering/test_normal_audio_source_phase.py \
  tests/packs/rendering/test_remotion_native_window.py \
  "$TASK/test_review_retry.py"
# 82 passed in 18.00s, exit 0 (-targeted-final.log; includes retry/reused-root cases).
# Earlier run before adding the reused-root cases: 76 passed, exit 0 (-targeted.log).

bash "$TASK/test-targeted.sh" "$TASK/test_review_retry.py" -k reused_managed
# 6 passed, 3 deselected, exit 0 (-reused-root.log).

bash "$TASK/test-targeted.sh" \
  tests/timeline/test_timeline_characterization.py \
  tests/core/timeline/test_source_role_tracks.py \
  tests/editing_conformance/test_compile_contracts.py \
  tests/core/rendering/test_service.py::test_window_timeline_allowlist_slices_to_layer_tracks \
  tests/core/rendering/test_service.py::test_window_timeline_without_allowlist_keeps_existing_pruning \
  tests/core/rendering/test_service.py::test_window_timeline_allowlist_track_without_window_clips_stays_present \
  tests/core/rendering/test_service.py::test_segment_request_stamps_astrid_layer_metadata_merged \
  tests/core/rendering/test_service.py::test_segment_request_z0_stamps_alpha_false
# 59 passed, 2 xfailed, 161 subtests passed; exit 0 (-neighbors.log).

bash "$TASK/test-targeted.sh" "$TASK/test_review_layer_duration.py"
# 2 failed as intended behavior counterexamples; exit 1 (-layer-defect.log).

env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/vw-m3-pcm-window-final-review \
  "$PY" -B "$TASK/source_phase_probe.py"
# Base red: exit 1, original start 0 -> rendered start 1 (-phase-base.log).
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TASK/candidate" \
  "$PY" -B "$TASK/source_phase_probe.py"
# Candidate green: exit 0, original/rendered start 0 (-phase-candidate.log).

env -u NODE_OPTIONS -u NODE_PATH "$NODE" "$TASK/audio-project/tests/normal-audio-sources.test.mjs"
# 8 passed; exit 0 (-public12-direct.log).
env -u NODE_OPTIONS -u NODE_PATH "$NODE" "$TASK/audio-project/tests/normal-audio-native-sources.test.mjs"
# 5 passed; exit 0 (-public12-native-direct.log).
# Earlier combined node --test invocation: 2 file passes, exit 0 (-public12.log).
# Direct execution above supplies the individual case counts.

git -C /home/user/work/wt/vw-m3-pcm-window-final-review diff --check \
  2019d7e69ceb9b10f18cc311e570d635b16c15d8 abd41eb2a6a8fe9224028018ac65225018e490bd
# exit 0.

env PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$TASK/freeze.py" verify
# exit 0; -source-verification.log: all 2930 blobs and overlay/package copies exact;
# shared metadata equal. Repeated after the final focused run.
```

Flat report/log/script prefix: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-window-final-review-`. Worker scripts remain runnable at the absolute TASK location above; flat copies preserve review inputs for inspection.

No full suite, browser, socket, HTTP fetch, normal video render, MP4 output, App Player comparison, end-to-end canonical-profile resolution, whole-repository lint/typecheck, or Gate 6/environment qualification was performed or claimed. Native-source tests retain their explicit unknown decoder-origin limitations. Review work is complete; the candidate defect belongs to the orchestrator/producer, so this reviewer writes DONE rather than marking its own task blocked.
