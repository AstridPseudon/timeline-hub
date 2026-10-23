# Handoff: A3 popup mounted caller

The App worktree contains the bounded popup ADD/SWAP caller repair. The new
`ShotTimelineMediaControls` is mounted inside the current popup editor and
uses Runtime `prepareMediaImport`, then the current mounted
`useTimelineCommandsService().addClip` path with `preparedAsset` and
`replaceClipId` for swaps. It captures the popup data reference plus
occurrence/document/project/timeline identity before the asynchronous import
and refuses stale ownership/context or unsupported media without invoking a
command.

`ShotTimelinePreview` passes its existing parent `timelineDataProvider` as the
popup media provider as well as the existing A2 save provider. This makes the
already-landed receiver's exact selection read and
`occurrence.fork` + `occurrence.add-media`/`occurrence.swap-media` command
construction reachable. No old parent swap port or direct writer was revived.

Files changed are limited to the new control and test, `ShotTimelinePreview`,
and its current test doubles. Caller tests pass (3/3); the combined preview
target is 36/37 because the existing raw opaque `__proto__` preservation test
fails at `ShotTimelinePreview.test.ts:752`. Root `tsc --noEmit`, scoped ESLint,
and diff check pass. Strict-islands is blocked by existing missing generated
and virtual Composition admission modules, with no changed-file diagnostics.
