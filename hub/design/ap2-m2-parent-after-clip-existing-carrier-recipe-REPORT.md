# AP2 M2: parent `afterClipId` existing-carrier review

## Result

There is no qualified existing carrier in the current integration pair for the
normal parent `afterClipId` generation consumer. This is a bounded peer request,
not an App activation recipe. No product files or public schemas were changed.

## Semantics that must be preserved

Normal `afterClipId` is parent flat-timeline scope: the user selected the raw
parent clip anchor, not an occurrence/shot child. Occurrence duplication and
occurrence auto-placement are separate paths and must not consume this request.
Pinned shot groups remain refused on the normal path.

The current Main implementation (`src/tools/video-editor/lib/duplicate-clip.ts`)
defines the exact local behavior: resolve the source row/track by the raw clip
ID; use `duration = max(0.05, source.end - source.start)`; create a new ID at
`source.end`; shift every later action on that same row by `duration`; insert the
new ID immediately after the anchor in clip order; and clone source metadata,
changing only the new identity/effect identity and asset. Other tracks and
occurrence-owned data are untouched. The prepared native branch explicitly
rejects `afterClipId`; the accepting prepared branch is the local
`place-prepared-media` writer.

Before the async generation await, the consumer must freeze the user's raw
`afterClipId`, the original parent bundle/head/projection/session basis, the
source row/track, source interval, parent clip collection membership/order, and
reserved destination clip/asset identities. After generation, it must retain the
exact returned five-field Runtime media selection and verified media. It must not
re-read a mutable catalog or substitute a late selection.

## Why current carriers do not qualify

* App `clip.add-media` is closed to `{row, media}` and validates a literal
  parent `at`/`hold`; its current capture appends the row to the authored parent
  clip collection. It has no anchor, insertion-order, or same-row ripple.
* Agent `Recording.create(..., after=...)` records collection insertion order
  only; it does not shift later clip timing. Agent `clip.move` is fixed/absolute
  placement with no ripple.
* Current `auto_place_completion` is occurrence-owned and may resolve an absent
  anchor to fallback/lane-end. That is the wrong scope and would violate the
  explicit parent anchor choice.
* The existing local prepared-media duplicate test passes only because the App
  writer performs the legacy ripple/metadata mutation; retaining it is not a
  native EditCommand solution.

## Minimal bounded peer request

Agent/Runtime should qualify the existing parent `clip.add-media` capture,
recording, inverse, and rebase machinery with one bounded parent ordered/ripple
birth mode. This is an extension of the agreed carrier, not a new endpoint,
store, or DTO. The Agent owner must choose and generate the command shape; this
report does not guess a new public field.

The stable reference and outcome are:

* Before: `parent/clip:<raw-afterClipId>` is present in the original parent clip
  collection, with its raw track, half-open source interval, and exact collection
  order recorded; the exact media selection/verification, reserved destination
  identity, parent ownership, and pinned output rate are also captured.
* After: create `parent/clip:<reserved-id>` on the anchor's track immediately
  after the anchor, at the anchor's exact end, with the normal duplicate duration
  (`max(0.05, source span)` reconciled by the provider's canonical frame/rate
  rules), and shift every subsequent same-track parent clip by that duration.
  Preserve the source-authored metadata and leave other tracks/occurrences
  unchanged. Record the exact registry binding and all derived mirror writes.
* Inverse/rebase: remove the created row and newly-created alias, reverse the
  exact ripple/order writes, and refuse if the anchor is absent or its owner,
  track, interval, membership/order, rate, registry binding, or media selection
  differs. Replay the captured literal result; never recompute against the latest
  catalog, append, clamp, or fall back to lane end. Exact retries must preserve
  the same IDs and command body.

The peer qualification needs source tests for anchor-present insertion, missing
anchor, changed anchor timing/track/order, identity collisions, exact media
binding, inverse, rebase, and retry. Existing literal parent birth and frozen
occurrence cohorts must remain unchanged. Once that pair is qualified, App can
adapt the existing `parentClipAddMediaPort`; it must not add an App metadata
guard or another local writer.

## Evidence

Successful targeted tests (no HTTP/provider/browser/socket/full suite):

```text
TMPDIR=/tmp/ap2-m2-parent-after-clip-existing-carrier-recipe-tmp node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/media.test.ts src/tools/video-editor/contexts/VideoEditorProvider.test.tsx
Test Files  2 passed (2)
Tests       70 passed (70)

TMPDIR=/tmp/ap2-m2-parent-after-clip-existing-carrier-recipe-tmp node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts
Test Files  2 passed (2)
Tests       81 passed (81)
```

`git diff --check` passed. The assigned App worktree remains clean; no full,
browser, live-provider, generation, pin, or adoption tests were run.
