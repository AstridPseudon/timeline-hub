# D09a selected-cut public-query qualification

The central service command is registered once as
`agent integration-viewing-mouth-selected-cut-public-query` in
`orch/tests/suites.conf`:

```sh
env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  ASTRID_NODE_EXECUTABLE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node \
  ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
  ASTRID_COMPOSITION_TEST_ARTIFACT=/home/user/work/wt/vw-m3-mouth-public-query-real-lane/remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  -m integration --tb=short \
  tests/packs/rendering/test_presenter_selected_cut_aggregate.py::test_actual_selected_cut_aggregate
```

Central result: `vw-m3-mouth-public-query-real-lane-integration-viewing-mouth-selected-cut-public-query-1020151841-32447`, **1 passed in 3.67s**, zero skips/deselections.

Local checks:

```sh
/tmp/.../workers/vw-m3-current-root-cap-three-stills-prep/node --check \
  tests/packs/rendering/presenter_selected_cut_query.mjs
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q \
  -o addopts= -p no:cacheprovider \
  tests/packs/rendering/test_timeline_visualize_motion_views.py::test_mouth_state_matches_presenter_core_cycle \
  tests/packs/rendering/test_presenter_selected_cut_aggregate.py::test_cut_selection_does_not_invent_a_reference
```

Local result: AST parse and Node syntax checks passed; pure targeted lane **3 passed**.
No full, browser, renderer, network, install, or local-server suite was run.
