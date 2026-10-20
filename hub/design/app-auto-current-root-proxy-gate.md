# App automatic placement on current root: real-proxy gate

## Final source and tree

- Current App root before composition: `9d518546d` (includes root `3599fc49a`).
- Approved production requester loop: `c34cf6ae4`, prospective source tree `9e8e48c32808d052f2ee79e7fbac65029993af9c`.
- Approved real-proxy source: `13c0934b4` (the parent of `c34cf6ae4`).
- Central test snapshot of this worktree: `15a588ac77216fc6e8e6799a3751081699aff1ee`.
- Central pair: Agent `8130a401bf44a518d5a40ae274d398b8c560be55` / Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a2`, public12 dependency graph, Chrome 141.

The composition carries the real operation host/client, requester, native verified capture, existing session/outbox pump, completion discovery, receipt projection/Undo ownership, and the real Vite discovery-proxy browser source. Current-root cold readiness was retained: `initialReadReady` and recovery gating remain in `useTimelineCommandSession`/`useTimelineSave`, with the approved image-placement host propagated through that gate.

## Controls and targeted evidence

Passed:

```text
node --check scripts/runtime-discovery-proxy.mjs
node --test --test-name-pattern='^pure:' scripts/runtime-discovery-proxy-operation.test.mjs
/home/user/work/app/node_modules/.bin/eslint --no-cache --max-warnings 0 playwright.auto-real-proxy.config.ts tests/e2e/local/auto-real-proxy.spec.ts src/features/tasks/components/TasksPane/hooks/useRuntimeTaskEvents.ts src/integrations/astrid/taskRoutes.ts src/integrations/runtime/clientLocalAdapter.ts src/integrations/runtime/operationHost.ts src/integrations/runtime/dataProvider.ts src/tools/video-editor/commands/autoCapture.ts src/tools/video-editor/commands/commitOutbox.ts src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/editorImagePlacement.ts src/tools/video-editor/commands/nativePlacementCapture.ts src/tools/video-editor/commands/placementRequester.ts src/tools/video-editor/commands/sessionPlacement.ts src/tools/video-editor/components/EditorImageGeneration.tsx src/tools/video-editor/contexts/VideoEditorProvider.tsx src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/hooks/useTimelineSave.ts
git diff --check
```

Passed targeted Vitest command (12 files):

```text
node --import /tmp/app-m2-auto-current-root-proxy-gate-vitest-preload.mjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  src/tools/video-editor/commands/commitSession.placement.test.ts \
  src/tools/video-editor/commands/commitSession.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts \
  src/tools/video-editor/commands/nativePlacementCapture.test.ts \
  src/tools/video-editor/commands/placementRequester.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/integrations/runtime/clientLocalAdapter.test.ts \
  src/integrations/runtime/operationHost.test.ts \
  src/features/tasks/components/TasksPane/hooks/useRuntimeTaskEvents.test.tsx \
  src/tools/video-editor/components/EditorImageGeneration.test.tsx \
  src/tools/video-editor/contexts/VideoEditorProvider.test.tsx
```

Result: **428 passed, 12 files, exit 0**.

## Central real browser result

Registered and ran the new literal suite:

```text
e2e-auto-current-root3599-tree-final-agent8130-runtime2c4-public12-e2e-integration
```

Test ID: `app-m2-auto-current-root-proxy-gate-e2e-auto-current-root3599-tree-final-agent8130-runtime2c4-public12-e2e-integration-1020153313-6990`

Result directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-auto-current-root-proxy-gate-e2e-auto-current-root3599-tree-final-agent8130-runtime2c4-public12-e2e-integration-1020153313-6990/`

The run stopped before browser execution with the first real final-tree API mismatch:

```text
SyntaxError: The requested module './support/harness.ts' does not provide an export named 'ASTRID_CHECKOUT'
Error: No tests found
```

`tests/e2e/local/auto-real-proxy.spec.ts` imports `ASTRID_CHECKOUT` (and `ASTRID_PYTHON`, `RUNTIME_CHECKOUT`, `ASTRID_PYTHON`) from `tests/e2e/local/support/harness.ts`; the current-root harness exports `RUNTIME_CHECKOUT` and `PRODUCT_ACTOR`, but no `ASTRID_CHECKOUT` or `ASTRID_PYTHON`. No browser assertion ran, and the gate is not a qualification pass.

## Main behaviors remaining unverified

Because of that source/API mismatch, the central run did not verify the real dynamically selected Vite origin authorization, GenericPackHost image capability/output, actual operation-handle task route, exact preadmission task body/key/approval/basis, reconnect and Runtime/Vite restart, completion discovery, verified media, canonical commit/readback, lost admission/commit ACK exact retry/receipt, reload, Runtime-owned Undo, or zero legacy traffic. No placement-row retirement claim is made.

No full suite, TypeScript check, install, build, or framePCM run was performed.
