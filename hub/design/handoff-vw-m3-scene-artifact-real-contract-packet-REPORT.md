# D09 scene artifact contract packet

## Result

Added one rendering-owned contract test:
`tests/packs/rendering/test_scene_artifact_contract.py`.

It uses the existing `prepare_filmstrip` producer and authoring candidate
compiler, the existing verified-source mint/capture helpers, the existing Root
preparation lifetime, and the public Node Scene query. It covers:

- a six-frame saved capture with `snapshot_label.status: committed`;
- a six-frame real candidate with `snapshot_label.status: candidate`;
- stale source and unavailable Node results with `status: unavailable`, label
  `revision unavailable`, empty `answers`, and empty `scene_clips`;
- exact canonical frame IDs, producer map keys, public row layer IDs, source
  labels, and the existing `filmstrip_bundle` ->
  `filmstrip-view/scene-answers.json` entrypoint.

The generated examples are in the sibling flat directory
`handoff-vw-m3-scene-artifact-real-contract-packet-examples/`; total size is
26,205 bytes. They contain only scene answers, managed/nested manifests, and
the four tiny ZIP artifacts. No full snapshot, source binding, credentials, or
PNG was exported.

Evidence is UNIT-REAL-NODE: the pinned Node is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node`
(`v20.19.4`); the test uses the existing fixture admission seam and extracts
the repository's immutable public12 artifact (77 files, SHA-256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`) into its
private host project. This is not live Runtime or ordinary SDK qualification.

## Exact checks

Passed locally with the pinned Node and read-only peer graph:

```text
ASTRID_NODE_EXECUTABLE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node \
ASTRID_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/vw-m3-scene-artifact-packet-test.dFBFLc \
  tests/packs/rendering/test_scene_artifact_contract.py -k scene_only_bundle
```

Result: `1 passed in 7.68s`.

Also passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m ruff check tests/packs/rendering/test_scene_artifact_contract.py
git diff --check
```

The allowed central targeted request was attempted once, but its runner lacked
the provisioned renderer peer graph and stopped at fixture setup (`ASTRID_TEST_NODE_MODULES`
resolved to the snapshot's empty `remotion/node_modules`; `esbuild` missing).
That result is not used as evidence; the pinned local UNIT-REAL-NODE run above
is the qualifying test result. No full suite, browser, live socket, install,
network, or production API run was performed.

## Scope and handoff

No SDK product file, authority field, DTO, provider, endpoint, source factory,
secret, or new envelope was added. The Agent peer should consume the existing
artifact path and check the existing status/extent/map/label shape before calling
the existing formatter. Any ordinary SDK activation or live Runtime claim
remains unverified and is outside this packet.
