# App initial recovery generation retry fix

## Result

Fixed the App initialization/recovery race in `useTimelineSave`.

Canonical reload now clears the existing checked-scope marker while still
advancing the existing recovery action generation. The initial recovery effect
also observes canonical data identity. Therefore a reload that adopts new
canonical data re-runs the existing scope check, while the old draft-read
completion remains cancelled/stale and cannot set `initialRecoveryChecked`.
No new store, counter, public field, timeout, or readiness weakening was added.

## Regression proof

Added a focused test in
`src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx` covering:

1. Initial draft read A is held pending.
2. Canonical reload invalidates the generation and adopts canonical data C.
3. Read A resolves stale; readiness remains false.
4. A fresh current-scope/current-generation read is started.
5. Only the fresh read settles readiness true and resumes deferred recovery.

Existing recovery, original-basis, cancellation, and command-session behavior
tests remain unchanged.

## Verification

- `npx vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.test.tsx`
  - PASS: 2 files, 12 tests.
- `npx vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx`
  - PASS: 3 files, 57 tests.
- `npx vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx --testNamePattern='cold seed hydration projects the verified initial head'`
  - PASS: 1 test; 20 unrelated tests skipped by the name filter.
- `npx eslint src/tools/video-editor/hooks/useTimelineSave.ts src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx --ext ts,tsx --max-warnings 0 --no-cache`
  - PASS.
- `git diff --check`
  - PASS.

Not run: full/project TypeScript suite, browser/localhost/socket journeys,
normal014 central Gate 5, installs, or shared-cache writes. App2 should run
the one justified exact normal014 journey after the harness commit and report
the resulting source/hash and test evidence.

Pre-commit source HEAD: `ed48d92d2a8bb8d9f013060e420eba646d88ace4`.
