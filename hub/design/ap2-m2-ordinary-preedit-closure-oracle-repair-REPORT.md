# AP2 M2 ordinary pre-edit closure oracle repair

## Result

Repaired the ordinary12181 final undo oracle as a row-local test-source fix. The retained failure is a source-shape mismatch, not demonstrated Runtime inverse loss:

- The normal `GET /composition-revisions/{revision}` response is the authored parent projection and does not expose `shot_revisions` or `internal_timeline_revisions`.
- The accepted undo response is a canonical full closure and materializes the retained `f2-shot` record.
- Therefore the old `expect(undoOrdinary.data.canonical_document).toEqual(agentEdit.data.canonical_document)` compared a full closure with an incomplete parent-only source object and expected `undefined` for `shot_revisions`.

The ordinary test now captures `beforeDocument` before A from the existing normal parent read, follows that response's exact dependency-manifest shot and internal-timeline pins through the existing Runtime GETs, and builds the full authored `CanonicalDocument` with the exact payloads, raw pin order, opaque fields, internal references, and manifest. The expected post-undo closure is an independent clone of that pre-A source with only the literal disjoint Agent-C S1 label changed. No expected data comes from undo/actual, and no absent closure field is dropped.

The approved b188966472/966472b61 donor delta was ported onto the requested integration base; the current e401af7215e9adf54b1cb4c5bce8d386721bec7d HOME alias repair was already present and was not changed.

## Assertion mapping

| Original assertion | Equivalent stronger source assertion |
| --- | --- |
| Entire undo canonical document equals `agentEdit` | Parent payload equals the independent pre-A parent payload after only S1’s literal Agent-C label overlay. |
| Implicitly compare child closure through that whole-object equality | `shot_revisions` equals the independently captured pre-A shot closure; `internal_timeline_revisions` equals the independently captured internal closure; `dependency_manifest` equals the independently captured manifest. |
| Existing position and opaque checks | Preserved unchanged; `expectImmutableClosure` independently re-reads accepted parent/shot/internal payloads and receipt history, and zero-legacy/command/retry/rebase/conflict/both-undo assertions remain. |

Added one focused pre-A shape regression in the ordinary journey: it requires the independently sourced document to contain the parent, one f2 shot revision, one internal timeline revision, and matching manifest pins. The old parent-only oracle fails this shape check.

## Verification

- `npx vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/ordinaryRealBatch.test.ts src/test/threeProductsAuthoring.test.ts` — **3 files, 21 tests passed**.
- `ASTRID_CHECKOUT="$PWD/vendor/astrid-browser" VITEST_LANE=checkout npx vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/dev/localExtensions.catalog.test.ts` — **2 tests passed**.
- `npx playwright test --config playwright.three-products.config.ts --grep 'M2 ordinary extension batch' --list` — **1 test listed; no browser execution**.
- `npx eslint --no-warn-ignored --max-warnings 0` on all touched TypeScript files — **passed**.
- `npx tsc --noEmit --pretty false` — **passed**.
- `git diff --check` — **passed**.

No real gate, browser/socket run, `request-test`, or full suite was run. The retained12181 failure remains the evidence for the original classification; independent conversion is ready for review.
