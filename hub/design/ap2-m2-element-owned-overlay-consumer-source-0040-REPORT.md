# App2 M2 owned overlay consumer source

## Result

No App source change was made. The owned overlay add path remains dormant and
the existing normal owner-pinned producer is preserved. This is required because
the f83 `clip.add.args.schema_source` carrier is source-ACKed but not
consumer-pinned in the current App tuple.

The hosted `rendering/effect/audio-reactive-colour` SYSTEM8e descriptor remains
blocked. It was not relabeled builtin2a, literal, or project-owned.

## Current ingress and actual callers

- `ElementsLibraryPanel.tsx` uses `buildElementOverlayRow` and the existing
  `elementOverlay` session only for an admitted effect with no `packId`
  (`ElementsLibraryPanel.tsx:84-115`). A normal owned catalog entry retains its
  `packId` and continues through `editorContext.elementOperationAdapter.execute`
  (`ElementsLibraryPanel.tsx:118-150`).
- Existing owned-element parameter edits use `AstridElementParams.tsx:51-75` →
  `captureClipParamsEdit`/`submitClipParamsEdit`, with
  `selectedParam.resolveAuthority` resolving the accepted history pin through
  `selectedParamPort.ts:56` → `resolveSelectedParamAuthority`.
- The existing selected edit producer reads the exact retained document and
  snapshot object through `readRetainedParamInputs` in `commitSession.ts:815-852`
  and sends the exact `schema_source` on `clip.set-params`; the old pin is not
  replaced by a catalog/latest lookup. Missing or changed authority leaves the
  UI draft in place.
- The already-mounted literal overlay session is exposed by
  `useTimelineCommandSession.ts:247-261` and `useTimelineState.ts:1383-1387`.
  Its live callers are the literal add branch above and the literal whole-row
  delete callback in `PropertiesPanelBody.tsx:241-267`.

No exports changed. No new live caller was introduced.

## Exact activation dependency

Before an owned `ElementsLibraryPanel` add may enter the existing native overlay
port, the authenticated project admission must provide the exact tuple already
used by f83:

```text
elementRef = {packId, id, kind: "effect", revision}
schema_source = {document_id, version, content_digest}
admitted snapshot_object = the retained object for that exact pin/admission
```

The current normal catalog exposes the first tuple but not the admitted
`DocumentPin`/retained snapshot binding. The App must carry that result through
the existing Provider/session seam, reusing the existing selected-source read
(`getProjectVerifiedDocument` + `getProjectVerifiedDocumentObject`) and the
existing overlay capture/session/outbox path. The shared patch should add only
the already-existing source carrier to the overlay operation and have the
session pass it to the f83 `clip.add` capture; it must not add an endpoint,
result field, store, DTO, admission-at-save, or a second adapter. App/Home owns
that patch, so it was not edited here.

For edit, the current `selectedParam` path is the correct seam: resolve the
original accepted pin from history, read the matching retained snapshot, and
submit that same pin. A missing, mismatched, stale, or changed pin must refuse
before commit while retaining the draft. No owner substitution or pin adoption
was added.

## Verification

Passed, using a worker-owned `TMPDIR`, the repository Vitest runner, no cache,
one worker, and no shared dependency writes:

```text
node /home/user/work/app/node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/components/ElementsLibraryPanel.test.tsx \
  src/tools/video-editor/commands/elementOverlayCapture.test.ts \
  src/tools/video-editor/commands/elementCapture.test.ts \
  src/tools/video-editor/commands/selectedParamAuthority.test.ts \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx
```

Result: **5 files, 28 tests passed**.

The mounted retained-read neighbor was also run. Its first test passed; its
second test failed before exercising the intended late-read refusal because
`latest.current?.commands.clipParamsPort` remained undefined during setup. No
source change was made for that existing readiness failure, and no mounted
positive or browser/socket qualification is claimed.

`git diff --check` passed; the worktree is unchanged. No full, browser,
localhost, live-socket, Runtime-door, or central suite was run.

