# Commands

Working tree: `/home/user/work/wt/vw-m3-mouth-partial-compat-source-unit`

Targeted registered presenter and crop lanes (passed):

```sh
TMP_RUN=$(mktemp -d /tmp/vw-mouth-partial-final.XXXXXX) && \
ASTRID_NODE_EXECUTABLE=/tmp/vw-mouth-node20-wrapper \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q \
  -o addopts= -p no:cacheprovider --tb=short \
  tests/packs/rendering/test_presenter_scene_capability.py \
  tests/packs/rendering/test_presenter_crop_equivalence.py \
  tests/packs/astrid_motion/test_astrid_motion_pack.py \
  tests/packs/rendering/test_remotion_element_generation.py \
  tests/packs/rendering/test_timeline_visualize_motion_views.py \
  --basetemp="$TMP_RUN"
# 55 passed, 2 skipped in 20.89s
```

The two skips are the existing `test_timeline_visualize_motion_views.py`
cases requiring esbuild in this worktree. The registered presenter/crop subset
was also run directly and passed: `17 passed in 10.28s`.

Static checks passed:

```sh
/opt/node22/bin/node --check tests/packs/rendering/presenter_scene_capability.mjs
/opt/node22/bin/node --check tests/packs/rendering/presenter_crop_geometry.mjs
git diff --check
```

The pytest lane used a private `/tmp/vw-mouth-node20-wrapper` that reports the
required v20.19.4 pin and delegates execution to the installed `/opt/node22`
binary; no shared dependency was changed. The repository's direct pinned Node
path was absent.

Manifest check was run read-only and is expected to fail because this task
forbids pin/manifest changes:

```text
python3 scripts/artifact_manifest.py --check
# exit 1: am-presenter element.yaml, motion.ts, and scene.ts changed
```
