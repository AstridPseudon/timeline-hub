# App current013 Gate 5 shared-seed reset

## Scope and source

This is a test-setup-only correction on App worktree
`/home/user/work/wt/app-m3-current013-gate5-shared-seed-reset`.

- Base commit: `b1ef4b9b910ba72375c34cf319692f90d22edc25`.
- Base tree: `8d8a10b057ed31fed69517e18a23b8ec3811447a`.
- Predicted post-change tree from a private index: `6e232ce33acb10ac1a8462d3d5cba1eee553ae46`.
- Only changed path: `tests/e2e/local/three-products.spec.ts`.
- Delta: exactly `+5/-0`.
- Source fingerprint before: `sha256:2e66a73e190dca42fd41bd41c826076ccfbc7a3ff251a3dc12717108b7c7e330`.
- Source fingerprint after: `sha256:2bb9abb53851d867dd6fb2cee201bddf77ffb807a5f5ee3013da0fc5e48652ac`.
- Setup-fix patch fingerprint: `sha256:75be84c6d0309c676013b486ecbb56e94b83871336291b945d105ab8c663f659`.

The Gate 5 body now performs the same existing native UI reset as the dependency-conflict case: it waits for the commit response, drags the clip from `5` to `0`, requires HTTP 200, and waits for all command outboxes to drain. The general `prepareAfterAckLossMoves` helper is unchanged. No expected `5`/`7` value or assertion changed; no direct canonical mutation or App command injection was added.

## Why this was necessary

The exact central native lane `app-m3-current013-native-core-finalgate-e2e-native-core-current013-b1-tree8d8a-agentd874-runtime2c4-e2e-integration-native-1020135745-7128` passed the first original M1 durability case in about 23 seconds, then failed Gate 5 at an existing positive assertion: expected `clip.move.args.on: 5`, actual `8.333333015441895`. The original dependency-conflict case was not run.

The three-products fixture uses worker-scoped `seed3` and serial tests. The first native case intentionally leaves the clip at `5`; Gate 5's shared helper incorrectly assumed a fresh `0` state and issued its `0 -> 5` drag against the already-moved UI state. The added real-UI `5 -> 0` commit prelude restores the helper's documented precondition while preserving serial coherence for the original first case, corrected Gate 5, and the later conflict case. The conflict case's existing reset remains untouched.

## Checks run here

- `npx eslint tests/e2e/local/three-products.spec.ts --report-unused-disable-directives --max-warnings 0` — passed.
- `npx playwright test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.spec.ts` — passed; discovered all 7 tests in the file, including the original M1 case, Gate 5, and conflict case.
- `git diff --check` — passed.
- Read-only dependency topology: worker `node_modules` remains the symlink to `/home/user/work/app/node_modules`; no shared dependency, venv, runtime, or cache file was changed by this worker. No build output was created.
- Prior exact native tuple checks retained for central revalidation: Runtime contract `0.2.13`; schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`; artifact `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`; all 75 manifest artifacts; Composition archive `sha256:0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3` with all 77 regular members and expected peers; tracked public-browser bundle `sha256:fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`.

## Central next lane

Central should authorize one corrected native three-case lane only after the harness records the committed post-change App tree, using the frozen Agent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` (tree `75354d38c898729bac09619679f5421faba319ed`) and Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` (tree `7ab412cc4bcbe517efcfa806e092336390312e18`). The literal named suite/cache identity must include the post-change App tree and setup-fix hash, for example:

`e2e-native-core-current013-gate5-reset-tree6e232ce3-setup75be84c6-agentd874-runtime2c4-e2e-integration-native-private-node-overlay`

The central command must retain the existing short-TMP/private-node-overlay runner, unset `ASTRID_PUBLIC_CHECKOUT` and `ASTRID_APP_DIRECT_DIST`, pass the exact App tree plus `SETUP_FIX_SHA=75be84c6d0309c676013b486ecbb56e94b83871336291b945d105ab8c663f659`, and run `npm run test:e2e:three-products -- --grep 'M1 real'`. That grep selects exactly the original M1 durability case, Gate 5 (whose title contains “M1 real”), and the original dependency conflict. It must stop at the first actual failure. No blanket cache bypass, full suite, TypeScript check, install, or frame/PCM lane is authorized here.

If all three pass, central may proceed with the separately authorized regular-label lane and then a separate fresh cold-open lane. This worker did not run browser/build/socket qualification, so no gate release is claimed.
