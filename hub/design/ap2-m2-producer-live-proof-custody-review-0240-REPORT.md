# AP2 M2 producer live-proof custody review

## Verdict

**REQUEST CHANGES / HOLD.** The exact new preparation tree is not ready for
central execution. It remains a future route-proof proposal only; this review
does not claim native acceptance, fresh/reloaded ownership qualification, or a
writer cut.

Reviewed branch `tl/ap2-m2-producer-ownership-live-proof-preparation-0210` at
commit `d19d9727a064fa4d476ee745d24fa7c94f93bd39` (tree
`f8f6f9c30dfc67571f9dd9144cbea9c7d6e45492`). It adds only:

- `tests/e2e/local/producer-ownership-live.spec.ts`
- `tests/e2e/local/support/producer-ownership.ts`

The two-file boundary is correct: no production source, DTO, authority, suite
wrapper, shared three-products spec, or source-repair file was changed.

## Findings

1. **Dedicated-timeline readback is wrong (blocking).** The fixture creates a
   random dedicated timeline at `producer-ownership.ts:73` and opens that URL,
   but `producerOwnershipRevision` at `:169-171` calls shared
   `currentHead(harness)` and `revisionBody(harness, head)`. Those helpers read
   `harness.seed.timelineId` (`tests/e2e/local/support/app.ts:52-54` and
   `:167-168`), not `seed.timelineId`. Consequently head changes, raw output,
   protected-clip comparisons, and retry readback inspect the harness's other
   timeline. The accepted path can time out and the refusal path can falsely
   pass against unrelated state. The helper must issue the same Runtime reads
   with the prepared seed timeline explicitly.

2. **The claimed lost-ACK path does not commit before losing the response
   (blocking).** The spec installs `holdCommandRequests` at
   `producer-ownership-live.spec.ts:110`. That existing helper holds delivery
   before Runtime sees it; `held.release(false)` at `:123` aborts the request.
   This is a dropped/uncommitted request, not “Runtime commits, then only the
   acknowledgement is lost.” Use the existing route-fetch/response-then-abort
   pattern so the real Runtime accepts the first request, then abort only its
   browser response. The current code also records/comparisons only
   `rawBody` (`:121-127`); it does not capture or assert the original and retry
   idempotency key, so it does not prove exact body/key retry.

3. **The accepted Scene move necessarily targets protected clips (blocking).**
   The seed places `sceneForeign` and `sceneUser` on visual track `V1`
   (`producer-ownership.ts:94-110`). The production Scene action's
   `moveExistingShotsToMarkers` operates on every visual clip, including those
   protected rows (`src/tools/video-editor/dev/scene-phase-markers/extension.ts:
   737, 821-834`). The accepted branch invokes it at
   `producer-ownership-live.spec.ts:150-154` and then asserts that no request
   targets protected IDs. A real accepted scalar move therefore includes
   `clip.move`/resize targets for the foreign and user clips, making the proof
   self-contradictory. The fixture/action pair must be narrowed so the exact
   producer action never includes protected rows, or the protected rows must be
   placed outside the action's selected visual set without inventing authority.

4. **Transcript IDs are not carrier-qualified (blocking for the accepted
   branch).** The fixture computes protected IDs and the expected fresh ID from
   bare source IDs at `producer-ownership.ts:31-33` and `:157`. The live
   transcript projection uses occurrence IDs of the form
   `sourceItemId@clipId` (`src/tools/video-editor/data/typed/transcriptProjection.ts:40`),
   and the producer hashes `item.id` (`src/tools/video-editor/dev/transcript-lane/extension.ts:356`).
   With the seeded `producer-ownership-speech-carrier`, the generated IDs are
   based on `source-id@producer-ownership-speech-carrier`; the expected missing
   ID is based on `source-id` alone. The accepted ownership assertion at
   `producer-ownership-live.spec.ts:101-105` therefore cannot find the fresh
   clip. Protected transcript rows also are not the IDs the producer would
   update, so this does not test the intended ownership collision.

5. **Protected presence is never asserted.** `protectedClipState` at
   `producer-ownership.ts:178-183` records `findIndex === -1` and
   `clip === undefined` as ordinary state. If initial publication or a read
   drops a protected row, every later comparison can still pass with the same
   absent sentinel. Add an explicit initial presence/identity assertion before
   treating deep raw equality and order as evidence.

6. **Refusal detection can reuse an old alert.** `waitForAction` checks all
   current alerts at `producer-ownership-live.spec.ts:48-56`, without a
   before/after marker or action-specific locator. In the refusal branch, the
   retry refusal remains visible before `sceneCreateShots` at `:89-97`; a
   missing/no-op Scene action can therefore be classified from the stale
   transcript refusal. Scope the refusal observation to the new diagnostic or
   clear/mark alerts per action.

7. **Branch whitespace check fails.** Exact `git diff --check` reports
   `tests/e2e/local/support/producer-ownership.ts:241: new blank line at EOF`.
   This is small, but the preparation report's claimed diff-check pass is not
   reproducible against the named branch.

## Checks run

All checks used an extracted copy of the named branch and the shared App
dependencies read-only; no browser, localhost, Runtime socket, central gate,
full suite, or source edit was performed.

- `node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 tests/e2e/local/producer-ownership-live.spec.ts tests/e2e/local/support/producer-ownership.ts` — **PASS**.
- Playwright one-case collection with a temporary minimal config and inherited
  isolated ports — **PASS, 1 test listed in 1 file**. No test executed.
- `node_modules/.bin/tsc --noEmit --pretty false` — **PASS** on the extracted
  branch tree.
- `git diff --check tl/ap2-m2-live-producer-ownership-negatives-0200 tl/ap2-m2-producer-ownership-live-proof-preparation-0210` — **FAIL**, one new blank line at EOF as noted above.

The independently approved source repair `9a5e`/`d148` remains untouched and
was not rerun. No acceptance or writer-retirement conclusion is made.

## Recommended next step

Repair the dedicated-timeline read helper, use a real accepted-then-response-
loss retry harness with exact body and idempotency-key checks, make the Scene
fixture's protected rows unreachable to the tested move selection, and derive
all transcript expected/protected IDs from the actual carrier-qualified
occurrence identity. Then rerun only lint and collection locally; central
execution remains the next qualification step after those source corrections.
