# App automatic-placement operation/client lifecycle adapter

Status: binding delta complete on App HEAD `316073355a67d46f98168ec2152141e0748198a9`; production automatic placement remains visibly unavailable until the real browser/Runtime gate.

## Source delta

- `src/integrations/runtime/operationHost.ts` now exposes the already-negotiated operation's capability, project-object, verified-media, and exact prepared-task methods. The generated `WorkspaceClient` is constructed with the operation's existing `Transport`; it performs no discovery or credential selection of its own.
- `src/integrations/runtime/clientLocalAdapter.ts` adapts those methods to the existing `AstridLocalClient` task surface (`catalog`, `objects`, `tasks`) used by reserved task routes. Admission uses the task route's canonical envelope order, reserves before POST, sends the exact saved body/key, validates project/capability response identity, and retains the existing reservation callbacks.
- `createEditorImagePlacementHost()` binds the operation to the editor's project and exposes the operation's synchronous `isCurrentIdentity` check. `commitSession` retires that host before releasing the claimed editor outbox/session, so late task/media/commit callbacks cannot use the old binding.
- `useTimelineCommandSession` now passes the optional editor host through the existing session seam. The App production caller intentionally supplies no host yet, so the checked-placement modal continues to show `IMAGE_PLACEMENT_UNAVAILABLE` and makes no task request.

No endpoint, header, DTO, authority store, generated source, second outbox, browser credential, parent-owner inference, or provider/root/product redesign was added. The operation still pins its upstream, credential, actor/realm, and Runtime instance; all bound reads/admission/transmit use its handle and retirement fences.

## Tests

Using the read-only shared dependency link, `--no-cache`, one worker, and the worker-owned temporary directory:

```sh
TMPDIR=/tmp/app-m2-auto-host-client-lifecycle-adapter-cache node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/runtime/operationHost.test.ts src/integrations/runtime/clientLocalAdapter.test.ts src/tools/video-editor/commands/autoCapture.test.ts src/tools/video-editor/commands/nativePlacementCapture.test.ts src/tools/video-editor/commands/placementRequester.test.ts src/tools/video-editor/components/EditorImageGeneration.test.tsx src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.test.ts
```

Result: **8 files / 484 tests passed**, exit 0. Scoped ESLint over all changed source/test files passed with `--max-warnings 0`; `git diff --check` passed. No full suite, project typecheck, build, browser, localhost/socket, install, or central live gate was run.

## Remaining real gate and boundaries

Before activation, the central service must qualify the matched Agent/Runtime pair with real task acceptance, current S2 occurrence-image completion and five-field media selection, reconnect/reload, lost admission/commit acknowledgement and exact retry, canonical reload, guarded undo/redo/ABA, retirement/claim races, and zero legacy traffic. Automatic production activation remains held; parent automatic placement waits for the next reviewed official pair. The checked modal must remain visibly unavailable until those proofs pass.

The legacy writer remains `src/shared/lib/placement/placementService.ts:placeGeneration`, reached through `src/shared/hooks/shots/addImageToShotHelpers.ts:runAddImageMutation` and `src/shared/hooks/shots/useShotGenerationMutations.ts`. This delta does not claim or perform its retirement.
