# Parent0333 result: ADD leaf diagnosis

## Outcome

No code change or ADD-leaf cut is qualified. The only authorized central run
failed before the native ADD request, so the required accepted request,
reload/lost-ACK/restart/exact-retry/body-and-key/undo/raw/zeroLegacy checks did
not run to completion.

## Exact source and result

- Source worker: `ap2-m2-parent-exact-negative-source-finish-0230`
- Source commit: `da6d910f7ab3dfc71142ece7f632d43341238882`
- Source tree: `6809757f93ca5e166b24b8bc0160ca09005e984a`
- Central result: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-parent-exact-negative-source-finish-0230-ap2-m2-parent-composed-driver-label-durable-stage-0323-e2e-integration-1021033417-13951`
- Command:

  ```text
  env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-composed-driver-label-durable-stage-0323/run-parent-manual-drop-evidence.sh run "$PWD"
  ```

- Result: `fail`, exit `1`, one test failed after `217s`.
- First failure: `tests/e2e/local/three-products.spec.ts:1491`; the
  `page.waitForResponse` for `GET /media-selection/verified?...` timed out
  after 90 seconds.
- Retained first evidence: `.../recorded-evidence/bounded-browser-evidence.json`,
  `error-context.md`, `runner-tail.log`, `playwright-trace.zip`, and
  `source-identity.txt` under
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-composed-driver-label-durable-stage-0323/recorded-evidence/`.

The retained request/response packet contains only:

- `POST /api/runtime/v1/projects/.../media-imports` -> `201`
- `GET /api/runtime/v1/projects/.../media-selection?...` -> `200`

There is no verified-selection request, commit request, accepted ADD, or
legacy request in the packet.

## Cause

This is a product-path failure, not an environment or fixture failure. The
build completed, the seeded WebM was imported, and the ordinary Runtime
selection read succeeded with no browser console errors.

The live path is:

1. `src/tools/video-editor/hooks/useAssetManagement.ts:498-524` imports the
   video and receives the prepared Runtime selection.
2. `src/tools/video-editor/lib/external-drop-utils.ts:489-501` creates a
   temporary uploading skeleton, then calls `dropAsset(..., preparedAsset,
   skeletonId)`.
3. `src/tools/video-editor/hooks/useAssetManagement.ts:298-304` forwards that
   skeleton ID as `removeClipId` to `commands.addClip`.
4. `src/tools/video-editor/hooks/useTimelineCommandsService.ts:474-504`
   intentionally refuses native parent ADD when `removeClipId` is present,
   before `getProjectVerifiedMedia` at line 537 can run.

That explains the exact packet: import and ordinary selection occur, but the
verified read never does. The test's wrong-selection refusal is therefore
unverified; this run does not establish a Runtime or fixture refusal.

## Live callers

- `src/tools/video-editor/lib/external-drop-utils.ts:482` — image drop,
  likewise passes the skeleton ID.
- `src/tools/video-editor/lib/external-drop-utils.ts:501` — video drop,
  the failing parent ADD path.
- `src/tools/video-editor/hooks/useAssetManagement.ts:298` — shared native
  prepared-video caller.
- `src/tools/video-editor/hooks/useSwitchToFinalVideo.ts:86`,
  `src/tools/video-editor/hooks/useAddVariantAsGeneration.ts:94`, and
  `src/tools/video-editor/components/AstridTimelineEditor.tsx:610` — other
  prepared-asset `addClip` callers; the latter two use `afterClipId` and are
  not qualified as native parent ADD callers by this run.

No shared persistence, serializer, duplicate-generation, bootstrap, or
private-ops code was changed or activated. No test assertion was removed or
weakened. No retry or second executor was run.

## Next step

Repair the external-drop skeleton/native-ADD handoff as a separately reviewed
product change, then run a newly authorized full original body. Do not cut the
native ADD leaf until that run reaches and passes the accepted request plus all
durability, exact-retry, undo, raw, and zeroLegacy assertions.
