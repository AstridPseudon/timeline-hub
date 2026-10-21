# D09 current public host assertions

## Result

Ported the approved bounded D09 replacement assertions into only
`tests/packs/rendering/test_scene_host.py` on the current Agent worktree.
The public13 fixture update is applied once, using the checked-in Composition
0.0.13 archive. Existing assertions remain intact.

The test-only delta adds:

- an audio-only track assertion for `layers == []`, `coverage == "GAP"`, and
  `content is None`;
- an absent registered element versus unsupported custom element assertion,
  preserving raw `visible`, `opacity`, `opaqueSupport`, findings, and
  `UNKNOWN` diagnostics;
- the existing `labels_for_scene()` adapter assertion that omits only the
  explicit absent row while retaining the unknown row; and
- the natural clip-opacity/track-opacity assertion `0.5 * 0.8 == 0.4`.

No product code, geometry cut, test retirement, strict xfail, dependency pin,
or package change was made.

## Evidence

The checked-in public13 archive has SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
The actual host lane used Node `v20.19.4` and the read-only immutable graph
`/home/user/work/runtimes/agent-remotion-0013`; the test extracted the archive
into its private pytest temporary project and did not install or mutate shared
dependencies.

```text
PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 \
  PATH="/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:$PATH" \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0013/node_modules \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0013 \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= \
  -p no:cacheprovider tests/packs/rendering/test_scene_host.py \
  tests/packs/rendering/test_scene_answers.py
47 passed in 23.77s
```

Additional bounded checks:

- three retained legacy on-screen neighbors: `3 passed in 0.21s`;
- adjacent capture/label lanes: `28 passed in 10.60s`;
- `ruff check --no-cache tests/packs/rendering/test_scene_host.py`: passed;
- `git diff --check`: passed.

## Limits

No full suite, managed/physical/renderer replay, browser, live socket, or
actual render was run. No source behavior outside the requested test file was
changed. The worktree is ready for the harness commit.
