# Agent review: two Viewing merge requests into `tl/integration`

Reviewer: worker `agt-review-viewing-landings` (read-only; no repo changes, no commit-msg).
Checked by reading the branch diffs (`git diff`, `git show`), not by running the suites.
Test results below are Viewing's, cited from their reports; I did not run them.

---

## 1. `tl/vw-m3-presenter-clean-land` at `8a78c25ac`: APPROVE

Base: merge-base with `tl/integration` is `ef6eec5572c5c0def7ca8a22c14caa12f24f0b82`. Eleven paths, +1068/-32. Reviewed against my earlier owner review `design/agent-review-presenter-port.md`, which required:
artifacts.json regenerated, the element.yaml comment trimmed, no review/report files in the repo, and tests actually run.

| Requirement | Result | Evidence |
|---|---|---|
| Scope limited to `astrid/packs/astrid_motion`, `tests/packs/rendering`, and `artifacts.json` | Met | `git diff --stat` lists `artifacts.json`, `astrid/packs/astrid_motion/pack.yaml`, four `am-presenter` files, and six files under `tests/packs/rendering/`. Nothing else. |
| No repo report, proposal, or receipt files | Met | None of the 11 paths is a report or receipt. |
| `artifacts.json` current | Met for the five presenter entries | I hashed each branch blob with `git show <branch>:<path> \| sha256sum` and compared it with the manifest. All five match: `component.tsx` `b1dea928…`, `element.yaml` `e7cc7df9…`, `motion.ts` `d2145b11…`, `presenter-core.ts` `6f3bc8fb…` (unchanged), `scene.ts` `bb1374c5…`. The manifest `version` digest was not recomputed by me. Viewing reports `artifact_manifest.check() == []`. |
| `element.yaml` comment trimmed to 3 lines | Met on count | Exactly 3 added comment lines, and the diff touches nothing else in that file. The wording is not byte-identical to any approved hunk I found in `design/`. It states the required content: 1 px horizontal and 2 px vertical padding, default/partial/raw-invalid known, mosaic unknown, no occupancy claim, and legacy equivalence separately qualified. I accept it. The orchestrator should confirm the wording. |
| Inspection rect = erase rect padded 1 px horizontal, 2 px vertical | Met | `mouthEraseRect` is `{x-1, y-1, w+2, h:4}`. `mouthInspectionRect` is `{x: r.x-1, y: r.y-2, w: r.w+2, h: r.h+4}`, i.e. `x-2..x+w+2`, `y-3..y+5`. That matches legacy `mouth_box`. |
| Default, partial, raw-invalid anchors known; mosaic unknown | Met | `mouthAnchor` → `anchorOr` (moved verbatim from the component) normalizes the anchor, and `scene.ts` returns `known` unless `presenterMosaicAt` is true, in which case it returns `unknown`. |
| Component drawing unchanged | Met | `presenterAt(props.params, frame, fps)` in the component and `presenterAt(clip.params, frame, fps)` in the scene use the same frame. `mouthEraseRect` and `pixelGeometry` replace the inline formulas with the same values. `DEFAULT_MOUTH` moved into `mouthAnchor`. `presenter-core.ts` is untouched. |
| No new public type | Acceptable | `PixelRect` and the helpers are exported from the element's own `motion.ts` and are pack-internal. The scene return shape is unchanged. |
| No threshold widening; private crop and statistics kept | Met | Nothing outside the presenter element and its tests changes. `timeline_visualize`, the 2% comparator, and the capture callers are untouched. |
| Tests are real | Met on reading | The new Python tests use `subprocess` to run Node, and contain no `skip` or `xfail` markers. The 286-hash fixture is a data file. |

Notes that are not blockers:
- `scene.ts` imports types from `@banodoco/timeline-composition/evaluation`. The import is type-only, so it is erased at runtime. The package version it needs is the one Viewing qualified (Composition 0.0.10). I did not check that export against the package.
- `pack.yaml` adds `scene.ts` to the presenter's implementation closure. That is a manifest content change, not a pin or schema change.

**Tests (Viewing's results, not run by me):** cited in `design/handoff-vw-m3-presenter-final-review-REPORT.md`, which reviewed `8a78c25ac` and reports APPROVE:
- `pytest -q -o addopts= tests/test_artifact_manifest.py`: 8 passed
- presenter scene capability and crop equivalence: 17 passed
- astrid_motion pack, remotion element generation, and timeline visualize motion views: 40 passed

Environment: Node 20.19.4 and a Remotion 4.0.509 `node_modules` from another worker's worktree (`/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules`). Not reproduced here. Running them myself would need the branch checked out in a worktree. `bin/request-test` snapshots my worktree, which is at `tl/integration`, so I did not request them. **Not run by me.**

---

## 2. `tl/vw-m3-current-capture-scene-hook` at `18ec2b573`: APPROVE, with one check not met as written

Base: `7261b4ad5827466b2e17f1a30bf35d2fd05e0700`, which is already in `tl/integration`. Two files, +380/-1: `astrid/packs/rendering/rendering/renderers/remotion/run.py` and `tests/packs/rendering/test_remotion_capture_scene_props.py`. The hook is not yet in `tl/integration`.

| Check | Result | Evidence |
|---|---|---|
| No scene evaluation in the save path | Met | The only addition in `run.py` is a call to `on_scene_props(merged_props, frame_numbers)`, placed after `props_path.write_text(...)` and before capture. It evaluates nothing. |
| No source authority, provider, or pin change | Met | Only the two files above change. No schema, pin, provider, manifest, or Runtime file is touched. |
| Observer inert unless explicitly installed | Met | The parameter defaults to `None`. `capture_remotion_frames` forwards it only when it is not `None` (`**({...} if on_scene_props is not None else {})`), so the existing call shape is unchanged. The test `test_default_callback_keeps_existing_call_shape` covers omitted and explicit `None`. The test `test_callback_leaves_serialized_node_props_unchanged` shows the Node props are identical with and without an observer. No caller installs it. |
| Failure never changes capture results | **Not met as written** | An observer exception propagates unchanged and aborts capture before submission (`test_callback_and_capture_failures_preserve_cleanup`, `failure="callback"`). `design/viewing.md` documents this as "an observer failure uses the existing cleanup path". So a failing observer does change the capture result. Because nothing installs the observer, nothing changes in production today. |

Other observations:
- The observer receives the live `merged_props` mapping and nothing enforces read-only. The file is already written before the callback runs, so a mutation cannot change what Node receives. The docstring says the observer must not mutate.
- If `frame_numbers` were `None`, an installed observer would be silently skipped. `capture_remotion_frames` always supplies frames, so this is not reachable today.
- The hook is a preparation seam only. The report correctly says it does not certify source, and that a retained observation is not a capture fact if the capture later fails.

**Decision for the orchestrator:** the fail-closed behaviour is a sensible choice for a preparation observer. It is a deliberate deviation from the literal check "failure never changes capture results". Either record fail-closed as the decided semantics, or change the callback to log and continue. I recommend recording fail-closed, since no caller is installed.

**Tests (Viewing's results, not run by me):** `design/handoff-vw-m3-scene-hook-current-review-REPORT.md` cites:
- `pytest -q -p no:cacheprovider -o addopts= tests/packs/rendering/test_remotion_capture_scene_props.py tests/packs/rendering/test_remotion_native_window.py tests/packs/rendering/test_remotion_frame_bench.py tests/packs/rendering/test_remotion_scratch_guards.py`: 41 passed in 3.52s
- `ruff check --isolated --select E4,E7,E9,F,I,BLE` on the new test file: clean
- `git diff --check`: passed

The test file has no `skip` or `xfail` markers. **Not run by me.** The same reason as above: no branch worktree is available to run them against.

---

## Summary

| Branch | Verdict | Blocking? |
|---|---|---|
| `tl/vw-m3-presenter-clean-land` `8a78c25ac` | **APPROVE** | No. Tests cited from Viewing, not run by me. Confirm the element.yaml wording. |
| `tl/vw-m3-current-capture-scene-hook` `18ec2b573` | **APPROVE** | No. Record the fail-closed observer semantics, since the literal check "failure never changes capture results" is not met. Tests cited, not run by me. |
