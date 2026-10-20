# AP2-M2 bootstrap scope-gate repair

## Result

Built one coherent App bootstrap candidate on latest `hub/tl/integration` by porting the reviewed bootstrap source/lifecycle chain and the missing reviewed fixture prerequisites:

- durable create/init bootstrap source and capture fixture;
- exact owner reservation/recovery semantics, including create ACK/init ACK retention;
- explicit `TimelineScope` and exact created-timeline list selection;
- lifecycle fixture that observes the owner while create/init are pending and verifies it drains after ACK;
- one actual bootstrap consumer gate in `tests/e2e/local/three-products.spec.ts`.

Current integration ports were preserved, including retained-document client/provider paths and existing journey helpers. Public pins, dependencies, shared worktrees, Runtime/Agent sources, and product/shared installations were not changed.

The gate maps the real New Project result, requested name/UI, exact Runtime create path, reserved timeline ID, exact project/timeline owner scope, native history, retry/reload/restart, guarded undo, and zero legacy snapshot traffic. The opaque/pristine refusal controls remain in the pure bootstrap tests; the live browser proof is not claimed.

## Checks

- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/bootstrapInitialization.test.ts src/integrations/runtime/createDefaultTimeline.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/commitOutbox.test.ts` — **PASS, 4 files / 128 tests**.
- `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts` — **PASS**.
- Targeted ESLint over all touched TS/TSX files — **PASS**.
- `npm run typecheck:strict-islands` — **PASS**.
- `npx tsc -p tsconfig.node.json --noEmit` — **PASS**.
- `npx playwright test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.spec.ts` — **PASS, 12 tests listed; exactly one bootstrap gate**.
- `git diff --check` and source guards — **PASS** (no bootstrap production legacy publisher; no build output created).

An initial Vitest invocation with `--configLoader=runner` stopped before collection because the repository config exposes `__dirname` as undefined in that loader. The same targeted command without that loader passed; no test was counted from the failed startup.

## Decisions

Source changes were required: latest integration had the current outbox/provider ports but did not contain the reviewed bootstrap source or create-reservation lifecycle. I ported the reviewed source chain rather than reviving the earlier `252da` scope-only candidate, then layered the `9308` exact-list and `8a408` pending-owner lifecycle fixes. No timeout inflation, forced persistence, arbitrary timeline selection, circular expected, neighboring gate, or dirty-test weakening was added.

## Unverified / blocked

No local browser, socket, Runtime Door, central, full, or neighboring Gate 5 suite was run, as required. The matched private Agent/Runtime provenance tuple (Agent `3c4f6de4`, Runtime `2020741107`, producer `a0dca169`, artifact `f021`, schema `6ba`) and live opaque/zero-legacy browser behavior remain unverified until the harness commits this candidate.

## Later gate

After harness commit, run the one authorized narrowed central suite:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-bootstrap-scope-gate-repair normal014-integration-e2e-gate5) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Do not substitute public013 sources or rerun the earlier failed unchanged candidate.

