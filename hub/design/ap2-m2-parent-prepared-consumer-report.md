# AP2-M2 prepared parent-media consumer report

## Result

Implemented the private current-root App candidate for one manual prepared
video `addClip` consumer. It accepts the carrier-supplied original five-field
selection, derives one existing-track media row, captures the raw row/alias,
selection, authored bundle, session generation, predecessor, and display head
before the verified-media await, rechecks the session fence, and submits one
`clip.add-media` intent through the existing durable outbox.

Registered-asset-only, automatic, popup, recovery, duplicate/group, and
new-track paths remain excluded. Existing unqualified prepared callers retain
their previous synchronous path.

## Tests

- `./node_modules/.bin/tsc --noEmit --pretty false` — passed.
- `git diff --check` — passed.
- Targeted Vitest command:
  `VITEST_CACHE_DIR="$PWD/.vitest-cache" node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts`
  — 4 files, 174 tests passed.
- Targeted ESLint over all touched App files — passed.

The targeted facade tests exercise actual `createTimelineCommands().addClip`,
capture-before-await and original-selection retention, wrong/missing verified
selection refusal without draft mutation, and the actual session port's single
intent plus exact body/key retry after an unknown ACK.

## Decisions and limits

- The approved carrier shape from `42e47ae11` is consumed structurally; the
  integration worktree did not contain that carrier commit, so no carrier
  files were copied into this candidate.
- The shared proposal is limited to four production files in
  `ap2-m2-parent-prepared-consumer-current-shared-proposal.md`; the consumer
  itself is row-local in `useTimelineCommandsService.ts`.
- No full/browser/socket suite was run per the orchestrator rule.
