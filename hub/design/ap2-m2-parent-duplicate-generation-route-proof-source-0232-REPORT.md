# Parent generation-duplication journey source proposal

## What I added

Added one new focused Playwright source file:

`tests/e2e/local/three-products-parent-duplicate-generation.spec.ts`

It uses the production App fixture and the production ClipAction context-menu trigger (`Duplicate generation`). It does not create a generation, fabricate a five-field media selection, call a compiler/session helper directly, add a route, or alter shared support/production code.

The case is intentionally bounded at the current refusal boundary. It looks for an existing generation-backed clip through the UI, clicks the real menu item, and requires the visible duplicate-generation refusal while asserting zero `/commit` and zero legacy composition-revision writes. The source comments preserve the single future case's required accepted-path assertions: one allocated identity, original local-generation/displayed-base fencing across producer awaits, native `clip.add-media` placement, reload/guarded undo, lost-ack/restart exact retry, and zero legacy traffic.

## Exact blocker

The current integration cannot run the accepted journey without inventing authority:

1. `tests/e2e/local/support/harness.ts:886-972` seeds `f2-app` and `f2-video` as Runtime object-backed registry entries. They have object IDs/content hashes, but no generation-backed catalog identity (`generationId`/`variantId`) and no normal catalog duplicate fixture. The new spec therefore reports the missing existing fixture rather than adding synthetic fields.
2. `src/tools/video-editor/adapters/app/generationLookup.ts:13-21` still implements `duplicateGenerationAsset` as the frozen `bridgeCapabilityUnavailable` refusal. The real UI callback cannot obtain a duplicated catalog result on this integration source.
3. `src/tools/video-editor/components/AstridTimelineEditor.tsx:543-608` still builds a local registration plan and submits a registered prepared asset. It does not carry the original Runtime five-field `MediaSelection` into the prepared asset on this branch. The already-reviewed producer/fence reports identify the existing required flow: duplicated result -> `prepareGenerationAsset` -> `TimelineProvisionedAsset.mediaSelection` -> `commands.addClip`, with the original selection detached before the producer await.
4. `src/tools/video-editor/hooks/useTimelineCommandsService.ts:481-484` explicitly refuses `afterClipId` for a qualified native prepared asset (`Native prepared parent media only supports a new manual clip.`). The existing native carrier has no exact insertion/order capability for this consumer; converting to append/time would change the requested behavior.

The existing parent preparation/session port is present in the integrated source (`useTimelineState.ts:949-969`, `useTimelineCommandSession.ts:271-283`, and `commitSession.ts:51-73,367+`). It is the carrier to reuse for the original bundle, displayed base/head, outbox basis, and `localGeneration` fence. No new writer, pin, activation, endpoint, DTO, or authority is proposed.

## Live callers

- UI trigger: `src/tools/video-editor/components/TimelineEditor/ClipAction.tsx:241-251` renders and invokes `Duplicate generation` for a generation-backed clip.
- UI forwarding: `TimelineEditorCoreBody.tsx:805-807` supplies the callback; `TimelineEditorCore.tsx:839` forwards it.
- Residual consumer: `src/tools/video-editor/components/AstridTimelineEditor.tsx:543-608` resolves the source generation, awaits duplication, prepares/registers media, and calls `commands.addClip({ ..., afterClipId })`.
- Producer adapter: `src/tools/video-editor/lib/generation-utils.ts` re-exports `src/tools/video-editor/adapters/app/generationLookup.ts`.
- Prepared parent-media path already integrated for normal qualified media: `useTimelineState.ts:949-969` creates the parent-media command facade; `useAssetManagement.ts` supplies prepared assets; `useTimelineCommandsService.ts:474-539` verifies media and submits through the native port.
- Durable fence/outbox: `useTimelineCommandSession.ts:271-283` wraps the existing parent add-media port; `commitSession.ts` owns preparation, capture, finish, and submit.

`duplicateIndependentShot` is not a caller: the canonical occurrence path was already deleted, as required by the task boundary.

## Checks

- `./node_modules/.bin/eslint tests/e2e/local/three-products-parent-duplicate-generation.spec.ts --max-warnings 0` — passed.
- `./node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products-parent-duplicate-generation.spec.ts --list` — passed; collected exactly 1 test in 1 file.
- `git diff --check` — passed.

Not run: browser, localhost, live socket, central, full, install, or external-provider tests. No accepted placement, reload/undo, lost-ack/restart retry, or native exact-order result is claimed.

## Next step

First supply an existing generation-backed catalog fixture and land the already-reviewed producer selection carrier. Then add exact insertion/order support to the existing native parent-media carrier (or explicitly keep the bounded refusal). Only after those source prerequisites are present should the one collected case be run centrally; no legacy writer deletion should be based on this source-only proposal.
