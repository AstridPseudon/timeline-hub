# AP2-M2 hosted-build heap environment diagnosis 1135

## Result

The retained parent1384 failure is an execution-environment boundary, not a
viewport or product-geometry failure. The `env -i` central invocation removed
the container's normal `NODE_OPTIONS=--max-old-space-size=8192`. The hosted
build then ran with Node22's default roughly 2 GiB V8 heap and aborted after
transforming 5,586 modules.

The minimal correction is one process-local assignment on the existing hosted
build command in each owned actual runner:

```sh
NODE_OPTIONS=--max-old-space-size=8192 npm run build:hosted
```

This is an unapplied runner-artifact diff for manager custody review. No App
source, shared `normal014` helper, global environment, product config, pin,
graph, test, timeout, or guard was changed.

## Exact first cause

The successful0939 retained central command was:

```text
... && env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 sh .../final-keeper-gate.sh run
```

Its hosted build completed (`built in 53.76s`). This command inherited the
container's normal `NODE_OPTIONS=--max-old-space-size=8192`; it did not use an
`env -i` boundary.

The failing1384 retained central command was:

```text
flock -n /home/user/work/.app-m1-browser.lock env -i HOME=/tmp/tl-pv-parent-1126-central/home LANG=C.UTF-8 PATH=/opt/node22/bin:/usr/bin:/bin TMPDIR=/tmp/tl-pv-parent-1126-central/tmp XDG_RUNTIME_DIR=/tmp/tl-pv-parent-1126-central/xdg NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent NORMAL014_USE_BASE_PYTHON=1 NORMAL014_PYTHON_BASE=/home/user/work/venv-app2-native/bin/python NORMAL014_LOCKED_GRAPH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph NORMAL014_LOCKED_GRAPH_ARCHIVE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar APP_ROOT=/home/user/work/wt/app-pin-6707a30f NORMAL014_RECORD_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-viewport-exact-one-central-1126/record/evidence-central NORMAL014_RUN_ROOT_PARENT=/tmp/tl-pv-parent-1126-central PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers sh .../final-keeper-gate.base.sh run
```

The exact child argv was recorded as:

```text
npm run build:hosted
-> node scripts/build-hosted.mjs
```

No `NODE_OPTIONS` appears in the `env -i` command or the child command. The
retained log shows:

```text
✓ 5586 modules transformed.
2036.8 (2084.4) MB
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
```

The first failure was therefore the hosted Node22 build at its default heap
limit. Browser launch and all journey assertions were unreached. The 8192 MiB
bound leaves approximately `8192 - 2036.8 = 6155.2 MiB` (about 6.0 GiB) of V8
heap headroom relative to the observed peak. This is the existing 8192 bound,
not an increase.

Preserved1384 custody remains unchanged: App `6707a30f...` / tree
`6ff32d79...`, Agent `6efc8150...`, Runtime `95bd3c5f...`, locked graph
`895c628a...`, Composition `9412ae25...`, helper `4f57561a...`, driver
`f11cefbb...`, gate `1dec33f4...`, one collected test, exit134, and the retained
central evidence directory.

## Exact owned runner diff and updated hashes

No existing build-only carrier exists in the parent or selected owned runner
artifacts. The proposed changes are exactly these single lines:

| owned artifact | existing line | proposed line |
|---|---:|---|
| `workers/ap2-m2-parent-viewport-exact-one-central-1126/record/artifacts/normal014-app-central.bound.sh` | 122 | `NODE_OPTIONS=--max-old-space-size=8192 npm run build:hosted` |
| `design/ap2-m2-selected-clean-keeper-main-port-1120-runner.sh` | 708 | `NODE_OPTIONS=--max-old-space-size=8192 npm run build:hosted >"$CHILD_LOG" 2>&1` |

The selected P1 driver at line169 is a guarded, non-executed legacy artifact in
this selected actual path; it remains byte-identical. Its existing 4096 export
also remains unchanged because the proposed prefix overrides memory only for
the hosted build, without changing the selected Runtime/browser process
environment.

Source and proposed SHA-256 values:

```text
parent bound app runner: d5d8a983b2248f237b35dd81ad91d6f5a8b730ebccb2d8ca35279b3aaf042c87
parent proposed runner:  da324447737623c000fee43c138e88c7445d2e0105a7984a23cde73a42605b00
selected runner:         6416f65db7b8f247bd8610b504435c8a18c4139ded1b8bbcf4fc7ae3da83e5ed
selected proposed:       8cd735c4d8322b588fade70ebbf6d64ca6af811ed50347e9442cf62a63a4ca43
selected P1 driver:      cf4ddff51c86e2be5a1d7bdae705aa3390eaf4c931e6cea7b2369311dadecea7 (unchanged)
```

Reverse proof: `diff -u` of each proposed stream has one hunk and one added
`NODE_OPTIONS=...` command prefix; no argv, assertion, cleanup, retention,
source, hash, graph, lock, or guard logic changes. The parent helper/driver/gate
hashes remain `4f57561a...`, `f11cefbb...`, and `1dec33f4...`. The corrected
selected transitive inputs remain source-common `647ea22a...`, parent-media
`ce9e86fa...`, selected P1 driver `cf4ddff5...`, and KEEP `e3b0c442...`.
Any landing must update only the corresponding owned runner registration/hash
binding to the proposed bytes and recompute its outer manifest; no source or
product hash may be rebound.

## Offline safety checks

No real npm build, browser, socket, Runtime service, request, install, full
suite, or actual journey was run.

- `sh -n` on the parent and selected proposed streams — PASS.
- A shell `npm` stub received `run build:hosted` with
  `NODE_OPTIONS=--max-old-space-size=8192` for both parent and selected cases
  and returned 37; the runner-side status remained 37 — PASS. This proves the
  prefix is on the hosted build only and preserves child failure propagation.
- With inherited sentinel values for `NODE_OPTIONS`, `NODE_PATH`, `LD_PRELOAD`,
  and `PYTHONHOME`, the same failing build stub left every parent sentinel
  unchanged after the prefixed child returned 41 — PASS. There is no global
  unset or export in the proposed diff.
- Existing App pack-host bootstrap seam:
  `tests/e2e/timeline/viewing-parity/bootstrap.ts:106-108` clones the env and
  removes `NODE_OPTIONS`/`NODE_PATH` before the helper spawn at `:124-128`.
  Its existing stub capture is `tests/e2e/timeline/viewing-parity/harness.test.ts:238-259`
  (child env assertions plus parent-sentinel preservation). The offline command
  `ASTRID_PACK_HOST_HELPER_CHECKOUT=<private carrier> ASTRID_CHECKOUT=$PWD node --import tsx --test --test-name-pattern='clears loader overrides only for the real pack-host child|preserves a safe helper failure' tests/e2e/timeline/viewing-parity/harness.test.ts` exited 0; no browser/socket/service was started.
- Runtime spawn isolation is explicit at
  `tests/e2e/local/support/harness.ts:489-495` and `:516-520`: the Runtime
  receives the narrow `runtimeEnv()` map, not the parent build environment.
- Downstream Remotion child policy is already an allowlist at
  `/home/user/work/agent/astrid/core/execution/remotion_host_session.py:193-204`.
  The existing Agent journey scrub removes `NODE_OPTIONS`, `NODE_PATH`,
  `LD_*`, `DYLD_*`, and `PYTHONHOME` at
  `/home/user/work/agent/astrid/core/dev/journey.py:214-220`; an inline child
  stub capture using that function observed all five classes absent — PASS.
  Its source tests at `tests/journeys/test_journey_plumbing.py:45-70` preserve
  the same child-capture contract.

The direct App bootstrap currently deletes two loader overrides at its own
helper boundary; the Agent-owned downstream Remotion host allowlist/scrub is
what removes `LD_*` and `PYTHONHOME`. I made no product change in this
App-only runner task. If the requirement is instead that the App helper process
itself must delete those latter names before `startRealPackHost` spawn, that is
a separate Viewing-owned product gap, not a consequence of this build prefix.

## Proposed next one preflight/body

After manager custody accepts the two one-line runner prefixes and recomputed
runner hashes, perform one existing parent/selected boundary preflight using
those bound bytes and all original source/hash/retention/RC/zero-test guards.
Then authorize at most one central body on the chosen lane with the existing
exact test list and no duplicate failure replay. The hosted build should be
invoked only as the prefixed command above; the later Playwright/Runtime/
pack-host children must use their existing sanitized environments. The 1384
packet remains the sole OOM evidence and is not replayed.

## Scope and status

Only diagnosis, offline stubs, source-line/hash comparison, and this report were
performed. The App worktree is clean. No product file, repo doc, `.gitignore`,
shared dependency, shared normal014 script, pin, graph, or retained evidence
was modified. The one temporary helper carrier was cleaned on exit.

