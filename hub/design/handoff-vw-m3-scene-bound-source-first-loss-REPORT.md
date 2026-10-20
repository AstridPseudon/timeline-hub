# Scene-only first source-binding loss

The first loss is at the GenericPackHost executor child boundary. The
managed capture is admitted and materialized, and
`PreparedTimelineInputs.mint_source()` creates the retained source. The
existing `handoff_source()` call is present for the command-capability branch,
but `rendering.timeline_visualize` uses the executor branch. That branch builds
`worker_env` and invokes the child without calling `handoff_source(inputs,
worker_env)`. The child therefore has no `ASTRID_VERIFIED_TIMELINE_SOURCE`;
the executor's `inherited_source()` returns `None`, its source-derived receipt
provenance remains absent, and the current SDK correctly returns advisory
`UNAVAILABLE` with `scene source binding unavailable`.

The exact unapplied owner correction is [handoff-vw-m3-scene-bound-source-first-loss-owner.patch](./handoff-vw-m3-scene-bound-source-first-loss-owner.patch): two lines immediately before the executor `try` block in
`astrid/core/execution/generic_host.py`. No SDK/core production file was
changed in this worker. The current executor23db source is byte-identical to
the current Agent executor source (`3e94cd6711f4e115841a8682d6f50899d0f2f5e2`);
the restored 4f29 source carrier and f82/d0a current ports do not add this
executor-branch handoff.

## Bounded regression

The owned `scripts/run_scene_only_central.py --source-regression` private
overlay check reproduces the strict failure with a plain mapping (ambient
source is cleared and no source is forwarded), proves the existing prepared
carrier succeeds with the retained anchor, and verifies the private executor
overlay inserts the exact owner patch. Result: exit 0.

The wrapper applies the two-line correction only to its disposable overlay;
it does not alter the shared Runtime, node modules, renderer peers, or this
worktree's core source. No live central retry, browser, PNG, or render was run
after the predecessor failure.

## Source cohort

| item | exact identity |
|---|---|
| Agent worktree | `2202d9fbfc07da1b1e02a75c89badde16f5e143a` |
| current executor source | `23db420c1` / blob `3e94cd6711f4e115841a8682d6f50899d0f2f5e2` |
| restored source carrier | `4f29c39a8` |
| current source ports reviewed | `f82da3220`, `d0a5072bb` |
| central SDK | `9b887e232` |
| central executor | `23db420c1` |
| central Runtime | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` |
| central Node | `v20.19.4`, SHA `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490` |
| central Composition | `banodoco-timeline-composition-0.0.13.tgz`, SHA `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` |

## Fixture/schema note

The predecessor's removal of `opaque_track`, `opaque_clip`, and `rect` was
limited to the private render-copy fixture because the unchanged host schema
rejects those fields there. It did not edit the authoritative authored closure
or any opaque-field tests. The authored closure and lossless/opaque tests stay
untouched; the normal single projector remains responsible for producing the
render config. No input was laundered before authority checks.

## Tests

```text
PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B scripts/run_scene_only_central.py --source-regression
PASS (exit 0)

PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= --basetemp=/tmp/scene-bound-source-targeted tests/sdk/test_managed_render_invocation.py tests/sdk/test_scene_dispatch_contract.py tests/sdk/test_scene_caller_preservation.py tests/packs/rendering/test_scene_only_executor.py
38 passed, 2 skipped in 1.70s

PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= --basetemp=/tmp/scene-bound-source-neighbor tests/packs/rendering/test_verified_source.py tests/sdk/test_capture_source_runtime.py
60 passed, 27 skipped in 4.73s

git diff --check
PASS
```

Next step: Agent owner applies the exact two-line core patch, reruns the
bounded source regression and the 38 + source neighbors, then schedules one
fresh central run with the same cohort. The saved/candidate/stale and receipt
claims remain unqualified until that run.
