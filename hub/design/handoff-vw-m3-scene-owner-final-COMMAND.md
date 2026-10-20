# Scene-only owner handoff commands

All paths below are the recorded evidence commands. They are not a request to
rerun the central lanes.

## Local executor qualification

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
/home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider \
tests/packs/rendering/test_scene_only_executor.py
# 10 passed in 0.52s
```

The neighboring rendering/public-dispatch command was:

```sh
PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q \
tests/packs/rendering/test_scene_only_executor.py \
tests/packs/rendering/test_timeline_filmstrip_execution.py \
tests/packs/rendering/test_timeline_visualize_public_view_dispatch.py
# 43 passed, 1 warning in 12.09s
```

Static checks were:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
/home/user/work/venv-agent/bin/python -B -m ruff check --no-cache --isolated \
tests/packs/rendering/test_scene_only_executor.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
/home/user/work/venv-agent/bin/python -B -m compileall -q \
astrid/packs/rendering/actions/timeline_visualize/filmstrip_execution.py \
astrid/core/timeline/scene_answers.py
git diff --check
# all passed
```

## Actual artifact contract

```sh
ASTRID_NODE_EXECUTABLE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node \
ASTRID_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
--basetemp=/tmp/vw-m3-scene-artifact-packet-test.dFBFLc \
tests/packs/rendering/test_scene_artifact_contract.py -k scene_only_bundle
# 1 passed in 7.68s
```

This is UNIT-REAL-NODE with the existing admission fixture and read-only peer
graph. Verify the peer graph before use:

```sh
realpath /home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules
# must not be /home/user/work/app/node_modules
```

## Central admission-double lanes

The two central requests both used the existing wrapper command:

```sh
/home/user/work/venv-agent/bin/python -B scripts/run_scene_only_central.py
```

The D1-ready lane selected exactly these two test functions:

```text
tests/packs/rendering/test_scene_answers.py::test_prepared_host_query_replaces_named_occluder_semantic_presence_positive
tests/packs/rendering/test_scene_answers.py::test_prepared_host_query_refuses_missing_or_stale_source_pair_and_cleans
```

The second function is parametrized for missing and stale source pairs, so the
lane is 3 cases: **3 passed in 13.03s**. The final venv lane selected the same
two functions inside the full bounded wrapper and reported **18 passed in
76.77s**. Both are admission doubles with a private copied 21,495-entry graph,
snapshot-local import origins, pinned Node `v20.19.4`, Runtime source
`2c4ac180`, and public12's 77-file artifact. Neither is live Runtime,
ordinary SDK, browser, or owner-film evidence.

## Patch and packet checks

```sh
wc -c design/handoff-vw-m3-scene-owner-final-executor-and-artifact-contract.patch
find design/handoff-vw-m3-scene-owner-final-examples -type f | wc -l
find design/handoff-vw-m3-scene-owner-final-examples -type f -printf '%s\n' \
  | awk '{total += $1} END {print total + 0}'
# 39,847 bytes; 17 files; 26,205 bytes
```
