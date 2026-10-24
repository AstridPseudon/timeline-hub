Partial A4 cut implemented. **Prepared-media preview no longer executes the runner; complete production import removal remains blocked.**

Changed only [media.ts](/home/user/work/wt/app-A4-preview-retirement-sol-0112/src/tools/video-editor/commands/media.ts:814) and its existing test: **148 insertions, 14 deletions**.

Removed the execution edge `applyPreparedMediaCommand → mediaCommandRunner.apply`. Preview now takes data directly from the existing placement/duplication builder, retaining input refusals, config validation, command details, and snapshot history. Existing production callers use this helper unchanged. Prepared media was also removed from the provisioned-media runner registry.

| Existing assertions | New execution boundary |
|---|---|
| Registry/replacement/pinned membership | Direct prepared-data builder |
| After-anchor allocation, order, ripple and sibling preservation | Existing upstream duplication utility |
| Opaque metadata, null/absence, transitions and source windows | Same editor utilities and materialization |
| Missing targets and invalid placements | Direct preview returns `null` |
| Command details and history | Exact comparison against retained runner |

All **53 original media assertions** remain unchanged. Every existing media invocation additionally compares the complete result against the retained runner. Added six refusal cases and one test asserting preview calls none of the descriptor’s validate/dryRun/apply/invert methods. Media now has **22 passing tests**.

Validation used Node **20.20.0**, the existing dependency graph, and private `$TMPDIR` preload/config/cache:

```bash
V=(/opt/node20/bin/node --import "$TMPDIR/dirname-preload.mjs" \
  node_modules/vitest/vitest.mjs run --config "$TMPDIR/vitest.config.mts" \
  --configLoader=runner --no-cache --maxWorkers=2)

"${V[@]}" src/tools/video-editor/commands/{media,runner,parentAfterAnchorCapture,trackReorderCapture,transcriptAssociateCapture}.test.ts \
  src/tools/video-editor/hooks/{useTimelineHistory.test.ts,useTimelineHistory.remote-boundary.test.tsx,useTimelineCommandsService.persistence.test.tsx,useAssetManagement.assetDrop.test.ts} \
  src/tools/video-editor/lib/{timeline-save-utils,timeline-asset-plans,duplicate-clip}.test.ts
# 12 files: 140 passed, 6 failed

"${V[@]}" src/tools/video-editor/hooks/{useTimelineCommit.test.tsx,useTimeline.test.tsx} \
  src/tools/video-editor/commands/fixtures/preparedImageRequestProducer.test.ts
# 3 files: 39 passed

"${V[@]}" src/tools/video-editor/commands/media.test.ts
# Final verification: 22 passed
```

**179 distinct tests passed.** The six persistence failures also reproduce with original `HEAD:media.ts`, loaded through a private Vite override:

```bash
/opt/node20/bin/node --import "$TMPDIR/dirname-preload.mjs" \
  node_modules/vitest/vitest.mjs run --config "$TMPDIR/vitest-baseline.config.mts" \
  --configLoader=runner --no-cache --maxWorkers=2 \
  src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx
# Same 6 failures
```

All three typechecks passed under the shared lock:

```bash
NODE_OPTIONS=--max-old-space-size=4096 flock -w 60 /home/user/work/.app-tsc.lock \
  bash -c 'set -e; set -x;
  /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.json --noEmit --incremental false;
  /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit --incremental false;
  /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit --incremental false'

/opt/node20/bin/node node_modules/eslint/bin/eslint.js \
  src/tools/video-editor/commands/media.ts \
  src/tools/video-editor/commands/media.test.ts --max-warnings 0

git diff --check
```

Lint and diff checks passed.

The smallest concrete blockers are:

- `VideoEditorProvider.tsx:625/633` still calls synchronous transaction `commands.dryRun/apply`; `useTimelineHistory.ts:294` still executes inverse transactions. I retained these consumers rather than introduce the prohibited compatibility executor.
- `useTimelineCommandsService.ts:460–462` requires Runtime `mediaSelection` for new prepared assets. The six persistence fixtures omit it, while their positive assertions require success. They fail before preview in both versions. Their owner must resolve this boundary; no expectation was changed.

Production import census therefore still finds `runner.ts` through `media.ts`, the command barrel, state, and history. Remaining A4 files include `runner.ts` (605 lines), `types.ts` (192), all **19 capture files**, and **19 fixture files**. D31 remains unchanged at **397 lines / 40 assertions**. No prohibited paths, dependencies, transport shapes, or save/outbox code were modified.

Source: `84330da5fd0886c84a9c4eb8dbfc9547b101a4b4`; base tree `d472e2a3163e0ccc389bd79b759d00238b5b5709`; final diff SHA-256 `c6d57eaa4902314882920e7ed1f0013a826fc5fb8ea7b0e30d44a83ecf8a44bb`.

`commit-msg` and `BLOCKED` were written. Recommend reviewing this independent cut, then assigning the remaining caller/API migration and fixture correction. No full/browser/backend/HTTP runs occurred; provider authority remains unverified.