# D09 real public RLE: 300 adjacent clips

## Result

Prepared a 160-line test-only delta at
`tests/sdk/test_scene_real_public_summary_rle.py`. The donor's existing 133
lines and every assertion remain intact. The added fixture creates 300
adjacent public-host clips, one frame each at 30 fps, and sends their real
public13 host answers through the same `_real_spans` carrier and
`Checkout._scene_problems` consumer.

The distinction is explicit:

- The retained donor case is **one clip observed for 300 frames** and must
  produce one detailed `0..300 COVERED/CONTENT` span and one summary row.
- The added case is **300 adjacent one-frame clips observed for 300 frames**.
  It retains 300 detailed `0..1` through `299..300` `COVERED/CONTENT` rows,
  with first membership `generated-000` and last membership `generated-299`,
  while the warning consumer reduces only class/content to the exact one-row
  summary `0..300 COVERED/CONTENT`.

No private boundary-call-count assertion, copied geometry/math, fabricated
Scene rows, golden JSON, production change, browser/full/physical run, or
managed replay was added.

## Evidence

Pinned real-host command:

```text
env -u NODE_OPTIONS -u NODE_PATH PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  PATH="/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:$PATH" \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules \
  ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= \
  -p no:cacheprovider --basetemp=/tmp/d09-real-rle-300-clip-final-neighbor \
  tests/sdk/test_scene_real_public_summary_rle.py \
  tests/sdk/test_scene_summary_projection.py
```

Result: **4 passed in 4.76s** (1 real public test plus 3 direct summary
neighbor tests).

Additional checks:

- `ruff format --check tests/sdk/test_scene_real_public_summary_rle.py tests/sdk/test_scene_summary_projection.py` — passed.
- `ruff check tests/sdk/test_scene_real_public_summary_rle.py tests/sdk/test_scene_summary_projection.py` — passed.
- `git diff --check` — passed.
- Isolated pinned real test — **1 passed in 4.92s**.

An initial combined attempt omitted the pinned renderer environment and failed
at fixture setup because shared peers were intentionally not available through
the worktree; it was not a source failure. The corrected pinned command above
passed.

The frozen Span helper and its private projection test were applied unchanged
only for these runs, then reversed. The final worktree contains only the new
test file. The Git-generated unapplied `PATCH` is 166 lines with SHA-256
`ce3eff5958e37beb6b9ea05e923689a62ba51cd43db76ad4c3acedcb81dca0e0`.
