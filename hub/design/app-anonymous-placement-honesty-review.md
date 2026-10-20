# Anonymous placement honesty review

Verdict: **APPROVE the bounded honesty fix; HOLD label activation and anonymous manual-recovery acceptance.** The prior design's statement that request parameters suffice to identify an unplaced output is false. No owner decision was changed: old unbound requests must not be retroactively auto-placed, and their assets still require a visibly recoverable manual path. This review does not establish that complete user journey.

## Counterexample and fix

Base App: `96849abcce8bfd6b0822f14a4d06f31cbf97d800` (`tl/app-m2-anonymous-auto-placement-visible-state`). Original main reference inspected: `580508eed1bf6ed95caaf476c9d69a4672472a2f`.

`git show origin/main:supabase/functions/complete_task/handler.test.ts` contains two successful historical fixtures:

- `attempts legacy timeline insertion when timeline_placement is present in task params` (line 380): request includes `timeline_id=timeline-1`, `source_clip_id=clip-source-1`, `target_track=V1`, `insertion_time=12.5`, `intent=after_source`. It asserts asset registration, clip addition, successful versioned save, and no persisted follow-up issues.
- `places a completed asset after the live anchor clip when placement_intent is present` (line 564): request includes `anchor_generation_id=gen-source-1`, `anchor_variant_id=variant-source-1`, relation `after`, preferred/fallback track `V1`, fallback time `22.25`. It asserts placement after the live anchor at `10.5`, successful save, and no persisted follow-up issues.

The original handler retains these params and completes the task/output. Replaying both exact parameter objects with `Complete`, an available asset, and empty legacy result data through the pre-fix adapter incorrectly returned `Not placed: place manually`. Both regression cases failed before the fix. Historical handler fixtures were inspected, not re-executed against historical main.

The adapter now requires the existing exact retired-completion marker; parameters alone never activate it. No task DTO, mapper, provider, writer, queue, approval, destination, or retry behavior was added. `TaskItem.tsx` and the existing manual placement implementation are unchanged. Its current invocation does not supply the marker, so this deliberately holds the label inactive on current public reads.

New rendered-row tests use both historical request objects and retained output, then click the real existing image action through the real navigation hook and verify the lightbox callback. Data-fetch hooks and preview/tooltip wrappers are mocked; this is component evidence, not a browser or current-tuple acceptance run.

## Current read facts and precise gap

Inspected Runtime source head: `84be33cf5422f2df49d8b0e069982d9616cfebb3`.

1. `AstridLocalTaskRoutes.list/get` actually read `/v1/projects/:project/tasks` and `/v1/tasks/:task`. The older mapper comments about bridge routes are stale.
2. Runtime `contract/schemas/task.json` is closed at the task level and explicitly permits optional `result`, whose object contents are open. `runtime_protocol/service.py::_task_resource` returns the stored task result when present. The schema permits a marker inside result; that does not prove any task actually has it.
3. App `runtimeTaskReadResourceSchema` validates that resource. `bridgeTaskSummarySchema` also permits optional `result`. However, `runtimeReadModels.ts::runtimeTaskToSummary` drops result on the actual list path. `runtimeTaskToDetail` retains result and derives outputs from `result.outputs` on the detail path.
4. `bridgeTaskReads.ts::bridgeTaskSummaryToTask` retains `spec.params`, but drops result even if its input has one. App `Task` has no result projection. The modern canonical-read regression verifies the list projection drops result, preserves legacy-shaped params, and does not label the rendered row unplaced. It uses top-level canonical `generation_intent`, not a fabricated retirement field.
5. Modern generation authority and local continuation ownership cannot be inferred from legacy-shaped generation params. Removing params as a trigger also prevents a continuation-bound request with those same params from being classified as old. No continuation store or authority was read or changed; an actual bound-continuation journey was not executed.
6. The retirement marker is currently written into Supabase `tasks.result_data.completion_follow_up` by `complete_task/completionHelpers.ts`, with degraded status and issue `{step: timeline_placement, code: automatic_timeline_placement_retired, message: ...}`. No inspected current Runtime producer/read or captured fixture demonstrates that Supabase marker in Runtime `result`. Runtime `runtime_protocol` contains no `completion_follow_up`/`result_data` mapping. The checked-in Runtime `conformance/responses/task_read_200.json` is a queued resource without result; the existing App `bridgeTaskOutputs.test.ts` fixture proves committed `result.outputs`, not retirement metadata.
7. There is an additional asset-read limitation: `bridgeTaskSummaryToTask` does not set `outputLocation`, while `useImageGeneration` enables its output read only when that field exists. The row tests supply/mock a resolved asset; they cannot establish real current-list image recovery. No output URL was inferred from an opaque result or request.

Consequently there is no verified existing read fact distinguishing an unknown historical placement outcome from a completion whose automatic placement was retired. Merely forwarding an optional result would not establish that fact. No marker was injected into a canonical fixture to make activation appear reachable.

## Explicit correction of prior worker expectations

All 51 tests predating the visible-state worker remain unchanged. Of that worker's five new adapter tests, two contained unqualified bug expectations; their original inputs are retained:

- `shows a reachable old placement request without interpreting its target`: same `task-intent` / `placement_intent` / complete / asset input; changed expected label to null and renamed to describe unknown outcome.
- `keeps the presentation scoped to the task and output item`: same `task-a` / `timeline_placement` input now expects null; the `task-b` exact retired-marker expectation remains intact, as does the distinct-result assertion.

The other three original adapter tests and every pre-worker expectation remain intact. The original four-file cohort now has 62 tests (56 original cases, including the two authorized corrections, plus six regressions); the neighbouring read suites add 33, for 95 passing cases total.

## Exact validation

Before the fix:

```sh
npm exec vitest -- run src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.test.ts --config config/testing/vitest.config.ts --maxWorkers=1
```

Result: 5 passed, 3 failed. The failures were the two historical-success counterexamples and a retained-generation-params case.

First post-fix cohort run:

```sh
npm exec vitest -- run src/features/tasks/components/TasksPane/__tests__/TaskItem.test.tsx src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.test.ts src/features/tasks/components/TasksPane/hooks/useTaskItemDisplay.test.ts src/features/tasks/components/TasksPane/utils/__tests__/task-utils.test.ts --config config/testing/vitest.config.ts --maxWorkers=1
```

Result: 60 passed, 2 failed because the new lightbox tests queried a nonexistent icon test ID. Corrected the test selector to the rendered existing button; expectations and product code were unchanged by that correction.

Final targeted run:

```sh
npm exec vitest -- run src/features/tasks/components/TasksPane/__tests__/TaskItem.test.tsx src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.test.ts src/features/tasks/components/TasksPane/hooks/useTaskItemDisplay.test.ts src/features/tasks/components/TasksPane/utils/__tests__/task-utils.test.ts src/integrations/astrid/bridgeTaskReads.test.ts src/integrations/astrid/bridgeTaskOutputs.test.ts src/integrations/astrid/taskReadSchemas.test.ts --config config/testing/vitest.config.ts --maxWorkers=1
```

Result: **7 files passed, 95 tests passed**, exit 0 (11.08 seconds).

```sh
npm exec eslint -- src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.ts src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.test.ts src/features/tasks/components/TasksPane/__tests__/TaskItem.test.tsx --max-warnings 0
git diff --check
```

Both passed, exit 0. No full suite, build, browser, localhost service, TypeScript check, dependency install, Runtime test or write was run.

## Recommendation / remaining acceptance

Keep activation HOLD. The orchestrator should obtain an actual current public task response demonstrating trustworthy completion outcome and retained asset availability, then qualify only a supported existing local read projection. If no such data exists, the exact `Not placed` claim cannot activate under this scope; a neutral unknown-outcome presentation needs an explicit product decision. Do not recover authority from params or auto-place old tasks.

Actual current-tuple UI execution is still required through the central service: historical successfully placed output must never say unplaced; a genuinely retired unbound completion must retain a selectable asset/manual shot-placement path; a modern bound continuation with legacy-shaped params must retain its own lifecycle. Include reopen/reload and verify no automatic retry or canonical write occurs before explicit manual selection. This worker's review/fix is complete; the activation and acceptance gaps above remain HOLD.
