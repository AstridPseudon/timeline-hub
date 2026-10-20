# Completed task output read

## What changed

- Removed the legacy `Task.outputLocation` requirement from completed image and video output hooks.
- Removed image/video pseudo-output fallbacks that fabricated a media row from `outputLocation`.
- Kept output discovery on the existing `tasks.get` → Runtime `result.outputs` → `readBridgeTaskOutputs` path.
- Made the existing output association reader fail closed for a mismatched task ID, mismatched project, non-succeeded task, or missing outputs.
- Added a normal-read component regression: `runtimeTaskToSummary` produces a completed `Task` without `outputLocation`, then the real detail/output read loads the managed output and opens the existing image lightbox callback.
- Preserved the existing legacy-placement label behavior: intent/request parameters do not infer `Not placed`; the retired completion marker remains unavailable on the current public `Task` projection, so label activation is still held.

## Validation

Exact targeted command:

```sh
npm exec vitest -- run src/integrations/astrid/bridgeTaskOutputs.test.ts src/features/tasks/components/TasksPane/__tests__/normalTaskOutputRead.test.tsx src/features/tasks/components/TasksPane/__tests__/TaskItem.test.tsx src/features/tasks/components/TasksPane/utils/legacyAutoPlacementPresentation.test.ts src/features/tasks/components/TasksPane/hooks/useTaskItemDisplay.test.ts src/features/tasks/components/TasksPane/utils/__tests__/task-utils.test.ts src/integrations/astrid/bridgeTaskReads.test.ts src/integrations/astrid/taskReadSchemas.test.ts --config config/testing/vitest.config.ts --maxWorkers=1
```

Result: **8 files passed, 100 tests passed, exit 0**.

Exact static checks:

```sh
npm exec eslint -- src/integrations/astrid/bridgeTaskOutputs.ts src/integrations/astrid/bridgeTaskOutputs.test.ts src/features/tasks/components/TasksPane/hooks/useImageGeneration.ts src/features/tasks/components/TasksPane/hooks/useVideoGenerations.ts src/features/tasks/components/TasksPane/hooks/useTaskContentType.ts src/features/tasks/components/TasksPane/__tests__/normalTaskOutputRead.test.tsx --max-warnings 0
git diff --check
```

Both passed, exit 0.

## Decisions and limits

- The output association is accepted only from the validated task detail and its recorded `result.outputs`; no URL, primary variant, identity, or placement was inferred from request parameters.
- Wrong-task/project detail responses are rejected before media rows are mapped. Non-terminal and output-less reads return no output rows.
- Multi-output behavior remains on the existing output association and lightbox path; no gallery-latest lookup, server/wire/DTO field, provider write, resolver, or cache framework was added.
- No full suite, build, browser, localhost/server, live-socket, TypeScript, or dependency-install run was performed. Actual current-tuple UI/server proof remains unqualified as required by the task brief.
