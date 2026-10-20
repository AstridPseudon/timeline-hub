# App cold-root final independent review

## Verdict

**APPROVE for root merge.** Reviewed `b77ccaf2dbf2da85d7ba5828e5114627325cdea6` / tree `74130f681f6b0c87a7c61cb33d4ae6a092c03046` against `05b6b488d1834650c459c5c565f2530d9bea20e9`. No blocking code finding.

## Source review

- `useTimelineSave` now keeps command bootstrap behind both visible `commit.data` adoption and the existing one-shot IndexedDB recovery check. It also keeps `isLoading` true while the command session is still loading, so editing is not exposed before readiness.
- `useTimelineCommandSession` still loads the validated command basis and installs the original accepted projection only through the existing `project(basis, [], true)` path. Its original guards remain present and unchanged: same displayed object, same head identity, no existing projection, clean legacy/recovery state, and disposal/generation fencing.
- Dirty, recovered, newer, and unmounted cases remain refusal/preservation paths. The late-basis regression specifically confirms dirty Unicode input remains the displayed object, with no projection and no commit.
- The raw/display capture comparison and original intent guards are byte-preserved: `commitSession.ts`, `trackLabelCapture.ts`, `clipMoveCapture.ts`, and `semanticGestures.ts` are not changed by this patch.
- Main17/mobile delegation is untouched: the mobile policy, `useTimelineState` delegation, and gesture-owner paths are outside the five changed files. The serial reset and unique-C browser fixtures are also untouched.
- The two test-environment changes are fixture correctness only: the fake Runtime now preserves the occurrence closure and supplies the pinned registry needed by the real projection shape. No behavior expectation was weakened, skipped, or deleted.

## Evidence

Static checks run by this reviewer:

```text
git diff --check 05b6b488d1834650c459c5c565f2530d9bea20e9 b77ccaf2dbf2da85d7ba5828e5114627325cdea6: PASS
git diff --name-status ...: exactly the five files described in the basis report
```

Per the brief, no additional Vitest/browser/full suite was run by this read-only reviewer; the supplied exact-tree evidence was adequate:

- Focused Vitest command (private preload/cache, `--configLoader=runner --no-cache`):

  ```bash
  NODE_OPTIONS='--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-cold-label-initial-basis-fix/notes/vitest-preload.cjs' node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx
  ```

  **360/360 tests passed**, exit 0.
- Central cold browser request/wait: `request-test app-m3-cold-label-initial-basis-fix e2e-cold-label-initial-basis-74130f68-cold-open`, then `wait-test app-m3-cold-label-initial-basis-fix-e2e-cold-label-initial-basis-74130f68-cold-open-1020145250-25068`; underlying command `npm exec -- playwright test --config playwright.track-label.config.ts --grep 'M2 cold-open'`: **1 passed**, exit 0.
- Central regular-label request/wait: `request-test app-m3-cold-label-initial-basis-fix e2e-cold-label-initial-basis-74130f68-labels`, then `wait-test app-m3-cold-label-initial-basis-fix-e2e-cold-label-initial-basis-74130f68-labels-1020145454-15009`; underlying command `npm exec -- playwright test --config playwright.track-label.config.ts --grep-invert 'M2 cold-open'`: **3 passed**, exit 0.
- Central native request/wait: `request-test app-m3-cold-label-initial-basis-fix e2e-cold-label-initial-basis-74130f68-native`, then `wait-test app-m3-cold-label-initial-basis-fix-e2e-cold-label-initial-basis-74130f68-native-1020145454-10038`; underlying command `npm run test:e2e:three-products -- --grep 'M1 real'`: **3 passed**, exit 0.
- Source/artifact/peer/cache guards: passed in all three central runs.
- Original-source countercheck: expected exit 1 with the exact pre-fix capture mismatch, confirming the regression is real and not a weakened assertion.

## Limits and next step

This approves the explicitly frozen d874/2c4/public12 cohort and this App root merge only. It does not claim newer Agent qualification, all writers, a full project typecheck/build, or a full browser/socket suite. Recommended next step: merge the root cold fix and retain the supplied focused/browser evidence with the release record.
