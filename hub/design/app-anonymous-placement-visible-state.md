# App anonymous automatic-placement visible state

## Result

The App task row now presents a completed legacy automatic-placement request as
`Not placed: place manually` when the task still has an output. The state is
scoped to the task row and its resolved output; it does not choose a project,
timeline, owner, approval, primary variant, or destination. The output remains
available to the existing task gallery/lightbox. The manual button opens the
existing image/video lightbox path, whose existing shot selector performs the
manual placement action.

## Exact source fields and paths

- Reachable legacy request fields: `Task.params.placement_intent` and
  `Task.params.timeline_placement`. They are carried by the public bridge task
  `spec.params` and projected by
  `src/integrations/astrid/bridgeTaskReads.ts::bridgeTaskSummaryToTask`.
- Retired completion metadata is written by
  `supabase/functions/complete_task/completionHelpers.ts::persistCompletionFollowUpIssues`:
  `result_data.completion_follow_up = { status: 'degraded', recorded_at,
  issues: [{ step: 'timeline_placement', code:
  'automatic_timeline_placement_retired', message }] }`.
- The exact marker is accepted by the pure adapter in
  `src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.ts`.
- The row presentation and existing manual action are in
  `src/features/tasks/components/TasksPane/TaskItem.tsx`; the action delegates
  to `useTaskNavigation`'s existing `handleViewImage` / `handleViewVideo`.
- Existing manual shot placement remains in
  `src/features/tasks/components/TasksPane/hooks/useShotActions.ts` and is
  passed to `MediaLightbox` in `src/features/tasks/components/TasksPane/TasksPane.tsx`.

## Public-read gap

The current bridge contract at
`src/tools/video-editor/data/bridgeContract.ts::bridgeTaskSummarySchema`
exposes optional `result`, not the legacy Supabase `result_data` field. The
bridge task mapper does not project `result` into `Task`, and `Task` has no
`resultData` field. Therefore `completion_follow_up` does not currently reach
the task UI through the public task read. No wire/provider/snapshot change was
made. The adapter test exercises the exact persisted `result_data` shape so a
future existing read projection can pass it without inventing a protocol field.

The currently reachable `placement_intent` / `timeline_placement` fields are
enough to show the bounded state for old completed tasks with a retained output.
Failed, pending, cancelled, and completed-without-an-output tasks are not
labelled as successful legacy recoveries. Tasks with current generation
bindings but no old request or retired marker are not labelled.

## Evidence

- `npm exec vitest -- run src/features/tasks/components/TasksPane/__tests__/TaskItem.test.tsx src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.test.ts src/features/tasks/components/TasksPane/hooks/useTaskItemDisplay.test.ts src/features/tasks/components/TasksPane/utils/__tests__/task-utils.test.ts --config config/testing/vitest.config.ts --maxWorkers=1`
  — 4 files passed, 56 tests passed.
- `npm exec eslint -- src/features/tasks/components/TasksPane/TaskItem.tsx src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.ts src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.test.ts --max-warnings 0`
  — passed.
- `git diff --check` — passed.

Per the worker brief, no full suite, build, browser, TypeScript check, install,
server, or snapshot/provider/Runtime wire test was run.
