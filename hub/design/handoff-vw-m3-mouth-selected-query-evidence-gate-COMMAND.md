# D09a selected-query evidence-gate commands

Review-only commands used:

```sh
git show d051bee072cef25e706b060e3318a80aa104f29c:tests/packs/rendering/test_presenter_selected_cut_aggregate.py
git show d051bee072cef25e706b060e3318a80aa104f29c:tests/packs/rendering/presenter_selected_cut_query.mjs
git show d051bee072cef25e706b060e3318a80aa104f29c:tests/packs/rendering/test_presenter_scene_capability.py
git diff-tree --no-commit-id --name-status -r d051bee072cef25e706b060e3318a80aa104f29c
sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node
```

Recorded central command/result (not repeated):

```text
env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
ASTRID_NODE_EXECUTABLE=/tmp/.../vw-m3-current-root-cap-three-stills-prep/node \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
ASTRID_COMPOSITION_TEST_ARTIFACT=/home/user/work/wt/vw-m3-mouth-public-query-real-lane/remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
-m integration --tb=short \
tests/packs/rendering/test_presenter_selected_cut_aggregate.py::test_actual_selected_cut_aggregate

1 passed in 3.67s; 0 skipped; 0 deselected
```

Recorded local exact command/result (not repeated):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
ASTRID_NODE_EXECUTABLE=/tmp/.../vw-m3-current-root-cap-three-stills-prep/node \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
ASTRID_COMPOSITION_TEST_ARTIFACT=$PWD/remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
-m integration --tb=short \
tests/packs/rendering/test_presenter_selected_cut_aggregate.py::test_actual_selected_cut_aggregate

1 passed in 3.70s
```

No new test run was needed: the source and immutable central result were
available and internally consistent. No full, browser, renderer, socket,
network, install, or git-mutation command was run.
