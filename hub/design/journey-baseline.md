# Runtime M0 cross-product Linux journey baseline

Date: 2026-10-19  
Scope: one bounded attempt for each App journey; Agent journey feasibility from the reviewed preflight and its recorded parser probe.

## Result

| Journey | Linux result | Evidence |
| --- | --- | --- |
| `npm run test:e2e:direct` | **PASS** | 39/39 Playwright tests passed in 2.8 minutes. |
| `npm run test:e2e:three-products` | **PASS** | 3/3 Playwright tests passed in 59.3 seconds. |
| `python -m astrid dev journey --tier smoke --reference generated` | **BLOCKED before journey execution** | The literal shorthand exits 2 because `--summary` is required. The corrected command is statically blocked by missing Agent Remotion dependencies. |

The two App runs are actual Linux runs from App product source base `60aa26b9529dcfa94f8ffdbd5edf42fa6c1babd2` in this worker worktree. They used the isolated Runtime fixture at `/home/user/work/wt/rt-m0-journey-runtime-env` (fixture branch `8345656`, product source base Runtime `8c1830d1ca64a3934c37611a28ffe8db7df879ea`), Agent source `/home/user/work/agent` at `e51595c68fc23d3d1734a0885c84a6511999697b`, pinned Node `v20.19.4`/npm `10.8.2`, and the explicit installed Chromium 141 executable. No package or browser installation was performed.

## App direct journey

The exact bounded invocation was:

~~~bash
cd /home/user/work/wt/rt-m0-journeys
timeout --signal=TERM --kill-after=30s 900s env PATH=/home/user/work/node-v20.19.4-linux-x64/bin:/usr/bin:/bin ASTRID_CHECKOUT=/home/user/work/agent ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-m0-journey-runtime-env ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python PYTHONPATH=/home/user/work/agent:/home/user/work/wt/rt-m0-journey-runtime-env PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome PLAYWRIGHT_OUTPUT_DIR=/tmp/timeline-direct-results XDG_CACHE_HOME=/tmp/timeline-journey-xdg/cache XDG_CONFIG_HOME=/tmp/timeline-journey-xdg/config XDG_DATA_HOME=/tmp/timeline-journey-xdg/data TMPDIR=/tmp/timeline-journey-tmp/direct NODE_OPTIONS=--max-old-space-size=4096 /home/user/work/node-v20.19.4-linux-x64/bin/npm run test:e2e:direct
~~~

`dist` was absent, so the suite's global setup built the hosted bundle successfully (`npm run build:hosted`, 1m5s) before running Playwright. The run then passed all 39 tests, including connection/readiness, Runtime-door origin and host security, App save/conflict/reload, media range/upload/download, Runtime restart, extension loading, and the direct speed table. The default Playwright revision was not used; the explicit Chromium 141 path was required and worked.

## App three-products journey

The exact separate invocation was:

~~~bash
cd /home/user/work/wt/rt-m0-journeys
timeout --signal=TERM --kill-after=30s 900s env PATH=/home/user/work/node-v20.19.4-linux-x64/bin:/usr/bin:/bin ASTRID_CHECKOUT=/home/user/work/agent ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-m0-journey-runtime-env ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python PYTHONPATH=/home/user/work/agent:/home/user/work/wt/rt-m0-journey-runtime-env PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome PLAYWRIGHT_OUTPUT_DIR=/tmp/timeline-three-products-results XDG_CACHE_HOME=/tmp/timeline-journey-xdg/cache XDG_CONFIG_HOME=/tmp/timeline-journey-xdg/config XDG_DATA_HOME=/tmp/timeline-journey-xdg/data TMPDIR=/tmp/timeline-journey-tmp/three-products NODE_OPTIONS=--max-old-space-size=4096 /home/user/work/node-v20.19.4-linux-x64/bin/npm run test:e2e:three-products
~~~

The hosted `dist` from the direct run was current, so setup skipped rebuilding. All three tests passed in 59.3 seconds: Agent task/publication adoption by the open App, the lost-acknowledgement/concurrent-edit conflict path, and Runtime restart with draft persistence and Agent endpoint follow-up. The run used the real Agent CLI and real Runtime, not a stub.

## Agent generated-reference journey

The requested shorthand was already attempted once by the reviewed preflight manager probe:

~~~bash
PYTHONPATH=/home/user/work/agent:/home/user/work/wt/rt-m0-journey-runtime-env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m astrid dev journey --tier smoke --reference generated
~~~

It exited 2 in 0.12s with `astrid dev journey: error: the following arguments are required: --summary`. No Runtime, daemon, renderer, or source-change phase started. The source registration delegates directly to `astrid.core.dev.journey`, whose parser requires `--summary`; therefore the shorthand is not a runnable command as written.

The source-supported corrected syntax is shown below against the inspected source. **Future execution must use a dedicated isolated Agent checkout with its Remotion dependencies, never `/home/user/work/agent`: the journey source-change phase temporarily edits its own module.** This block was not run:

~~~bash
cd /home/user/work/agent
env PATH=/home/user/work/node-v20.19.4-linux-x64/bin:/usr/bin:/bin PYTHONPATH=/home/user/work/agent:/home/user/work/wt/rt-m0-journey-runtime-env ASTRID_RUNTIME_FREE_DISK_FLOOR_BYTES=4294967296 /home/user/work/venv-agent/bin/python -m astrid dev journey --tier smoke --reference generated --summary /tmp/timeline-astrid-dev-journey-smoke.json
~~~

It was not launched because the first source-defined preflight failure is present:

~~~text
Remotion node_modules is missing: /home/user/work/agent/remotion/node_modules
~~~

The checked-out Agent has no `/home/user/work/agent/remotion/node_modules` or Remotion CLI. The generated reference's `ffmpeg`/`ffprobe` prerequisites are present, but the default `rendering.remotion` backend also requires the locked Remotion project and Composition/schema/theme packages. The journey's Runtime doctor still requires a usable Remotion renderer even if an ffmpeg backend is selected. No additional dependencies were installed, and no corrected journey attempt was made.

The older Agent journey documentation calls the full smoke macOS-only, but that is not an observed Linux failure here: current Runtime `_spawn_runtime` contains a non-Darwin launch path. Linux Runtime lifecycle behavior for this Agent command remains unverified until the Remotion prerequisite is supplied.

## Cleanup and next step

The hosted `dist` created in this worker worktree was removed after the runs; no product source or shared environment was modified. Playwright summaries and direct measurements remain under `/tmp/timeline-direct-results` and `/tmp/timeline-three-products-results` for inspection.

Next step: provide the locked Agent Remotion installation and a compatible Agent Remotion browser in a dedicated isolated checkout/environment, then run the corrected command once. Do not treat the Agent journey as a Linux pass based on the App results.


Manager review: report copied to the actual shared ORCH design directory (the worker wrote a local literal ORCH/ path). Test counts/commands were checked against its log; no test/source/shared-env change was made. The unused ASTRID_RUNTIME_PYTHON environment variable in the exact invocation is not an App override: its existing .venv-based lookup used the isolated Runtime fixture. These are main baseline journeys, including main's expected stale-head conflict behavior; they do not prove the new EditCommand commit/outbox path or new gates2–5. No macOS or Agent render smoke pass is claimed.
