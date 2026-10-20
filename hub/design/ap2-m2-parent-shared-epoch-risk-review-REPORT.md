# ap2-m2-parent-shared-epoch-risk-review

## Decision

**APPROVE — bounded shared-session packet only.** `f7e4f762f` is safe to merge
onto the current App integration root `20ea14c26526fe4924354f10a177aebbaf6002bc`.
It is not an approval of the downstream row-local parent-media producers or of
the complete parent-media migration.

## Review scope and ancestry

- Base under review: `tl/ap2-m2-parent-current-shared-packet` at `f7e4f762f`.
- Exact parent/current App root: `20ea14c26526fe4924354f10a177aebbaf6002bc`
  (`hub/tl/integration`, local `/home/user/work/app` `tl/integration`).
- `f7e4f762f` is one commit directly on that root; `git rev-list --left-right
  --count 20ea14c26..HEAD` reports `0 1`.
- The latest integration tree has no later overlapping updates. The source
  worker's required `bin/merge-forward` attempt was blocked before tree changes
  by the shared Git metadata refusing `ORIG_HEAD.lock` (`Read-only file
  system`). No conflicts or markers remain. The merge-ready source is therefore
  `f7e4f762f` with parent `20ea14c265...`; HOME can resolve the remaining shared
  merge operation.

Only these four files differ from `20ea14c...`:

- `src/tools/video-editor/commands/commitSession.ts`
- `src/tools/video-editor/commands/commitSession.test.ts`
- `src/tools/video-editor/hooks/useTimelineCommandSession.ts`
- `src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx`

No source edits were made by this review.

## Data-loss review

The add and swap preparation ports capture detached session authority before an
external producer can await:

- a deep-copied authored bundle;
- the command-session `localGeneration`;
- the predecessor basis (`after: lastIntent`) or accepted head basis;
- a copied displayed head.

`assertPreparationCurrent` checks all four values against the original live
session before a caller can finish or enqueue the producer result. The mounted
hook wrapper also checks `legacyClean()` both at preparation and at the later
assertion, so a dirty legacy save refuses without changing the outbox. Session
closure is covered by the existing `assertReady()` guard; recovery/undo paths
advance the local generation and rebuild the authored bundle from the persisted
intent or accepted basis, so an old in-session carrier cannot be adopted after
those transitions.

The original five-field `MediaSelection` authority is unchanged. The existing
add capture still deep-copies `media`, `finish` still passes `basis.media` to the
existing verified-media/native recorder, and retry stores the exact original
command payload. The packet adds no lookup, refresh, DTO, registry field, or
selection mutation.

Normal add behavior remains unchanged. The current integration root has no
activated native swap producer; the new swap surface is preparation/assertion
only and performs no write. The ordinary prepared `afterClipId` path and the
qualified native branch's explicit `afterClipId` refusal remain in
`useTimelineCommandsService.ts` untouched. No donor assertion was removed.

Important qualification boundary: the shared port cannot force an external
caller to invoke `assertPreparationCurrent`; the downstream row-local producer
must call `prepare()` before its first await and call the matching assertion
immediately before `finish`/native enqueue. That producer work is explicitly
outside this four-file packet and remains unqualified here. This is not a
blocker for merging the shared seam, but it is a blocker to claiming the full
parent-media journey or writer retirement.

## Evidence

Passed directly in this worktree:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
4 files / 129 tests passed

node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/media.test.ts
1 file / 5 tests passed

./node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx
passed

git diff --check HEAD
passed
```

The targeted session tests cover newer local generation refusal, dirty legacy
save refusal at preparation/assertion/finish/submit, exact native add retry
payload, and existing recovery/disposal behavior. No full, browser, localhost,
live-socket, dependency, pin, or external-provider suite was run.

## Next step

Merge `f7e4f762f` after the parent `20ea14c...` integration state is selected,
then review/qualify each row-local add and swap producer independently. Require
the downstream callers to retain the detached original selection, preserve the
raw `afterClipId` refusal, assert the captured session preparation after every
producer await, and prove no legacy traffic before any deletion claim.
