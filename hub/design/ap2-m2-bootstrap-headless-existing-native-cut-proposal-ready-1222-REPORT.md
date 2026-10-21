# AP2-M2 current-public014 native headless-repair proposal

Status: proposal complete, intentionally unapplied. The App worktree is unchanged.

## Result

The smallest current-public014 native cut is already present on `tl/integration` at
`c85da5427` (including ancestor `5c53ed21f`). `createDefaultTimeline.ts` now routes
both new canonical timelines and an existing null-head shell through
`RuntimeDataProvider.initializeNativeBootstrapTimeline`. The headless path keeps the
existing timeline ID, passes `createName: null`, and uses the existing native
`timeline.init@1` / guarded capture / outbox flow.

No row-local edit is required. There are no `publishEmptyTimeline` or
`publishParentComposition` references in `src/integrations/runtime/createDefaultTimeline.ts`.

The companion patch is the exact row-local deletion and one-to-one native test
conversion from ancestor `5c53ed21f^` to `5c53ed21f`. It is supplied for HOME review
only; it is already in the current base and therefore must not be applied to this
worktree.

## HOME-owned shared writer decision

No honest deletion/replacement hunk exists yet for either shared writer. Leave both
sites unchanged and preserve their current capabilities:

```text
src/integrations/runtime/dataProvider.ts:295
  this.client.publishParentComposition(
    request.projectId, request.parentDocumentId, publication, idempotencyKey
  )

src/integrations/runtime/dataProvider.ts:1131
  this.client.publishParentComposition(
    this.projectId, timelineId,
    { expected_head, parent_revision_id: idempotencyKey,
      parent_composition, internal_timeline_revisions: [], shot_revisions: [] },
    idempotencyKey,
  )
```

The first is the shot-composition/placement graph carrier; the second is the generic
editor snapshot/config carrier. They accept non-pristine authored graphs, raw opaque
values, null-head publication, and nonempty timelines. `timeline.init@1` only
represents the authenticated App default-pristine bootstrap (the default name/slug,
output/config, tracks, and `registry.assets` birth with no children or dependencies).
Replacing either call with the native initializer would silently down-convert or lose
authored data. This is the exact genuine block for a shared cut, not a blanket refusal
of those inputs.

Raw/custom carriers additionally require the unpublished `timeline.init@2` contract.
Do not invent `init@2`, add a custom-canvas downconversion, introduce a new baseline
writer, DTO, authority, or pin. Preserve those capabilities through the existing
writer until a published command carrier and consumer proof exist. The two shared
families must be qualified and cut independently; the current native default-pristine
initializer does not qualify either family.

## Existing test delta and preservation

The native targeted coverage is already present in
`src/integrations/runtime/createDefaultTimeline.test.ts`:

- The old canonical-empty publication test is converted one-for-one to
  `creates and initializes a canonical empty timeline through the native Runtime transport`.
- The old stable-publication retry test is converted to
  `replays the exact native initialization request after a lost response`, asserting
  identical commit bodies, stable idempotency, and no legacy composition-revision
  write.
- The headless repair test keeps the original same-ID/null-head intent and now asserts
  `parent-0`/`bootstrap-p0`, one create, one init, and no `publishParentComposition`.
- Existing opaque-headed, alias, reassignment, CAS, additional-timeline, unresolved-
  alias, and metadata-preservation successes remain positive tests.

The original generic null-head graph positive remains unchanged in
`src/integrations/runtime/shotCompositionRuntime.test.ts` (`publishes a prepared graph
against a null initial Runtime head`). The adapter's explicitly-null expected-head
positive also remains unchanged. Neither is skipped, weakened, or converted to an
expected failure, because the shared writer capability is still required.

## Review evidence

Independent source checks on the clean worker tree:

- `git diff --check` — PASS.
- `rg -n "publishEmptyTimeline|publishParentComposition" src/integrations/runtime/createDefaultTimeline.ts` — no matches.
- Shared writer references are only the two retained `dataProvider.ts` sites at lines
  295 and 1131.
- `5c53ed21f` is already an ancestor of `HEAD`; the companion patch is deliberately
  unapplied historical/current-public014 activation material, not a second edit.

Targeted evidence:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/integrations/runtime/bootstrapInitialization.test.ts \
  src/integrations/runtime/createDefaultTimeline.test.ts \
  src/tools/video-editor/commands/bootstrapCapture.test.ts \
  src/tools/video-editor/commands/commitOutbox.test.ts
PASS — 4 files, 129 tests

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism \
  src/integrations/runtime/shotCompositionRuntime.test.ts \
  src/integrations/runtime/dataProvider.test.ts
PASS — 2 files, 95 tests

./node_modules/.bin/eslint src/integrations/runtime/createDefaultTimeline.ts \
  src/integrations/runtime/dataProvider.ts \
  src/integrations/runtime/bootstrapInitialization.ts \
  src/integrations/runtime/createDefaultTimeline.test.ts \
  --report-unused-disable-directives --max-warnings 0
PASS

./node_modules/.bin/tsc -p tsconfig.strict-islands.json --noEmit
PASS
```

`./node_modules/.bin/tsc -p tsconfig.app.json --noEmit` was also checked and fails on
pre-existing unrelated composition/viewing errors (missing transition/audio/player
exports and existing timeline typing errors); no files were changed to mask them.
No browser/full suite was requested, per the task boundary.

## Next step

HOME should treat the companion patch as already landed row-local evidence, not apply
it again. The next shared cut requires a separately qualified native command producer
for the shot graph at line 295, followed by an independent migration for the generic
snapshot carrier at line 1131. Until then, keep both writers and their original
success tests.
