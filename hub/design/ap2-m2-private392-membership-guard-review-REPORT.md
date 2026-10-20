# App private392 generic membership guard review

## Decision

**APPROVE private native consumer preparation.** The new delta is limited to
the generic membership seam and its focused tests at candidate
`3b4d84089119d09d5b7e9b7ee5fba33d17e3594c` (tree
`1df593ec9b5e8755533a9e9c5a51071c79d99f7e`), compared with
`tl/ap2-m2-private392-app-counterpart-preparation`
(`acc27e8dcf13b2296e7738d2e06199777ab3cb1f`). Changed paths are only:

- `src/tools/video-editor/commands/genericPatchCapture.ts`
- `src/tools/video-editor/commands/genericPatchCapture.test.ts`
- `src/tools/video-editor/commands/projectDataMember.ts` (compatibility
  exports only)

No source edit was made by this review.

## Membership and safety findings

- `captureGenericPatch` validates every member before owner resolution. A
  valid `project-data.write` is assigned the existing parent owner without
  calling the host resolver; ordinary members retain their existing resolver
  path.
- The original operation object, including its declared `order`, reaches
  `captureProjectDataMember`. Generic capture sorts the complete batch using
  the existing order rule, captures each member against the copied sequential
  `after` bundle, and emits one existing `commands[]` carrier with contiguous
  ordinals.
- Merge/default/replace lowering, finite-JSON and namespace limits, and exact
  original namespace/cell claims remain in `projectDataMember`; the generic
  seam does not diff a whole config or recapture a fresh safety basis. Replay
  dispatches through `executeProjectDataMember`, not a parallel writer.
- Preview applies the same exported `projectDataValue` to copied `config` and
  `resolvedConfig`, preserving null, absence, opaque siblings, and insertion
  order. It does not serialize command records or derived fields.
- An unsupported delete/unset-like member makes a batch containing a valid
  native member classify as `mixed`; the generic capture preflight then
  refuses the complete batch before owner resolution, command construction,
  preview, enqueue, or legacy fallback. The input bundle is unchanged.
- Standalone unsupported delete/unset remains `unsupported` and therefore
  follows the pre-existing legacy path in `useTimelineOps`; this is unchanged
  behavior and remains intentionally outside native qualification while the
  delete carrier is absent. No public integration or legacy writer was
  changed. This review does not approve delete/unset activation.

The existing helper’s direct evidence covers opaque values, null/presence,
sibling preservation and original-leaf guards; this review reused it rather
than duplicating that already-approved matrix.

## Verification

Passed in the assigned worktree:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts src/tools/video-editor/commands/ordinaryMoveMember.test.ts src/tools/video-editor/commands/ordinaryScalarMember.test.ts src/tools/video-editor/commands/ordinaryStructuralMember.test.ts
=> 6 files, 41 tests passed

node_modules/.bin/eslint src/tools/video-editor/commands/genericPatchCapture.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/projectDataMember.ts src/tools/video-editor/commands/projectDataMember.test.ts --ext ts --max-warnings 0
=> exit 0

node_modules/.bin/tsc --noEmit --pretty false
=> exit 0

git diff --check
=> exit 0
```

No full, browser, localhost, live-socket, native provider/Door, dependency,
pin, activation, release, or integration run was performed. Runtime final
approval, the normal Agent private pin, and one exact matched private392
native/provider/Door pair remain prerequisites.

## Recommended next step

Preserve this private preparation and perform the separately gated reciprocal
Runtime/Agent/App identity review, then run exactly one matched private392
native/provider/Door qualification. Keep delete/unset on the existing legacy
path until its own native carrier and qualification exist.
