## A4 report

**Scope:** `tl/app-A4-current-final-census-0438` at `c0fe88994405fd517b58473c14678a0d1b73056d`, tree `8e3ef15ee5f7c08381d8dc9efb38b5c98845466d`; clean and unchanged.

**Result:** **PASS for shipped production mounts.** Main, popup, and AgentChat element mutations reach the source-bound local v2 handoff and `commitTimeline`:

- Main: [VideoEditorPage.tsx:138-141](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/video-editor/pages/VideoEditorPage.tsx:138), [useTimelineSave.ts:99-129](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/video-editor/hooks/useTimelineSave.ts:99), [useTimelineSave.ts:267-288](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/video-editor/hooks/useTimelineSave.ts:267).
- Popup: [LocalTimelineShotBrowser.tsx:83-122](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/travel-between-images/pages/LocalTimelineShotBrowser.tsx:83), [ShotTimelinePreview.tsx:525-537](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/travel-between-images/components/ShotTimelinePreview.tsx:525), [ShotTimelinePreview.tsx:643-665](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/travel-between-images/components/ShotTimelinePreview.tsx:643).
- Popup source/head guards and A2 send: [shotTimelineDataProvider.ts:982-1048](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/travel-between-images/components/shotTimelineDataProvider.ts:982), [shotTimelineDataProvider.ts:1068-1185](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/travel-between-images/components/shotTimelineDataProvider.ts:1068).
- AgentChat registration and stale/authority checks: [VideoEditorProvider.tsx:307-367](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/video-editor/contexts/VideoEditorProvider.tsx:307), [element-adapter.ts:460-487](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/video-editor/runtime/element-adapter.ts:460).

Forged, missing, mismatched, stale, disconnected, and replaced bindings fail closed through [timelineLocalSaveHandoff.ts:55-72](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:55) and [useTimelinePersistence.ts:259-261](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/video-editor/hooks/useTimelinePersistence.ts:259).

The retained `saveTimelineAtHead` implementation at [dataProvider.ts:1065-1078](/home/user/work/wt/app-A4-current-final-census-0438/src/integrations/runtime/dataProvider.ts:1065) has no shipped production caller. The popup `saveTimeline` compatibility method delegates A2 first at [shotTimelineDataProvider.ts:1326-1337](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/travel-between-images/components/shotTimelineDataProvider.ts:1326), so it is not counted as an old writer.

### Dormant custody

Both ledgers list all retained D37 subsets unchanged:

- [deletion-ledger.app.md:69-74](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.app.md:69)
- [deletion-ledger.md:31-35](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/deletion-ledger.md:31)

D31 transcript test remains exactly **397 lines / 40 `expect` assertions**. Current protected blobs match the retained dormant map: track `81ec…/61d1…`, raw birth `2703…/346a…`, transcript `bd14…/5c39…`, session `0d15…`, labels `5fd0…/c2b6…`, executor `eb1c…`; required helpers and tests remain present. No ledger or source changes were made.

### Bounded caveat

The generic fallback at [useTimelinePersistence.ts:415-419](/home/user/work/wt/app-A4-current-final-census-0438/src/tools/video-editor/hooks/useTimelinePersistence.ts:415) remains reachable for non-production in-memory/dev harness providers. The dev-only route is [routes.tsx:109-120](/home/user/work/wt/app-A4-current-final-census-0438/src/app/routes.tsx:109). It is not a shipped production timeline callback; if the scope includes dev harnesses, that scope is **FAIL/PENDING retirement**, with the smallest future owner being the existing `useTimelineSave` A2 handoff.

**Proof status:** A2/A3 joined proof is **PENDING**; its `DONE` and report are not yet present.

**Verification:** `git diff --check` passed. No tests, typecheck, lint, browser, backend, service, or full suites were run per instruction. Commit message recorded; `DONE` marker created.