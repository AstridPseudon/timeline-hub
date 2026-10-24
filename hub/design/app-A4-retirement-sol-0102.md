Partial A4 cut ready for review: **379 lines removed, 21 added; 384 targeted tests passed.** Whole executor/adapter/golden retirement remains incomplete.

- Deleted `commands/clipParamsGesture.ts` with `apply_patch`: its gesture functions had no callers. Its remaining port contract is private to `commitSession.ts`; no compatibility exports were added.
- Removed the duplicate scalar executor from `genericPatchCapture.ts`. Hold capture/replay now uses the existing `ordinaryScalarMember.ts` implementation.
- Removed the circular dependency from `ordinaryScalarMember.ts` back to the generic adapter.

All other files remain unchanged, including `runner.ts`, `types.ts`, remaining capture files, goldens, D31 and its helpers, preview dispatch, save/handoff code, prepared producer, and Luna0059’s fixture test.

| Existing assertions | Execution after this cut |
|---|---|
| Generic hold commands, records, reads, ordering and guards | Existing ordinary scalar implementation |
| Ordinary scalar hold/clear and sequential batches | Existing scalar recorder directly |
| Preview, undo, refusal, opaque/null/absence and D31 | Existing paths unchanged |

No test files were edited; no skips, xfails, or weakened expectations were introduced.

Commands run successfully, with file lists compacted using shell braces:

```bash
V=(node --import "$TMPDIR/dirname-preload.mjs" node_modules/vitest/vitest.mjs run \
  --config "$TMPDIR/vitest.config.mts" --configLoader=runner --no-cache --maxWorkers=2)

"${V[@]}" src/tools/video-editor/commands/{genericPatchCapture,ordinaryScalarMember,ordinaryMoveMember,ordinaryRealBatch,ordinaryTrimMember,ordinaryStructuralMember,commitSession.genericPatch,commitSession.clipScalar,clipParamsCapture,selectedParamAuthority,selectedParamPort}.test.ts
# 11 files, 92 tests passed

"${V[@]}" src/tools/video-editor/commands/{commitSession,commitSession.placement,commitSession.occurrenceDuplicate,shotSetSession,transcriptAssociateCapture,media,runner,localSaveSession,localSaveSession.v2,documentPatchIntent,parentAfterAnchorCapture,trackReorderCapture}.test.ts \
  src/tools/video-editor/hooks/useTimelineHistory.test.ts \
  src/tools/video-editor/lib/{timeline-save-utils,sha256}.test.ts
# 15 files, 292 tests passed
```

The private config extends the repository config with a private cache directory.

```bash
NODE_OPTIONS=--max-old-space-size=4096 flock -w 50 /home/user/work/.app-tsc.lock \
  bash -c 'set -e; set -x;
  node node_modules/typescript/bin/tsc -p tsconfig.json --noEmit --incremental false;
  node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit --incremental false;
  node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit --incremental false'

node node_modules/eslint/bin/eslint.js \
  src/tools/video-editor/commands/commitSession.ts \
  src/tools/video-editor/commands/genericPatchCapture.ts \
  src/tools/video-editor/commands/ordinaryScalarMember.ts --max-warnings 0

git diff --check
```

All passed. Import census confirms no production session constructor caller and no remaining parameter-gesture references. Live preview still calls the existing runner from `media.ts`, `useTimelineState.ts`, and `useTimelineHistory.ts`.

The smallest concrete preservation contradiction is [the explicit same-order write assertion](/home/user/work/wt/app-A4-retirement-sol-0102/src/tools/video-editor/commands/trackReorderCapture.test.ts:63). Current Agent `b61cebe8` rejects `track.reorder` as `unsupported_operation`; the current document-patch emitter returns `null` for unchanged documents. I retained that positive test and port. Current literal media birth also does not establish parity with the retained raw after-anchor clone/ripple assertions.

Next bounded cut: migrate `commitSession.genericPatch.test.ts` to `localSaveSession`, retaining record/guard coverage through the actual provider seam before deleting the remaining adapter.

`commit-msg` and `BLOCKED` were written. No commit, full suite, browser, Runtime service, or live HTTP run was performed.