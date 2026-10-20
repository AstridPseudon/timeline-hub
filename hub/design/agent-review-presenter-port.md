# Agent review: Viewing `tl/vw-m3-presenter-current-port` (802669926) into `tl/integration`

Reviewer: Agent worktree `agt-review-presenter-port` (read-only; no repo changes, no commit-msg).
Base: `tl/integration` merge-base `ef6eec5572c5c0def7ca8a22c14caa12f24f0b82`. Branch is one commit `80266992` ("feat(astrid-motion): expose current presenter scene capability"), 10 files, +1068/-28.
Checked against: my conditions in `design/agent-review-viewing-20261020b.md` section 2, and the approved 3-file patch `design/handoff-vw-m3-mouth-approved-four-still-product.patch` plus `design/handoff-vw-m3-mouth-capture-retention-fix-MANAGER-PASS.md`.

## Verdict: REJECT as submitted

The substance is approvable. Three things block it:

1. **Stale `artifacts.json` (blocking, gate-failing).** The branch changes three files that the manifest pins and adds a fourth that it matches, but does not regenerate `artifacts.json`. `artifacts.json` is not in the branch diff. `pattern astrid/packs/astrid_motion/rendering/elements/**/*.{ts,tsx,yaml}` covers all four. Hash comparison (`git show <branch>:<path> | sha256sum`):

   | Path | Manifest (= base, verified) | Branch file | Result |
   |---|---|---|---|
   | `am-presenter/component.tsx` | `3943547…386168` | `b1dea928…4cc` | stale |
   | `am-presenter/element.yaml` | `73e0055a…7302` | `bb6f21ef…270f` | stale |
   | `am-presenter/motion.ts` | `3b9af4f7…925668e` | `d2145b11…2c3` | stale |
   | `am-presenter/scene.ts` | (absent) | `bb1374c5…1c7a` | missing |

   `tests/test_artifact_manifest.py::test_committed_artifact_manifest_is_current` asserts `artifact_manifest.check() == []`, so it fails on this branch. The manifest also feeds the astrid-app vendor set and the tool catalog. Fix: regenerate with `python scripts/artifact_manifest.py` in the same change. That is a mechanical digest update for files this change must alter, not a pin-policy change. The brief says "no pin changes", so the orchestrator should confirm that reading.

2. **`element.yaml` comment is longer than approved (required trim).** Condition 2 said to trim the comment. The approved patch net-adds about 3 lines. This branch adds 8 lines, including new claims ("Scene diagnostics use the supplied speed-remapped component frame and motionAt", "Source-qualified MOUTH_LEVEL…"). Trim it to the approved wording: the padding (1 px horizontal, 2 px vertical), known default/partial/raw-invalid anchors, mosaic/unsupported unknown, no occupancy claim, legacy equivalence separately qualified.

3. **Tests not run by me (required evidence).** See section 3.

## 1. Checked against the approval

| Condition | Result |
|---|---|
| Actual erase rect padded 1 px horizontal / 2 px vertical = legacy `mouth_box` | Met. `mouthInspectionRect` = `{x: r.x-1, y: r.y-2, w: r.w+2, h: r.h+4}` over `mouthEraseRect`, giving logical `x-2..x+w+2, y-3..y+5`. For 151/104/19 that is `(149,101)-(172,109)`, i.e. `(894,606,1032,654)` at 6x. The test expectations match. |
| Default / partial / raw-invalid stay KNOWN; mosaic unknown | Met. `mouthAnchor` → `anchorOr` (copied verbatim from the old component), so normalized anchors are known. Mosaic branch unchanged. |
| Partial anchors stay unqualified | Met. `legacy_qualified` in `test_presenter_crop_equivalence.py` excludes default, partial, clamps, rawInvalid and fractional. |
| No new public type | Acceptable. `PixelRect` is exported from the element's own `motion.ts`; the approved post-image exports it too. The scene return shape is unchanged. |
| No threshold widening; pixel verification and private crop/statistics kept | Met. Nothing outside `astrid/packs/astrid_motion/` and `tests/packs/rendering/` changes. `timeline_visualize`, the 2% comparator and the capture callers are untouched. |
| Long comment trimmed | **Not met** (item 2 above). |
| Existing SSR/scene geometry expectations updated in the same change | Satisfied trivially. The base has no mouth-rect or erase-rect expectations (grep of `tests/`, `remotion/tests`, `remotion/src`, `astrid/packs`). The branch adds new tests and keeps the 286-hash historic SSR fixture unchanged. |

Byte-level identity with the approved work:
- `motion.ts` post-image blob `dfe1e25b…` equals the approved patch's post-image.
- `scene.ts` blob `74512683…` equals the approved patch's post-image.
- `element.yaml` differs from the approved text (item 2).

Beyond the approved patch, and accepted:
- `component.tsx` now imports the shared helpers (`mouthAnchor`, `mouthEraseRect`, `pixelGeometry`, `presenterMosaicAt`), renames `AmPresenter` and default-exports `Object.assign(AmPresenter, {prepareSceneCapability})`. This is needed to avoid a second erase formula and to expose the capability. I checked the formulas by reading: `mouthEraseRect`, `pixelGeometry`, `presenterMosaicAt` and the `DEFAULT_MOUTH` literal all match the old inline values. The 286 SSR hashes cover the drawing.
- `motion.ts` newly exports `anchorOr`, `mouthAnchor`, `PixelRect`, `pixelGeometry` and `MOUTH_LEVEL`. These are pack-internal.
- `pack.yaml` adds `scene.ts` to the presenter's implementation resources. This is a manifest content change, not a schema, provider, pin or compiler change. `test_presenter_pack_declares_source_closure` asserts it, and `test_astrid_motion_pack.py` checks the file exists.

Not in the diff: no schema, provider, compiler or `schemas/` file. `artifacts.json` is the only pin file affected (item 1).

No "deletion-only" claim is made in Viewing's report. The product files are +93/-28 and the report says so, which I accept as stated.

## 2. Tests named by the branch are real

Read from the branch (not executed):
- `tests/packs/rendering/test_presenter_scene_capability.py`: `test_presenter_existing_registered_ssr_markup`, `test_presenter_public_scene_contract` (5 parametrized), `test_presenter_public10_declarations`, `test_presenter_pack_declares_source_closure`. Total 8.
- `tests/packs/rendering/test_presenter_crop_equivalence.py`: `test_registered_default_and_clamped_anchors_are_not_legacy_defaults`, `test_same_frame_compatibility_and_separate_erase_denominators` (4 parametrized), `test_minimal_two_percent_counterexample_without_invented_pixels`, `test_frame_zero_series_crop_cannot_follow_a_moving_region`, `test_source_bound_unknown_is_not_a_replacement_crop`, `test_public_known_normalization_is_not_legacy_qualification`. Total 9.
- Together these are 17, matching Viewing's "17 passed".
- The companion `.mjs` helpers exist and are consistent with the Python. The node-side asserts check the same numbers (`894,606,1032,654`; `799/387`).

Not checked: the six neighbour tests Viewing lists (`test_remotion_element_generation.py` and three `test_timeline_visualize_motion_views.py` functions).

## 3. Tests: not run

- `bin/request-test agt-review-presenter-port targeted --files "..."` snapshots my worktree, which is on `tl/agt-review-presenter-port` at base. The branch is not checked out here, and I must not change my worktree, so request-test cannot run the branch's tests as things stand.
- Running them from a `git archive` snapshot in scratchpad needs an extract step. That step was blocked by the permission gate, so I stopped and did not work around it.
- Viewing's logged results are therefore unverified by me: `17 passed` (direct), `6 passed` (neighbours), `ruff` clean, `node --check` exit 0, `git diff --check` exit 0. Their env used `/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules` (absent here) and `/tmp/vw-m3-agent-gate-node20.19.4/bin/node`. Candidate peers: `/home/user/work/runtimes/agent-remotion-0010/node_modules` has remotion 4.0.509. React 18.3.1 there is unverified. Node 20.19.4 is at `/home/user/work/node-v20.19.4-linux-x64/bin/node`.

Commands the owner should run on the fixed branch (in a worktree where it is checked out):
```
python scripts/artifact_manifest.py --check
pytest -q -o addopts= tests/test_artifact_manifest.py
pytest -q -o addopts= tests/packs/rendering/test_presenter_scene_capability.py tests/packs/rendering/test_presenter_crop_equivalence.py
pytest -q -o addopts= tests/packs/astrid_motion/test_astrid_motion_pack.py tests/packs/rendering/test_timeline_visualize_motion_views.py
```
The presenter pytest files need `ASTRID_NODE_EXECUTABLE` (Node 20.19.4) and `ASTRID_COMPOSITION_TEST_NODE_MODULES` (a remotion 4.0.509 node_modules). Also run `make check` or the relevant lanes if the orchestrator wants the full gate.

## 4. Decision for the orchestrator

Reject as submitted. Re-review is needed after:
1. `artifacts.json` regenerated (digest-only; confirm this is allowed under "no pin changes").
2. `element.yaml` comment trimmed to the approved wording.
3. Targeted tests above green on the branch, with exact commands and results.

Once those are in, I expect APPROVE. The rest of the diff matches the approval.
