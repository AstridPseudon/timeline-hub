# Bootstrap concrete patch review

Verdict: **REQUESTCHANGES**.

Patch reviewed: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-bootstrap-currentroot-consumer.patch`

- Base: `05b6b488d1834650c459c5c565f2530d9bea20e9`
- Patch SHA256: `bb57d5e9b575ceb534d88c9843a67a98d723a095464501458047d5f805fa48b9`
- Scope: 11 files, `+2904/-191`; product additions are the row-local bootstrap capture/init path, the existing-client `createTimeline` wrapper, and same-store outbox checkpoints. No generated source, dependency/pin, shared file, new endpoint/DTO, second store, or additional journal was found.

## Finding

`src/integrations/runtime/createDefaultTimeline.ts:96-120, 135-142` adds an injectable `bootstrap` callback to the production `createCanonicalTimeline` and `ensureProjectHasTimeline` APIs. The test then supplies that callback (`createDefaultTimeline.test.ts:47-64, 147-180`) and the old 135-line real `AstridRuntimeClient` transport/lost-response positive test is deleted and replaced by callback-call assertions. This is a callback bypass of the production create/init guards and an assertion deletion, contrary to the brief's explicit “no callback bypass” and “no assertion deletion” constraints. It also leaves the focused client tests unable to prove the new wrapper through the real generated method.

Minimal correction: keep the production signatures on the existing API path with no callback parameter; preserve the real transport/lost-response positive test, updating its expectations to the native create/init request sequence. If test injection is unavoidable, keep it in a test-only module/harness rather than a production escape hatch.

## Scope classification

- Product: the native capture/init path and thin `AstridRuntimeClient.createTimeline` wrapper are on the requested seam; same-ID headless repair, headed/non-empty refusal path, stable IDs/keys, metadata aliasing, and existing outbox identity/checkpoints remain represented.
- Tests: the 127 focused tests cover bootstrap capture/init and outbox behavior; the 31 client-neighbor tests pass. The callback replacement is the review blocker.
- Fixture: `recipe_m2_app_bootstrap.json` is 1,672 lines, but it is consumed by the parity and initialization tests and matches the bounded native command/record closure; I found no separate fixture bloat finding.
- Legacy publisher: removal is confined to the proposed `createDefaultTimeline` bootstrap cutover; the client method and other data-provider callers remain.

## Verification

Independent private-copy commands:

```sh
node /tmp/ap2-m2-bootstrap-review.YJyof7/node_modules/vitest/vitest.mjs run --config /tmp/ap2-m2-bootstrap-review.YJyof7/config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/integrations/runtime/bootstrapInitialization.test.ts \
  src/tools/video-editor/commands/bootstrapCapture.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/integrations/runtime/createDefaultTimeline.test.ts
# 4 files, 127 tests passed

node /tmp/ap2-m2-bootstrap-review.YJyof7/node_modules/vitest/vitest.mjs run --config /tmp/ap2-m2-bootstrap-review.YJyof7/config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts
# 2 files, 31 tests passed

git -C <private archived 05b6 copy> apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-bootstrap-currentroot-consumer.patch
# PASS
```

Not run: browser, localhost/live socket, full suite, Runtime-door, or central actual gate. The proposed actual-gate source was inspected; it remains a meaningful positive gate and correctly stays held pending normal014 compatibility, the Agent opaque-inverse repair, and real Door/browser evidence. The four original opaque-inverse positives remain a visible hold, not skipped or xfailed in this App patch.
