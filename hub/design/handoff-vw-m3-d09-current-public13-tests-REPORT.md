# Worker report

## Result

Joined the two D09 replacement coverage units into the current Agent test
source. The only product-repository change is
`tests/packs/rendering/test_scene_host.py`.

- Base commit: `5c5173dcb57669a9d43e5add2674543333f1c6d2`
- Base tree: `8626f868a3869b23baaca9814adb930e8952e4c7`
- Source branches inspected:
  - `tl/vw-m3-d09-scene-audio-none-filter-coverage` at
    `a1d659b6b9c71c89fd1783c8eaf1aa998c3f6097`
  - `tl/vw-m3-d09-public-layer-order-alpha-case` at
    `79be4b00dfef8f677cdcda35f73397b01de64928`
- The overlapping fixture update was applied once: public13 artifact,
  SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- The existing Node pin remains exact `v20.19.4`; final tests used the
  read-only immutable4913 graph at
  `/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules`.

## Changes

- Added the public13 audio-only track gap assertion (`layers == []`,
  `content is None`).
- Added public13 absent-element versus unsupported-custom coverage assertions
  for `visible`, `opacity`, `opaqueSupport`, findings, and `UNKNOWN` coverage.
- Preserved the existing painter-order/role assertion and added the natural
  clip-opacity × track-opacity assertion (`0.5 * 0.8 == 0.4`).
- Preserved every current assertion and did not port the audio branch's
  unrelated `test_scene_answers.py` change.
- No production code, deletion, or test retirement.

## Evidence

Final immutable-graph targeted run:

```text
PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 PATH="$(dirname "$NODE"):$PATH" ASTRID_NODE_EXECUTABLE="$NODE" ASTRID_TEST_NODE_MODULES="$PEERS" ASTRID_REMOTION_PROJECT_DIR="$RUNTIME" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_scene_host.py tests/packs/rendering/test_scene_answers.py
47 passed in 12.84s
```

Directly related pure legacy behavior run:

```text
... pytest ... tests/core/timeline/test_onscreen.py::test_visible_at_lists_layers_top_first_with_role_and_opacity_product tests/core/timeline/test_onscreen_more.py::test_a_none_element_is_not_listed tests/core/timeline/test_onscreen_more.py::test_audio_clips_and_audio_tracks_are_ignored
3 passed in 0.13s
```

Collection check: `47 tests collected` for the host plus scene-answer target.
`git diff --check` passed.

The first local attempt without renderer provisioning was not a source failure:
the worktree had no `remotion/node_modules/esbuild` and PATH had only Node
22.22.0, so pytest reported setup errors. Re-running with the read-only
immutable4913 graph, Node v20.19.4, and the public13 runtime project passed.

## Limits and next step

No full suite, browser, live-render, or production test was run, per task
scope. The bounded patch is in `PATCH.diff`; exact commands and environment
are in `COMMAND`. The Agent owner can review and merge this test-only change.
