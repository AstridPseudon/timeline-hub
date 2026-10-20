# AP2 M2 prepared-video refusal and intent repair

## Result

Fixed review findings 1 and 3 from the parent consumer shared-seam HOLD. The
App-owned `useAssetManagement` hook now treats every prepared video as native:
missing original selection, missing `addClip`, and native service refusal are
visible bounded errors returning `false`; no local `applyEdit` fallback runs.
Native placement/removal inputs are forwarded unchanged to the existing
`commands.addClip` service. Image/audio and other non-video local behavior is
unchanged. The parallel external-drop await finding was not touched.

## Source and scope

- Source head for combined review: `b4d443057823520e956c87e8c06c2874208eff57`
- Changed files only:
  - `src/tools/video-editor/hooks/useAssetManagement.ts`
  - `src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx`
- No provider, store, schema, API, session, or shared construction changes.

## Assertion map

- Existing selected prepared-video success: native `addClip` returns success,
  the exact five-field selection identity is retained, default
  `forceNewTrack: false` and `insertAtTop: false` are forwarded, and
  `applyEdit` is not called.
- Missing selection: prepared video returns `false`, emits a bounded visible
  error, leaves the data reference unchanged, and never calls `applyEdit`.
- Missing native carrier: returns `false`, emits a visible unavailable-service
  error, and never calls `applyEdit`.
- Native refusal: returns `false`, preserves no-fallback behavior, and caps the
  service message at 240 characters in the existing error toast.
- Caller intent/refusal: `forceNewTrack: true`, `insertAtTop: true`, and
  `removeClipId: 'uploading-1'` arrive exactly at `addClip`; a service refusal
  is toasted and does not call `applyEdit`.
- Original Runtime import, size guard, selection carrier, and direct-Bridge
  refusal assertions remain present and passing.

## Verification

Passed:

```text
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts
2 files, 19 tests passed

node node_modules/eslint/bin/eslint.js --no-cache --max-warnings 0 src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx
exit 0

node node_modules/typescript/bin/tsc --noEmit --pretty false --incremental false
exit 0

git diff --check
passed
```

The direct Vitest invocation without the established external runner was not a
product failure; it stopped at config loading because `__dirname` is undefined
under the ESM runner. No browser, localhost/socket, request-test, or full suite
was run, per task scope.

## Decisions and limits

The native service message is trimmed and capped at 240 characters, with a
fixed fallback for an empty message. Placement/removal intent is always passed
to the existing service, including combinations that service may reject; the
hook surfaces that refusal and never silently downgrades to local editing.

No blockers remain for this assigned scope. Combined review should verify the
separate external-drop await repair and the shared construction against this
source head.
