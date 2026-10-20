# handoff: presenter owner rejection preserve state

Base: `ee71010a0947edcbbacbf8178e5fee11ab6bab3d`.

Implemented one bounded candidate for the owner rejection:

- Added a normalized `mouthStateRect()` seam for public scene diagnostics. Defaults, partial anchors, clamped/fractional anchors, and raw-invalid anchors retain the existing KNOWN state derived from `mouthAnchor()`.
- Kept `mouthInspectionRect()` as the legacy compatibility seam. Missing/malformed raw mouth parameters remain absent there; partial `{x,y}` retains legacy width 16 (the separately proven 697-pixel ROI).
- Direct tests now assert the public explicit/default ROI (799 pixels at 640x360), partial legacy 697 versus normalized public 799, raw-invalid normalized public state, and unchanged erase/crop statistics. No production component, threshold, crop consumer, or geometry/statistics implementation was changed.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" ASTRID_NODE_EXECUTABLE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_presenter_scene_capability.py tests/packs/rendering/test_presenter_crop_equivalence.py --basetemp=/tmp/vw-m3-presenter-owner-reject-focused3` — **17 passed**.
- Same pinned-runtime command for `tests/packs/astrid_motion/test_astrid_motion_pack.py tests/packs/rendering/test_remotion_element_generation.py tests/packs/rendering/test_timeline_visualize_motion_views.py` — **38 passed, 2 skipped** (existing esbuild-dependent skips).
- `/opt/node22/bin/node --check tests/packs/rendering/presenter_scene_capability.mjs` and `presenter_crop_geometry.mjs` — **passed**.
- Ruff focused check — **passed**.
- `git diff --check` — **passed**.
- `python scripts/artifact_manifest.py --check` — **exit 1** because the base already has stale presenter entries and this task forbids pin/manifest changes; normal owner artifact refresh remains required after admission.
- No full suite, browser/replay, live socket, physical capture, install, network, or normal consumer activation was run.

The central generic targeted request was not qualification evidence: it exited 5 after deselecting all 17 integration tests because that suite did not supply the pinned integration environment. The direct pinned-runtime run above is the qualifying targeted result.

## Scope

Changed only the permitted presenter `motion.ts`/`scene.ts` files and direct presenter test helpers/tests. `component.tsx` was unchanged. No blocker remains for this candidate; owner artifact regeneration and the normal coordinated admission remain next.

