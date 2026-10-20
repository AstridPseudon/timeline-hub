# Fresh mouth public carry final-gate command

Run from `/home/user/work/wt/vw-m3-fresh-mouth-public-carry-final-gate`:

```sh
NODE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node
ARTIFACT="$PWD/remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz"
PEERS=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" env -u NODE_OPTIONS -u NODE_PATH \
  ASTRID_NODE_EXECUTABLE="$NODE" \
  ASTRID_COMPOSITION_TEST_NODE_MODULES="$PEERS" \
  ASTRID_COMPOSITION_TEST_ARTIFACT="$ARTIFACT" \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  -m integration --tb=short tests/packs/rendering/test_presenter_selected_cut_aggregate.py \
  -k 'fresh_public_mouth_facts_drive_existing_consumer or planted_public_fact_failures_keep_private_fallback'
```

Result: **4 passed, 17 deselected in 3.59s**.

The lane used Node `v20.19.4` (SHA-256
`43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`), the
public12 artifact (SHA-256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`), and
the read-only f816 peer root. No shared dependency or cache was modified.
