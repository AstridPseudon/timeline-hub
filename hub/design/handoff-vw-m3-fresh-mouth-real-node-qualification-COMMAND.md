# Exact qualification commands

## Local final aggregate

```sh
NODE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node
ARTIFACT="$PWD/remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz"
PEERS=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" env -u NODE_OPTIONS -u NODE_PATH \
  ASTRID_NODE_EXECUTABLE="$NODE" \
  ASTRID_COMPOSITION_TEST_NODE_MODULES="$PEERS" \
  ASTRID_COMPOSITION_TEST_ARTIFACT="$ARTIFACT" \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  -m integration --tb=short tests/packs/rendering/test_presenter_selected_cut_aggregate.py
```

Result: **21 passed in 4.34s**.

## Local neighbor

Same environment, with
`tests/packs/rendering/test_presenter_crop_equivalence.py`.

Result: **9 passed in 3.71s**.

## Central service lane

Registered once as `agent integration-viewing-mouth-fresh-context-carry` in
`orch/tests/suites.conf`. It runs only:

```text
tests/packs/rendering/test_presenter_selected_cut_aggregate.py::test_fresh_public_mouth_facts_drive_existing_consumer
tests/packs/rendering/test_presenter_selected_cut_aggregate.py::test_planted_public_fact_failures_keep_private_fallback
```

The command includes `-o addopts= -m integration`, unsets Node injection
variables, and points at the exact retained Node, current snapshot artifact,
and read-only peer root. Central result:

`vw-m3-fresh-mouth-real-node-qualification-integration-viewing-mouth-fresh-context-carry-1020153431-24440`
— **4 passed in 3.57s**, zero skips/deselections.
