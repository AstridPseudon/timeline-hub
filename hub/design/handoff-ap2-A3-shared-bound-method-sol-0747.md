# A3 shared popup receiver correction

Status: correction complete; ready for independent review. No commit was run; the harness must commit this worktree before review.

## Source and scope

- Worktree: `/home/user/work/wt/ap2-A3-shared-bound-method-sol-0747`.
- Inherited HEAD: `95367498b311a5b45981aa143aa9576746039afe` (the independently failed 0735 return).
- Protected integration parent: `890b9561666c3619f69335dd747b15e042b3a9a3`.
- Correction patch SHA-256 (`git diff HEAD | sha256sum`): `7be0a268be95a4ff1ed95b5debf1c0d9f49fd7acee37481cd1665c3eb103f9c9`.
- Cumulative patch SHA-256 (`git diff 890b9561666c3619f69335dd747b15e042b3a9a3 | sha256sum`): `e161fd625fbf7f89514bfd6de035af311c79f22aec32a598b6816eb0dfa12f5c`.

Final worktree blobs (`git hash-object`, without writing objects):

| Authorized file | Blob |
| --- | --- |
| `src/tools/travel-between-images/components/shotTimelineDataProvider.ts` | `2a710a34cf6ffd16e8b4bc8a3abaebb7210ef09f` |
| `src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts` | `a07697d56deb511c070fd8097465b13c1724866b` |
| `src/integrations/runtime/dataProvider.ts` | `fea25c9f28fa617eb3cf252a0a86818ef1218be2` |
| `src/integrations/runtime/dataProvider.test.ts` | `7f5f49789b600e2ab3f10f04a31918e49d3d216a` |

Only the two shot provider files changed in this correction. The cumulative delta remains exactly the four authorized files. Runtime adapter/test blobs are unchanged from 95367498b, so the protected current-890 paired-head behavior was not edited. No files were deleted. No schema, generated, pin, lock, package, ops, fixture, Undo, move, or placement changes.

## Correction and production caller

The 0741 review was correct: extracting the real class method lost its receiver and threw on `this.projectId` before outbox append. `projectMediaSelection` now binds the existing method to its provider before invoking it. Binding preserves its arity and both existing one-argument and project/query call forms; no API, transport, or command grammar was introduced.

Production caller source remains:

`pages/LocalTimelineShotBrowser.tsx:88,299` constructs `RuntimeDataProvider` and passes it through `pages/ShotEditorView.tsx:359` to `components/ShotTimelinePreview.tsx:520-529`, then `createShotTimelineDataProvider -> saveTimeline -> sharedPopupMediaCommands -> projectMediaSelection -> RuntimeDataProvider.getProjectMediaSelection -> existing authenticated AstridRuntimeClient read -> LocalSaveSession/outbox`.

Added two focused ADD/SWAP regressions with an actual RuntimeDataProvider instance. Its media-selection class method and authenticated client are unmocked; existing runtimeFixture supplies health/handshake/realm and an in-memory transport returns the selected media identity. The regressions assert the handshake, exact media query, one durable request/key, `occurrence.fork` first for `occurrence:occ-3`, then exactly one registered add/swap command, and accepted head adoption. Canonical basis, recovery identity, and commit reply remain controlled spies; this is receiver/ingress evidence, not Python execution evidence. Replies are serialized using the same JSON boundary as the existing shared-media test.

## Commands and results

All commands ran locally in the assigned App worktree unless noted. Vitest used `--no-cache`; no shared install was changed.

- Before the production correction: `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts --testNamePattern 'preserves the real Runtime provider receiver'` — 2/2 new cases failed with `Cannot read properties of undefined (reading 'projectId')`, stack through the real RuntimeDataProvider method. The same command after correction passed 2/2 (23 tests unselected by the name filter).
- Final: `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts src/integrations/runtime/dataProvider.test.ts` — PASS, 2 files / 101 tests (existing 99 plus 2 receiver regressions).
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/travel-between-images/components/ShotTimelinePreview.test.ts src/tools/video-editor/runtime/element-adapter.test.ts` — 41/42 passed, existing `ShotTimelinePreview.test.ts:716` opaque `__proto__` assertion failed. Element adapter passed.
- `npm exec tsc -- --noEmit` — PASS.
- `npm exec eslint -- src/tools/travel-between-images/components/shotTimelineDataProvider.ts src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts src/integrations/runtime/dataProvider.ts src/integrations/runtime/dataProvider.test.ts --max-warnings 0` — PASS.
- `git diff --check` and `git diff --check 890b9561666c3619f69335dd747b15e042b3a9a3` — PASS.
- `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — PASS.
- From `/home/user/work/agent`: `python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — PASS.
- Read-only inline `python3 -` tarfile/hashlib comparison: archive `vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz` SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`; all 80 regular archive files byte-equal to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P3-env-final-0407/record/private/node_modules/@banodoco/timeline-composition`, version 0.0.14 — PASS.
- Read-only inline Node `require.resolve` check with `NODE_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P3-env-final-0407/record/private/node_modules`: all 9 package exports resolve inside that exact private package (8 code exports plus package.json) — PASS. No claim about changing the shared installed package.

The first post-binding run exposed a test-reply serialization gap (the controlled reply retained non-JSON values); the regression now uses the existing shared-media test's JSON serialization. No production workaround or weakened behavior expectation was added.

## Contract, decisions, limits, next step

Followed PLAN §3 A3, C0 §§1–5,7 and D15. The existing request carrier still emits full-v2 ABI `api_version: 1`, scope/base pair, commands, label/step patch/reads, merge/reads/dry-run and persisted idempotency key. Accepted/merged canonical document/head/digest, receipt/effects/bindings/dependencies/history/undo/publisher/provider/compiler and conflict/invalid handling remain outside this correction. The command builder still validates the physical closure and forks only the selected shared owner before its media command; it adds no broadcast, duplicate, managed-edge patch, guessed successor, or executor.

Normal Runtime client/producer freeze remains `34eac0041b0891e9011966b39bcbd26053fde5bc`, tree `9853574865f25e08284e82ffb26c0bdecaa16a30`. Separate compatible Agent execution source remains `4edc4b321cae5cfc58252d7ed89e3f0408238646`, tree `f17b84c48bae3461dd11cedb8719bd17495a8210`; its command registry at lines 79,81–82 contains fork/add/swap. No repin.

Retain the prior exact-890 baseline disclosure: 0741 independently reproduced the same `__proto__` failure on 890b95616 (25/26), and reported `element-admission-build.test.ts` failing with `spawnSync /opt/node22/bin/node EPERM`. That build test was not rerun here because this brief forbids builds. No tests were skipped, disabled, deleted, or weakened; the name-filtered regression run is separately identified above.

No blocker to this correction. No HTTP/browser/body/live service/socket/build/full/central-request run occurred. Real Python fork admission, exact materialized successor closure/sibling preservation, accepted/merged/refused physical integration and UI browser proof remain unverified here and manager-owned. Do not interpret mocked canonical replies as that proof. Recommended next: harness commit, independent Luna review of the fresh correction and cumulative four-file delta, then the manager's authorized integration proof/merge.
