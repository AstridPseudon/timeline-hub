# vw-m3-d09-role-metadata-duplicate-cut

## Result

Removed the genuinely duplicate static-role/coverage metadata loader and role
classifier bodies from `astrid/core/timeline/onscreen.py`. The existing helper
`astrid.core.timeline.scene_roles` is now the only implementation. The old
`onscreen` names remain available as aliases, including `_coverage_of`,
`_has_value`, `element_coverage`, and `role_of`.

The legacy `_PACKS_ROOT`, `_COVERAGE_CACHE`, `_COVERAGE_COMPAT` patchpoints and
their `_LEGACY_*` sentinels remain intact. `scene_roles.element_coverage` keeps
its existing interception of monkeypatched `onscreen` values, so old tests and
callers retain the same root/cache/compatibility behavior. No `_cached_coverage`
or cache-clear API exists in this source tree and no such behavior was removed.

## Source delta

- One product file changed: `astrid/core/timeline/onscreen.py`.
- 16 lines added, 74 lines deleted (`git diff --numstat HEAD`).
- Deleted only the duplicate metadata parser/cache/classification bodies and
  their now-unused imports.
- `scene_roles.py` was not changed; its hash remains
  `40f21f323d881b86c3c42f14c7475819d5534aac`, matching donor blob
  `40f21f32`.
- Geometry, visibility, mouth, crop, timing, pixel, `_timing_evaluators`,
  sourceauthority, SDK, package, pin, and public API code were not touched.

## Verification

Exact inherited static/SDK/labels/save-no-node control:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/core/timeline/test_scene_roles.py tests/core/timeline/test_onscreen.py tests/core/timeline/test_onscreen_more.py tests/sdk/test_intent_app_astrid.py tests/sdk/test_timeline_reflow_golden.py tests/packs/rendering/test_labels_overlay.py tests/packs/rendering/test_timeline_visualize_labels.py tests/sdk/test_scene_save_core.py
69 passed in 2.20s
```

`git diff --check` passed. No full, browser, live-socket, physical, install,
push, or shared-dependency operation was run.

## Handoff

`PATCH`, `FILELIST`, and `COMMAND` are flat in this worker directory. The
patch is the Git-generated diff from base `48feba659` and contains only the
one allowed product path. No blocker encountered.
