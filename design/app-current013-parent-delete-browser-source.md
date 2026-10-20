# Current013 parent-delete browser source

Prepared on App base `cee68b807017efc8669c7d75318cf51aa70ec855` (base tree `b2c510ca8893c4d3c238fb042f9ec7e7252edbc0`). This is source preparation, not actual qualification. The current tuple's actual qualification must finish first; native delete composition and its own later central browser gate precede writer retirement.

One case collects through `playwright.clip-delete.config.ts`:

`M2 current013 real parent DELETE: lost ACK, reload, Runtime restart, exact retry and UI inverse restore raw opaque clip`

1. Reuse the real three-products fixture with an explicit `parent-delete` variant. Its target is the RAW parent `f2-app-clip`, with unknown `app.canonical` fields, nested opaque JSON, explicit nulls, ordered arrays, and own `__proto__`, `constructor`, and `prototype` keys. Validate those values in the immutable Runtime seed read before editing. Retain the second parent clip, registry assets, occurrence, shot/internal revisions and existing opaque child/config fields. Only this seed variant omits the second clip's transition, because the approved native delete conservatively refuses semantic dependencies. The ordinary M1 fixture is unchanged.
2. Click the actual rendered clip and press Delete. Require one real `/v1/.../commit`, `clip.delete` v1, a whole-row original-value guard including opaque keys, recorded collection selections/reads, and a real Runtime accepted result/history record whose root write ends in `{state: "absent"}`. No direct session call or synthetic accepted response.
3. Check the immutable RAW parent payload and both clip mirrors: only the target is removed. Compare the complete remaining payload, registry, child revisions and manifest exactly. Read the browser's real IndexedDB owner and require the exact persisted request body/key/path and original intent.
4. Use the existing Agent `commitCaptured` helper and its own credential to add a disjoint parent audio track after the delete was accepted but before its ACK reaches the browser. Preserve its actual publication through recovery and undo.
5. Abort only the accepted network ACK, wait for durable retry state, reload, close the page, restart the real Runtime, and reopen in the same browser context. Require a new Runtime instance in the same realm, the original outbox bytes/guards, and no implicit retry. Check the current immutable head still equals the Agent result.
6. Click the existing owner-specific Recover saved edits UI. Require byte-exact original body, key, method and path, the identical accepted receipt/result, and exactly one delete publication. Reload the accepted absent state.
7. Click the real Undo button. Require `timeline.inverse` naming the delete publication and actual Runtime acceptance based on the disjoint Agent head. Restore the exact original RAW clip and full parent payload, with only the independent track added; retain both mirrors, registry, occurrences and complete child closure. Reload and compare the immutable current head and visible clip again. Require zero browser legacy snapshot/revision/restore mutations throughout opening, delete, retry, recovery and inverse.

The optional concurrent guard-conflict case is not added; this source is bounded to the required positive journey. Existing conflict coverage and the positive group-delete 261 case are untouched. No parent/group ownership inference or product writer changes are included.

## Exact later source inputs and cache convention

The launcher `scripts/testing/current013-parent-delete.mjs` reuses `readCurrent013Inputs` and `checkCurrent013Sources` from the existing current wrapper at both boundaries. It preserves dirty-source rejection, executable Python paths, vendor-lock checks, metadata/manifests, public archive bytes/counts, normal hosted-build freshness, and failure propagation. No caller-supplied `ASTRID_APP_DIRECT_DIST` is allowed.

| Input | Required value |
| --- | --- |
| `TIMELINE_CURRENT013_RUN` | `1`, only for the manager-approved later gate |
| `TIMELINE_CURRENT013_APP_TREE` | Literal full tree SHA of the final clean App composition; not this source-preparation base tree or a moving default |
| `TIMELINE_CURRENT013_AGENT_SHA` | `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` |
| `ASTRID_CHECKOUT` | `/home/user/work/wt/app-m3-agent013-current-pair-source`, retained clean at that Agent SHA |
| `TIMELINE_CURRENT013_RUNTIME_SHA` | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` |
| `ASTRID_RUNTIME_CHECKOUT` | `/home/user/work/wt/app-m3-runtime013-producer-source`, retained clean at that Runtime SHA |
| `TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT` | `/home/user/work/wt/app-m3-runtime013-producer-source` |
| `ASTRID_PYTHON` | `/home/user/work/venv-agent/bin/python` |
| `ASTRID_RUNTIME_PYTHON` | `/home/user/work/venv-runtime/bin/python` |
| App + Agent generated client | Runtime `0.2.13`; producer `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56` |
| Public Composition | `0.0.12`, archive `sha256:0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, exactly 77 files |
| Chromium | Existing Editing Chromium 141; no frame-grant dependency or Chrome 155 requirement |

The launcher forwards the validated Agent/Runtime values as `TIMELINE_BUNDLE_AGENT_HEAD` and `TIMELINE_BUNDLE_RUNTIME_HEAD`. `TIMELINE_CURRENT013_CACHE_ID` must equal:

```text
parent-delete-tree<APP_TREE>-agentd8749a9ce12a699672faf3ad96b4e4cbea9245c2-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-client13-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-runner<SHA256 current013-parent-delete.mjs>-helper<SHA256 current013-integration.mjs>
```

`parentDeleteCacheIdentity(readCurrent013Inputs())` computes that string without launching a gate. The final tree binds the case/config/shared fixture bytes; the runner/helper hashes bind the launch path. The manager must register a distinct central test request with literal final inputs/cache identity, after composition. Do not reuse an M1, label, proxy, or previous App-tree result. Actual later invocation is `node scripts/testing/current013-parent-delete.mjs` through the central service, never an ad-hoc local browser run. Use worker-owned Playwright/temp/output caches and the existing normal build helper; keep all shared dependencies read-only.

## Composition remaining

This branch intentionally does not contain native delete product source. Compose the approved `8ecefbd8e6a2726971b9e5a62cf457746a7e10a4` parent-delete capture/session/UI ports onto the qualified current013 App in a separate reviewed product step (the approval's 520 targeted + 2 native checks are prior evidence, not rerun here). In particular, the real mounted delete must reach the durable session's `clipDeletePort`/native delete path. This new case fails at the required command/acceptance assertion if those ports are missing; it cannot pass on the legacy writer. Group deletion remains unchanged/unsupported by this native parent-delete port, and positive 261 remains intact. Writer retirement is still pending actual composed qualification.

## Checks performed

All commands below exited 0. No actual browser, sockets, build, full suite, tsc or install ran.

```sh
node --experimental-vm-modules scripts/testing/current013-parent-delete.test.mjs
# 7 launcher-control tests passed; VM module experimental warning only.
node scripts/testing/current013-integration.test.mjs
# 15 existing current-wrapper tests passed.
node --experimental-vm-modules --test scripts/testing/current013-parent-delete.test.mjs scripts/testing/current013-integration.test.mjs
# Both test files passed (Node reports 2 file-level subtests).
node node_modules/eslint/bin/eslint.js tests/e2e/local/clip-delete-command.spec.ts tests/e2e/local/support/harness.ts playwright.clip-delete.config.ts scripts/testing/current013-parent-delete.mjs scripts/testing/current013-parent-delete.test.mjs
# No lint findings.
env PWTEST_CACHE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-current013-parent-delete-browser-source/playwright-cache npm run test:e2e:three-products -- --config playwright.clip-delete.config.ts --list
# Exactly 1 test in 1 file; no setup/build/browser executed.
env PWTEST_CACHE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-current013-parent-delete-browser-source/playwright-cache node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --list
# Original 7 tests in 1 file still collect; their source is unchanged.
git diff --check
# Clean.
```

There is no browser pass claim: gesture reachability, native Runtime acceptance on this composition, restart/recovery and exact inverse restoration remain unverified until the later central gate. Source-preparation work is complete with no blocker; native-port composition is the next product dependency.
