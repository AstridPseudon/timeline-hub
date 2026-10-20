# ap2-m2-parent-existing-swap-media-member

Implemented the App-side native `clip.swap-media` member for one qualified
prepared parent-clip replacement.

## Changes

- Added detached parent swap capture/finish and Agent-parity authored execution,
  reusing the existing parent media recorder, verified-media checks, raw bundle
  guards, registry create-or-require, and command claims.
- Preserves the target clip's raw asset carrier: trim/source window, hold, speed,
  clip type, track, order, and opaque fields. Untrimmed parent video clips are
  accepted without inventing `from`/`to`; same-alias rebinds validate every
  consumer before changing the bounded registry binding.
- Added the durable command-session port, legacy-clean fence, Timeline state
  wiring, and the qualified `addClip({ preparedAsset, replaceClipId })` callback.
  It freezes the bundle/head/generation and exact five-field prepared selection
  before the single Runtime verification await.
- Kept `useSwitchToFinalVideo.updateToLatestVideo` on its existing path. Its
  `ShotFinalVideo` carrier has only URL/generation metadata and no exact
  `MediaSelection`; this task therefore does not fabricate a catalog lookup or
  command. That ingress remains a peer prerequisite until preparation carries
  the exact selection and the caller proves unchanged replacement semantics.

## Validation

- Targeted Vitest: 9 files, 239 tests passed. Command:
  `node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/parentClipSwapCapture.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts src/tools/video-editor/commands/commitSession.clipScalar.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx`
- ESLint on all changed source/test files: passed.
- `npm run typecheck:strict-islands`: passed.
- `git diff --check`: passed.

No full, browser, live-socket, Runtime Door, reload/undo acceptance, or central
integration suite was run.
