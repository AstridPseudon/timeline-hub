## A4 independent census: FAIL

The prior 0340 PASS misses a live popup fallback:

- `LocalTimelineShotBrowser.tsx:85-86,297` creates/passes `RuntimeDataProvider`.
- `ShotTimelinePreview.tsx:524-536,640-660` wraps it in `createShotTimelineDataProvider()` and mounts that wrapper.
- The wrapper exposes only legacy `saveTimeline` (`shotTimelineDataProvider.ts:1137`); v2 capabilities remain internal.
- `useTimelinePersistence.ts:412-416` therefore calls the popup’s `saveTimeline` fallback in production.
- Its internal branch eventually uses `commitTimeline`, but the legacy writer carrier remains reachable.

Main UI, AgentChat registration, element adapter, and mounted media routes correctly reach the A2 handoff/outbox path. No current production caller was found for `saveTimelineAtHead`, executor, generic-patch, or dormant `useTimeline`.

Evidence:

- HEAD `f90e708b`; tree `afc357e3`.
- Exact content/tree match with reviewed `2c786c161f...`; no diff.
- D37 implementations/tests byte-identical to `5ad7907e`.
- Transcript test: 397 lines, 40 assertions, byte-identical.
- D37 ledger entries present at deletion-ledger lines 69–74.
- `git status --short`: clean.
- `git diff --check`: passed.
- Tests were not run, per task prohibition.

Smallest next worker: migrate only the popup save route in `ShotTimelinePreview.tsx` / `shotTimelineDataProvider.ts` so the mounted provider consumes the existing v2/local-save handoff directly and no longer invokes `useTimelinePersistence`’s legacy `saveTimeline` branch. No product or test files were changed.