**Bounded candidate implemented; clean CURRENT qualification is BLOCKED by five preserved M2 test expectations.** No decision was changed, and no extra product scope was ported. No DONE marker is written.

Tested CURRENT base: `c456b3281497653cecf44f61acd6fa30565d83c8`, branch `tl/vw-m3-current-native-extent-unit`, plus the uncommitted five-file delta in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-unit-scope.patch`. The harness has not yet created a resulting commit SHA. Exact tested file hashes are in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-unit-source.json`.

**Minimal delta.** Three product files only: service +46/-10, run +46/-3, Root +14/-2 (106 insertions / 15 deletions). Two new direct-test files: Python 328 lines and the exact Root 227-line file.

- Service `_segment_request` is byte-identical to that method in approved `61f1a420f1f355ee0d16ffb0dbeb617b83b1b044`: ONLY its original-track filtering from 2019d7e69 -> abd41eb2 and its original-extent delta were taken. It strips caller reserved extent before early returns, measures the original render-ready document before isolation, excludes Source-role references through the existing render view, refuses windows beyond that extent, retains selected clips and absolute windows, and preserves alpha/private input hashing and legacy slicing.
- Run ports only the positive-safe-integer parser, native-layer/clock/bounds guards, staging/protocol forwarding and optional Root prop. Support and locked execution use the same retained fact and FPS; the negative tests compare the actual error text across those paths.
- Root is byte-identical to approved 61f1a420f. The seven-case test file is byte-identical to `20d4ab1aa9a1fb436634163e4606fc05b6e2318f` on `tl/vw-m3-native-extent-root-test-unit`; SHA-256 `181950efa7e91f646d57496b33897e4e40ec6723c695f6bb6d8ffe940443b6cc`.
- CURRENT `capture_remotion_frames` is AST-identical; its callback parameter/body and callback invocation in locked execution remain. Current M2 files, Three.js implementation, package/pin/lock files and serializer remain unchanged. No normal PCM caller/helper/kernel, for_render precision, old branch ancestry, DTO, factory, authored stamp, projector, or saved-timeline write was added.

**Direct test evidence.** All commands below ran from `/home/user/work/wt/vw-m3-current-native-extent-unit`. No full, browser, socket, render, install, network, git mutation or push was run. The sole dependency link is a TypeScript leaf under this worker's private real `root-modules/node_modules` directory, targeting the read-only shared package. No shared dependency/cache files were written.

```sh
env -u PYTHONPATH -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_native_layer_extent.py tests/packs/rendering/test_remotion_native_window.py tests/packs/rendering/test_remotion_capture_scene_props.py
```

PASS: **109 passed in 4.35s**, exit 0. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-unit-direct.log`. Covers CURRENT full/window/default commands, selected PNG, alpha, legacy and Three.js seams; empty/sparse/source layers at original 300/600 frames with integer/rational FPS; reserved forgery, too-short/overlong bounds, FPS/source-range/speed/clock conflicts and malformed layer facts; both staging paths; unchanged capture callback lifecycle. Original input bytes remain unchanged. The added Three.js comparison proves that its existing adapter still produces the same complete local slice, source range/rate/hold, pin and alpha metadata as the previous service slice, for z=0/1.

The borrowed producer fixture initially produced two failures because it expected the held serializer to preserve `at=0.016682`. The CURRENT port now asserts that the private service input preserves the raw clip and that CURRENT serialization still yields `at=0.017`. This does not port precision. An initial added 600-frame rational fixture incorrectly used 20 seconds (=599 frames at 30000/1001); it was corrected to derive seconds from the intended frame count. Product arithmetic was unchanged.

```sh
env -u PYTHONPATH -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/core/rendering/test_service.py -k 'window_timeline or segment_request'
```

PASS: **5 passed, 47 deselected in 0.29s**, exit 0. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-unit-service-neighbors.log`.

```sh
env -u NODE_OPTIONS -u NODE_TEST_CONTEXT ROOT_SOURCE_DIR=/home/user/work/wt/vw-m3-current-native-extent-unit/remotion/src NODE_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-native-extent-unit/root-modules/node_modules /tmp/vw-m3-agent-gate-node20.19.4/bin/node remotion/tests/root-metadata.test.cjs
env -u NODE_OPTIONS -u NODE_TEST_CONTEXT ROOT_SOURCE_DIR=/home/user/work/wt/vw-m3-current-native-extent-unit/remotion/src NODE_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-native-extent-unit/root-modules/node_modules /tmp/vw-m3-agent-gate-node20.19.4/bin/node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-unit-root-supplement.test.cjs
```

PASS: exact file **7/7**, supplement **2/2**, both exit 0. Logs: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-unit-root-direct.log` and `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-unit-root-supplement.log`. The supplement exercises both actual Root callbacks for empty/sparse 300/600 extents at 30000/1001 and boolean refusal. The two files were also run together with `node --test` (exit 0, two passing file-level tests; `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-unit-root.log`). These transpile actual Root and stub framework/package imports; they do not constitute semantic TypeScript typechecking, public-package behavior or rendered parity.

```sh
env -u PYTHONPATH -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_live_scene_composition.py -k 'not real_render'
```

**RED: 5 failed, 10 passed, 1 deselected in 12.85s**, exit 1. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-unit-scene-neighbors.log`. The deselected case is the real browser/render test prohibited by this brief. All five failures are in the unmodified CURRENT M2 file:

- `test_service_layered_plan_native_renderer_isolates_and_adjusts_once[0]` and `[1]` expect the service input already rebased to `(at,from,to,speed,hold)=(0,63,65,2,2)`; the granted filter retains `(2,55,75,2,20)` for the existing Three.js adapter to slice once.
- `test_native_window_layer_is_materialized_once_with_pin_hold_and_alpha[0]` and `[1]` require `adapted.window is None`; the grant retains the original FrameWindow.
- `test_layer_materialization_retains_null_window_support_rejection` also requires a null window and refusal by a windows-only renderer. The grant retains a valid native window, so this expectation conflicts with it.

These tests were not rewritten, weakened, deleted, skipped or marked xfail. The successful new adapter comparison demonstrates the same bounded Three.js output description, but does not erase the five red repository nodes or authorize changing M2 tests. The brief explicitly preserves CURRENT M2 files, so the orchestrator must resolve that test-contract conflict before a clean CURRENT qualification can be claimed. No unrelated product fix was attempted.

```sh
/home/user/work/venv-agent/bin/python -B -m ruff check --no-cache tests/packs/rendering/test_native_layer_extent.py
git diff --check
```

Both PASS. Product-file Ruff has **13 inherited diagnostics** (service 6, runner 7): stdin checks with `--stdin-filename <path> --output-format=json` compare CURRENT HEAD against the candidate and have identical code/message multisets. No new lint diagnostic; `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-unit-ruff-comparison.json`. `make check` and semantic TypeScript typecheck were not run under this bounded no-install/no-full brief.

**Held scope and next step.** The exact three-test tail-positive regression file from `e2d926319718c396fe579236eb9c8de5fb00f19f` is preserved separately at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-unit-held-tail-test.py`, byte-identical SHA-256 `f4bdead08a44791188e66b3e479941513689703da9480a20c6c8dc1815c9b792`. It is not ported into this unit and was not rerun on CURRENT: its public12 fixture remains separately HELD. Its original report records two red positives plus one passing ordinary control. No generalized tail qualification is claimed. Tail/legacy clock conflicts still refuse; precision and actual normal PCM activation remain separately held. Nothing here certifies Runtime capture, HTTP, MP4, pixels/audio, the dependency graph, or consumer adoption.

Recommended next action: review this five-file extent-only candidate and authorize a separate migration of the conflicting M2 intermediate-state expectations (retaining the same final slice/pin/alpha behavior), or give an explicit narrower service scope. Until that judgment, this worker stops with BLOCKED for clean CURRENT qualification and leaves the candidate reviewable.

All evidence is flat under absolute prefix `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current-native-extent-unit-*`; no repository documentation or temporary build output was added.
