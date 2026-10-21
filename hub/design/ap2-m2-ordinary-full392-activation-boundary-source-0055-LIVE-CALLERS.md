# Live callers — ordinary project-data boundary

- `src/tools/video-editor/hooks/useTimelineState.ts:827-831` supplies the
  generic command port to `useTimelineOps`.
- `src/tools/video-editor/hooks/useTimelineOps.ts:270-274` is the live generic
  classification/capture/finish/submit seam.
- `src/tools/video-editor/hooks/useTimelineCommandSession.ts:262-270` wraps
  that port with the clean-save fence.
- `src/tools/video-editor/commands/commitSession.ts:954-986` constructs the
  generic port and calls `captureGenericPatch`.
- `src/tools/video-editor/commands/ordinaryScalarMember.ts:397` calls the
  generic helper internally for an ordinary scalar producer.
- `src/tools/video-editor/lib/compiler-canary.ts:421-441` is the current
  source/source-map project-data producer; no external production
  instantiation of its factory was found.
- `src/tools/video-editor/lib/source-map-runtime.ts:151-174` exposes
  project-data write/delete helpers; no live production instantiation was
  found, and delete is excluded.
- `src/tools/video-editor/commands/projectDataMember.ts:299-354` has no
  non-test caller and remains inert.

Examples and dev extensions containing `project-data.write` are not mounted
production callers and are excluded from the cut.
