# App M2 parent-delete integrated root compose

## Final source composition

Composed only the approved corrected parent-delete delta `29564148789ef00a8c28ea44d7ba87faf19d1602` / tree `7b86b7aff415007f679c29ffa71a1d16f8551e24` (against merge-base `b1ef4b9b910ba72375c34cf319692f90d22edc25`) onto integration `3599fc49ad76dfdd7847ab4c813fc9317a0304eb` / tree `74130f681f6b0c87a7c61cb33d4ae6a092c03046`.

Prospective final worktree tree: `a3ea802324e3d269c474046fe71526e99fea5228`.

The cold-start initial-read/recovery readiness fix, Main17, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, public12 Composition archive, source tests, and the existing seven root cases remain present. No old root/pin files were copied. The only setup correction was changing the parent-delete launcher/test/source convention from the superseded Agent d874 to the ready current-compatible Agent keeper `8130a401bf44a518d5a40ae274d398b8c560be55` (tree `236c3e57e0265c52b81ba8085de3193026176bff`), with the same official Runtime/client tuple.

## Diagnosis of prior actual deletion

Prior TestID: `app-m2-parent-delete-actual-candidate-gate-e2e-parent-delete-tree7b86b7a-runner61a036d-e2e-integration-1020150047-3749`.

This was the initial-basis readiness race, not a UI/key/owner-routing failure. The trace/context showed the real `f2-app` clip selected, the rendered Delete control present, and the browser delivered `Page.keyboardPress {"key":"Delete"}`. No native `/commit` POST followed; the wire remained at zero posts. The old source allowed editing before the durable native capture port was installed. The composed cold-start fix keeps the editing surface loading until verified initial recovery readiness, including the command session port. No delete fallback, display-ID ownership inference, group261 change, or guard weakening was added.

## Controls run

All local controls below passed:

```sh
node --experimental-vm-modules --test scripts/testing/current013-parent-delete.test.mjs scripts/testing/current013-integration.test.mjs
```
2 file subtests passed, 0 failed.

```sh
NODE_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-actual-candidate-gate/notes/private12/node_modules XDG_CACHE_HOME=$PWD/xdg-cache npm_config_cache=$PWD/npm-cache npm_config_offline=true TMPDIR=/tmp/tl13-parent-delete-integrated node_modules/.bin/vitest run --config vitest.private.config.ts src/tools/video-editor/commands/clipDeleteCapture.test.ts src/tools/video-editor/commands/clipDeleteGesture.test.ts src/tools/video-editor/commands/commitSession.clipDelete.test.ts src/tools/video-editor/hooks/useTimelineOps.clipDelete.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts
```
7 files passed, 159 tests passed.

```sh
NODE_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-delete-actual-candidate-gate/notes/private12/node_modules XDG_CACHE_HOME=$PWD/xdg-cache npm_config_cache=$PWD/npm-cache npm_config_offline=true TMPDIR=/tmp/tl13-parent-delete-integrated node_modules/.bin/eslint --no-cache --max-warnings 0 [all touched App TS/TSX/MJS/config files]
```
Exit 0, no findings.

```sh
PWTEST_CACHE_DIR=$PWD/playwright-cache npm_config_cache=$PWD/npm-cache npm_config_offline=true TMPDIR=/tmp/tl13-parent-delete-integrated npm run test:e2e:three-products -- --config playwright.clip-delete.config.ts --list
```
Exactly 2 parent-delete tests in 1 file.

```sh
npm_config_cache=$PWD/npm-cache npm_config_offline=true TMPDIR=/tmp/tl13-parent-delete-integrated node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --list
```
Exactly 7 existing root tests in 1 file.

```sh
git diff --check
```
Passed.

All runs used private12/cache/temp paths. No full suite, build, browser, sockets, project typecheck, install, or framePCM run was performed locally.

## Central gate status

No new central browser TestID was created. The only available named parent-delete suite is still registered with the obsolete App tree `7b86b7a` and Agent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`; invoking it would violate the strict source guards and silently substitute the non-preferred keeper. The manager must register the two-case central invocation against the final tree above, Agent8130, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, public12, exact Chromium/cache/preload settings, and this cache identity:

```text
parent-delete-treea3ea802324e3d269c474046fe71526e99fea5228-agent8130a401bf44a518d5a40ae274d398b8c560be55-runtime2c4ac180c2220bdad966bc01e95ad230e99ce26a-client13-public12-0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3-runnera71c71b3613f34d4b382a73959bf798271c7d646c380c011f1725a217e399bc7-helper82ff12281994e3bce006d643fc2b090ef356784c6854b959e82c87caf3347901
```

Remaining call: run both real parent-delete cases centrally on that exact registered tuple; stop on the first product failure and record its TestID/results. Candidate only; merge and deletion ledger remain manager-owned.
