# Anonymous manual recovery after the 08:04 decision

Bounded source work complete on App base `f8b8d48248ff1e97a41eb3457c3365c8c873eaf8`. **Runtime-mode/manual-chooser browser acceptance remains open.** No writer retirement or merge is claimed.

## Changes and decisions

- Completed old placement intents with a retained readable image/video show **Placement unconfirmed: place manually** by default. Request params identify a recovery candidate only; they never prove placement outcome, owner, destination or approval.
- The existing exact `completion_follow_up.status=degraded` issue with `step=timeline_placement` and `code=automatic_timeline_placement_retired` is the only path to **Not placed: place manually**. The old marker unit fixture is retained. No marker was added to a canonical Runtime fixture.
- `TaskItem` reads the existing Runtime Task resource through `AstridRuntimeClient.getTask`, verifies task/project/succeeded state, reads its actual `result`, and excludes top-level `generation_intent`. Params containing generation intent are also excluded. No Task DTO, wire schema, endpoint, continuation store, approval or writer was added. Metadata is read before activation; if that read fails, existing media actions remain but the extra placement label does not activate. This avoids classifying an unread bound request as anonymous.
- Image output reads no longer require `outputLocation`. Completed video actions can trigger the existing lazy output read without it. `readBridgeTaskOutputs` now reads/paginates the existing managed-output API, checks task/project/available/object identity and derives display addresses from the actual object ID and media type. The old `result.outputs` migration read is retained for an empty managed list; unavailable/unrelated managed rows cannot resurrect an older output. Errors and repeated cursors propagate.
- The new managed-output path obtains no URL, object identity or generation provenance from request params. Video rows use a parent only from the read row; the pre-existing explicitly marked outputLocation fallback keeps its old behavior. The pre-existing image outputLocation fallback is also retained. Association IDs identify output rows; an object digest is not promoted into a generation/owner identity.
- The extra button calls the existing image/video lightbox navigation handlers. Existing gallery/lightbox actions remain tested. Task row memoization now notices project/params/updatedAt/output changes so a completed read is not permanently stale.

## Authorized expectation corrections — every old/new pair

All historical request objects and output inputs are retained. No test was skipped, disabled or marked expected-to-fail.

| Existing case | Old expectation | New expectation (08:04 authorization) |
| --- | --- | --- |
| Adapter `task-intent`, old placement_intent | presentation null | label Placement unconfirmed: place manually |
| Adapter scoped `task-a`, timeline_placement | presentation null | label Placement unconfirmed: place manually; distinct task-b exact marker expectation unchanged |
| Historical successful timeline_placement handler fixture | presentation null | label Placement unconfirmed: place manually |
| Historical successful placement_intent handler fixture | presentation null | label Placement unconfirmed: place manually |
| Rendered historical timeline_placement row | extra manual button absent | unconfirmed label and existing manual button; old Not placed absence and original lightbox callback assertions retained |
| Rendered historical placement_intent row | extra manual button absent | unconfirmed label and existing manual button; old Not placed absence and original lightbox callback assertions retained |

Every other pre-existing expectation remains. In particular, modern read-projection assertions still prove the list drops result/top-level intent; the new row uses a separate existing Task read instead of adding fields to that projection.

## Exact test commands and results

Working directory: `/home/user/work/wt/app-m2-anonymous-manual-recovery-decided-ui`.
Own node_modules symlink points to standard physical `/tmp/app-m2-coherent-deps8/node_modules`. Shared dependencies were not edited; no overlay/install was needed.

Initial nine-file command:

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.test.ts src/features/tasks/components/TasksPane/__tests__/TaskItem.test.tsx src/features/tasks/components/TasksPane/__tests__/TaskItem.managedOutput.test.tsx src/features/tasks/components/TasksPane/hooks/useTaskItemDisplay.test.ts src/features/tasks/components/TasksPane/hooks/__tests__/useTaskNavigation.test.ts src/features/tasks/components/TasksPane/utils/__tests__/task-utils.test.ts src/integrations/astrid/bridgeTaskReads.test.ts src/integrations/astrid/bridgeTaskOutputs.test.ts src/integrations/astrid/taskReadSchemas.test.ts
```

**9 files / 104 tests passed**, exit 0, 17.81 seconds.

Final expanded direct cohort:

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.test.ts src/features/tasks/components/TasksPane/__tests__/TaskItem.test.tsx src/features/tasks/components/TasksPane/__tests__/TaskItem.managedOutput.test.tsx src/features/tasks/components/TasksPane/hooks/useTaskItemDisplay.test.ts src/features/tasks/components/TasksPane/hooks/__tests__/useTaskNavigation.test.ts src/features/tasks/components/TasksPane/utils/__tests__/task-utils.test.ts src/integrations/astrid/bridgeTaskReads.test.ts src/integrations/astrid/bridgeTaskOutputs.test.ts src/integrations/astrid/taskReadSchemas.test.ts src/integrations/runtime/recordedResponses.test.ts src/features/tasks/components/TasksPane/RuntimeTaskList.test.tsx src/features/tasks/components/TasksPane/RuntimeActivityDock.test.tsx src/features/tasks/components/TasksPane/hooks/useRuntimeTasks.test.ts
```

First attempt: **155 passed / 1 failed**, 13 files, exit 1, 26.72 seconds. The new managed-read rejection test exposed an implicit `beforeEach` return: Vitest treated the returned mock as teardown and invoked the rejected mock during cleanup. Isolated confirmation:

```sh
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/integrations/astrid/bridgeTaskOutputs.test.ts --reporter=verbose
```

**7 passed / 1 failed**, exit 1, 1.48 seconds, same hook bug. Changed the hook bodies to return void; kept the rejection expectation.

Final expanded cohort rerun, same exact command above: **13 files / 156 tests passed**, exit 0, 25.04 seconds. Includes unchanged neighbouring Runtime task-list/dock/actions suites and recorded-response contracts. Test counts are distinct final cases, not summed across reruns.

```sh
./node_modules/.bin/eslint src/features/tasks/components/TasksPane/TaskItem.tsx src/features/tasks/components/TasksPane/hooks/useImageGeneration.ts src/features/tasks/components/TasksPane/hooks/useTaskContentType.ts src/features/tasks/components/TasksPane/hooks/useVideoGenerations.ts src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.ts src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.test.ts src/features/tasks/components/TasksPane/__tests__/TaskItem.test.tsx src/features/tasks/components/TasksPane/__tests__/TaskItem.managedOutput.test.tsx src/integrations/astrid/bridgeTaskOutputs.ts src/integrations/astrid/bridgeTaskOutputs.test.ts --max-warnings 0
git diff --check
```

Both passed, exit 0. ESLint was also clean before the final hook correction. No full suite, build, tsc, install, browser, localhost server, live socket or Runtime suite was run/requested.

## Evidence boundary

The new `TaskItem.managedOutput.test.tsx` runs the real task projection, real image/video hooks, real managed-output read adapter and real navigation handlers against normal typed Runtime Task/ManagedOutput values. One video case uses the vendored daemon `managed_outputs_200` page **unchanged**; the recorded queued Task is explicitly adapted to succeeded with historical placement params. It does not invent completion metadata. Other cases cover image recovery/reopen, video hover/action, and a top-level bound generation request retaining old params. The fixtures prove normal shapes and callback behavior, not a live producer or a browser chooser.

Runtime clients are mocked at their public methods in these UI cases. Preview/tooltip wrappers, task-type/resources/project providers are mocked, and lightbox callbacks are spies. **No live read, actual MediaLightbox/shot chooser rendering, placement commit, or modern bound continuation lifecycle execution is claimed.** The ordinary old icon and manual button both reach the same existing callback. The unit marker fixture proves recognition only; it does not establish a readable retired task in the current tuple.

Inspected current Runtime `runtime_protocol/service.py` still returns stored Task result. `rg` found no `completion_follow_up` or `automatic_timeline_placement_retired` producer/read mapping under current Runtime `runtime_protocol` or conformance responses. The App Supabase migration helper still persists completion follow-up to result_data. No actual current public retired Task/result response was captured. Unknown wording is therefore the supported claim for an old output without proof.

## Exact remaining seams and next step

These are proposals for the owning manager, not changes in this worker:

1. `TasksPane.tsx:633` selects RuntimeTaskList when runtimeProjectId is present; its activity dock also uses RuntimeTask objects. Both bypass legacy TaskItem. `RuntimeTaskList.tsx` has Inspect/export/cancel/retry only; `RuntimeActivityDock.tsx` lists managed result filenames. Add the same recovery presentation to these existing Runtime Task surfaces and pass a local `onOpenManagedTaskOutput(task, output)` callback from TasksPane. Consume their actual Task.result and existing managed-output reads; keep generation_intent tasks in their existing lifecycle. This is an existing product wiring change, with no wire/DTO fields.
2. Connect that callback to the existing TasksPane MediaLightbox and shotWorkflow chooser using only the actual read output. `useShotActions` currently accepts a **generation ID**. The recorded normal managed output has `generation_id: null`. An association ID/object digest cannot be used as a generation ID or placement authority. The owning manager must qualify an existing authoritative generation/variant read when present, or the existing immutable media-selection/manual command seam for such an output. Do not infer lineage from params or add a writer/authority here.
3. Match the contract tuple and hosted artifact before requesting the single focused browser case. At inspection, App base metadata is 0.2.1 / `4e52f7df017db99483ffcd0c593ce414b6443d5d0214ada943bb26fdfcc1714d`, Agent integration is 0.2.3 / `a435dde3b552999ea75ff593868ff4d56debdd64bd8f79c134fb470a279a05e6`, and Runtime integration is `8d7f29873ff3417cda746e243ebc81cb9d54e41c972596d4d3ae591fc1de00cf`. Observed heads: Agent `408f3ba3f60dda8fcecfcf4384048114c487a5fb`, Runtime `94114269d1ce23ab3224d7eca5a85138ce2b5fed`, Composition `5e06f40146573a529896cc812229eb890c53c81a`. These moving integration heads were read, not modified or qualified.

A focused **unapplied, unexecuted draft patch** adding one case to the existing three-products editing spec is retained at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-anonymous-manual-recovery-decided-ui/notes/anonymous-manual-recovery.browser.patch`. It creates and completes an actual CPU marker task with old params, reads the actual Task and managed output, expects unconfirmed/manual chooser with no canonical write/retry, reopens, then explicitly places the same output through Agent and reloads to ensure it is never labelled Not placed. This is a specification for the missing seam; selectors/admission details remain unverified. It does not fabricate a retired canonical response, add a test skip or alter the active browser suite. The real retired-marker browser branch still needs a genuine existing readable retired response; the bound lifecycle needs its real producer/continuation journey.

Use the central service only for that focused spec after the owner supplies the surface wiring and matched tuple. No broad suite request is useful while these prerequisites are missing. Keep the source candidate and staged patch for review; do not count this worker as manual-recovery browser acceptance or writer retirement.
