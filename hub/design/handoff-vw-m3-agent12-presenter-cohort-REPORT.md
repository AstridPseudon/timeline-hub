# Agent12 presenter cohort

Completed in `/home/user/work/wt/vw-m3-agent12-presenter-cohort`, HEAD/base
`f29a9475ee1cb5c13bc1371eee8ff36030dede3e`. No checkout, commit, merge,
installation, shared dependency mutation, browser, socket, full suite, or
central test request was used.

## Change and apply-order decision

Ported only the exact approved `ef6eec5572c5c0def7ca8a22c14caa12f24f0b82`
→ `8a78c25ac331ff769291c0207119b3f4ee49b822` presenter delta (10 paths),
then the tests-only combined mouth12 patch. Regenerated `artifacts.json`
mechanically on the final base. All five approved product files are byte-for-byte
identical to clean8a78, including the exact three YAML comment lines.
No ancestry merge was performed.

The combined patch's `test_composition_package.py` delta is already identically
present in f29: reverse-apply check of that file passes. Excluded only this
redundant file when applying the combined patch; retained the complete f29 test
file, including every readiness negative. No absent presenter test was treated
as intentionally retired. The remaining combined patch reverse-checks cleanly.
The complete final patch, including every new file and PNG, reverse-checks
cleanly on the actual worktree.

Final scope: 22 paths (5 modified existing paths, 17 additions). Every one of
2,898 existing base files outside that allowlist was checked byte-for-byte
against `git archive f29a9475ee1`. Root/Remotion package and lock files, runtime
readiness, artifacts, Runtime/client/provider/core/custody/compiler bytes remain
base-exact. Only the presenter and its pack declaration are product changes.

## Actual own-worktree commands and results

All commands below ran from the assigned worktree. Presenter tests used its
own checked-in 0.0.12 artifact by default; `ASTRID_COMPOSITION_TEST_ARTIFACT`
was absent. Existing readonly dependencies were used without installation.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
tests/packs/rendering/test_presenter_scene_capability.py \
tests/packs/rendering/test_presenter_crop_equivalence.py \
tests/packs/rendering/test_presenter_series_inspection.py \
tests/packs/rendering/test_presenter_selected_cut_aggregate.py
# 33 passed in 11.77s; exit 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
-m 'not integration' tests/packs/rendering/test_composition_package.py
# 5 passed, 1 deselected in 0.24s; exit 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
tests/test_artifact_manifest.py \
tests/packs/astrid_motion/test_astrid_motion_pack.py \
tests/packs/rendering/test_remotion_element_generation.py \
tests/packs/rendering/test_timeline_visualize_motion_views.py
# 48 passed in 16.37s (8 manifest + 40 neighbors); exit 0

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py
# wrote artifacts.json: 162 artifacts,
# sha256:9c6bc05bef1d7a2c4d76ad3dc62e18437e12e9f9df2947798fdd941e1e715a68
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
# artifacts.json is current; exit 0

/home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE \
tests/packs/rendering/test_presenter_scene_capability.py \
tests/packs/rendering/test_presenter_crop_equivalence.py \
tests/packs/rendering/test_presenter_series_inspection.py \
tests/packs/rendering/test_presenter_selected_cut_aggregate.py \
tests/packs/rendering/test_composition_package.py
# All checks passed!; exit 0

/tmp/vw-m3-agent-gate-node20.19.4/bin/node --version
# v20.19.4
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check tests/packs/rendering/presenter_scene_capability.mjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check tests/packs/rendering/presenter_crop_geometry.mjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check tests/packs/rendering/presenter_series_inspection.mjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check tests/packs/rendering/presenter_selected_cut_query.mjs
# all exit 0

git diff --check
# exit 0
```

The 33 tests include actual strict/noEmit TypeScript checking against the
extracted public12 declarations, registered source/owner dispatch, normalized
KNOWN and mosaic/outer UNKNOWN assertions, component-zero series query,
selected-cut adjacency/order/duplicate/missing-file/half-open controls,
original retained PNG analysis, and strict 15/799 versus 16/799 controls.
All 286 historical SSR hashes (22 cases × 13 entries) are unchanged and pass
with the explicit historical black/Georgia theme; the actual public12 navy
DEFAULT_THEME assertion also passes. Original PNG and inspection hashes match.
No new skip/xfail or marker beyond the exact approved test delta was introduced.
The one deselected test is the existing package integration case, as requested
by the five-test package lane; it was not rewritten or disabled.

Composition artifact remains 58,444 bytes / 77 files, SHA256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.

## Current full source census

This is a filesystem/source census, not a full-suite result. Counted tracked
paths plus the 17 new files destined for the harness commit, excluding ignored
output: 2,903 existing tracked paths → 2,920 current files. Complete top-level
counts and changed-file list are in the adjacent census JSON.

- Python/JS/MJS/TS/TSX across the full tree, including tests/scripts: 1,956 files,
  587,043 physical lines.
- Prior report's authored-product convention (Python under `astrid`, non-test/
  non-script JS/MJS/TS/TSX under `remotion`): 898 files / 290,012 lines:
  `astrid` 287,276; `remotion` 2,736. This convention does not count pack TSX
  as product Python; the full-source count above includes it.
- 162 current manifest artifact entries; exact path allowlist and original
  base bytes outside it verified.

## Limits and next step

No blocker for this bounded source cohort. Remote owner review remains next;
the final current Runtime/client tuple is still held. No normal caller
activation, production source/custody qualification, private crop/statistics
retirement, new physical render capture, or parity/Gate 6 claim. Original PNGs
remain explicitly retained public10 evidence, not a current Runtime receipt.
No full suite or make check was run under this no-full/no-browser/no-socket
brief. Do not infer broader qualification from these targeted passes.

Handoffs (all flat absolute paths):
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-agent12-presenter-cohort-REPORT.md`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-agent12-presenter-cohort-complete.patch`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-agent12-presenter-cohort-approved-presenter.patch`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-agent12-presenter-cohort-census.json`
