# Gate6 download-name diagnosis

## Verdict

This is a fixture/assertion mismatch, not a product defect. The first valid
physical result `18439` failed before any download body, frame, audio, or parity
claim: the frozen harness expected `frame-parity.mp4`, while the normal App
admission request carried `timeline-6c0e5aa0-99af-408a-af71-11a9e2e337de.mp4`.

The exact retained failure is in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-short-temp-device-inode-source-fix-0845/gate6-20261021T0845/playwright-output/player-export-normal-profi-d4d71-without-a-parity-comparison-native-codec-chrome155/error-context.md:17-25,481-482`

The 0856 report records that this was the first case, that execution stopped
without retry, and that no valid media/parity positives were produced:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-gate6-single-lock-exact-command-executor-0856-REPORT.md`

## Source-backed contract

- Frozen d00 harness fixture writes `frame-parity.mp4` at
  `tests/e2e/timeline/viewing-parity/fixture.ts:229`.
- Frozen d00 harness then incorrectly treats that fixture field as the
  managed output contract at `tests/e2e/timeline/viewing-parity/cases.ts:90-91`
  and again as the browser download contract at `:159`.
- The normal UI path admits the request from `useRenderState.ts:905-917` and
  does not supply `request.outputFilename`.
- Both frozen d00 and `origin/main` define
  `src/tools/video-editor/lib/renderRouter.ts:741-744` as
  `timeline-${timelineId}.mp4`, and
  `buildRenderTimelinePayload` applies that default at `:879` when no explicit
  output filename is supplied.
- `origin/main:src/tools/video-editor/lib/renderRouter.test.tsx:926-935`
  independently expects the generated payload filename to contain the
  timeline ID.

Thus the original product contract is the timeline-id-derived managed filename;
`frame-parity.mp4` is fixture data, not an explicit UI render-name authority.
The observed `timeline-<id>.mp4` is the expected normal path.

## Proposed correction

Unapplied, test-only patch:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-gate6-download-name-source-diagnosis-0910-PATCH.patch`

It changes only the two parity assertions in
`tests/e2e/timeline/viewing-parity/cases.ts` to expect
``timeline-${fixture.timelineId}.mp4``. It does not change production code,
media bytes, frame/audio checks, source guards, managed-output checks, or
negative controls. `authoredOutput` remains recorded as fixture evidence.

This assertion conversion requires independent review before adoption. No live
callers changed; no production callers changed.

## Verification

- Pure regression with the frozen `frame-parity.mp4` expectation: **red**, exit
  1; actual source function returned
  `timeline-timeline-physical18439.mp4`.
- Pure regression with only the proposed timeline-id expectation: **green**,
  exit 0.
- `git diff --check`: **PASS**.
- Final App worker worktree status: **clean**.

Exact commands and source paths are recorded in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-gate6-download-name-source-diagnosis-0910-COMMAND`

No browser, helper, Runtime, central test, export, install, or full suite was
run. No retry was made. The temporary pure test and private cache were removed.
