# MAIN17 / current013 bounded Node transport qualification

**PASS for the bounded real-Runtime Node operation lane only.** One new central request executed one real acceptance/restart/replay case; no cache hit, failure, retry or source fix. UI-root release remains HOLD and requester activation remains unqualified. Manager authorization explicitly separated this lane from the refused-label-row-unmount UI HOLD.

## Exact source

| Component | Source HEAD | TREE | Retained checkout |
| --- | --- | --- | --- |
| App baseline | `927545cf52fdfbb273afbe7f190e00e11e5e2d70` | baseline `96605f2a46c49fcf96cd12ca3679014f00ae28de` | `/home/user/work/wt/app-m2-main17-proxy-live-current013-gate` |
| Final App source | baseline plus approved port below; harness commit pending | `dce17b5dd0a7d571a2a61bfac3a6b7c547768c16` | same worker; central snapshot tree verified |
| Agent | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` | `75354d38c898729bac09619679f5421faba319ed` | `/home/user/work/wt/app-m3-agent013-current-pair-source` |
| Runtime producer | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` | `/home/user/work/wt/app-m3-runtime013-producer-source` |

Read PLAN, the prepared source report and its independent APPROVE, the operation agreement and the paired executor report/helper. No settled decision changed. Ported only the approved `171a259acbeb3ced855ca8f72fed0943a2f5a5cb..5e0d5de2b6ecc40baa8be8f36491420e22bc602d` delta. All thirteen paths compare byte-equal to approved source; six existing server/config paths already matched and were not written. The seven changed/new paths are:

- `src/integrations/runtime/dataProvider.ts` (shared acceptance decoder extraction; existing cache logic preserved)
- `src/integrations/runtime/operationHost.ts`
- `src/integrations/runtime/operationHost.test.ts`
- `scripts/runtime-operation-host-integration.test.mjs`
- `scripts/runtime-operation-host-real-runtime.test.mjs`
- `scripts/runtime-operation-proof-inputs.mjs`
- `scripts/runtime-operation-proof-inputs.test.mjs`

Runtime/package/lock pins, generated files, Main17/nativeLabel code, three-products journey and existing harness/Agent helper remain unchanged. No behavior expectation was weakened, skipped or removed. No journal, automatic requester, endpoint, DTO, browser bearer, fallback or native acceptance bypass was added.

Normal consumer Runtime contract/client `0.2.13`, schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`, producer artifact `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`, public Composition `0.0.12`. Both clean retained source identities and pins pass strict guards before and after the case (and in runner boundary checks). Agent preflight verifies imported source and real authority/instance.

## Central execution and frozen inputs

**Test ID:** `app-m2-main17-proxy-live-current013-gate-proxy-real-current013-tdce17b5dd0a7d571a2a61bfac3a6b7c547768c16-integration-1020124426-15357`  
**Result:** PASS, exit 0, 15 seconds service elapsed; one case passed, zero failed/skipped/cancelled. Test body 11250.844511 ms.  
**Service cache key:** `bad669b92c48e674074526462eb45695`  
**Log:** `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-main17-proxy-live-current013-gate-proxy-real-current013-tdce17b5dd0a7d571a2a61bfac3a6b7c547768c16-integration-1020124426-15357/log.txt`  
**Summary:** `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-main17-proxy-live-current013-gate-proxy-real-current013-tdce17b5dd0a7d571a2a61bfac3a6b7c547768c16-integration-1020124426-15357/summary`

The own `.test-app-m2-main17-proxy-live-current013-gate-*` snapshot helper verified the exact App TREE, clean snapshot, public12 dependency declaration, archive SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, all 77 unique safe regular archive members, byte-equal installed contents with no extra files, and all six React/Remotion peer versions. React/ReactDOM `18.3.1`; Remotion/Player/Media/Layout-utils `4.0.509`. Only this snapshot's ignored node_modules link could be repointed. The worker's own ignored link points to the same read-only `/tmp/app-coherent-deps12/node_modules`.

Immutable inputs: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-proxy-live-current013-gate/notes/inputs-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-appdce17b5dd0a7d571a2a61bfac3a6b7c547768c16.json`. Interpreter paths remain the venv bin/python symlinks, without resolving them to a system interpreter. Helper and runner live only in this worker's ORCH notes. Runner verifies the input/helper/runner SHA-256 values bound into the literal command; cache identity includes all three hashes, exact App TREE, Agent/Runtime SHAs and public12 archive hash. No requester environment forwarding or moving dependency defaults are used.

Exactly one new named service entry was appended; existing entries/bin were unchanged:

```text
app proxy-real-current013-tdce17b5dd0a7d571a2a61bfac3a6b7c547768c16-integration flock -w 600 /home/user/work/.app-m1-browser.lock env TIMELINE_PROXY_REAL_RUNTIME_RUN=1 TIMELINE_PROXY_PROOF_INPUTS=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-proxy-live-current013-gate/notes/inputs-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-appdce17b5dd0a7d571a2a61bfac3a6b7c547768c16.json TIMELINE_PROXY_INPUTS_SHA=312f8b322ed9544b7d3bb6eeaa964ca991a04ba0c146c81c6d2f11a662a9a3eb TIMELINE_PROXY_HELPER_SHA=7797d8936d8f2d889d1b9f994528b1cbf4b4a973e891f989cbda975f698fd156 TIMELINE_PROXY_RUNNER_SHA=d3039f74756749f08cbecbbafc2dd81fea402c1c3a332afd98c317459b1ee802 TIMELINE_PROXY_CACHE_ID=appdce17b5dd0a7d571a2a61bfac3a6b7c547768c16-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-input312f8b322ed9544b7d3bb6eeaa964ca991a04ba0c146c81c6d2f11a662a9a3eb-helper7797d8936d8f2d889d1b9f994528b1cbf4b4a973e891f989cbda975f698fd156-runnerd3039f74756749f08cbecbbafc2dd81fea402c1c3a332afd98c317459b1ee802 TSX_DISABLE_CACHE=1 PYTHONDONTWRITEBYTECODE=1 NODE_OPTIONS=--max-old-space-size=4096 python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-proxy-live-current013-gate/notes/run-node-proof.py
```

Exact request/wait performed (the script stored the result directory in notes):

```sh
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
S=proxy-real-current013-tdce17b5dd0a7d571a2a61bfac3a6b7c547768c16-integration
R=$("$O/bin/request-test" app-m2-main17-proxy-live-current013-gate "$S")
"$O/bin/wait-test" "$R" 1
```

The registered runner executes precisely:

```sh
node --import tsx --test --test-concurrency=1 scripts/runtime-operation-host-real-runtime.test.mjs
```

Execution is service-side only. `TSX_DISABLE_CACHE=1`, `PYTHONDONTWRITEBYTECODE=1`; Vite caches and TMPDIR/npm cache are private under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-main17-proxy-live-current013-gate/notes/cache`. Per-run temporary contents were removed after evidence collection. No worker-local socket was opened. No shared dependency/runtime/venv/cache was written. Before/after hashes and file metadata of `.vite`/`.vite-temp` at both shared dependency roots compare equal (`notes/shared-cache-{start,end}.json`); this is a cache-subtree check, not a complete dependency census.

## What the passing case establishes

A real native Agent-captured move establishes the immutable basis. An App command session captures a Unicode track-label edit and sends its original outbox bytes through production host/decoder/admission/proxy helpers into the normal startup-loaded semantic provider. No synthetic accepted envelope replaces Runtime acceptance.

The case observes HTTP 200 plus the scoped durable history publication, then injects a lost acknowledgement. The saved pending request retains exact UTF-8 body and key. Discovery endpoint/credential/instance replacement cannot retarget an acquired operation. Actor/realm/project/timeline mismatches and retired operations refuse under the existing fences.

After real Runtime stop/start with a new endpoint/instance, the old page cannot follow silently and its retired server handle returns 410. A fresh Vite SSR module lifetime negotiates new health/handshake/realm. Recovery remains explicit: exactly one commit ingress before recovery, exactly two after. Both ingress buffers/keys match the original reservation; both complete acceptance envelopes/receipts match; history adds exactly one publication. Accepted label, previous move, children and opaque seed data survive. Final source guards are reached and pass.

Recorded operation traffic exposes no server credentials or private response headers; handles are confined to acquisition replies/operation headers and absent from URLs/bodies/outbox records. Recorded operation requests never use `/api/runtime` fallback.

## Other exact checks

All from `/home/user/work/wt/app-m2-main17-proxy-live-current013-gate`:

| Command | Result |
| --- | --- |
| `node scripts/runtime-operation-proof-inputs.test.mjs` | 1 passed, 0 failed/skipped/cancelled |
| `node --test-name-pattern='^pure:' scripts/runtime-discovery-proxy-operation.test.mjs` | 7 pure cases passed, 0 failed/skipped/cancelled; no sockets selected |
| `node --check scripts/runtime-operation-host-real-runtime.test.mjs` | exit 0 |
| `node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/runtime/operationHost.test.ts src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/dataProvider.parity.test.ts` | 3 files / 159 tests passed, exit 0 |
| `node node_modules/eslint/bin/eslint.js scripts/runtime-operation-proof-inputs.mjs scripts/runtime-operation-proof-inputs.test.mjs scripts/runtime-operation-host-real-runtime.test.mjs src/integrations/runtime/operationHost.ts src/integrations/runtime/operationHost.test.ts src/integrations/runtime/dataProvider.ts` | exit 0, no findings |
| `git diff --check` | exit 0 before/after central run |

Read-only byte comparison confirms all approved paths and protected files; Agent/Runtime remain clean at their exact SHAs at completion. No project tsc, full suite, build, install, browser, frame, render, audio or production activation command ran.

## Limits and next step

This is Node transport/semantic acceptance evidence, **not UI-root release or browser proof**. Vendored fake IndexedDB `0.0.0-local`, an in-process lock set and the first lifetime's storage object survive modeled relaunch. Native IndexedDB transactions, browser locks/reload, browser/process-crash/disk durability and actual packet loss are unproven. Lost ACK is injected after observed Runtime durability.

The recorder observes proxy ingress, not Runtime-side HTTP bytes. This case does not inject X-First/X-Second headers; direct planted stripping evidence remains the unchanged prior actual-Vite synthetic lane. Absolute same-origin workspace-config fetching bypasses the operation recorder, so the no-secret/no-fallback conclusion covers recorded operation traffic only.

The test-only sender adapter reads the already reserved exact outbox body for the parsed session callback. Production requester ownership/wiring, UI label refused-row-unmount repair, browser gate and production activation remain separate work. Undo, full journeys, frame/audio parity, owner-film and macOS behavior are not qualified by this case. No blocker remains for the assigned bounded lane; no decision deviation or additional run is recommended. Manager should review this exact tree/result and retain the UI/activation holds until their separate gates pass.

DONE/KEEP retain the source, frozen input/helper/runner and result references for manager review; commit message supplied for the harness. No manual commit/push/ref mutation was performed.
