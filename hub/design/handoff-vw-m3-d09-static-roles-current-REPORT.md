# vw-m3-d09-static-roles-current-owner-port

## Result

Ported the bounded D09 static-role donor onto current Agent owner `5c5173dcb`.
Restored `astrid/core/timeline/scene_roles.py` exactly from source
`4a4725e7e` (blob SHA `40f21f323d881b86c3c42f14c7475819d5534aac`) and migrated
only the requested `scene_answers`, SDK `check`, and SDK `reflow` imports/call
site. Current `onscreen.py` wrappers, patch points, and tests remain untouched.

## Changed paths

- `astrid/core/timeline/scene_roles.py` — restored source helper.
- `astrid/core/timeline/scene_answers.py` — role/coverage import.
- `astrid/sdk/timeline/check.py` — cached coverage import/call and docstring.
- `astrid/sdk/timeline/reflow.py` — doomed-cut role import/call.

No geometry, timing, crop, renderer, DTO, store, resolver, or save behavior was
changed. `scene_roles.py` matches `4a4725e7e:astrid/core/timeline/scene_roles.py`
byte-for-byte. `onscreen.py` has no diff.

## Verification

- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= tests/core/timeline/test_onscreen.py tests/core/timeline/test_onscreen_more.py tests/sdk/test_intent_app_astrid.py tests/sdk/test_timeline_reflow_golden.py tests/packs/rendering/test_labels_overlay.py tests/packs/rendering/test_timeline_visualize_labels.py tests/sdk/test_scene_save_core.py`
  — **67 passed in 1.95s**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -c '...'`
  — static `scene_roles.role_of` smoke checks passed.
- `git diff --check` — passed.
- Source blob and `onscreen.py` authority guards — passed.

The 67-test lane includes the save-without-renderer/no-Node guards in
`tests/sdk/test_scene_save_core.py`; no exact Node 20 lane was needed because
this change is pure metadata/import plumbing and does not add a rendering or
save dependency. No full, browser, live-socket, managed-proof, install, or
shared-dependency mutation was run.

## Decision / limits

The current owner had deleted `scene_roles.py`, so this was not a NOOP. The
settled proposal and source authority were followed exactly. The harness must
commit the four product paths; no commit, merge, rebase, checkout, or push was
performed by this worker.
