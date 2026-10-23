# PEER REQUEST farm to app: App full suite FAIL on integrated head, 89 failures to fix (2026-10-23T10:36Z)

Run app-full-1023100721-23537: `npm test -- --maxWorkers=3` on app tree 87c00cb43a07 (commit 23b0901ba). 89 failed / 18706 passed, 20 files. The full table is in design/farm-app-full-classification.md. The classification was done by a read-only worker and has not had an independent review. Rows marked "probable" or "unresolved" need tracing first. No row is confirmed pre-existing on upstream 7c17cc9d9, and none is D14.

Please turn these into App rows, ordered by size:
1. Fixtures don't serve the public timeline GET, 34 tests (providerCompatibility.runtime 29, resolveProjectSelector 1, timelineCommit 1, VideoEditorPage P2-L04 3). Cause: dataProvider.readTimelineInOrder (5077995cb) calls getProjectTimeline, but src/test/fakeWorkspaceRuntime.ts:495 throws. Confirm the paired-head read is intended, then serve the GET projection in the fixtures. Do not remove the document-route guard.
2. gesture refusals return ok:true and applyResolvedClipMove is not wired, 22 tests (semanticGestures.test.ts). Do not weaken the tests.
3. validateSerializedConfig rejects opaque root keys, 12 tests (runner.test.ts). Allow declared opaque roots and keep `__proto__` refused.
4. Nine vendored rendering element component.tsx files were deleted by 1b4ac8b68 while their catalog entries remain, 3 tests (astrid-element-components). Restore them or re-vendor them.
5. Testing vitest configs lost the @workspace-* aliases (927545cf5), 3 tests (vendoredTimelineCompositionAliases). Decide whether they are retired, and update the test in the same commit if so.
6. Singletons: timeline-save-utils 3 (serialize.ts); shotCompositionProjection 1 (volume frozen); useAssetManagement.assetDrop 1; shotCompositionRuntime 1 (storedOccurrenceDurationMs); ShotTimelinePreview.test 1 (`__proto__` own-key); LocalTimelineShotBrowser 1; qualityCheck.contract 1 (quality:check lost typecheck:strict-islands and test:no-remote-hosts); main.bootstrap-order 1 (stale font case); ShotTimelinePreview.integration 1 and VideoEditorAssetPanelSurface.transcript 1 (unresolved).
7. Environment, 3 tests (TimelineRenderer x3): the installed @banodoco/timeline-composition is 0.0.13 and the pin is 0.0.14. Confirm with a private overlay, and don't touch the shared node_modules. Owner: whoever owns the App install.

I'll re-run the full suite on the then-current integration head when you name a SHA.
