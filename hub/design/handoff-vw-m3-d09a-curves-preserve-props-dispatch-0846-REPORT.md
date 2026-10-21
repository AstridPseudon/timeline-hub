# VW-M3-D09a — preserve original property dispatch without a public mouth override

## Result

Applied the bounded correction on top of `637dd07fd` (base integration
ancestor `a9f4cfdae`). `props_at` now uses the public presenter override only
when `presenter_mouth_state is not None`; an absent or refused row therefore
falls through to the existing `PROPS` lookup and call unchanged. Explicit
`"closed"` remains a valid override and returns mouth scalar `0.0`.

Added one regression in the existing selected-cut test file. It replaces the
`am-presenter` entry in `model.PROPS` to prove the missing-override call keeps
custom dispatch, then proves the valid closed override still returns `0.0`.
The prior public-row curve/missing-frame regression and all prior assertions
remain retained.

## Source scope

Exactly these three files are in the cumulative source packet:

- `astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py`
- `astrid/packs/rendering/actions/timeline_visualize/motion/model.py`
- `tests/packs/rendering/test_presenter_selected_cut_aggregate.py`

The first file is unchanged relative to the prior worker; it is included in
the cumulative packet so HOME receives the complete three-file source result.

## Evidence

- Selected-cut, pinned Node/public13 environment: **25 passed in 5.14s**.
- Motion neighbor `tests/packs/rendering/test_timeline_visualize_motion_views.py`:
  **33 passed in 10.27s**.
- Ruff on all three source files: **passed**.
- Cumulative `git diff --check a9f4cfdae` on all three files: **passed**.
- Node: `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`,
  `v20.19.4`, SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Public13 peer leaves: `/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules`
  (read-only); retained artifact SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

The first selected-cut setup attempt used a new, nonexistent registry project
path and errored before tests; the second attempted to use the orchestrator's
`tmpdir` marker file as a directory and errored before tests. Neither changed
source or shared dependencies. The final run reused the qualified public13
registry path and an owned pytest basetemp and passed.

No full, browser, helper, Runtime, socket, central, repeated source/cache
qualification, install, shared dependency write, or Git mutation was run.
No API, DTO, store, provider, authority, admission, state-label, clock,
pixel/crop, or private fallback behavior was changed.

The harness must supply the final commit; this worker did not commit.
