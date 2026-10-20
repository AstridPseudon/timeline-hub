# ap2-m2-parent-preparation-original-epoch-fence

## What changed

- Added an internal parent-media preparation carrier using `Pick` of the existing capture basis. It snapshots the authored bundle, outbox basis, displayed raw head, and command-session `localGeneration` before producer work.
- Wrapped that carrier in the existing legacy-clean guard. The generation-duplication callback captures it before `duplicateGenerationAsset` awaits, checks the raw data/head snapshot, then asserts the original session basis immediately before asset preparation and native submission.
- A pending local/native edit with an unchanged accepted film head now produces a visible refusal before preparation, native enqueue, or legacy registry registration. The catalogued duplicate remains unplaced.
- Existing `afterClipId` semantics are unchanged. The current native carrier still visibly refuses exact after-clip placement as an unsupported prerequisite; no append conversion or fake guard command was added.

## Tests and checks

- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx` — passed, 4 files / 110 tests.
- `./node_modules/.bin/tsc --noEmit --pretty false` — passed.
- `./node_modules/.bin/eslint src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/components/AstridTimelineEditor.tsx src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx --report-unused-disable-directives --max-warnings 0` — passed.
- `git diff --check` — passed.

The focused callback suite includes the predecessor’s generation-duplication cases and a new pending-native-move race: the accepted head stays unchanged, the session generation advances while producer work is pending, and the callback refuses with zero `addClip` and zero legacy registration calls.

## Decisions and limits

- Reused the existing parent-media capture port and basis fields; no wire field, DTO, store, public command method, selection refresh, or fallback writer was introduced.
- No AppProvider duplicate/parent forwarding changes were made; that final join remains separately pending.
- No full, browser, localhost, live socket, or external-provider suite was run, per the task constraints.

## Recommended next steps

- Merge through the harness, then qualify the AppProvider final join separately.
- Keep the exact native `afterClipId` insertion/order prerequisite visible until the peer native carrier supports that shape and can be proven with the existing command expectation/record tests.
