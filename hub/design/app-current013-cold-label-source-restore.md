# Current013 retained cold-label source restoration

SOURCE RESTORED; static checks PASS; actual editing qualification UNRUN. Only two App files added: `playwright.track-label.config.ts` (7 lines) and `tests/e2e/local/track-label-command.spec.ts` (638 lines). No product, MAIN17 touchNameSheet, helper, seven-case three-products body, package, lock, wrapper or generated-client change. No central suite registered/requested and no KEEP needed.

## Sources and preserved behavior

Base App HEAD `927545cf52fdfbb273afbe7f190e00e11e5e2d70`, tree `96605f2a46c49fcf96cd12ca3679014f00ae28de`. Restore from `tl/app-m2-cold-label-spec` = `bccebd3f7732cec4c984b5a8b3158f1749eed05a`. Its four case bodies are byte-identical to reviewed `080a5743a4e38847e0cc84dd07ccada67adb27f1`; its first three are byte-identical to `d347cfff47fc6d3fc609884a38c07d12992cec3b`. Config is byte-identical to the retained branch.

| Retained case | Direct expect/expect.poll calls in body | Restored |
| --- | ---: | --- |
| Move, Unicode rename, reload, independent Agent edit, guarded UI undo | 42 | Body byte-equal |
| Same-label conflict, Keep, lost ACK, exact reload/retry, guarded undo | 46 | Body byte-equal |
| Dependent suffix retained, Keep unavailable, reload, Use latest publishes nothing | 25 | Body byte-equal |
| Cold initial head, Unicode rename, native guards/outbox, closure, reload, undo | 36 | Body byte-equal |
| Total | 149 | Four cases |

Every top-level fixture, constant, import, type and helper outside the source preflight is unchanged as TypeScript source text. Shared assertion helpers, opaque-state/readback checks and zero-legacy assertions remain intact. No skips, expected failures, changed fixture inputs or assertions removed. The existing `seedThreeProducts()` still uses reference time 15 and the original API seed; no helper delta was needed.

Restored Git blobs: config `cd2fde569dd87490bddb86ec5d1d13c19eb072c5`; spec `1ccf7cf3cb98fd8a2c858a94509630ba737acb19`. SHA-256: config `c6abca4e7ef5846050b86241b6ada9c6ff7465fa71422e729d8bd4b9cfe56b12`; spec `f838af67336ff5ff2072d4c318ea907ebb94e3a028042a058bbdf8c36fd2817e`.

## Old to current mapping

| Retained assumption | Current use / classification |
| --- | --- |
| Optional `TIMELINE_BUNDLE_AGENT_HEAD` / `TIMELINE_BUNDLE_RUNTIME_HEAD`, diagnostics saying frozen bundle | Same existing three-products environment names; now mandatory full lowercase SHAs before the original exact HEAD/cleanliness checks. Manager binds actual current sources below. No Bundle1 pin is embedded or relabelled. |
| Historical comment says initial label-only work is pending | Comment now distinguishes moved conflict setup from the retained cold-open case. No body changed. |
| Native `/v1` commit, accepted publication/revision pair, command guards, history/readback DTOs | Retained unchanged; no obsolete wire assumption requiring adaptation was found statically. Actual current013 compatibility is unverified until the real journey runs. |
| Four serial cases share worker-scoped Runtime/seed | Preserve scope and inputs. Run cold-open in its own fresh Playwright process, as the prepared executor does. Do not run all four together and call the final case cold: earlier cases mutate the shared head, while the cold case requires the original seed head. Other three can run in a separate process with `--grep-invert 'M2 cold-open'`. |
| Chrome155 prescribed by the previous executor | Superseded for EDITING by the explicit task correction: use existing Chromium141 below; frame/parity155 remains separate and is not activated. |

Literal current inputs for manager's central command:

- Agent `/home/user/work/wt/app-m3-agent013-current-pair-source`: HEAD `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, tree `75354d38c898729bac09619679f5421faba319ed`.
- Runtime/producer `/home/user/work/wt/app-m3-runtime013-producer-source`: HEAD `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Normal client/contract `0.2.13`; public Composition `0.0.12`, archive SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. No lock change.
- Editing executable `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`; manager-verified version `141.0.7390.37`; this worker's read-only SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`. No version/browser launch here.

## Commands actually run

Working directory `/home/user/work/wt/app-m3-current013-cold-label-source-restore`. Abbreviations below expand exactly to:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W=$O/workers/app-m3-current013-cold-label-source-restore
```

For successful discovery/lint, only this worker's ignored `node_modules` symlink was temporarily pointed at read-only `/tmp/app-coherent-deps12/node_modules`, then restored to `/home/user/work/app/node_modules`. No shared dependency, venv, runtime or cache file was modified. Playwright transformation/output paths were private under `$W/notes`.

```sh
env PWTEST_CACHE_DIR=$W/notes/playwright-cache PLAYWRIGHT_OUTPUT_DIR=$W/notes/discovery-output node node_modules/playwright/cli.js test --config playwright.track-label.config.ts --list
env PWTEST_CACHE_DIR=$W/notes/playwright-cache PLAYWRIGHT_OUTPUT_DIR=$W/notes/discovery-output node node_modules/playwright/cli.js test --config playwright.track-label.config.ts --list --grep 'M2 cold-open'
env PWTEST_CACHE_DIR=$W/notes/playwright-cache PLAYWRIGHT_OUTPUT_DIR=$W/notes/discovery-output node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --list
node node_modules/eslint/bin/eslint.js playwright.track-label.config.ts tests/e2e/local/track-label-command.spec.ts --no-cache --max-warnings 0
node "$W/notes/preserve-sources.cjs"
git diff --check
sha256sum /opt/pw-browsers/chromium-1194/chrome-linux/chrome
```

Results respectively: PASS exit0, 4 cases; PASS exit0, 1 cold case; PASS exit0, 7 original cases; PASS exit0, zero lint diagnostics; PASS exit0, four complete bodies/149 expectation calls and all fixture/helper source preserved, plus eight current support/config/wrapper files unchanged; PASS exit0; hash above. Static script/result retained at `$W/notes/preserve-sources.cjs` and `preservation-result.json`.

Initial discovery using the private12 CLI while the App still resolved the other physical Playwright copy failed with `test.describe.configure()` / duplicate-instance error (0 discovered). Corrected only the worker-local ignored link, then discovery passed. The first static comparison attempt hit sandbox `spawnSync git EPERM` with default piped stdin; using `stdio: ['ignore', 'pipe', 'pipe']` fixed the audit subprocess. Neither failure changed product/tests. Initial scoped lint via the absolute private12 executable also passed.

## Ready child command and actual remaining work

UNRUN child command for a manager-prepared private12 central snapshot; private paths below belong to this worker and are literal runtime inputs. For the other three cases use a separate process with `--grep-invert` instead of `--grep`.

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock env \
 ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source \
 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source \
 ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
 TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 \
 TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
 PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
 PWTEST_CACHE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-cold-label-source-restore/notes/central-cold-cache \
 PLAYWRIGHT_OUTPUT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-cold-label-source-restore/notes/central-cold-output \
 PYTHONDONTWRITEBYTECODE=1 NODE_OPTIONS=--max-old-space-size=4096 \
 node node_modules/playwright/cli.js test --config playwright.track-label.config.ts --grep 'M2 cold-open'
```

This is the ready child invocation, not a registered central suite or qualification claim. Manager must first compose the parallel refused-unmount fix and these two source files, obtain the required final-root review/checks, then bind the NEW App TREE and actual literal inputs into a NEW named central command/cache identity. Reuse existing `checkCurrent013Sources(readCurrent013Inputs())` before/after and producer/public12 dependency verification; keep private transformation/build/tool caches. The old executor's snapshot helper hardcodes tree96605f2 and its runner hardcodes the absent Chrome155/hash, so that old registered command must not be requested unchanged. Rebind those inputs and verify Chromium141/hash; do not relax source/package checks. Requester environment is not forwarded by the service.

Actual M1/new Gate5, cold-label and restore acceptance remain UNRUN, Test IDs NONE. No browser, hosted build, localhost/socket, tsc, full suite, install, render/frame/audio parity or frame grant was run/requested. This bounded restoration is complete; overall paired qualification still awaits final composition/review and central execution by the manager. No source-restoration blocker remains.
