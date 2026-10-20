# App initial recovery generation risk review

## Decision

**APPROVE** `741c785399b0954544b9992215f952a621739ea2` (`fix(timeline): retry stale initial recovery check`). No data-safety finding.

## Review result

- The existing recovery action generation remains the stale-work fence. Reload start increments it and clears only the existing checked-scope marker.
- A pending draft read A cannot offer recovery, clear a draft, or set initial readiness after reload: its effect cleanup sets `cancelled`, and its completion checks both the current scope marker and the captured generation before any action. Its `finally` also refuses to set readiness or resume deferred saves when the generation is stale.
- Canonical adoption changes `commit.data` identity, so the effect starts a fresh read for the same current scope. Only that current-generation read can set `initialRecoveryChecked` and resume deferred recovery saves.
- The existing async Retry, Discard/reload, original-head/CAS, unmount, and command-session timeline-switch guards are preserved; the candidate does not add a store, new counter, public field, timeout, or readiness bypass.

## Verification

- `npx vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.test.tsx` — PASS, 2 files / 12 tests.
- `npx vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx` — PASS, 1 file / 11 tests.
- `npx vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx` — PASS, 3 files / 57 tests.
- `npx vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx --testNamePattern='cold seed hydration projects the verified initial head'` — PASS, 1 test; 20 skipped by name filter.
- `git diff HEAD^ HEAD --check` — PASS.

Not run: full/project TypeScript suites, browser/localhost/socket journeys, installs, or shared-cache writes. The initial-read unmount/project-switch conclusion is code-path verification; this candidate adds no dedicated initial-read unmount test.
