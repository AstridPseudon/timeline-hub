Applied the Agent-approved preserve-known proposal on exact base `751dd75e2866712a661edce20c4c50b6ac89d7c7`, with the required shorter YAML comment and scene expectations. Read the full approval with `git show hub/timeline/agent/tl/agt-reviews-audio-mouth-scanner:design/agent-review-viewing-20261020b.md`. No branch was merged or switched.

Only three product files changed: am-presenter `motion.ts`, `scene.ts`, `element.yaml`. `mouthInspectionRect` pads the shared actual erase geometry; drawing uses its existing erase helper and body unchanged. Default, partial, fractional and raw-invalid normalized public regions remain KNOWN; mosaic and unsupported outer geometry retain their existing unknowns. Legacy absent/partial/un-normalized anchors remain unqualified, with the private absent-mouth skip, `mouth_box`, fallback and statistics intact. No manifest, registry, generator, core, provider, pin or public type changes. Six direct test files changed alongside these three product files.

The cheap geometry tests now compare private old crop, padded public compatibility ROI and a distinct erase control, using the literal existing generic coordinate-to-PNG conversion. Erase geometry comes from actual shared drawing helpers; no private mouth geometry formula or clock was copied. Cases include partial and malformed anchors and retain the old erase-denominator counterexample. Compatible explicit integer anchors equal the actual normalized anchor; other anchor cases make no legacy equivalence claim.

Prepared ONE explicitly selected central test, `tests/packs/rendering/presenter_crop_capture.py::test_actual_registered_presenter_crop_pixels`. It uses the ordinary generated host/registered TimelineComposition with the immutable public10 archive. The caller prepares one Root, resolves its exact compiled clip id and owner, validates that the public DrawPlan mounts component zero, queries that SAME prepared Root exactly once, and retains this ROI for the series. Cheap tests cover missing, ambiguous, foreign and stale selections; inherited exact-fold tests retain the source-projector occurrence join. This is test preparation, not a production consumer migration or certification claim.

The central capture makes exactly four actual renderStill calls at `[0,3,4,5]`, 1920x1080, fps30, duration60, scale1/3 (640x360), mouth151/104/19, words[[.1,.4]], chrome none, blinkEvery0, seed7. On the same unaltered PNGs it requires old == compat == `(298,202,345,219)` /799, erase `(300,206,343,215)` /387, identical old/compat pixels and fractions, natural >2% positives and matching unchanged natural decisions (including the retained erase control). Fresh copies plant 8 pixels (8/799 vs8/387), 20 detected by all, 15/16 at the old/compat boundary, and 16 padding-only pixels detected by old/compat and missed by erase. All use the existing `_diff_fraction`, CHANGE_LEVEL and strict >2%; original PNG SHA256 bytes must remain unchanged. No image normalization or edited-original positive is allowed.

Flat handoff prefix is `design/handoff-vw-m3-mouth-approved-four-still-` under ORCH:

- `product.patch`: ONLY the three product-file updates against base751; SHA256 `4a442358b70cd51f5a36b9b6228013561fb282db0766037693e10cf796ddbf3d`.
- `patch`: all nine changed files against base751 (not the old branch); SHA256 `169090396f16dba72d8247671d859c68dfc062f91f739b9fb131edd22b9b02cc`.
- `run-central.py`, `READY.sh`, `check.py`, seven `fixture-*` source copies, and this `REPORT.md`. Fixtures are flat review copies; execute the repository paths after applying the selected patch.

The new worker's `READY.sh` selects a clean committed source with ASTRID_CHECKOUT and VIEWING_CROP_REVISION and requires a NEW exact-SHA READY_GRANTED in this worker directory. It acquires the shared browser flock. The controller makes an exclusive RUN_STARTED claim, so the grant is one-shot; no predecessor grant is reused. QUIET writes a fresh PAUSED_ACK and exits75. Pre/post source hashes, full shared dependency bytes/symlink targets, exact six historical Agent Remotion/Player patch hashes, Node, artifact, controller and full browser1194 tree are checked, including after render failure. The existing fixture validates all77 extracted public10 files, six resolved peer entrypoints/hashes/versions before and after, React18.3.1 and Remotion4.0.509. Bundle caches are disabled; private temporary output is removed, and timeout cleanup terminates the Node process group. Machine/SIGKILL cleanup is not claimed. These future controller guards were syntax/AST inspected, not exercised by launching a capture.

Exact final checks (cwd `/home/user/work/wt/vw-m3-mouth-approved-four-still`):

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-mouth-approved-four-still
P=/home/user/work/venv-agent/bin/python
N=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
python3 "$W/check.py" "$P" -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_presenter_crop_equivalence.py tests/packs/rendering/test_presenter_scene_capability.py tests/packs/rendering/test_presenter_motion_fold.py tests/packs/rendering/test_timeline_visualize_motion_views.py::test_presenter_face_box_follows_zoom_and_focus tests/packs/rendering/test_timeline_visualize_motion_views.py::test_mouth_state_matches_presenter_core_cycle --basetemp=/tmp/vw-mouth-approved-final
# 20 passed in 15.18s, exit0. Includes exact286 existing SSR hashes and strict TS declarations.
python3 "$W/check.py" "$P" -m ruff check --no-cache tests/packs/rendering/test_presenter_crop_equivalence.py tests/packs/rendering/presenter_crop_capture.py tests/packs/rendering/test_presenter_scene_capability.py
# All checks passed, exit0.
python3 "$W/check.py" "$P" -m pytest --collect-only -q -o addopts= -p no:cacheprovider tests/packs/rendering/presenter_crop_capture.py
# Exactly1 test collected in0.30s; not executed.
python3 "$W/check.py" "$N" --check tests/packs/rendering/presenter_crop_geometry.mjs
python3 "$W/check.py" "$N" --check tests/packs/rendering/presenter_crop_entry.mjs
python3 "$W/check.py" "$N" --check tests/packs/rendering/presenter_crop_capture.mjs
python3 "$W/check.py" "$N" --check tests/packs/rendering/presenter_scene_capability.mjs
python3 "$W/check.py" bash -n "$W/READY.sh"
git diff --check
git apply --check --reverse /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-mouth-approved-four-still-product.patch
git apply --check --reverse /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-mouth-approved-four-still-patch
# All syntax/whitespace/reverse-applicability checks exit0.
```

Additional inline Python inspection used ast.parse on the changed Python tests and controller/check.py, asserted exact nine-file/three-product-file scope and base751, verified drawing/core/SSR baseline files unchanged, and removed all three own pytest scratch directories: PASS. `targeted.log` retains the final20PASS output. All CPU checks used the absolute QUIET/REVIEW wrapper; neither marker was present. No tests were skipped, removed, weakened to refuse lost behavior, or marked xfail.

An initial targeted attempt had10PASS/9setupERROR because the new test-only geometry bundle kept a bare Remotion import in a data URL. Fixed the loader to resolve that import from its actual installed host graph. Focused geometry then10PASS/4.29s; final combined20PASS above includes the final loader and all source changes. No product behavior failed in this transient loader issue.

No browser, render, socket, full suite, install, network or test-service request ran. No central grant or RUN_STARTED exists. No git commit/ref mutation or push. Commit message is written; worktree contains only the intended nine files and no build output. No implementation blocker remains in this preparation scope.

Next: manager reviews the selected three-file patch and tests, ports only approved source onto current Agent prerequisites (the review tree itself lacks the presenter source), and separately grants/schedules the ONE central capture. The webpack/browser path and all decoded-pixel assertions remain UNVERIFIED. This limited fixture does not establish all legacy-input equivalence, selected-cut aggregate qualification, current/public11 adoption, owner-film parity or Gate6. No private crop/statistic deletion is authorized by this result; retain them until Agent review and central qualification complete.
