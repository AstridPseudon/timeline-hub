# ap2-m2-parent-duplicate-generation-real-producer

## Changes

- Extended the duplicated-generation result and prepared-asset flow to preserve the original five-field Runtime `MediaSelection`.
- Migrated the non-canonical `AstridTimelineEditor` generation-duplicate callback away from local registration-plan construction. It now snapshots the current timeline before the async producer call, refuses stale head/projection changes, prepares the captured selection without calling the legacy registry writer, and submits one `commands.addClip` intent with the original `afterClipId`.
- Kept exact placement semantics intact. The callback does not convert `afterClipId` into append/time placement; the current native carrier can therefore return its exact-placement prerequisite refusal until that carrier supports the shape.
- Added focused callback coverage for one qualified native intent, stale-head refusal, visible exact-placement refusal, and absence of legacy generation registration. Existing native parent tests cover exact retry, opaque preservation, registry creation/reconciliation, and full command records.

## Evidence

- `./node_modules/.bin/tsc --noEmit --pretty false` — passed.
- `./node_modules/.bin/eslint src/tools/video-editor/adapters/app/generationLookup.ts src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/components/AstridTimelineEditor.tsx src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx --report-unused-disable-directives --max-warnings 0` — passed.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts` — passed, 3 files / 87 tests.
- An initial `--configLoader=runner` attempt was not usable because this repository's Vitest config requires CommonJS `__dirname`; the successful run used the normal bundled loader with `--no-cache`.

## Decisions and limits

- Did not modify AppProvider duplicate/parent forwarding or claim mounted activation; the current bridge still reports duplicate-generation capability unavailable.
- Did not change the canonical occurrence-duplicate handler, automatic/recovery flows, or the native carrier's exact-placement contract.
- No full, browser, localhost, socket, or external-provider suite was run, per the worker brief.

## Handoff

The harness should commit the worktree changes with the supplied commit message. The current native carrier still needs a peer-side exact insertion/order capability before this callback can produce a successful mounted parent insertion for `afterClipId`.
