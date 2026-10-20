# Final current013 cold-label composition and project typecheck

PASS: composed only the retained cold-label config/spec onto the fixed refused-unmount root. Four retained cases/149 expectations and all seven M1/Gate-5 cases are preserved. Narrow fixed-label controls: **248 passed across six files**. Actual project TypeScript check: **one invocation, exit 0, zero diagnostics**. Actual browser/paired acceptance remains UNRUN, pending the manager's gate and independent approval.

## Exact source

| Input | Commit | Tree |
| --- | --- | --- |
| Fixed refused-unmount App base / current HEAD | `2b75c7e684afe44283ce0d5fe31c72fc9da2b7c6` | `098023fc386ebd1ab949b79eda44e0bb2b4bb502` |
| Cold-label restore source | `9208b613c18b07fb00013d2b0d84fe05089804a9` | `0d3077210df4a4a6d88d5823874791a3eb85f4a3` |
| Restore comparison base | `927545cf52fdfbb273afbe7f190e00e11e5e2d70` | `96605f2a46c49fcf96cd12ca3679014f00ae28de` |
| Agent keeper `/home/user/work/wt/app-m3-agent013-current-pair-source` | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` | `75354d38c898729bac09619679f5421faba319ed` |
| Runtime/producer keeper `/home/user/work/wt/app-m3-runtime013-producer-source` | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` |

**Final composed App source tree: `b2c510ca8893c4d3c238fb042f9ec7e7252edbc0`.** Computed using Git's blob/tree encoding without writing the index or object store; the same computation reproduces the base tree. The new commit SHA is assigned by the harness after this worker exits; the HEAD above is its parent, not a claimed final commit.

The source restore delta against 927 contains exactly these two additions, copied byte-for-byte:

| File | Lines | Git blob | SHA-256 |
| --- | ---: | --- | --- |
| `playwright.track-label.config.ts` | 7 | `cd2fde569dd87490bddb86ec5d1d13c19eb072c5` | `c6abca4e7ef5846050b86241b6ada9c6ff7465fa71422e729d8bd4b9cfe56b12` |
| `tests/e2e/local/track-label-command.spec.ts` | 638 | `1ccf7cf3cb98fd8a2c858a94509630ba737acb19` | `f838af67336ff5ff2072d4c318ea907ebb94e3a028042a058bbdf8c36fd2817e` |

All **5,832 existing tracked files**, their modes and symlink contents remain exact to the fixed base. This preserves MAIN17 touch editing, the fixed owner-scoped draft lifetime, normal013 client/pins, public12, server/proxy, wrapper and every existing helper/journey. MAIN17 `17e46de99b7cef52fe494de1703a9865a8d4be24` is an ancestor. No product or source overlay was used. No assertion, fixture input, helper body, skip or expected-failure marker was changed.

Read the plan plus `app-current013-cold-label-source-restore.md` and `app-root-label-refused-unmount-fix.md` before composing. The retained-body audit also reproduces reviewed lineage `bccebd3f7732cec4c984b5a8b3158f1749eed05a`, `080a5743a4e38847e0cc84dd07ccada67adb27f1`, and the first three bodies from `d347cfff47fc6d3fc609884a38c07d12992cec3b`. Expectation counts remain **42 + 46 + 25 + 36 = 149**; every top-level fixture/constant/helper remains intact.

## Exact checks and results

All commands below ran in `/home/user/work/wt/app-m3-current013-final-cold-compose-typecheck`. Abbreviations:

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W=$O/workers/app-m3-current013-final-cold-compose-typecheck
N=$W/notes
```

Collection only; each invocation exited 0. Results in order: **4 cases; 1 cold case; 3 other label cases; 7 M1/Gate-5 cases**. `--list` did not execute global setup, build, fixtures or browsers.

```sh
env PWTEST_CACHE_DIR="$N/playwright-cache" PLAYWRIGHT_OUTPUT_DIR="$N/discovery-output" node node_modules/playwright/cli.js test --config playwright.track-label.config.ts --list
env PWTEST_CACHE_DIR="$N/playwright-cache" PLAYWRIGHT_OUTPUT_DIR="$N/discovery-output" node node_modules/playwright/cli.js test --config playwright.track-label.config.ts --list --grep 'M2 cold-open'
env PWTEST_CACHE_DIR="$N/playwright-cache" PLAYWRIGHT_OUTPUT_DIR="$N/discovery-output" node node_modules/playwright/cli.js test --config playwright.track-label.config.ts --list --grep-invert 'M2 cold-open'
env PWTEST_CACHE_DIR="$N/playwright-cache" PLAYWRIGHT_OUTPUT_DIR="$N/discovery-output" node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --list
```

Narrow fixed-label controls, exit 0, **6 files / 248 passed / 0 failed / 0 skipped**, 24.76 seconds. Breakdown: label command 43; management 28; Ops label 24; gesture 8; capture 73; commit session 72. These are jsdom controls, including retained desktop/phone/tablet refused-teardown and owner-isolation tests. Log/JSON: `notes/fixed-label-controls.log` and `notes/fixed-label-controls.json`.

```sh
env TMPDIR="$N/tmp" node --require "$O/managers/app/notes/snapshot-vitest-runner.cjs" \
  node_modules/vitest/vitest.mjs run --config "$N/vitest.config.ts" \
  --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx \
  src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts \
  src/tools/video-editor/commands/trackLabelGesture.test.ts \
  src/tools/video-editor/commands/trackLabelCapture.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  --reporter=default --reporter=json --outputFile.json="$N/fixed-label-controls.json"
```

Other checks, all exit 0:

```sh
python3 -B "$N/source-audit.py"
node "$N/preserve-sources.cjs"
node --experimental-import-meta-resolve "$N/dependencies.mjs"
python3 -B "$N/dependency-content.py"
node node_modules/eslint/bin/eslint.js playwright.track-label.config.ts tests/e2e/local/track-label-command.spec.ts --no-cache --max-warnings 0
node scripts/quality/check-known-failures.mjs
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m3-runtime013-producer-source
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /home/user/work/wt/app-m3-agent013-current-pair-source/scripts/vendor_lock.py check /home/user/work/wt/app-m3-agent013-current-pair-source/runtime.lock.json --producer /home/user/work/wt/app-m3-runtime013-producer-source
git diff --check
sha256sum /opt/pw-browsers/chromium-1194/chrome-linux/chrome
```

Lint: zero diagnostics. Known-failures: 3 existing authorized markers / 0 forbidden. Normal vendor checks passed for **13 App / 15 Agent** files against the exact producer; source audits additionally checked file digests and byte equality against that producer. Runtime's 75-artifact manifest and both generated metadata digests match. Both keepers remained clean with every tracked byte verified. The existing wrapper's complete clean-App preflight must run after the harness commit; it cannot accept this intentionally uncommitted composition, and was not weakened or replaced in product source.

## Single actual project TypeScript check

Executed once by `bash "$N/run-tsc.sh"`; exact child command:

```sh
env npm_config_cache="$N/npm-cache" npm_config_offline=true npm_config_update_notifier=false \
  flock -w600 /home/user/work/.app-tsc.lock \
  env NODE_OPTIONS=--max-old-space-size=4096 \
  npm exec tsc -- --noEmit -p tsconfig.app.json \
  > "$N/tsc-diagnostics.txt" 2>&1
```

Start **2026-10-20T12:55:27Z**; end **2026-10-20T12:56:21Z**; elapsed **54 seconds**, including lock/npm overhead. **Exit 0. Full combined diagnostics: 0 bytes / 0 lines.** Retained `tsc-start.txt`, `tsc-end.txt`, `tsc-exit.txt`, `tsc-diagnostics.txt` and `npm-debug.log` contain the complete result; npm confirms the exact argv and exit 0. No compiler rerun, suppression, configuration adjustment or product fix occurred.

Used the existing project `tsconfig.app.json`: strict `src` checking with its existing test exclusions and `skipLibCheck`. Root `tsconfig.json` (`files: []`) was not substituted. This check qualifies the inherited product fix on this final source tree; the earlier 927 pass was not reused as evidence.

Only this worktree's ignored `node_modules` symlink was temporarily redirected to the existing **read-only `/tmp/app-coherent-deps12/node_modules`**. No dependency was installed, extracted, patched or linked inside that dependency tree. Node **22.22.0**, npm **10.9.4**, TypeScript **5.9.3**; compiler path `/tmp/app-coherent-deps12/node_modules/typescript/bin/tsc`, SHA-256 `8d5fa5bd883fec0979fc2004f1fe1d99aef40570155d550eadc0b03b55513bf0`.

Public Composition **0.0.12**, archive SHA-256 **`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`**: all **77** installed files match the immutable archive; package/lock specification and SHA-512 integrity match. App and Composition resolve the same React/React DOM **18.3.1**, Remotion/Player/Media/Layout Utils/Three **4.0.509**, and Three **0.185.1** peers. Full ambient/compiler/package paths are in `dependencies-before.json` / `dependencies-after.json`.

Source, dependency-resolution and dependency-content snapshots were taken before controls, immediately before tsc, and after tsc. Each corresponding pair compared byte-equal using `cmp` (exit 0); retained-body audits before/after also compare equal. The full reachable dependency census hashes **32,509 unique files / 452,551,865 bytes**, with **39 symlinks**, modes and link targets. All three census hashes are **`0bb604c9ccb61b5d11d0537c41dd84fab38745742bd45c9d013afdc67cf0a680`**. This includes the borrowed package links; no shared cache/dependency change was observed. Scripts and every snapshot are retained under `notes/`.

## Handoff

No blocker or settled-decision deviation. Cold-open requires its **own fresh Playwright process** using `--grep 'M2 cold-open'`; the other three label cases require a separate process with `--grep-invert 'M2 cold-open'`. The worker-scoped Runtime/seed is shared, so running all four together does not establish a cold initial head. Bodies, fixtures and scope were preserved; only collection was run here.

Manager next: obtain independent fix approval, bind a new central gate/cache identity to final App tree **`b2c510ca8893c4d3c238fb042f9ec7e7252edbc0`** and the exact keeper pair above, run the existing source/producer/public12 preflight before and after, and execute the actual required journeys. Use the preinstalled editing Chromium141 executable `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, SHA-256 **`85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`**. Its 141.0.7390.37 version comes from the prior manager verification; this worker checked its file hash without launching it. Rebind the old executor's hardcoded App tree/browser rather than requesting that stale command unchanged. Actual gate remains pending independent **APPROVE** and the manager's actual **PASS**.

No full suite, install, build, browser, localhost/live socket, central test-service request, actual Runtime acceptance, frame/audio parity, owner-film or macOS qualification ran. Type compatibility and jsdom controls do not establish actual cross-product acceptance.

Restored the local ignored dependency symlink to `/home/user/work/app/node_modules` after verification. Removed this worker's private transformation/Vite/npm/temp caches after retaining logs; no build output or temporary file remains in the worktree. The requested local design report is ignored by existing policy; identical copies are saved in ORCH/design and worker `report.md`. Supplied `commit-msg`, `DONE` and `KEEP`; no commit, merge, checkout, push, ref mutation or integration-worktree edit was performed.
