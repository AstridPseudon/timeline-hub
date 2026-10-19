# Runtime M0 journey preflight (Linux)

Status: static/source preflight only. No journey, Playwright browser, build,
install, or test suite was run by this worker.

## Result

The App journeys have a complete source-defined Linux topology, but the current
shared environments do not satisfy the harness's Runtime interpreter path:
`tests/e2e/local/support/harness.ts` only accepts
`<ASTRID_RUNTIME_CHECKOUT>/.venv/bin/python`. The ready shared environment is
`/home/user/work/venv-runtime`, and `/home/user/work/runtime/.venv/bin/python`
is absent. `ASTRID_RUNTIME_PYTHON` is not an App harness variable. Direct tests
would skip at `harnessUnavailableReason`; three-products fails its `beforeAll`.

The requested Agent command is also not currently runnable as written. The
literal command omits required `--summary`; the valid form is shown below. On
the current Agent tree its first source-checkable failure is the missing
`/home/user/work/agent/remotion/node_modules` for the default
`rendering.remotion` backend. Agent documentation says full smoke is macOS-only due Darwin custody, but this is **not a verified current-code Linux blocker**: Runtime main `astrid_runtime/runtime_boundary.py:_spawn_runtime` explicitly has a non-Darwin platform launch path. The docs may predate portability changes. Missing Remotion is confirmed; later Linux lifecycle/host behavior remains untested.

## Source tuple and shared evidence

| Product | Source path | SHA | Relevant shared state |
| --- | --- | --- | --- |
| App | `/home/user/work/app` | `60aa26b9529dcfa94f8ffdbd5edf42fa6c1babd2` | `node_modules` present; `dist` absent; App manager recorded Chromium 141 launch/page probe pass and Playwright revision 1223 absent |
| Agent | `/home/user/work/agent` | `e51595c68fc23d3d1734a0885c84a6511999697b` | `/home/user/work/venv-agent` ready, dependency-only, Python 3.13.16; source injection required; `remotion/node_modules` absent |
| Runtime | `/home/user/work/runtime` | `8c1830d1ca64a3934c37611a28ffe8db7df879ea` | `/home/user/work/venv-runtime` ready, dependency-only, Python 3.13.16; no checkout-local `.venv` |

The Runtime baseline is already recorded in
`design/runtime-baseline.md`: the required default suite is red on unchanged
main (the completed runs were 3391 passed/9 failed/18 skipped and 3392
passed/8 failed/18 skipped); focused door/lock/idempotency coverage passed
1332 tests. This preflight does not rerun it. Frozen R4 branches and protocol
assumptions were not used.

Relevant source locations:

- App paths and Runtime launch: `tests/e2e/local/support/harness.ts:37-50,
  433-457`.
- App browser fallback: `tests/e2e/local/support/app.ts:22-29, 39-46`.
- App hosted build gate: `tests/e2e/local/global-setup.ts:24-47`.
- App journey configs: `playwright.direct.config.ts:3-21` and
  `playwright.three-products.config.ts:4-15`.
- Agent command registration: `astrid/core/gateway/dev_operator.py:693-714`.
- Agent journey parser/preflight: `astrid/core/dev/journey.py:912-985,
  1075-1112`.
- Agent generated reference: `astrid/core/dev/reference_realm.py:32-37,
  69-103`.
- Agent Linux limitation: `docs/development/journeys.md:76-86`.
- Agent Remotion requirements: `astrid/core/rendering/node_pin.py:1-15,
  101-130` and `astrid/core/rendering/remotion_runtime.py:1147-1165`.
- Remotion browser override: `remotion/shared-browser.mjs:15-16, 25-39,
  54-69` and `remotion/remotion.config.ts:22-23`.

## App Linux prerequisites and command shape

Use isolated journey worktrees at the recorded integration SHAs for execution. Do not build or run a source-mutating journey in the integration directories. The Runtime fixture is staged without source changes by rt-m0-journey-runtime-env; preserve it until the App journey finishes:

```bash
export APP_CHECKOUT=/home/user/work/wt/rt-m0-journeys
export AGENT_CHECKOUT=/home/user/work/agent
export RUNTIME_CHECKOUT=/home/user/work/wt/rt-m0-journey-runtime-env
export AGENT_PYTHON=/home/user/work/venv-agent/bin/python
export RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python
export NODE_ROOT=/home/user/work/node-v20.19.4-linux-x64

export PATH="$NODE_ROOT/bin:$PATH"
export ASTRID_CHECKOUT="$AGENT_CHECKOUT"
export ASTRID_PYTHON="$AGENT_PYTHON"
export ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT"
export PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT${PYTHONPATH:+:$PYTHONPATH}"

# App's local resolver uses this path when Playwright's lock-aligned revision
# is absent. The shared App evidence says Chromium 141 launches here.
export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
export PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome

# Keep output out of a checkout. The direct config defaults to door 17340 and
# the three-products config must never run concurrently with direct.
export PLAYWRIGHT_OUTPUT_DIR=/tmp/timeline-direct-results
```

The App package requires Node `>=20.19.0`; the shared pinned runtime is Node
`v20.19.4` with npm `10.8.2`. App's `@playwright/test` is 1.60.0. The
preinstalled browser directory contains `chromium-1194`; the source fallback
selects the highest `chromium-N` directory when the default Playwright
executable (revision 1223) is absent. The explicit path above is therefore the
deterministic choice. The App manager's launch/page probe is the evidence for
Chromium 141; this worker did not launch a browser.

The harness also needs `openssl` to create its temporary HTTPS certificate;
`/usr/bin/openssl` is present. `ffmpeg` and `ffprobe` are on PATH at
`/usr/bin/ffmpeg` and `/usr/bin/ffprobe`. App's `makeVideo()` uses `ffmpeg` for
a decodable WebM and falls back to a checked-in MP4 when it is absent, but the
Runtime's typed-media validation requires both tools for typed video/audio
admission. Keep `/usr/bin` on PATH.

The Runtime interpreter mismatch is the first App-specific blocker. The
harness computes:

```text
runtimePython() = ASTRID_RUNTIME_CHECKOUT/.venv/bin/python
```

There is no `ASTRID_RUNTIME_PYTHON` override in the source. Do not install into
the shared venv or alter `/home/user/work/runtime` for this preflight. The manager has dispatched rt-m0-journey-runtime-env: its isolated Runtime worktree supplies an ignored `.venv` symlink to the shared dependency-only environment. This uses the harness unchanged and preserves real Git identity. It is ordinary environment wiring, not a launcher shim. No integration-root edit or dependency reinstall is needed; readiness is recorded in journey-runtime-env.md.

The second App prerequisite is the hosted production bundle. `dist` is absent
at `/home/user/work/app/dist`. Both configs inherit `globalSetup`, which runs
`npm run build:hosted` when `dist/index.html` is missing or stale, and checks
that a JavaScript asset contains `http://127.0.0.1:17340`. This build is part of
the future heavy run and was deliberately not run here. A prebuilt alternative
must set `ASTRID_APP_DIRECT_DIST` to a directory containing a matching hosted
bundle; when that variable is set, global setup trusts it without rebuilding.

Once the Runtime interpreter path and hosted bundle are supplied, the exact
journey commands are:

```bash
cd "$APP_CHECKOUT"
npm run test:e2e:direct

# Separate run; never overlap it with direct because both use door 17340.
npm run test:e2e:three-products
```

The three-products run additionally requires the explicit Agent variables above;
its source checks `astrid/__init__.py`, `ASTRID_PYTHON`, and
`astrid/core/dev/cross_client.py`, then forces `PYTHONPATH=ASTRID_CHECKOUT` for
each Agent subprocess. It reads the Runtime discovery file before each call,
so no fixed Runtime service port should be exported. The harness itself starts
the Runtime on a dynamic port and the browser door on 17340 (override with
`ASTRID_APP_DIRECT_DOOR_PORT` only when a validated port reservation is made).

## Agent `dev journey` command

The command registered by `dev_operator.py` delegates to
`astrid.core.dev.journey.main`. `--tier`, `--reference`, and `--summary` are
required. For generated reference, `--timeline` defaults to `journey/main` and
the excerpt defaults to `2 6`; the generated reference creates three four-
second clips with `ffmpeg` and a media-only timeline. A valid source-injected
command is:

```bash
export AGENT_CHECKOUT=/home/user/work/agent
export RUNTIME_CHECKOUT=/home/user/work/wt/rt-m0-journey-runtime-env
export AGENT_PYTHON=/home/user/work/venv-agent/bin/python
export NODE_ROOT=/home/user/work/node-v20.19.4-linux-x64
export PATH="$NODE_ROOT/bin:$PATH"
export PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT${PYTHONPATH:+:$PYTHONPATH}"

# The variable is optional; the source default is 4 GiB. The journey checks
# free space on its temp volume against this floor plus render scratch.
export ASTRID_RUNTIME_FREE_DISK_FLOOR_BYTES=4294967296

cd "$AGENT_CHECKOUT"
"$AGENT_PYTHON" -m astrid dev journey \
  --tier smoke --reference generated \
  --summary /tmp/timeline-astrid-dev-journey-smoke.json
```

This command was not exercised. The exact source-supported requirements are:

1. `PYTHONPATH` must expose both Agent and Runtime source because the shared
   Python environments are dependency-only. `runtime_checkout_path()` locates
   the Runtime source from the imported `runtime_protocol`; generated
   reference invokes `python -m astrid_runtime` with that same source context.
2. `ffmpeg` is mandatory for `--reference generated`; `ffprobe` is used to read
   render duration. Both must be resolvable from PATH.
3. The default `rendering.remotion` backend resolves the exact Node pin
   `v20.19.4` from `agent/remotion/package.json` (npm is pinned to `10.8.2`)
   and requires the installed Remotion project, including the locked CLI and
   `@banodoco/timeline-composition`, `@banodoco/timeline-schema`, and
   `@banodoco/timeline-theme-2rp` packages. The current
   `/home/user/work/agent/remotion/node_modules` is absent. The first failure
   for this command is therefore the source-defined preflight message:

   ```text
   Remotion node_modules is missing: /home/user/work/agent/remotion/node_modules
   ```

4. Remotion also needs a browser. Its explicit override is
   `ASTRID_REMOTION_BROWSER_EXECUTABLE`, and the Linux layout is
   `chrome-headless-shell/linux64/.../chrome-headless-shell`. The shared-browser
   module's default cache is spelled `~/Library/Caches/astrid-remotion-browser`
   even on Linux; the App's Playwright Chromium path is not proof of Agent
   Remotion compatibility. No Agent Remotion browser launch was attempted.
5. The Runtime renderer doctor still requires a usable Remotion Node even when
   `--backend rendering.ffmpeg` is selected. That backend skips the journey's
   Node-install preflight and shortens rendering, but does not bypass the
   Runtime `doctor` renderer readiness check.
6. The journey has a 4 GiB default Runtime free-disk floor plus an estimated
   render scratch budget. It creates a disposable root under `/tmp`, mutates
   its own `journey.py` source probe temporarily, starts/restarts Runtime and
   pack-host process groups, and must be allowed to signal/reap those groups.

The docs at `docs/development/journeys.md:78-84` claim macOS-only smoke, but current Runtime main has explicit non-Darwin launch/termination paths (`runtime_boundary.py:367,754`). No Linux lifecycle failure was executed here, so do not report the docs as a proven current-code blocker. Once Remotion is available in an isolated Agent checkout, a bounded real run is needed to establish the next limitation. No Linux Agent journey pass is claimed. The smoke source-change phase must run only in that isolated checkout, never `/home/user/work/agent`.

## Checks performed

Read-only checks performed:

- `git -C <checkout> rev-parse HEAD` for the three integration source tuples
  above and this Runtime worker.
- Existence checks for shared `node_modules`, App `dist`, both shared Python
  interpreters, Agent Remotion `node_modules`, `/opt/pw-browsers`, OpenSSL,
  ffmpeg, and ffprobe.
- Version-only checks: system Node/npm (`v22.22.0`/`10.9.4`), pinned Node/npm
  (`v20.19.4`/`10.8.2`), and local Playwright (`1.60.0`).
- Dependency-only import probe with `PYTHONPATH` for Agent and the installed
  timeline schema; no Runtime daemon or browser was started.

Not run: `npm run test:e2e:direct`, `npm run test:e2e:three-products`,
`python -m astrid dev journey ...`, any `--help`/`--list` collection command,
any build, browser launch, install, Runtime start, Agent host, or full suite.

## Handoff

The heavy journey worker should first resolve the App harness's
checkout-local-Runtime-Python contract without changing shared dependencies,
then allow the App hosted build to run once, set the explicit Playwright
browser path, and run direct and three-products serially. The Agent command remains unexecuted with a confirmed missing Remotion prerequisite; current Linux lifecycle support is unproven rather than declared unavailable. Coordinate a dedicated Agent journey checkout/environment with Agent/Viewing before a later heavy run. No new platform decision is needed merely because the older docs say macOS-only.

Manager review (18:13 UTC): corrected unproven OS claim, removed an unnecessary harness-approval suggestion, and changed executable App/Runtime paths to isolated worktrees. Original static worker performed no journey; actual runs remain rt-m0-journeys with --net/--heavy and at most one attempt per suite.

## Manager parser probe (18:29 UTC)

Ran the literal requested Agent shorthand once, with source-only PYTHONPATH and no bytecode writes:

```bash
PYTHONPATH=/home/user/work/agent:/home/user/work/wt/rt-m0-journey-runtime-env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m astrid dev journey --tier smoke --reference generated
```

Exit **2** in 0.12s: `astrid dev journey: error: the following arguments are required: --summary`. No journey, daemon, renderer or source-change phase started. The corrected command with --summary remains unexecuted and requires the missing Remotion installation; no Linux custody failure was observed. This manager probe supplements the worker's static-only checks; it is not a journey result.
