# App2 M2 selected normal-DEV frozen source

## Result

Prepared the one selected proof source on current HOME App `42b0c6c8434e2c491f8dbdf00a210ed755e41a95` / tree `fa887b5689d7ad44957021080f74d13a9d0c4e30`.

The only product-tree change is the already-approved selected journey source:

```text
tests/e2e/local/three-products.selected-param-dev.spec.ts
```

Its final SHA-256 is `10250fa44db4e2d4423f8d06258105df267e3ba4e29700d700bb1d3182a6def1`, byte-identical to immutable approved commit `8e9975005d18c6278000ab4c8cc8b18291d03e12` / tree `87d2350417a876e14b81c58b64da29f1a30b35b6`.

The current HOME harness is retained unchanged from `42b0c6c84`:

```text
tests/e2e/local/support/harness.ts       af61e605e1930ae061506a317008d670c7c1be01511c7c1a57188a6a91cc0465
config/vite/vite.config.ts               5f26c8fa9beae5691c7c94ae11d008eb6c548eb28aaa2b66887b7512efe6c70d
scripts/runtime-discovery-proxy.mjs      93989e634008d1c9a6aaeddbca7b0aa0f97c40a7ce232860157d04bc6b2155c0
```

No browser, build, daemon, live socket, actual selected case, full suite, install, shared helper mutation, selector/navigation edit, or pin updater was run.

## Minimal diff

The selected spec restores the approved real-source readiness contract only:

- restores the real 20-second `#root > *` startup mount check;
- uses the existing visible `Select timeline` combobox and exact `project`/`timeline` URL identity at the original three readiness points;
- restores the existing displayed clip/P1 surface checks after both reloads;
- leaves the 90-second semantic ceiling, 240-second fixture timeout, P1/P2 admission and source removal, refusal and dirty draft, lost acknowledgement, restart/reload, exact retry body and idempotency key, undo/inverse, and zero-legacy assertions intact.

The diff is one file, 27 insertions and 5 deletions. No other live journey or shared helper bytes changed.

## Existing driver/profile/cohort

The unique existing selected suite is `ap2-m2-selected-real-p1-history-fixture-fix`, with the literal driver:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh
```

Its literal selected command is:

```sh
node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep "$TEST_TITLE" --list
npm run build:hosted
flock -w 600 /home/user/work/.app-m1-browser.lock npm run test:e2e:three-products -- --grep "$TEST_TITLE"
```

The driver currently supports the old013/public13 cohort, not current014/final95:

```text
profile: astrid private workspace
Agent:   8130a401bf44a518d5a40ae274d398b8c560be55 / tree 236c3e57e0265c52b81ba8085de3193026176bff
Runtime:  2c4ac180c2220bdad966bc01e95ad230e99ce26a / tree 7ab412cc4bcbe517efcfa806e092336390312e18
Runtime manifest: 75 artifacts, version sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56
Composition: 0.0.13, nested archive sha256 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738, 77 members
Driver graph archive: sha256 895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
Python: /home/user/work/venv-app2-native/bin/python
Driver SHA-256: a959de6e0041f0d8ee28b949a19f5add97d7fb5de27714da6beaad15abd6ce4f
```

Current HOME App is pinned to Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / tree `d3a290b407fa61e6ab2d476f50c068073f70df00`, Runtime manifest 76, artifact digest `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`, package/client `0.2.14`, and Agent final95 candidate `6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`. The App lock has source commit `95bd3c5f`, manifest count 76, and the exact generated hashes for that pair. The exact final95 checkouts are present and clean; their Runtime/Agent schemas are byte-identical at `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

Therefore the existing driver cannot be used to claim a current014 proof. The smallest exact cohort/source composition is: retain the current selected source and 0.2.14 App lock, bind the selected role to the final95 Agent/Runtime pair above, retain the same locked `0.0.13`/9412 Composition graph, and add only a closed selected-role App SHA/tree check after the harness commit. Do not relabel the old driver as current014 and do not alter unrelated profiles, pins, or guards.

Proposed role-only patch for review, not applied to the shared driver:

```diff
 APP_ROOT=${1:?usage: $0 APP_ROOT}
+APP_SHA=<harness-produced-selected-App-commit>
+APP_TREE=<harness-produced-selected-App-tree>
 test -f "$APP_ROOT/package.json"
 test -z "$(git -C "$APP_ROOT" status --porcelain=v1 --untracked-files=all)"
+test "$(git -C "$APP_ROOT" rev-parse HEAD)" = "$APP_SHA"
+test "$(git -C "$APP_ROOT" rev-parse 'HEAD^{tree}')" = "$APP_TREE"
```

This patch is insufficient until the driver owner first closes the final95 Agent/Runtime cohort binding; that binding is outside this worker's delegated authority. Whole-file before/after driver hashes were not created because the shared driver was intentionally not mutated.

## Bounded prerequisite preflight

| Prerequisite | Result | Evidence |
|---|---|---|
| Source ancestry | PASS | Current HEAD `42b0c6c84` is an ancestor of `hub/tl/integration`; selected spec is the only worktree diff. |
| Final source protection | PASS | Empty worker `KEEP` marker created; no shared helper or graph was changed. Harness commit remains pending by design. |
| Literal helper role | PASS | `harness.ts` owns `seedSelectedParamDev`, `advanceSelectedParamAndRemoveSource`, and `startSelectedParamDevServer`; the spec is their sole selected caller. |
| Approved spec identity | PASS | Selected spec SHA matches approved `8e9975005` exactly. |
| Normal graph / Composition | PASS for existing locked graph | Driver graph exists; Composition package is `0.0.13`; nested archive is 77 members and SHA `9412ae25…`; graph archive SHA is `895c628a…`. |
| Current App package graph | PASS by lock; local shared install not used | App declares Composition `0.0.13`, Remotion `4.0.509`, Vite lock `5.4.21`, Vitest `4.1.5`, Playwright `1.60.0`, tsx `4.21.0`. The shared `node_modules` resolves Composition `0.0.8`, so it is not a valid execution graph and was not modified. |
| Node/Vite | PASS as observed | Node `v22.22.0`; Vite `5.4.21`. |
| Exact Agent/Runtime artifacts | PASS separately; FAIL driver cohesion | Final95 source objects and schema checks pass, but the existing driver is still hard-coded to old013 Agent/Runtime. No execution was authorized. |
| Operation origin | PASS statically | Selected harness passes `this.devOrigin` as `ASTRID_RUNTIME_OPERATION_ORIGIN` to proxy and Vite. |
| Discovery proxy | PASS statically | Existing `scripts/runtime-discovery-proxy.mjs` is started as a managed child, with `ASTRID_WORKSPACE_DISCOVERY` set to the Runtime-written `support/discovery.json`; Vite targets the proxy loopback URL. |
| Credential FILE | PASS statically | Agent child receives `ASTRID_RUNTIME_CREDENTIAL` as the selected credential path; App receives `WORKSPACE_RUNTIME_TOKEN_FILE` as the product credential path. No bearer token is copied into browser env. |
| Argv/config | PASS statically | Driver uses the literal `playwright.three-products.config.ts` and exact test title; no selector or navigation change was made. |
| Collection/list1 | PASS | `node node_modules/playwright/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list` reported exactly 1 test in 1 file. |
| Short child-path isolation | PASS statically | Driver uses a private `mktemp` run root, private Agent/Runtime clones, private App overlay, private caches, and no shared checkout writes. |
| Disk floor | PASS | `df -Pk` observed 13,758,108 KiB free on `/tmp` and `/home/user/work`, above the 10 GiB floor. |
| Browser flock | PASS observation | `/home/user/work/.app-m1-browser.lock` was not held. It was not acquired. |
| Copy count | PASS statically | Driver has one App overlay `cp -a`; Agent/Runtime are shared-object private clones; no second App copy was created. |
| No execution | PASS | No browser, build, daemon, live socket, central actual, full suite, install, or shared-helper mutation was performed. |

The only unresolved prerequisite is the existing-driver/current014 cohort mismatch. It is reported rather than silently changed.

## Prior evidence reused

- Design `peer-app-to-app2-20261021T0634-normal-dev-merged.md`: `42b0c6c84` contains the discovery-proxy join; origin transport had 76 passing tests; old18585 remains UNKNOWN.
- `ap2-m2-selected-real-scope-conversion-review-0335-REPORT.md`: approved `8e9975005` replacement is source-backed by the real mount, timeline combobox, URL identity, clip, and element-parameter surfaces; all original journey assertions remain required.
- `ap2-m2-selected-normal-dev-harness-proposal-r1-REPORT.md`: existing proxy/credential lifecycle and exact one-file harness delta; selected spec was not to be changed by that proposal.
- `ap2-m2-selected-approved-real-scope-one-case-0342-REPORT.md`: prior one-case result `18585` failed at the original 20-second startup assertion after a workspace-config 404; it did not qualify or disprove downstream P1/P2/recovery behavior.
- `ap2-m2-main014-home-pin-independent-qualification-REPORT.md` and the final95 peer ACK: current Runtime `95bd3c5f`, App lock/client `0.2.14`, and final95 artifact identities above. These are source/lock evidence only; no matched selected actual is claimed.

## Live callers

The only changed live caller is `tests/e2e/local/three-products.selected-param-dev.spec.ts`. Its existing helper callers remain in `tests/e2e/local/support/harness.ts`; that file was not changed in this worker. The unique suite remains `ap2-m2-selected-real-p1-history-fixture-fix` and targets exactly the selected spec.

## Tests and checks

```text
node node_modules/playwright/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list
  PASS: exactly 1 test in 1 file

git diff --check
  PASS

node --check scripts/runtime-discovery-proxy.mjs
node --check scripts/runtime-discovery-proxy-operation.test.mjs
  PASS (syntax only)

source guard for startup20/semantic90/P1-P2/two reloads/lostACK/body+key/undo/zeroLegacy/real timeline identity
  PASS
```

Not run: browser/e2e execution, build, daemon, localhost/live sockets, central actual, full suite, dependency installation, Vitest/Playwright execution, and any shared helper or pin mutation.

## Handoff

The harness commit is intentionally pending. Pre-harness source is `42b0c6c8434e2c491f8dbdf00a210ed755e41a95` / tree `fa887b5689d7ad44957021080f74d13a9d0c4e30`; final commit/tree will be assigned by the worker harness after this report and commit message are consumed. The source is not execution-qualified until the driver owner closes the final95 cohort and submits the one exact selected case through the central test service.
