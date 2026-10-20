# current013 core browser candidate: build contract blocked

One authorized central attempt completed on 2026-10-20. **FAIL, exit 1, 40 seconds.** The normal fresh hosted build failed before any browser case could execute. This is a frozen App/Agent build-source contract failure, not App gesture proof or an observed gesture regression. No retry was submitted.

TestID: `app-m3-current013-core-browser-candidate-e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration-1020131434-28008`.

- [Central summary](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-current013-core-browser-candidate-e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration-1020131434-28008/summary)
- [Unmodified first-failure log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-current013-core-browser-candidate-e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration-1020131434-28008/log.txt)
- [Source snapshot and service cache key](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-current013-core-browser-candidate-e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration-1020131434-28008/snap)
- [Literal registered command](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/suite-line.txt)
- [Cache identity](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/cache-identity.txt)

## Exact source and dependencies

| Input | Commit | Tree | Path |
| --- | --- | --- | --- |
| App candidate | `cee68b807017efc8669c7d75318cf51aa70ec855` | `b2c510ca8893c4d3c238fb042f9ec7e7252edbc0` | `/home/user/work/wt/app-m3-current013-core-browser-candidate` |
| Agent keeper | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` | `75354d38c898729bac09619679f5421faba319ed` | `/home/user/work/wt/app-m3-agent013-current-pair-source` |
| Runtime and normal producer keeper | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` | `/home/user/work/wt/app-m3-runtime013-producer-source` |

The service snapshot tree was exactly the requested App tree above; its synthetic test-snapshot commit is not a new App qualification target. Original App HEAD and source cleanliness were independently checked before and after the run. There were no product, test or tracked-wrapper changes.

Both `ASTRID_CHECKOUT` and `ASTRID_PUBLIC_CHECKOUT` were the same exact Agent keeper above. Agent Python was `/home/user/work/venv-agent/bin/python`; Runtime Python was `/home/user/work/venv-runtime/bin/python`. These entry paths preserve the venv prefix rather than resolving their interpreter symlinks to `/usr/bin/python3`. No venv changes or installs occurred; `PYTHONDONTWRITEBYTECODE=1` was set.

Runtime normal locks and metadata matched 0.2.13: producer version `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`, schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`, component manifest `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`. All 75 producer artifacts were verified against their manifest and frozen git blobs, and App's 13 / Agent's 15 normal vendored files matched the producer. Both normal vendor-lock commands passed at start and after failure.

Composition was the immutable `banodoco-timeline-composition-0.0.12.tgz`, SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. Both source archives passed the existing guards. Every one of the installed package's 77 files matched App's archive, with no extra package files. The overlay linked `/tmp/app-coherent-deps12/node_modules` read-only packages; all five declared peers matched (React and React DOM 18.3.1, Remotion, layout-utils and media 4.0.509), plus player and three 4.0.509. Actual build tool: Vite 5.4.21.

Existing Chromium **141.0.7390.37** was checked centrally at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, SHA256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`. Only its version check ran: the build failure prevented browser launch.

## Commands and results

Registration (one new literal named suite; no existing suite replacement):

```sh
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/register-suite.py
```

Registered line:

```sh
app e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration flock -w 600 /home/user/work/.app-m1-browser.lock env TIMELINE_CURRENT013_RUN=1 TIMELINE_CURRENT013_APP_SHA=cee68b807017efc8669c7d75318cf51aa70ec855 TIMELINE_CURRENT013_APP_TREE=b2c510ca8893c4d3c238fb042f9ec7e7252edbc0 TIMELINE_CURRENT013_AGENT_SHA=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source ASTRID_PUBLIC_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers PYTHONDONTWRITEBYTECODE=1 NODE_OPTIONS=--max-old-space-size=4096 TIMELINE_CURRENT013_CACHE_ID=appcee68b807017efc8669c7d75318cf51aa70ec855-treeb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-tree75354d38c898729bac09619679f5421faba319ed-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-tree7ab412cc4bcbe517efcfa806e092336390312e18-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-chromium141-85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95-run-lane.sh12cfe518ffe2e34d1891b256e4963124952a24cb33ad23c4a9da96ca1cb9ecd2-exact-three.mjs6e793902f18509575376a035b7c5f2436641f49f232ea506e5d000e6d3cbf8ee-prepare-overlay.pyc872ca9f14d06151b64e09602d7c326f51804792828f02a8017637fe06df0f4e-audit.py6b3310764a1105607b16db44bde8729ca3e126e5401ecc583185ef44fb3fb193 bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/run-lane.sh
```

Submitted once:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m3-current013-core-browser-candidate e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-m3-current013-core-browser-candidate-e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration-1020131434-28008 1
```

`request-test` returned this TestID; `wait-test` returned **1**, reporting the single central failure. The existing exported `readCurrent013Inputs` / `checkCurrent013Sources` guards surrounded exactly this subprocess in a notes-only launcher, including its failure path:

```sh
npm run test:e2e:three-products -- --grep 'M1 real'
```

The requested selection comprises exactly these existing three cases (source titles at lines 904, 1017 and 1135):

1. `M1 real gesture: lost durable ACK, dependent B, reopen, Runtime restart, exact retry and UI undo preserve independent Agent work`
2. `M2 real gate 5 (M1 real mounted path): Agent edit, lost ACK, newer local gesture, exact retry, restart and undo preserve intent`
3. `M1 real dependency conflict retains B original guards and pending identity`

**Zero browser cases executed**: global setup failed first. The build command that actually ran was:

```sh
npm run build:hosted
# package script:
VITE_ASTRID_EDITOR_ONLY=1 VITE_RUNTIME_ORIGIN=http://127.0.0.1:17340 VITE_WORKSPACE_RUNTIME_EXPECTED_ACTOR_ID= VITE_WORKSPACE_RUNTIME_EXPECTED_REALM_ID= VITE_WORKSPACE_RUNTIME_EXPECTED_INSTANCE_ID= vite build --config config/vite/vite.config.ts
```

No dist existed in the clean central snapshot, so the original freshness helper exercised a normal fresh build. `ASTRID_APP_DIRECT_DIST` was absent. The build transformed 2,409 modules and failed after 23.52 seconds:

```text
[vite:load-fallback] Could not load /home/user/work/wt/app-m3-agent013-current-pair-source/astrid/packs/rendering/elements/public-catalog.ts (imported by src/pages/Home/astrid-public-host.tsx): ENOENT: no such file or directory, open '/home/user/work/wt/app-m3-agent013-current-pair-source/astrid/packs/rendering/elements/public-catalog.ts'
Error: Command failed: npm run build:hosted
```

Read-only triage confirms App line 2 imports that exact `@astrid-public` path; the normal alias at `config/vite/vite.config.ts:160` maps it to the required frozen keeper's `astrid` directory. The file is absent both on disk and in `git ls-tree HEAD` for Agent d874. The failure occurs even with the normal editor-only build flag. This exact frozen pair does not satisfy the normal build's public-source import contract. No decision was changed to work around it.

Local read-only checks (all passed, no sockets/browser/build locally):

```sh
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/run-lane.sh
node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/exact-three.mjs
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/prepare-overlay.py --verify-only
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/audit.py
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/preflight-command.txt
```

The last two commands ran before and after the central attempt; their outputs were byte-identical. `preflight-command.txt` contains the complete pinned environment and normal exported guard invocation. The source check commands are checks, not additional behaviour-test passes.

## Build-cache isolation, start/end guards and normal editing configuration

Only the central service's own `.test-*` snapshot had its initial `node_modules` symlink replaced. The replacement was a private real directory: package entries linked to the existing read-only private12 packages, with private scope directories and private `.bin` links, while `.vite` and `.vite-temp` were owned real directories. No shared node_modules link, file or cache was created, deleted or replaced. `TMPDIR`, npm cache, Playwright transform cache and XDG cache were outside all dependency trees in this worker's notes run directory. No install was run.

- [Source start](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/runs/.test-app-m3-current013-core-browser-candidate-e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration-1020131434-28008/source-start.json) and [source end/failure](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/runs/.test-app-m3-current013-core-browser-candidate-e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration-1020131434-28008/source-end.json): **byte-identical**, existing exported guards passed.
- [Artifact/lock/dependency audit start](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/runs/.test-app-m3-current013-core-browser-candidate-e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration-1020131434-28008/audit-start.json) and [end](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/runs/.test-app-m3-current013-core-browser-candidate-e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration-1020131434-28008/audit-end.json): **byte-identical**, including all75/all77 and peers.
- [Shared cache start](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/runs/.test-app-m3-current013-core-browser-candidate-e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration-1020131434-28008/cache-start.json) and [end](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/runs/.test-app-m3-current013-core-browser-candidate-e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration-1020131434-28008/cache-end.json): **byte-identical** for `.vite` / `.vite-temp` in both the private12 borrowed install and integration App dependencies.
- [First failure source triage](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-core-browser-candidate/notes/first-failure-triage.txt).

Normal editing fixture/configuration was unchanged: one worker, zero retries, ordinary Chromium args (no-sandbox, disable-dev-shm-usage, no-proxy-server, fixture host resolver, pinned certificate SPKI and hosted-origin IP-address-space override), with the existing `local-network-access` context permission. No frame grant or renderer/parity workaround was added. Exact config/source hashes:

```json
{
  "playwright.direct.config.ts": "656406fea27e39b7f434d1448db4030caedd74a022e2faef99ed47c793effcad",
  "playwright.three-products.config.ts": "5e21bb734436b03fee239ac5f280a78c34e276c8d79aba530a29636a51105a9e",
  "tests/e2e/local/support/app.ts": "80191a47c1890be4ba04c533b9b9934b8506fbd95cf3b2271fcbdbcce006905d",
  "tests/e2e/local/support/harness.ts": "0269c80498baa8d4e2609ef9b6cf3aeee199f044f9b8f95fd4e62b1210427cc5",
  "tests/e2e/local/global-setup.ts": "fecd2698e9e78ba5dbfe9b52cc3634bb0bb6ceba0cf9c6570b0bfb92ed1d0a89",
  "tests/e2e/local/three-products.spec.ts": "2e66a73e190dca42fd41bd41c826076ccfbc7a3ff251a3dc12717108b7c7e330",
  "config/vite/vite.config.ts": "ed32f0ba69ee7628953b151da8c5d1a2fa7816500386b48dac0ca78ba737311b",
  "scripts/testing/current013-integration.mjs": "82ff12281994e3bce006d643fc2b090ef356784c6854b959e82c87caf3347901"
}
```

Temporary cache directories were removed by the central postflight; its snapshot and partial build output were removed by the test service. The assigned worktree remains clean and unchanged. Only requested ORCH notes/report files and the single suite registration were written.

## Limits and next step

This attempt is candidate evidence for the exact tuple above only. It gives no App gesture, renderer-OFF commit, M1/Gate5, restart/retry/undo, conflict or UI qualification because the fixture never started. The local track-lock lifetime HOLD and ActualRoot policy fix remain separate; no root release approval is granted or implied. It cannot qualify the manager's future policy/UI tree. No full suite, project tsc, browser installation, frame/PCM run, source overlay, mock, weakened assertion or automatic retry was performed.

The manager should resolve the normal App public-host/frozen Agent source contract, freeze the resulting reviewed tuple, and request fresh central qualification. The eventual policy-tree final gate remains required. This worker stopped at the preserved first failure as instructed; it did not choose a new source pair or implementation fix.

Qualification is **BLOCKED** by the missing frozen-source build input. Worker `BLOCKED`, `report.md` and `commit-msg` are written; no `DONE` or `KEEP` is retained because validation is blocked and no test is still running.
