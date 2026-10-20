# Corrected public-source current013 App browser gate

**BLOCKED: Chromium 141 launch failure; actual UI remains unqualified.** The corrected normal hosted build **PASSed** on the approved App tree. The central seven-case lane then returned **exit 1 / 95 seconds**, with **1 browser-fixture failure / 6 cases not run / 0 passes**. Chromium exited with **SIGTRAP before any page opened**. Source, normal vendor metadata, public bundle, Composition installation and shared Vite-cache boundary checks all passed and remained byte-equal. Stopped on this new actual error; did not request either label lane or retry browser execution.

Read PLAN first and applied the manager's [public-source correction](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-browser-public-source-correction.md). The two preceding missing-public-catalog build stops were environment failures with zero browser cases, not product or gesture failures. The same final [APPROVE + project tsc PASS review](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-final-live-policy-review-typecheck.md) applies; no old synthetic-UI HOLD is asserted. That review's 73 targeted passes and project typecheck are historical evidence, not tests rerun by this worker.

## Exact source and environment

| Input | Read-only checkout | HEAD | TREE |
| --- | --- | --- | --- |
| App | `/home/user/work/wt/app-m3-current013-corrected-public-browser-gate` | `b1ef4b9b910ba72375c34cf319692f90d22edc25` | `8d8a10b057ed31fed69517e18a23b8ec3811447a` |
| Agent/provider/CLI | `/home/user/work/wt/app-m3-agent013-current-pair-source` | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` | `75354d38c898729bac09619679f5421faba319ed` |
| Runtime/server/producer | `/home/user/work/wt/app-m3-runtime013-producer-source` | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` |

All original checkouts were clean and exact at both boundaries. The central service's generated snapshot commit was `65b9ee22194096b4ac1a885926a4fb7a3a536904`; its tree was exactly the asserted App tree. No product, test, assertion, config, package, lock, generated client or pin changed.

`ASTRID_CHECKOUT` stays the exact Agent keeper above. **`ASTRID_PUBLIC_CHECKOUT` is explicitly UNSET** in the literal suite (`env -u`) and runner, so the unchanged resolver uses tracked `vendor/astrid-browser/astrid`. `ASTRID_APP_DIRECT_DIST` is also explicitly absent. No alias, copied code, public catalog substitution, fake provider, source overlay or stale distribution was supplied. The central snapshot started without `dist`; unchanged global setup invoked the normal `npm run build:hosted`, which built 5,567 modules in **1m 6s**.

The normal `node scripts/build/verify-astrid-vendor-sources.mjs` passed before and after: **65 pinned build-input files, 155 browser provenance files, 20 public-host imports**. The extra read-only check compares all **222 tracked files** under both vendor roots against committed HEAD bytes, including both manifests and provenance. Its canonical sorted path/hash map SHA256 is `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`, literally included in the new suite/cache identity. Browser provenance records Astrid commit `680d1aa4f1f9576d65a603472f1dd7fc0ae9ccd1`, tree `07ce61f24ec38a1a60c4a981b6bd666f4971bd67`. This is the tracked public demo/build input, separate from the exact current Agent provider/CLI input.

| Public input | SHA256 |
| --- | --- |
| `vendor/astrid-browser/provenance.json` | `5b0924452cbb51d74be04f0a4a6ac390c462d77a11bebb5274836a4e66468f82` |
| Browser `public-catalog.ts` | `7ec1e6b7f2e445b02f1714929933a8044feb16cdc2f4a268ea79f91f2a57a281` |
| `vendor/astrid-build-inputs/manifest.json` | `5cedfb8b544b73dc0db769e45ba19740de61b5296aca107fbb550185f58ee2df` |

Normal contract/client remains **0.2.13**, schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`, artifact `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`, component manifest `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`. Both normal producer-backed vendor checks passed at both boundaries. The prepared audit also checked **all 75 Runtime artifacts** against manifest hashes and committed bytes, plus **13 App / 15 Agent** locked destinations against producer bytes.

Public Composition **0.0.12** archive SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`: both consumer archives match; all **77 unique safe regular members**, exact installed file set and bytes match the read-only private12 installation. React/ReactDOM **18.3.1**; Remotion/Player/Media/Layout Utils/Three **4.0.509**; Vite **5.4.21**, Rollup **4.60.2**, Playwright **1.60.0**. Full package identities are in [dependency-versions.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-corrected-public-browser-gate/notes/dependency-versions.json).

Only this worker's central `.test-*` snapshot got its own module root/scopes and `.vite` / `.vite-temp`, linking read-only package contents from `/tmp/app-coherent-deps12/node_modules`. npm, Playwright, XDG and temp caches were private beneath this worker's notes and removed after the run. Shared node_modules/venvs/runtimes were not written. Existing `.vite` / `.vite-temp` records under private12 and App shared dependencies compare equal before/after; this is a scoped cache audit, not a full shared-dependency census.

Editing browser was the required preinstalled `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, **141.0.7390.37**, SHA256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`. No install, browser substitution or Chromium155/frame grant.

## Exact central requests and results

One new suite was registered: **`e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration`**. Its [complete literal registration](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-corrected-public-browser-gate/notes/suite-line.txt) binds all full source SHAs/trees, source paths, venv entrypoints, public-source hash, browser hash, review hash and all six helper hashes. The central service does not rely on requester exports. Existing suites and central tools were preserved. Reused the final paired notes runner; changes only bind this worker, unset the corrected environment, add normal public-source verification and handle the service's generated snapshot commit correctly.

Commands (from the assigned App worktree; `O` is the literal ORCH path above):

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W="$O/workers/app-m3-current013-corrected-public-browser-gate"
S=e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration
"$O/bin/request-test" app-m3-current013-corrected-public-browser-gate "$S" --files three-products > "$W/notes/three-products-result-dir.txt"
"$O/bin/wait-test" app-m3-current013-corrected-public-browser-gate-e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020132515-1968 1
# The waiter returned 124 while running; resumed the SAME completed result:
"$O/bin/wait-test" app-m3-current013-corrected-public-browser-gate-e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020132515-1968 0
```

**Actual execution TestID:** `app-m3-current013-corrected-public-browser-gate-e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020132515-1968`. **Fresh FAIL / exit 1 / 95s**, no cached result. [Full log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-current013-corrected-public-browser-gate-e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020132515-1968/log.txt), [summary](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-current013-corrected-public-browser-gate-e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020132515-1968/summary), [snapshot/cache key](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-current013-corrected-public-browser-gate-e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020132515-1968/snap), [browser error excerpt](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-corrected-public-browser-gate/notes/actual-browser-failure.txt). Cache key `61b9fcc16b2dc251e2455abdf2ea0e0c`.

Exact unchanged child path:

```sh
node scripts/testing/current013-integration.mjs
npm run test:e2e:three-products
# package script:
playwright test --config playwright.three-products.config.ts
# unchanged global setup:
npm run build:hosted
```

The build passed. Playwright selected all seven existing cases with one worker. The first case, `three-products.spec.ts:341`, failed in worker browser setup at `tests/e2e/local/support/app.ts:43`:

```text
Error: browserType.launch: Target page, context or browser has been closed
<launched> pid=17120
open /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq: No such file or directory (2)
open /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq: No such file or directory (2)
<process did exit: exitCode=null, signal=SIGTRAP>
1 failed
6 did not run
```

The missing sysfs files were printed by crashpad; the log does not establish the cause of SIGTRAP. No page opened or UI journey assertions ran. M1 real gesture, after-ACK Gate5, dependency conflict and mixed-editing cases did not run. No HTTP refusal or product behavior failure is established by this launch error. Trace/error context are retained under [browser artifacts](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-corrected-public-browser-gate/notes/runs/.test-app-m3-current013-corrected-public-browser-gate-e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020132515-1968-three-products/browser-artifacts).

**Earlier notes-runner preflight failure, disclosed:** the first request, `app-m3-current013-corrected-public-browser-gate-e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020132428-24962`, failed exit 1 in **3s**, before any build/browser case. I incorrectly compared the service's generated snapshot HEAD with the original App HEAD in the copied audit. Fixed only that notes audit to check the original checkout's frozen HEAD (the unchanged wrapper checks snapshot tree/clean bytes), updated its helper hash in this worker's suite registration, then made the single actual execution above. [Original summary](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-current013-corrected-public-browser-gate-e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020132428-24962/summary), [prior literal registration](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-corrected-public-browser-gate/notes/suite-line-before-audit-repair.txt). This was one bounded harness repair, not an assertion change or retry of a product error. No further request followed the actual SIGTRAP failure.

**Regular labels (3) and separate fresh cold-open (1): UNRUN / no TestIDs.** Per the stop-on-new-error instruction, did not submit these dependent stages. Prepared argv remains:

```sh
npm exec -- playwright test --config playwright.track-label.config.ts --grep-invert 'M2 cold-open'
npm exec -- playwright test --config playwright.track-label.config.ts --grep 'M2 cold-open'
```

All original tests and expectations are unchanged; “6 did not run” is Playwright's serial failure consequence, not edited skip/xfail markers.

## Boundary evidence and historical restore scope

The original wrapper's source/normal-vendor guards passed before and after the failure; the reused runner independently did the same. Central `audit-start/end`, `source-start/end` and `cache-start/end` each compare byte-equal, including normal public-source verification. [Boundary comparison hashes](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-corrected-public-browser-gate/notes/boundary-comparisons.json), [run boundary records](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-corrected-public-browser-gate/notes/runs/.test-app-m3-current013-corrected-public-browser-gate-e2e-corrected-public-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020132515-1968-three-products). Local read-only preflight also passed and its repaired start/end output compares equal.

Exact local checks, all exit 0:

```sh
bash -n "$W/notes/run-lane.sh"
node --check "$W/notes/run-selected.mjs"
bash "$W/notes/read-only-preflight.sh"
git diff --check
git status --short
```

The preflight script's literal command is retained; it checks the final review hash, invokes the normal public verifier, reads all tracked public bundle bytes, audits the 75 producer artifacts and both locks, and verifies the private12 install without modifying the worker's shared node_modules link. No worker-local socket, browser or build command ran.

The already-passed restore lane is cited **historically only**, not rerun: TestID `app-m3-current013-restore-consumer-gate-restore-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-tb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-integration-1020130731-30085`, **2 passed / exit 0**, on earlier App cee68/b2 with the same exact Agent/Runtime pair. [Original restore report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-current013-restore-consumer-gate.md). Compared **11 restore test/config/provider/client/harness/ShotEditor inputs** byte-for-byte from that App commit to this final App; all equal, recorded in [restore-inputs-byte-equal.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-corrected-public-browser-gate/notes/restore-inputs-byte-equal.json). This preserves the limited HTTP restore evidence; it does not qualify final browser behavior.

## Decisions, limits and next steps

No settled decision changed; no evidence calls for a product or tuple change. Corrected the public-source environment exactly as directed. Stopped after the concrete central launch failure rather than broad retry, browser/source/provider substitution or weakening tests. No full suite requested.

Manager next step: diagnose the central preinstalled141 launch/SIGTRAP using the retained log/trace, then authorize a bounded central rerun on the same frozen tuple and tracked public bundle. Once the seven cases pass, evaluate the three-label lane, then a separate fresh cold-open process. Root merge remains manager-owned after actual acceptance evidence; writer retirements remain later.

Unverified: all actual UI acceptance on this tree, ordinary labels/cold-open, actual UI ACK/reload/undo, full suite, frame/PCM parity, owner-film and macOS qualification. Existing independent review/typecheck APPROVE+PASS remains valid within its scope.

Artifacts saved in local ignored `design/app-current013-corrected-public-browser-gate.md`, ORCH design and worker report.md. Conventional commit message supplied. **BLOCKED**, no DONE; **no test remains running**, so KEEP removed. Worktree tracked diff is empty; its original node_modules symlink remains `/home/user/work/app/node_modules`; no build/temp output remains there. No git commit/merge/rebase/checkout/push/ref operation.
