# Final current013 paired App executor

**BLOCKED / UI NOT QUALIFIED.** The exact final App passed the required independent **APPROVE + project tsc PASS** gate before execution. One fresh central seven-case request then **failed exit 1 in 30 seconds during normal hosted-build setup**: the exact Agent keeper lacks the public catalog imported by App Home. **Zero browser cases started**; no case assertion failed or passed. Source/dependency/cache checks passed before and after the failure. No product/source/test/config/lock edits, no retry, no substitute source or fake provider.

## Exact source

| Source | Retained path | HEAD | TREE |
| --- | --- | --- | --- |
| App | `/home/user/work/wt/app-m3-current013-final-paired-executor` | `b1ef4b9b910ba72375c34cf319692f90d22edc25` | `8d8a10b057ed31fed69517e18a23b8ec3811447a` |
| Agent | `/home/user/work/wt/app-m3-agent013-current-pair-source` | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` | `75354d38c898729bac09619679f5421faba319ed` |
| Runtime/server/producer | `/home/user/work/wt/app-m3-runtime013-producer-source` | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` |

Read PLAN first, repository CLAUDE.md, preceding executor/preparation/restore notes, the live-policy fix and actual-parent reachability reports, and the final independent review. Decisions remained settled. All three retained checkouts remained clean and exact; the service snapshot TREE was exactly `8d8a10b057ed31fed69517e18a23b8ec3811447a` (`result/snap`). No moving ref supplied the execution source.

The written [final review/typecheck](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-final-live-policy-review-typecheck.md) explicitly approves this App SHA/TREE, records **73 targeted tests passed**, and records one actual project `tsc --noEmit -p tsconfig.app.json`, **exit 0 / zero diagnostics**. Those are the review worker's results, not tests rerun here. Its report SHA256 `8e40c07c172fdfa96a91a6a8462098a465c13fcbeddc6e32f91f0cc5064ab79c` was checked centrally before launch; its exact copy is `notes/approved-review.md`. Earlier split-hook HOLD is not being used as an actual-UI blocker; the final +4 product fix and review cover that construction.

## Actual central result and blocker

**TestID:** `app-m3-current013-final-paired-executor-e2e-final-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020131907-3792`  
**Result:** fresh **FAIL / exit 1 / 30 seconds**, no `cached_from`, no resubmission. [Full log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-current013-final-paired-executor-e2e-final-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020131907-3792/log.txt), [summary](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-current013-final-paired-executor-e2e-final-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020131907-3792/summary), [snapshot/cache identity](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m3-current013-final-paired-executor-e2e-final-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020131907-3792/snap).

Exact failure after 2,817 transformed modules / 21.90-second Vite build:

```text
[vite:load-fallback] Could not load /home/user/work/wt/app-m3-agent013-current-pair-source/astrid/packs/rendering/elements/public-catalog.ts (imported by src/pages/Home/astrid-public-host.tsx): ENOENT: no such file or directory
```

`src/pages/Home/astrid-public-host.tsx:2` imports `@astrid-public/packs/rendering/elements/public-catalog.ts`; `config/vite/vite.config.ts` resolves `@astrid-public` from the explicitly bound `ASTRID_PUBLIC_CHECKOUT`, which was the SAME exact Agent keeper as `ASTRID_CHECKOUT`. That keeper contains `elements/catalog.ts`, but not `elements/public-catalog.ts`. The unmodified global setup's `execFileSync('npm', ['run', 'build:hosted'], ...)` fails at `tests/e2e/local/global-setup.ts:46` before fixtures/browser/Runtime acceptance. `ASTRID_APP_DIRECT_DIST` was absent and central snapshot `dist` absent before setup. No stale distribution or alias/catalog/provider overlay was supplied.

The selected final App source therefore cannot reach the required UI journeys through its authorized normal build. This is a concrete build/source prerequisite blocker, not evidence about final gesture correctness. The preceding diagnostic `app-m3-current013-core-browser-candidate-e2e-core-current013-cee68b8-d8749a9-2c4ac18-integration-1020131434-28008` independently failed on older App CEE/b2 with the same missing-file error; it is **not** claimed as evidence on this final TREE. Nine relevant final browser/build inputs compare byte-equal to that older candidate (`notes/unchanged-browser-build-inputs.json`).

After assessment, **did not submit** the regular three-label or single cold-open lanes: both use the same global hosted-build setup and the prerequisite failure remains unresolved. Their original tests and expectations remain intact. They are **UNRUN**, not skipped/passed/xfail. No broad automatic retry, source repair or policy decision was made by this executor.

## One literal registration and exact commands

Appended exactly ONE new named suite; no pre-existing suite or central bin changed. Lane arguments via `--files` give separate command/cache identities without requester environment forwarding. Literal source/producer/venv paths, full SHAs, App TREE, public12/browser hashes and helper/review identity are all in the command:

```text
app e2e-final-current013-b1ef4b9-d8749a9-2c4ac18-integration flock -w 600 /home/user/work/.app-m1-browser.lock env TIMELINE_CURRENT013_RUN=1 TIMELINE_CURRENT013_APP_SHA=b1ef4b9b910ba72375c34cf319692f90d22edc25 TIMELINE_CURRENT013_APP_TREE=8d8a10b057ed31fed69517e18a23b8ec3811447a TIMELINE_CURRENT013_AGENT_SHA=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source ASTRID_PUBLIC_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python TIMELINE_BUNDLE_AGENT_HEAD=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 TIMELINE_BUNDLE_RUNTIME_HEAD=2c4ac180c2220bdad966bc01e95ad230e99ce26a PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers PYTHONDONTWRITEBYTECODE=1 NODE_OPTIONS=--max-old-space-size=4096 TIMELINE_CURRENT013_REVIEW_SHA256=8e40c07c172fdfa96a91a6a8462098a465c13fcbeddc6e32f91f0cc5064ab79c TIMELINE_CURRENT013_CACHE_ID=appb1ef4b9b910ba72375c34cf319692f90d22edc25-tree8d8a10b057ed31fed69517e18a23b8ec3811447a-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-tree75354d38c898729bac09619679f5421faba319ed-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-tree7ab412cc4bcbe517efcfa806e092336390312e18-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-chromium141-85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95-review8e40c07c172fdfa96a91a6a8462098a465c13fcbeddc6e32f91f0cc5064ab79c-run-lane.shdb04490f27fd390cd77d5c4d59fe506e7681816387e82cc51fe14b58c7899c7a-run-selected.mjsc789559be0b1045b103c178f18150f15a773db29147673edcab3499c66029674-prepare-overlay.py4f9e0969dd1bd0575ea10e9fe4a64aa52ed72ac9b8990cf5e839e89096412fa9-audit.py19204292ce5b8e3da843f15bbfe7c9de99af01a108a6d75917728a1f12f2e48a-check-review.py370b57bc54aa8068d50c15be00ab3774920169dd2c7bb22b4eb8313262cb603a bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-final-paired-executor/notes/run-lane.sh
```

Exact request, made once:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m3-current013-final-paired-executor e2e-final-current013-b1ef4b9-d8749a9-2c4ac18-integration --files three-products > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-final-paired-executor/notes/three-products-result-dir.txt
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-m3-current013-final-paired-executor-e2e-final-current013-b1ef4b9-d8749a9-2c4ac18-integration-1020131907-3792 1
```

The waiter completed exit 1 on that same ID. Central child argv (no grep restriction; all seven existing cases including new Gate5 were selected):

```sh
node scripts/testing/current013-integration.mjs
# Existing wrapper delegates unchanged:
npm run test:e2e:three-products
# Existing script:
playwright test --config playwright.three-products.config.ts
# Existing global setup invokes:
npm run build:hosted
```

Prepared, **not executed**, as separate fresh invocations using the same named suite with `--files labels` or `--files cold-open`:

```sh
npm exec -- playwright test --config playwright.track-label.config.ts --grep-invert 'M2 cold-open'
npm exec -- playwright test --config playwright.track-label.config.ts --grep 'M2 cold-open'
```

The unchanged existing current013 guard ran before and after the child even on failure. The notes-only runner also surrounds each selected lane with that same guard and records exact source/config fingerprints. No test body, provider or assertion was replaced.

## Pins, dependencies and isolation

Both normal producer-backed vendor checks pass before/after. Existing wrapper verifies metadata/locks/archives and both peer source identities; the reused notes audit additionally checks all **75 Runtime artifacts** against manifest hashes AND committed bytes, and **13 App + 15 Agent** locked destinations against exact producer bytes. Both consumers use normal contract/client **0.2.13**, schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`, artifact `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`, component manifest `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`. Raw producer manifest SHA256 `129abdbbf1f877643618b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497`.

Public Composition **0.0.12** archive SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3` matches both consumer archives. All **77 unique safe regular members** and exact installed file set/bytes verified before/after against read-only `/tmp/app-coherent-deps12/node_modules`. React/ReactDOM **18.3.1**; Remotion/Player/Media/Layout Utils/Three **4.0.509**. Vite **5.4.21**, Rollup **4.60.2**, Playwright **1.60.0**, ambient Vitest **4.1.5**, TypeScript **5.9.3** (latter two recorded, not invoked by this executor). `notes/dependency-versions.json` retains paths.

Existing editing browser `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`: **Chromium 141.0.7390.37**, SHA256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`. Hash read locally and version/hash checked centrally; browser itself never launched because setup failed. No Chromium155/frame grant/install.

Only this worker's central `.test-*` snapshot received an owned node_modules root/scopes, read-only package symlinks to private12, and owned `.vite`/`.vite-temp` directories. The original worktree's `node_modules -> /home/user/work/app/node_modules` remains unchanged. This prevents shared Vite bundle-cache writes through a global node_modules link. TMPDIR, npm, Playwright transform/output and XDG caches were private under this worker's ORCH `notes/runs/`; temporary caches were removed after execution. Shared `.vite` and `.vite-temp` paths under **both** `/home/user/work/app/node_modules` and `/tmp/app-coherent-deps12/node_modules` compare byte-equal (file content/mode/size/mtime records). This is scoped shared-cache verification, not a full shared dependency census.

Python entry points remain literally `/home/user/work/venv-agent/bin/python` and `/home/user/work/venv-runtime/bin/python`, preserving symlink/venv prefixes; no venv modification. All socket/build activity was central-only. The service removed its failed-build snapshot; no running test, KEEP, build output or temporary worktree source remains.

Read-only local verification commands, all **exit 0**, with source/pair/cache comparisons repeated after the central failure:

```sh
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-final-paired-executor/notes/audit.py
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-final-paired-executor/notes/audit.py --caches
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-final-paired-executor/notes/prepare-overlay.py --verify-only
bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-final-paired-executor/notes/run-lane.sh
node --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-current013-final-paired-executor/notes/run-selected.mjs
# With exact literal environment stored in notes/inputs.json:
node --input-type=module -e 'import {checkCurrent013Sources,readCurrent013Inputs} from "./scripts/testing/current013-integration.mjs"; console.log(JSON.stringify(checkCurrent013Sources(readCurrent013Inputs()),null,2));'
git diff --check
git status --short
```

Local `source-start/end.json`, `pair-start/end.json`, `cache-start/end.json` and central `source`, `audit`, `cache` start/end pairs all compare byte-equal. Helper hashes in `notes/helper-sha256.json` still match the literal suite registration. Product/test tracked diff remains empty.

## Retained HTTP restore evidence

Reuse the actual **2 PASS / exit0** Runtime HTTP result `app-m3-current013-restore-consumer-gate-restore-current013-ad8749a9ce12a699672faf3ad96b4e4cbea9245c2-tb2c510ca8893c4d3c238fb042f9ec7e7252edbc0-integration-1020130731-30085`, documented in [restore consumer gate](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-current013-restore-consumer-gate.md). That run used App **CEE/b2**, the identical exact Agent/Runtime pair and real normal Runtime provider/fixture. It is **historical HTTP evidence, not a fresh run on final App TREE and not UI evidence**.

`notes/restore-byte-equality.json` proves exact equality for **115 explicit files**: provider/generated/runtime and consumer data files, both existing integration tests' file, integration/base configs, actual Runtime/Agent fixture helpers, ShotEditorView, shot composition adapter, package/lock/normal lock and public12 archive. The complete CEE-to-final App diff is limited to `trackLabelGesture.ts`, `useTimelineTrackManagement.ts`, and `TrackLabel.command.test.tsx`; none changes this HTTP provider lane. Thus no unchanged HTTP test rerun was needed or submitted.

## Handoff

Manager should assign the owned hosted-build/public-catalog compatibility fix, then approve and qualify its resulting exact source tuple with a new literal cache identity. Do not claim this final App UI/Gate5 qualified, merge the root as proven, or retire required writer paths based on this build failure. Once build prerequisites pass, seven-case acceptance, retained three-label invocation and fresh cold-open invocation remain required.

No decision was relitigated. The exact-source/public-source bindings expose an incompatibility; this executor reports it rather than selecting a different Agent checkout or editing product source. No local sockets/browser/build, full suite, project tsc, install, renderer/frame/PCM/audio parity, owner-film or macOS qualification was run here. Conventional commit message and **BLOCKED** supplied; **no DONE**, because required UI qualification is blocked; no KEEP, because nothing is running. Requested report copies are in local ignored `design/`, ORCH design and worker report.md. No git commit/merge/rebase/checkout/push/ref operation or other worker/integration edit.
