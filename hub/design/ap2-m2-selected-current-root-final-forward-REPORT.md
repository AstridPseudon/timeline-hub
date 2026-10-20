# ap2-m2-selected-current-root-final-forward

## Candidate

- Worktree: `/home/user/work/wt/ap2-m2-selected-current-root-final-forward`
- Current App root: `hub/timeline/app/tl/integration` at `8cfcee9c0`
- Selected source: `hub/tl/ap2-m2-selected-mounted-production-join` at `f90c4e97b`
- Shared merge base: `b0efbffae` (`tl/ap2-m2-consumer-types-fix`)
- Forwarded the four reviewed selected-stack commits after the shared base: `60bc95121`, `ff6a55c30`, `c0af4e411`, `f90c4e97b`.

The net selected stack is carried onto the current root with minimal hunks. No old file was replaced wholesale, no current ordinary/element/parent/duplicate/recovery/verified-media work was reverted, and no production contract, operation, pin, endpoint, local Ajv path, or catalog was added. The result has the selected stack's 23 affected paths: retained reader/resolver and native `clip.set-params` capture, authority/live-basis fencing, provider/session/state/PropertiesPanel forwarding, and selected mounted tests.

## Behavioral preservation and deletion accounting

- Existing `RuntimeDataProvider.paramReadClient` and authenticated retained document/object reads are forwarded through `useTimelineSave` and the command session. Exact `DocumentPin` identity, retained input bindings, generation/head fencing, and draft-preserving refusal remain enforced.
- The native carrier is the existing `clip.set-params` command. No new edit operation or DTO was introduced.
- The mounted path is `clipParamsPort` from the production command session through `useTimelineState`, `VideoEditorProvider`, `PropertiesPanel`, `ClipPanel`, and `AstridElementParams`.
- No selected-PARAM snapshot writer remains in the production selected path. `AstridElementParams.tsx:83` retains the ordinary `onChange(next)` fallback only for unplaced/unqualified catalog-literal flows; owner-qualified selected-pack edits use the native port and never call that fallback. The safe literal element path remains on the existing element port.
- No deletion-ledger row was marked `DELETED`; this worker does not claim HOME merge or a deletion gate.

## Verification

Passed:

- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/selectedParamAuthority.test.ts src/tools/video-editor/commands/selectedParamPort.test.ts src/tools/video-editor/commands/clipParamsCapture.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx src/integrations/runtime/dataProvider.test.ts` — 7 files, 145 tests passed.
- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx` — 4 files, 164 tests passed.
- Touched-file ESLint with `--max-warnings 0` over the 23 selected-stack paths — passed.
- `git diff --check` — passed.

Required project check:

- `./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false` — exit 2, with 24 pre-existing current-root diagnostics and zero selected-stack diagnostics. The unchanged baseline includes the existing `MediaSelection` string-index error at `src/integrations/runtime/dataProvider.ts:1677`, `shotSetCapture.ts:163`, Composition 0.0.13 export/type mismatches in Preview/Composition files, existing `useTimelineCommandsService.ts` typing errors, and `lib/config-utils.ts:43`. The selected-stack diagnostics found during the first composed check (missing imports/wiring and strict narrowing in the new selected files) were fixed narrowly; none remain in the final output.

Not run per brief: full suite, browser/e2e, localhost/live sockets, Runtime/Agent qualification, public pin/release, and independent review routine.

## Decisions

- Applied the selected source net diff against the shared merge base, then resolved only current-root overlaps. Current-root provider, recovery, ordinary, and other App ports remained authoritative.
- Added the one required `JsonObject` narrowing at the selected capture boundary because current App's `ClipParamsCapturePort` requires an object while the shared session JSON helper is typed as general JSON. This is type-only and does not alter the command payload.
- Tightened `selectedParamPort`'s existing live-basis guard with an explicit `undefined` check so the real `tsconfig.app.json` check can prove the existing refusal behavior under strict TypeScript.

No blockers beyond the recorded pre-existing project-check baseline. No extra App copy, archive, dependency, cache, or build output was created.
