# App root label clean-focus fix

## Exact delta

- `src/tools/video-editor/components/TimelineEditor/TrackLabel.tsx`
  - `finishNameEdit` now records whether the captured label is dirty.
  - A clean successful finish clears `nameDraft`, allowing the controlled input to show the current `track.label` after a remote prop update.
  - Dirty edits still call the original captured finish callback; callback refusals still retain the draft and error.
  - No remote-prop callback, refresh guard, capture change, empty-string handling, or mobile/root/source/boot/generated change was made.
- `src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx`
  - Added the permanent desktop direct-row regression: focus `Original`, rerender with `Remote name`, blur without typing, assert the same input shows `Remote name`, and assert no command finish occurs.
  - Existing dirty remote-label, empty-string, refusal, original-capture, and mobile assertions remain unchanged.

## Test mapping

- `node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-runtime029-app-normal-pin/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx`
  - PASS: 1 file, 32 tests.
- Same cache-free runner/options with `TrackListRenderer.test.tsx`, `TimelineCanvas.test.tsx`, and `useTimelineCommandSession.test.tsx`.
  - PASS: 3 files, 126 tests.
- `node scripts/quality/check-known-failures.mjs`
  - PASS: 3 authorized expected-failure markers, 0 forbidden markers.
- `git diff --check`
  - PASS.

No full suite, build, browser, socket, install, or project typecheck was run, per task limits.

## Decisions / blockers

- Used the smallest state transition at clean blur: clear only the draft after the captured edit is known clean and no finish callback is invoked.
- No blockers. No evidence contradicted the settled P2 decision.
