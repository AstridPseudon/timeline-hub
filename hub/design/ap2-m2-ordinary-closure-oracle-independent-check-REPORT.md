# AP2 M2 ordinary closure-oracle independent check

## Result

**APPROVE** candidate `bbffe1a56a96badc49049bb92ca072d74330c93a` (`test(app): repair ordinary undo closure oracle`). No HOLD findings.

The retained 12181 failure was correctly classified as a source-shape mismatch: the old `beforeDocument = revisionBody(...)` was the normal parent projection, so `beforeDocument.shot_revisions` was `undefined`, while the accepted undo response was a full canonical closure containing the retained `f2-shot` record. The candidate fixes only that ordinary test oracle over the approved `b1887f206`/`966472b61` donor.

## Assertion review

The new `canonicalDocumentAt` source read is correct and pre-A: it reads the parent through the existing normal composition-revision GET, obtains the exact dependency manifest, reads every manifest shot and internal-timeline revision through normal Runtime GETs, and reconstructs the canonical document with the original array order, pins, payloads, opaque data, internal references, and manifest. It does not use post-undo or `agentEdit` data, normalize absent fields, or substitute empty closure arrays.

The focused shape control requires the authoritative pre-A source to contain the seeded parent, `f2-shot`, internal timeline, and matching manifest pins; this fails the old parent-only source shape. The expected final state is an independent clone of that pre-A canonical source with only the literal disjoint Agent-C `S1` label overlaid. The final assertions retain exact parent payload, shot closure, internal closure, and dependency-manifest equality, followed by the existing immutable-closure, opaque, zero-legacy, retry/rebase, credential, and both-undo guards.

Old -> new assertion map:

| Old assertion | New assertion |
| --- | --- |
| `undoOrdinary.data.canonical_document` equals post-ordinary `agentEdit.data.canonical_document` | Parent payload equals an independently captured pre-A parent after only literal Agent-C `S1` label overlay. |
| Whole-document equality implicitly checked closure | `shot_revisions`, `internal_timeline_revisions`, and `dependency_manifest` each equal the independently captured pre-A source. |
| Parent-only `revisionBody` source supplied `undefined` closure fields | Normal parent + manifest-driven shot/internal reads build the full authoritative closure; one focused shape control proves it. |

The candidate-vs-donor oracle delta is row-local to `tests/e2e/local/three-products.spec.ts`; the donor’s `S1` fixture, authoring setup, ten commands, records, raw ordering, conflict/guard, retry/rebase, credentials, zeroLegacy, and both undo assertions are preserved. No product Runtime inverse, API, provider, schema, pin, dependency, or fallback change is introduced by this repair.

## Evidence

Read-only candidate checks:

```text
git diff --check b1887f206 bbffe1a56a96badc49049bb92ca072d74330c93a — PASS
old `toEqual(agentEdit.data.canonical_document)` absent in candidate — PASS
```

Writer-provided targeted evidence, verified in its worker log:

```text
npx vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/commands/ordinaryRealBatch.test.ts \
  src/test/threeProductsAuthoring.test.ts
  3 files, 21 tests passed

ASTRID_CHECKOUT="$PWD/vendor/astrid-browser" VITEST_LANE=checkout \
  npx vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/dev/localExtensions.catalog.test.ts
  2 tests passed

npx playwright test --config playwright.three-products.config.ts \
  --grep 'M2 ordinary extension batch' --list
  1 test listed; no browser execution

npx eslint --no-warn-ignored --max-warnings 0 [all touched TypeScript files] — PASS
npx tsc --noEmit --pretty false — PASS
git diff --check — PASS
```

No browser, socket, real gate, `request-test`, or full suite was run, as required. The central 12181 journey remains the retained pre-repair failure; this review establishes assertion-conversion approval, not a new central pass.
