# App M2 automatic-placement production owner

## Candidate

- Worker worktree: `/home/user/work/wt/app-m2-auto-production-operation-owner`
- Base candidate commit: `25e828af6d96f2cc0182a5014eb90ebeab4fec11`
- Base candidate tree: `3b69f7cb30daca7bf498519acae32b5827ccaad5`
- Uncommitted candidate diff SHA-256: `e4e5f1df050cc83d7906bdd9f8f62f45efc07740af82203c061a8271ee05d3f5`
- Candidate diff: 3 App files, `+27/-2`; no integration merge or activation claim.

## Actual owner path

`VideoEditorProviderInstance` creates one `RuntimeOperationHost` per keyed editor lifecycle, calls `bindEditorImagePlacementHost(operationHost, projectId)` for a non-null project, and exposes only the resolved host through `VideoEditorRuntimeContext`. The effect retires the exact host on scope cleanup; the existing keyed provider lifecycle covers project, timeline, user, and data-provider identity changes. React Strict Mode is safe because each effect setup creates a fresh host.

`useTimelineSave.ts:41` consumes that context host and passes it at `useTimelineSave.ts:100` into the existing `useTimelineCommandSession` options. The existing command session owns the same `EditorImagePlacementHost` and outbox, and `commitSession.dispose()` retires it before releasing the editor claim. Failed negotiation and hosted/remote Runtime origin leave the host absent, so `EditorImageGeneration` retains the existing visible unavailable/refuse-draft behavior.

The existing adapter continues to enforce the approved operation contract: task catalog, admission, managed/object/media reads, and timeline transmit use the operation's pinned transport/handle; exact request bytes and idempotency keys are reserved durably before admission; synchronous identity/claim checks fence callbacks; S2 occurrence-image placement remains the only supported automatic-placement scope.

## Evidence

- `TMPDIR=/tmp/app-m2-auto-production-operation-owner-cache node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/runtime/clientLocalAdapter.test.ts src/integrations/runtime/operationHost.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx` — 5 files / 149 tests passed.
- `TMPDIR=/tmp/app-m2-auto-production-operation-owner-cache node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx` — 3 files / 38 tests passed.
- Scoped ESLint over the 5 changed/adjacent implementation files — passed.
- `git diff --check` — passed.

## Remaining central gate

Integration activation remains held. Central qualification must use the matched official Agent/Runtime pair and the existing actual proxy handler/harness with a real same-origin local Runtime: modal admission and completion for an S2 occurrence image, exact task/commit retry after lost acknowledgement on a fresh equal-actor/realm binding, reconnect/reload, durable outbox recovery, undo/redo/ABA guards, retirement races, and zero legacy automatic-placement traffic. Hosted/remote operation remains intentionally unavailable. Parent automatic placement waits for the next normal reviewed S3 pair. No browser, localhost/socket, full-suite, project typecheck, build, or live Runtime qualification was run here.
