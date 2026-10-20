# Selected PARAM actual-control ingress — source stage

Base: `5541998086415c7b1794d83cc579f06f89712c66` (reviewed recovery follow-up). Worktree: `/home/user/work/wt/app-m2-selected-param-production-ingress-stage`. **D01 remains OPEN; source-only, no writer retirement or production qualification.**

## Implementation and decisions

- Added optional `TimelineOps.setClipParams(clipId, args, signal?)`, using the existing generated `ClipSetParamsArgs` input. It captures one exact raw parent/stable occurrence binding through the existing session, copies the structurally checked native command before asynchronous reads, prefetches at its original `schema_source`, and submits against that same captured basis. No recapture, basis-flag promotion, latest read, command-body addition, local PARAM execution, Ajv, Agent browser export, or semantic validator.
- Wired the existing session port into `useTimelineOps` in `useTimelineState` (one line). Existing `apply`/preview/snapshot routes are unchanged. Selected session, compiler, outbox, recovery, retry, inverse and transport implementations are untouched.
- The actual `AstridElementParams` form accepts an explicit `retainedDocumentPin`, `timelineOps`, and live `commandState` binding through the existing `ClipPanel` props. With that pin it renders controlled raw JSON parameter fields and explicit Apply. Only edited keys enter native `values`/`clear`; a blank field explicitly clears. Numeric 16 is parsed as 16 and reaches the provider unchanged, independent of schema min/max/defaults. JSON parse/finite-JSON/native-input-shape checks are structural only; operational input-read/basis/pin failures keep the visible draft.
- Accepted values are displayed separately from raw input drafts. Pending reads and the existing session PENDING/error/conflict are visible; PARAM state is installed only through the existing provider-closure projection. New typing while awaiting ACK survives; accepted draft fields are cleared individually, preventing stale previously accepted values from being resent with a later unrelated edit.
- Retain only display hints for the explicit single binding through live pack replacement/removal. These hints neither authorize nor normalize input. The original retained pin stays fixed. Closing/changing the form target aborts its unfinished read before submission; an already submitted command remains owned by the existing session/outbox lifecycle.
- The existing form without the explicit pin binding keeps its original behavior and tests. This is a bounded source stage: no root installs the pin/state binding or `paramReadClient` here, and the ordinary selected writer remains until the separately qualified migration. No interception of generic scalar/default/mixed patch batches was added.

## Exact allowlist and size

Only these seven repository paths changed:

- `src/sdk/video/timeline/timelineOps.ts`
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx`
- `src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx`
- `src/tools/video-editor/hooks/useTimelineOps.ts`
- `src/tools/video-editor/hooks/useTimelineState.ts`
- `src/tools/video-editor/components/PropertiesPanel/SelectedElementParamFields.tsx`
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.selected.test.tsx`

Six product paths: **+137 / -7, net +130 lines**. Scoped physical product-path census (including pre-existing surrounding hook code): origin/main `44f0b9ca9` = 2,449; reviewed base = 2,485; current = 2,615. This is a task-local census, not an App-wide/M4 census. Tests and generated clients are excluded. New direct test file: 310 lines; every pre-existing source test is byte-identical to the reviewed base.

Read upstream `44f0b9ca9` with `git show`/`git diff`; no main merge. `AstridElementParams` and the SDK interface have no competing main change. `ClipPanelBody` differs for upstream duration/touch/optional-move behavior: port only this type import and the three optional binding props, preserving refreshed main behavior. `useTimelineOps` already differs from main for the reviewed track-label ingress; preserve it and add this separate method. `useTimelineState` has upstream layout/render/precision differences: port only the one `clipParamsPort` option next to the existing session adapter options; never replace that file or merge this old tree wholesale.

## Contract mismatch found

The assigned base's `generated-contract-metadata.ts` says **0.2.8**, although the brief calls the existing types 0.2.9. Read-only comparison against `tl/app-m3-runtime029-app-normal-pin` (whose metadata is 0.2.9) proves these five declarations byte-identical: `ClipSetParamsArgs`, its two variants, `DocumentPin`, and `EditCommand`. The implementation reuses those native declarations. No client/pin/generated file changed. This is a composition prerequisite to report, not grounds to invent a DTO or change the settled source-only scope.

## Evidence

All Vitest runs use private config/cache/output under this worker's `notes`, `--configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism`, and a private extraction of this worktree's existing Composition 0.0.12 tarball. Shared node_modules and its caches were read-only. Private extraction/cache is removed after the runs; reproduce with `python NOTES/prepare-test-env.py`, replacing NOTES with the absolute worker notes path below.

CWD for all commands: `/home/user/work/wt/app-m2-selected-param-production-ingress-stage`.

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-production-ingress-stage/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.selected.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.shader.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.sequence.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.astridCatalog.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.test.tsx > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-production-ingress-stage/notes/targeted-final.log 2>&1
```

PASS: 19 files / 398 tests, 65.11 s. This includes all original 8 files / 241 tests, the 17 new mounted UI/SDK cases, and neighbouring existing scalar/default/sequence/inspector/track-label positive tests.

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-production-ingress-stage/notes/vitest.counterexamples.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-production-ingress-stage/notes/counterexamples.log 2>&1
```

PASS: unchanged external 4 controls, 3.43 s.

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-production-ingress-stage/notes/vitest.probes.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-production-ingress-stage/notes/probes.log 2>&1
```

PASS: unchanged external 2 recovery repros + cancellation/new-capture positive (3 tests), 3.60 s.

```bash
node node_modules/eslint/bin/eslint.js src/sdk/video/timeline/timelineOps.ts src/tools/video-editor/hooks/useTimelineOps.ts src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx src/tools/video-editor/components/PropertiesPanel/SelectedElementParamFields.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.selected.test.tsx --max-warnings 0 > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-production-ingress-stage/notes/lint.log 2>&1
```

PASS: exit 0, zero warnings.

```bash
git diff --check
```

PASS: exit 0.

The 17 new cases cover mounted accepted8/PENDING/last-accepted4 and newer raw typing, raw16 under retained V1 despite V2 hints with typed 409/422/conflict refusal, invalid JSON and correction/clear, pin mismatch, live hint removal, recoverable read error, malformed native SDK shape/non-finite JSON, basis changes during reads, form close/cancel during reads, the permanent original false basis after ordinary ACK, detached SDK args/pin/expression literals, and later unrelated edits preserving newer accepted values.

Read-only checks also verified every pre-existing source test file byte-identical to `5541998086415c7b1794d83cc579f06f89712c66`, both external test files byte-identical to the reviewed follow-up copies, and the five native type declarations byte-identical to the separate 0.2.9 pin branch. No test was weakened, skipped, deleted, or changed to expect refusal.

Earlier development checks: an initial four-file run had two new assertion errors (an ambiguous status query due to output elements' implicit status roles, and an incorrect expectation that `flush` resolves for a deliberately unsent original basis). Only these new assertions were corrected; subsequent narrower runs passed (83 and 17 tests). A 19-file 397-test pass preceded the final stale-draft regression/dirty-label refinements; the final 398-test run above is on the final source. No test-service/full rerun was requested.

## Unqualified / next step

No full suite or test-service request, install, build, browser, localhost/live socket, project `tsc`, native Agent provider process or Runtime process was run. The mounted UI tests use the real App session, native command builders, outbox, retained-input adapter, SDK hook and normal-port transport with deliberately synthetic acceptance/refusal specimens. They do **not** establish native schema semantics, actual retained storage/build/custody, or a production matching pair.

Still OPEN: final 0.2.9 App/Agent/Runtime composition and production exact-pin/read-client/state binding; real V1 max10 4→8 acceptance and raw16 refusal after V2 max20/removal and process restart; lost-ACK durable exact retry; real inverse/undo/redo/reload; browser zero-legacy qualification. Drafts typed but not submitted are component-local; this change does not add persistence or rehydrate raw fields from the recovered outbox. Existing submitted-command recovery tests remain the source evidence for restart/reload lifecycle.

Recommended next step: review/port only the seven-path delta onto refreshed main with the separately owned 0.2.9 pin and exact retained binding, then qualify the real Runtime/browser journey before activating the route or retiring the writer. No implementation blocker within this source-only task.
