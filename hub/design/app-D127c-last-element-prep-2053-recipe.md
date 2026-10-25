# D127c source-only prepared recipe

Status: `PREPARED_SOURCE_READY`. This packet records one deferred normal
`p2-element --submit` controller invocation. It has not run preflight,
bootstrap, submit, a browser body, a Runtime body, or a live socket.

The source root is the clean normal App home at
`b5c9eadfa1950f46feac50d7d6a89c47f27f4881` / tree
`8e10af0976b012205f27a18a432c750a27de0725`. The committed App source guard
is blob `dea8cda5c28fb4cfe9142c046e9771398274aac9`, SHA-256
`59a4d116683f88d415024b6d9236e578cf03c11e2c913b56278f9d57448b40ef`, and
explicitly accepts the reviewed profiler helper `095c252b...`.

The private helper is the regular file
`evidence/p2_commit_phase_capture.py`, mode `0600`, in this packet's mode
`0700` evidence directory. It is the exact committed Runtime helper blob from
`368f53f4454d5908c86de53d174f0bedcf23781c` (also present at the reviewed
`fb4addba95ca4bae0482c93be94e5cae2770ca09` source), SHA-256
`095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d`.
It is an external diagnostic helper only; the Runtime product pin remains
`ab1e4f6141987706132916e2da16477f5a019464`.

## Deferred one-command controller route

The manager must first request the detached App checkout through the ordinary
request-checkout route at `b5c9eadfa1950f46feac50d7d6a89c47f27f4881`; the
expected path is `app-pin-b5c9eadf`. The manager also owns the Runtime normal
home helper receipt. Do not invent either receipt, and do not run this block
until the manager records genuine available disk of at least 5.2 GB once at
controller dispatch. Keep one heavy body, stop at 4.0 GB, and do not reapply
the 5.2 GB floor during dependency preparation.

`ACTUAL_CONTROLLER` is supplied by the future controller; this preparation
does not create its submission directory or plan.

```sh
set -eu
umask 077
ORCH='/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch'
ACTUAL_CONTROLLER='app-D127c-<manager-controller>'
WORKER="$ORCH/workers/$ACTUAL_CONTROLLER"
APP_SOURCE_ROOT='/home/user/work/app'
NODE='/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node'
HELPER="$ORCH/workers/app-D127c-last-element-prep-2053/evidence/p2_commit_phase_capture.py"
export D66_OUTPUT_DIR="$WORKER/submission/p2-element"
export D66_SUBMIT_PLAN_PATH="$WORKER/submission/p2-element/p2-element-submit-plan.json"
export D66_SUBMIT_TARGET='app-pin-b5c9eadf'
export D66_CHECKOUT_ROOT='/home/user/work/wt'
export D66_APP_SHA='b5c9eadfa1950f46feac50d7d6a89c47f27f4881'
export D66_APP_TREE='8e10af0976b012205f27a18a432c750a27de0725'
export D66_APP_CHECKOUT='/home/user/work/wt/app-pin-b5c9eadf'
export D66_AGENT_SHA='070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2'
export D66_AGENT_TREE='6056414359ae9fce08d999d54cbecf719fda33c3'
export D66_AGENT_CHECKOUT='/home/user/work/wt/agt-pin-070dfc5e'
export D66_RUNTIME_SHA='ab1e4f6141987706132916e2da16477f5a019464'
export D66_RUNTIME_TREE='7d8e77b2f5a4af79305c9212ce5174d3ea9fd657'
export D66_RUNTIME_CHECKOUT='/home/user/work/wt/rt-pin-ab1e4f61'
export D66_COMPOSITION_SHA='635f4de06fda22a85fc2e4cfc764d0153a4c9f40'
export D66_COMPOSITION_TREE='5ab5191a296980a0a6bcd1178ab6902d6478a148'
export D66_COMPOSITION_CHECKOUT='/home/user/work/wt/vw-pin-635f4de0'
export D66_P2_COMMIT_PHASE_CAPTURE_HELPER="$HELPER"
export D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256='095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d'
export ASTRID_PYTHON='/home/user/work/venv-agent/bin/python'
export ASTRID_RUNTIME_PYTHON='/home/user/work/venv-runtime/bin/python'
export ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS='2'
cd "$APP_SOURCE_ROOT"
test "$(git rev-parse HEAD)" = "$D66_APP_SHA"
test "$(git rev-parse 'HEAD^{tree}')" = "$D66_APP_TREE"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
test "$(sha256sum tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts | cut -d ' ' -f 1)" = '59a4d116683f88d415024b6d9236e578cf03c11e2c913b56278f9d57448b40ef'
test "$($NODE --version)" = 'v20.19.4'
test -f "$HELPER"
test ! -L "$HELPER"
test "$(stat -c %a "$HELPER")" = '600'
test "$(sha256sum "$HELPER" | cut -d ' ' -f 1)" = "$D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256"
test "$(realpath "$APP_SOURCE_ROOT/node_modules")" = '/home/user/work/app/node_modules'
test "$(realpath "$APP_SOURCE_ROOT/node_modules/tsx/dist/loader.mjs")" = '/home/user/work/app/node_modules/tsx/dist/loader.mjs'
test "$($NODE --input-type=module -e 'console.log(import.meta.resolve("tsx"))')" = 'file:///home/user/work/app/node_modules/tsx/dist/loader.mjs'
$NODE --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p2-element --submit
```

The route is the existing D66 controller and its normal source-preflight
then-one-body sequencing. It preserves selector count 1, the unchanged
5-second assertion, all canonical/history/reload/guarded-undo assertions,
zero legacy-route assertions, and the existing 2-second watchdog. It does not
add a CJS API hook to the product controller; Node20 CJS API controls only
proved unit loading. The browser D66 submit route stays unchanged.

The deferred run must retain the complete C0 v2 request and reply semantics:
`api_version`, project/timeline and base revision/publication, commands with
schema/version/select/args/created, label, per-step intent/tags/ordinals/patch
and optional reads, `merge`, reads, `Idempotency-Key`, dry-run, source,
rationale, and group id. Accepted/merged replies keep canonical document,
digest, normalized commands, identity/base/landing, receipt, records, bindings,
effects, dependencies, history and undo steps. Conflict, invalid and preview
forms retain their reason/head, code/path/hint/suggested command, and
would-status/null receipt respectively.

The cProfile arm is opt-in only for the first real mounted element selection:
the existing `_timeline_commit` helper instrumentation selects one traced
`_dispatch`/bounded-prefetch request matching the mounted App `doc.patch`
`list.insert` element operation. It excludes setup/native/media traffic,
parameter `doc.patch`, `timeline.inverse`, mixed commands, dry-runs and retry
promotion. Published output is only the safe top 40
`(file,line,function,ncalls,tottime,cumtime)` plus caller→callee edges. Raw
pstats/capture remains private 0600 under a private 0700 runtime directory;
no raw logs, payloads, keys, auth, URLs, locals, private frames or historical
profile reconstruction are exported.

No acquisition/install, source fix, pin change, manual generated file, product
retarget, upstream push, hub write, merge request, M5 work, D135 cut-pin claim,
SWAP/WAL/recovery/full-tour, or refused-route retry is part of this recipe.
