# App root label clean-focus follow-up review

## Reviewed SHA and verdict

- Parent: `5117b9da2e17828ec0b3cfbcdf3ff4987dc77ab3`
- Candidate: `eac3e87d5c2d1f2ad4cb528412f8285a7f49d154`
- Diff: exactly `TrackLabel.tsx` plus its direct `TrackListRenderer.test.tsx` regression; no root, render, mobile-source, boot, or generated paths.
- Verdict: **HOLD for one semantic edge clarification; the requested P2 clean-focus case itself passes.** No KEEP marker or merge approval is issued by this review.

## Evidence

The candidate was exported to a private review snapshot and run with the shared `node_modules` symlink read-only and cache-free, single-worker Vitest:

```text
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-runtime029-app-normal-pin/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx
PASS: 1 file, 32 tests

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-runtime029-app-normal-pin/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx
PASS: 3 files, 126 tests

node scripts/quality/check-known-failures.mjs
PASS: 3 authorized expected-failure markers, 0 forbidden markers

git diff --check 5117b9da2..eac3e87d5
PASS
```

The exact requested sequence—focus `Original`, rerender with remote `Remote name`, blur without typing—shows `Remote name`, does not call the finish callback, and captures once. Existing dirty remote-capture, empty-string, refusal/error-retention, original-callback, row/canvas/session, and mobile no-capture tests remain unchanged and pass. No new failure markers were added; the 10:13 mobile owner decision remains intact.

## Edge requiring clarification

A review-only probe of `Original → Temporary → Original`, followed by a remote `Remote` prop and blur, observed candidate behavior `{ value: 'Remote', finishCalls: 0 }`. `TrackLabel.tsx:347-356` defines cleanliness only by final value versus the captured original, so it releases the draft in this case. The native contract separately says same-value writes are direct intent (`commands/trackLabelCapture.test.ts:71-81`), and the session explicitly never refreshes original guards across remote changes (`commands/commitSession.ts:293-297`). If that native rule makes typing away and back an authored intent, this candidate silently loses it instead of preserving it for the captured guard/refusal path. If UI semantics intentionally define it as clean, add a permanent regression documenting that choice before approval.

This is the only hold. The requested no-typing P2 fix is minimal and correct; dirty/refused drafts are retained, no callback is reauthored, and same-owner/suffix behavior is outside the two-file delta.

## Limits and next step

No full suite, build, browser, socket/live Runtime test, TypeScript project check, or install was run. The private extracted snapshot and temporary probe were removed. Confirm the typed-away/back-to-original semantics with the Agent/App owner, then either add the explicit clean-edge assertion or preserve that authored intent before issuing KEEP.
