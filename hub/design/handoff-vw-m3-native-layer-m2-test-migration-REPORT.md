Completed the granted test-only migration on `626eed656edf2a6398703e9e5318343069e47019`. Only `tests/packs/rendering/test_live_scene_composition.py` changed (three existing test functions, five previously failing nodes; one new function adds two nodes). No product, nonowned M2, dependency or pin files changed. All other existing definitions, including the browser case, remain byte-identical. No skips, xfails, removed behaviors, new contracts or git mutations.

The five migrated existing nodes are:

- `test_service_layered_plan_native_renderer_isolates_and_adjusts_once[0]`
- `test_service_layered_plan_native_renderer_isolates_and_adjusts_once[1]`
- `test_native_window_layer_is_materialized_once_with_pin_hold_and_alpha[0]`
- `test_native_window_layer_is_materialized_once_with_pin_hold_and_alpha[1]`
- `test_layer_materialization_retains_null_window_support_rejection`

Native inputs retain the complete original selected clip and absolute FrameWindow. The first pair still asserts the exact local slice `(at,from,to,speed,hold)=(0,63,65,2,2)` at 10 FPS after the existing Three.js adapter. The second pair now exercises actual Three.js protocol serialization/window adaptation at 30 FPS, stopping at a mocked capture executor before any render. For each z=0/1 it compares the native payload against the existing supports_windows:false legacy payload, checks exact clip ID/source bounds/rate/hold, alpha and MP4/MOV choice, complete pinned package/source/revision and nested opaque app data, and unchanged original input bytes. Legacy still receives a null window and the old service slice; its adapter remains a no-op. Exact payload equality and single window suffix catch double trimming. Local duration is one second; all 30 visible frame source times match the original absolute clock and remain in [63,65), with the hold clamped to 2 source seconds and the half-open visibility ending at local second 1.

New coverage: **two** `test_native_layer_window_supports_windows_only_backend[0/1]` nodes, **four** capture-seam observations (native/legacy × z=0/1), **120** per-frame source-clock comparisons. The old null-window windows-only refusal remains a direct backend negative and still checks the full-timeline refusal reason. Its matching new positives prove valid native windows are accepted. Static fixture clip/track declarations were completed so these support results exercise the clock capability rather than missing content declarations. An initial run caught those missing fixture declarations (two new positives failed; all 15 existing nonbrowser nodes passed); no product behavior or fixture timing was changed to hide a consumer difference.

Exact test commands and results (all run directly from `/home/user/work/wt/vw-m3-native-layer-m2-test-migration`):

```sh
env -u PYTHONPATH -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_live_scene_composition.py -k 'not real_render'
```

Original: **5 failed, 10 passed, 1 deselected**, exit 1. Final: **17 passed, 1 deselected**, exit 0. The deselected test is the unchanged `test_real_render_scene_window_audio_and_overlay`.

```sh
env -u PYTHONPATH -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_native_layer_extent.py tests/packs/rendering/test_remotion_native_window.py tests/packs/rendering/test_remotion_capture_scene_props.py
```

**109 passed**, exit 0.

```sh
env -u PYTHONPATH -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/core/rendering/test_service.py -k 'window_timeline or segment_request'
```

**5 passed, 47 deselected**, exit 0.

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m ruff check --no-cache tests/packs/rendering/test_live_scene_composition.py
git diff --check
```

Both pass, exit 0. No full suite, browser, socket, real render, install, network, dependency/cache writes, remote operation or push was performed. The tests use real serializers/adapters and stop before capture; they do not qualify actual TypeScript execution, MP4 pixels/audio, Runtime capture or package/consumer integration. No final adapter payload or clock defect was found within this tested scope. No blockers remain for this bounded migration.

Handoff artifacts (flat absolute paths):

- Report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-native-layer-m2-test-migration-REPORT.md`
- Exact patch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-native-layer-m2-test-migration-exact.patch`
- Tested source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-native-layer-m2-test-migration-source.py`
- Base/source hashes and scope checks: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-native-layer-m2-test-migration-source.json`
- Exact commands/results: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-native-layer-m2-test-migration-tests.txt`
- Original five-red log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-native-layer-m2-test-migration-original-red.log`
- Final nonbrowser log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-native-layer-m2-test-migration-nonbrowser.log`
- Direct controls: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-native-layer-m2-test-migration-direct.log`
- Service controls: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-native-layer-m2-test-migration-service.log`
- Lint: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-native-layer-m2-test-migration-lint.log`
- Initial new-fixture failure: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-native-layer-m2-test-migration-initial-new-positive.log`

Recommended next step: orchestrator reviews this narrow test patch and composes it with the approved pre-tail fix, then performs the separately authorized integration qualification. This worker has not merged or remotely changed anything. Commit message and DONE are in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-native-layer-m2-test-migration`.
