# vw-m3-mouth-series-landing-review

## Decision

**DEFECT — conditional approval of the component-zero helper; public12 fixture lane is not green.**

## Verified

- HEAD `47a3be2a7` changes exactly the four intended test files relative to clean presenter `8a78c25ac`; no production presenter source or package artifact was changed.
- `seriesInspection` uses public `queryDrawFrame` and public `querySceneFrame` only. It selects one exact `am-presenter` clip, requires owner `{kind: effect, id: am-presenter, packId: astrid_motion}`, checks the exact track and compiled `clipIndex`, and makes one component capability read from the same prepared scene. The generated-host fixture separately verifies the discovered owner is the actual `pack:astrid_motion` source rooted in this checkout, so no production authority is fabricated.
- The candidate has no private clock inverse, unbounded search, copied timing/geometry math, or negative-bounds acceptance. Positive delayed input (`at: 5`, `from: 17`, `to: 18`, `speed: 2`) resolves component zero at frame 150; clipped negative start refuses. Missing/duplicate IDs, foreign owner, stale params, empty scene, and mosaic-unknown diagnostics refuse rather than supplying a guessed ROI. The helper is explicitly test-only.
- Public10: presenter/series integration lane **9 passed**; crop-equivalence lane **9 passed**.
- Public12: crop-equivalence lane **9 passed**; retained original-PNG proposal lane **15 passed**. The retained strict `>2%` controls, original PNG bytes, and selected-cut result were unchanged on both public10 and public12.
- Syntax, Ruff targeted checks, `git diff --check`, and clean worktree checks passed. No browser, live socket, full suite, install, or capture was run; the existing static SSR-markup test was run and is the one public12 failure above.

## Defect and exact fix owner

With the accepted immutable public12 artifact and pinned Node v20.19.4, the current four-file suite is **8 passed, 1 failed**:

`tests/packs/rendering/test_presenter_scene_capability.py::test_presenter_existing_registered_ssr_markup`

`tests/packs/rendering/presenter_scene_capability.mjs:49` uses package `DEFAULT_THEME`, while the unchanged snapshot at `test_presenter_scene_capability.py:100-103` is the historical public10 SSR fixture. Public12 intentionally changes that package default theme. The new artifact override at `test_presenter_scene_capability.py:23-28` therefore exposes a public12 lane that cannot pass its retained snapshot; do not rewrite the snapshot or weaken its control.

**Owner:** Viewing manager / current-port test-fixture owner (`presenter_scene_capability.mjs`). Pin the historical explicit theme for the retained SSR fixture while asserting public12’s changed default separately, or scope the public12 override away from this snapshot lane. Keep the public10 default path and all original-PNG controls strict.

**Next caller:** the selected-cut aggregate caller may proceed only after this public12 fixture defect is repaired and rerun. Production activation still belongs to the Agent/source owner and requires the Runtime-backed exact source closure plus cut/track/occurrence identity; this test helper does not provide that authority.

## Exact evidence commands

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules ASTRID_COMPOSITION_TEST_ARTIFACT=$PWD/remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz /home/user/work/venv-agent/bin/python -m pytest -q -m integration -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_presenter_scene_capability.py tests/packs/rendering/test_presenter_series_inspection.py
# 9 passed in 9.52s

... same command with ASTRID_COMPOSITION_TEST_ARTIFACT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.12.tgz
# 8 passed, 1 failed in 9.10s (retained SSR snapshot; all other presenter/series tests passed)

... crop-equivalence command with each artifact
# 9 passed on public10; 9 passed on public12

sed ROOT override of handoff-vw-m3-mouth-series-current-port-check.py 10 and 12
# retained original-PNG proposal: 15 passed on public10; 15 passed on public12

/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check presenter_crop_geometry.mjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check presenter_series_inspection.mjs
/home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE ...
git diff --check 8a78c25ac..HEAD
# all passed; worktree clean
```
