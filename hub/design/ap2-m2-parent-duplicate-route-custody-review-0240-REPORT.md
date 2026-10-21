# Parent generation-duplication route review

## Verdict

**Approved for the exact source-only scope, as a bounded-refusal proposal.**
This is not accepted-workflow evidence and must not activate or delete any
production path.

The reviewed source is commit `70820a770` and adds only:

`tests/e2e/local/three-products-parent-duplicate-generation.spec.ts`

The source correctly refuses to invent a catalog result, media tuple,
version, metadata, compiler result, fixture, or writer. Its accepted-path
assertions are comments describing future work; they are not presented as
passing evidence.

## Custody review

- The UI trigger is the real ClipAction context-menu item `Duplicate
  generation` (`ClipAction.tsx:241-251`), forwarded to
  `AstridTimelineEditor`'s `handleDuplicateGenerationClip`. It is distinct
  from the independent-shot path; the reviewed source does not call or
  recreate `duplicateIndependentShot`.
- The test uses the existing three-products harness. That harness creates a
  throwaway Runtime realm and project, so it does not mutate an existing user
  project. The test itself performs no accepted mutation.
- The normal seed's `f2-app` and `f2-video` registry entries have object/digest
  authority only; they do not have generation-backed catalog identity. The
  source therefore fails closed when no generation-backed ClipAction exists,
  rather than adding synthetic `generationId`, `variantId`, or
  `MediaSelection` fields.
- The current adapter still raises the frozen bridge-capability refusal for
  generation duplication. The proposed refusal assertion expects the visible
  `Failed to duplicate generation` result and checks zero Runtime commit
  requests, zero legacy composition-revision writes, and an empty timeline
  command outbox.
- The source does not claim to prove stable allocation, reload/undo, lost-ack
  restart retry, or producer fencing. Those are correctly listed as pending
  accepted-path assertions. The existing preparation carrier preserves the
  intended original bundle, displayed head, outbox basis, and
  `localGeneration` authority, but this source cannot exercise it while the
  producer is unavailable.
- The current native prepared-media command explicitly refuses `afterClipId`
  placement (`useTimelineCommandsService.ts:474-492`). The source keeps that
  exact placement requirement visible and does not convert it to append/time
  placement.

## Required boundary before any central run

Keep execution held until all of these are supplied by their owners:

1. An existing normal generation-backed catalog fixture and the real catalog
   duplication producer returning the original five-field Runtime selection.
2. The reviewed producer-to-prepared-asset carrier, with the original
   selection detached before producer awaits and the existing base/epoch
   guards retained.
3. Native prepared parent placement supporting the requested `afterClipId`
   order through the existing command session/outbox.

Until then, the source is a refusal proposal only. Do not treat its comments,
static checks, or refusal boundary as proof of accepted duplication.

## Verification

Passed on the exact source blob or review tree:

- `./node_modules/.bin/eslint --stdin --stdin-filename tests/e2e/local/three-products-parent-duplicate-generation.spec.ts --max-warnings 0`
- `git diff --check hub/timeline/app/tl/integration...tl/ap2-m2-parent-duplicate-generation-route-proof-source-0232`
- Static changed-file check: the source branch changes only the one new e2e
  spec; no production or shared support file is changed.
- Submitted-source collection:
  `./node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products-parent-duplicate-generation.spec.ts --list`
  — passed, exactly one test collected. The source worktree was recycled
  before this review, so this collection result is the source worker's exact
  in-repo evidence, not a browser execution.

Not run: browser, localhost/live socket, central, full suite, install, or
production activation/deletion. No accepted placement, reload/undo,
lost-ack/restart retry, or native duplicate result is qualified.

