# Chromium 141 central launch diagnosis

**Launch blocker isolated to the long temporary path.** On the same central host, full Chromium 141 failed with the reconstructed long TMPDIR, then opened a real page and passed JavaScript/DOM assertions with only TMPDIR shortened. Keeping the long XDG paths did not prevent success. No product/test/config source changed; the frozen App b1 / Agent d874 / Runtime 2c4 tuple stays unchanged.

## Central execution and bounded results

TestID: `app-m3-chromium141-launch-diagnose-chromium141-launch-diagnose-integration-1020133523-30467`. Named suite `chromium141-launch-diagnose-integration`: **PASS, exit 0, 10 seconds, fresh execution**. This means a usable launch configuration was found; the deliberately failing baseline is retained, not hidden. Exactly **4 launch attempts: 1 expected diagnostic reproduction / 3 DOM passes**; no retries. Two `--version` identity queries are additional non-launch checks.

[summary](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-chromium141-launch-diagnose-chromium141-launch-diagnose-integration-1020133523-30467/summary) · [log.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-chromium141-launch-diagnose-chromium141-launch-diagnose-integration-1020133523-30467/log.txt) · [snap](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-chromium141-launch-diagnose-chromium141-launch-diagnose-integration-1020133523-30467/snap) · [suite-line.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/suite-line.txt) · [matrix.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/results/matrix.json)

| Case | TMPDIR / profile bytes | XDG cache + config | Browser exit | Page + JS + DOM |
| --- | --- | --- | --- | --- |
| Full Chrome, long baseline | 306 / 344 | long | SIGTRAP, no exit code | FAIL before page |
| Full Chrome, short temp only | 23 / 61 | same long paths | 0 | PASS |
| Full Chrome, short all | 23 / 61 | short | 0 | PASS |
| Matching headless shell, short all | 23 / 61 | short | 0 | PASS |

Each child used the same Playwright 1.60.0 implementation, `chromium.launch({executablePath, headless: true, timeout: 15000})`, default normal launch arguments, no `ignoreDefaultArgs`, no extra browser switches. Default Playwright `--no-sandbox` remains as installed. The shell comparison ran only after the full-Chrome baseline failed. It invokes installed `headless_shell.real` directly to avoid the installed shell wrapper's three additional font/color flags; no browser was modified or substituted into a product journey.

Each green case created a browser page, navigated to inline data HTML, executed an inline script that wrote `42` into `<main>`, then evaluated and asserted title `Timeline launch probe`, DOM text `42`, and JavaScript `6 * 7 === 42`. Browser version was `141.0.7390.37`; each closed cleanly. This is actual page/DOM evidence, beyond version/launch detection.

Full Chrome: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, SHA256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`.
Matching shell: `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell.real`, SHA256 `6c82af1bb96955970f0ff50884bcbd75f200222414dc136076ada667bf4628d1`, same version.

## Exact environment and retained stderr

The literal suite registration explicitly binds the private root `/tmp/tla141-a3c7141`, browser SHA, all three runner source hashes, browser install path and no-download flag. It uses the existing central request-test service and browser lock. No dependency installation, build, Vitest/Vite invocation, localhost server or worker-local browser ran.

Playwright comes read-only from `/tmp/app-coherent-deps12/node_modules/playwright-core` (the original failed gate's installation). Its `lib/coreBundle.js` SHA256 is `f74353fcb8e406756a70a6af0dfc4a5069acd577e35ec9d923ccf36ac009c2f5`, equal to the App shared installation.

The own long root is **302 bytes**, exactly the failed gate's run-root length, with `TMPDIR=<long>/tmp`, `XDG_CACHE_HOME=<long>/xdg-cache`, `XDG_CONFIG_HOME=<long>/xdg-config`. This recreates path length in this worker's own directory; it does not write the prior worker's files. Short values are `/tmp/tla141-a3c7141/tmp`, `/tmp/tla141-a3c7141/xdg-cache`, `/tmp/tla141-a3c7141/xdg-config`. The middle row changes only TMPDIR between browser child environments. Profile names are generated normally by Playwright and recorded verbatim in [matrix.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/results/matrix.json).

Explicit suite environment: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`, `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`, `PYTHONDONTWRITEBYTECODE=1`, `NODE_OPTIONS=--max-old-space-size=4096`, `TSX_DISABLE_CACHE=1`, `ASTRID_PUBLIC_CHECKOUT` and `ASTRID_APP_DIRECT_DIST` unset. Child environment adds `DEBUG=pw:browser`, `PROBE_BROWSER=<exact executable>`, `npm_config_cache=/tmp/tla141-a3c7141/npm-cache`, `PWTEST_CACHE_DIR=/tmp/tla141-a3c7141/playwright-cache` plus the row's TMPDIR/XDG values. No HOME/CODEX_HOME reassignment. Observed inherited HOME `/root`, CODEX_HOME absent; LD_LIBRARY_PATH, LD_PRELOAD, DISPLAY, WAYLAND_DISPLAY, DBUS_SESSION_BUS_ADDRESS, XDG_RUNTIME_DIR absent. Relevant inherited environment, PATH, exact source/cache identity, kernel, UID and process limits are retained in [metadata.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/results/metadata.json). Linux kernel `6.18.44-fc-v139`, Node `v22.22.0`, UID 0, 4 CPUs; fd limit 20,000, stack 8 MiB, core size 0.

Original gate TestID: `app-m3-current013-corrected-public-browser-gate-e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020132515-1968`; historical normal hosted build PASS, **1 browser-fixture failure / 6 unrun / 0 passes**. Its original log remains [log.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-current013-corrected-public-browser-gate-e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020132515-1968/log.txt); the initial error was also copied unchanged into [initial-browser-failure.txt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/initial-browser-failure.txt).

The new baseline reproduces the same SIGTRAP and crashpad missing `scaling_cur_freq` / `scaling_max_freq` lines. All stderr and exact launch argv/exit/profile paths are retained per row:

- `chrome-long-long`: [chrome-long-long.stderr](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/results/chrome-long-long.stderr), [chrome-long-long.stdout](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/results/chrome-long-long.stdout).
- `chrome-short-long`: [chrome-short-long.stderr](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/results/chrome-short-long.stderr), [chrome-short-long.stdout](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/results/chrome-short-long.stdout).
- `chrome-short-short`: [chrome-short-short.stderr](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/results/chrome-short-short.stderr), [chrome-short-short.stdout](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/results/chrome-short-short.stdout).
- `shell-short-short`: [shell-short-short.stderr](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/results/shell-short-short.stderr), [shell-short-short.stdout](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/results/shell-short-short.stdout).

The bounded comparison supports the actionable conclusion that shortening TMPDIR resolves this launch failure on this host. An overly long Unix socket path is a plausible mechanism, **not proven** by these logs: no fatal socket error or native stack trace identifies the failing internal call. Crashpad's missing cpufreq files do not establish causation. Full Chrome succeeds under the unchanged host environment once TMPDIR is short, so a host-wide inability to run installed Chrome is disproven by this probe. Exact failure threshold and flakiness were not measured.

## Commands and validation

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W="$O/workers/app-m3-chromium141-launch-diagnose"
node --check "$W/notes/launch-child.cjs"
node --check "$W/notes/matrix.cjs"
bash -n "$W/notes/run-matrix.sh"
"$O/bin/request-test" app-m3-chromium141-launch-diagnose chromium141-launch-diagnose-integration > "$W/notes/result-dir.txt"
"$O/bin/wait-test" app-m3-chromium141-launch-diagnose-chromium141-launch-diagnose-integration-1020133523-30467 1
# Same request read after completion:
"$O/bin/wait-test" app-m3-chromium141-launch-diagnose-chromium141-launch-diagnose-integration-1020133523-30467 0
git diff --check
git status --short
```

Syntax and git checks exit 0; tracked worktree diff/status empty. Central waiter reports exit 0. No full suite requested. Probe source lives only in this worker's notes ([launch-child.cjs](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/launch-child.cjs), [matrix.cjs](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/matrix.cjs), [run-matrix.sh](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-chromium141-launch-diagnose/notes/run-matrix.sh)); only an appended named-suite entry was written to the shared central allow-list. Existing suite registrations/tools remain intact. Shared dependencies, venvs, runtimes and their caches were not written. All created long/short temporary roots were removed after the matrix; only requested diagnostic artifacts remain. No test remains running; KEEP removed. Commit message and DONE written.

## Decision and next step

Use the **same full Chrome 141 executable/hash** for the next authorized central gate; provision an exclusive short own root with literal TMPDIR (and preferably short own XDG/npm/Playwright cache paths) inside its runner/suite, not requester exports. Record the short path in its cache identity. No browser install, system change, frame grant or shell substitution is needed. Keep all existing authorization/origin/certificate/HTTP cases and UI assertions unchanged. Have the orchestrator schedule that gate on the frozen tuple after the runner-only environment change. This worker stops after the requested launch diagnosis.

Unrun: corrected seven-case App journey, three regular labels and separate fresh cold-open, M1/Gate5, native IndexedDB, renderer/frame/audio parity, full App suite/build, and macOS. The old hosted-build pass is historical; no acceptance claim is made from this launch smoke. No blocker remains for this diagnostic task; actual App qualification still awaits the central journey.
