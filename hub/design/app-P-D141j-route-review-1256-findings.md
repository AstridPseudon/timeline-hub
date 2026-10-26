# D141j route-1249 independent review

Verdict: `FAIL` (`FAIL_FINITE_SOURCE_PACKET`). This is a readonly packet review. The native route remains `NOTRUN_FINITE_MISSING_SEAM`; no registration, request, browser collection, diagnostic body, CAS, queue, registry, or test service activity occurred.

## D141J-ROUTE-001 — wrong source-map test path

`route-1249/evidence/source-map.json` points its test-only installer/artifact/checker controls at `src/tools/video-editor/components/TimelineEditor/TimelineEditor.test.tsx`. That path is absent in candidate `3bb09fc656c6b8a81243f8f796115013b56d621f`. The actual file is `TimelineEditorCore.test.tsx`, with the first control at lines 254-294 and the repeated-read control at lines 296-371. The route’s source-change manifest already names the correct file, so this is a finite evidence-coordinate defect, not a source-semantics finding.

## D141J-ROUTE-002 — normal recipe is not emitted by the unchanged builder

Using pinned Node 20, actual tuple hashes, the existing Runtime helper identity, and only the exported `buildSubmitPlan`/`serviceRecipe` functions, the preflight recipe matched the packet exactly. The packet normal recipe did not: it is 1,114 bytes and omits `D66_RUNTIME_CHECKOUT='/home/user/work/wt/rt-pin-95d98f03'`; the pure builder emits 1,172 bytes. Packet normal SHA-256 is `94aa6d3f80f8489e83ec1f476aad3f55785effb4f48f20d4f7643fb1dd1f4b4b`; regenerated normal SHA-256 is `5cdd8db6eb6b1eac72eae8b37af7cc7efdf8542c425a1f54427eb1066df979e9`. This is a finite prospective route defect and must be corrected before any future admission.

## Confirmed facts and limits

- Original proof tuple remains App `82e9e13d`, Agent `ecdc242e`, Runtime `95d98f03`, Composition `635f4de0`; the prospective tuple is App `3bb09fc6` plus Agent/Runtime/Composition `ecdc/95d/635f`, and the App checkout remains unmaterialized.
- The popup ADD selector is unchanged at `tests/e2e/local/three-products.p2-popup.spec.ts:941-947`; builder, selector, normal manifest, and build-input manifest blobs match base.
- The accepted-read, active-occurrence, useShotGroups input/result, and pre-overlay coordinates resolve in the candidate. The independent 1245 review is `PASS_SOURCE_VISIBILITY`; that qualifies source semantics separately, not native mounted collection.
- The collector remains module-private and starts inactive. Candidate production code has no mounted caller for `installD141jVisibilityCollector` and no D66 transfer of `collector.snapshot()`. The Runtime phase helper is a Runtime capture sink only.
- Existing integration support has potential hooks: the real mounted page fixture/context lifecycle in `tests/e2e/local/support/app.ts`, mounted bootstrap retention in `mounted-readiness-safety.ts`, and page/context diagnostic retention in `support/p2-element-diagnostic.ts`. These are existing hooks for sole 1255 assessment only; they are not claimed wired to D141j at `3bb09fc6`.
- The initial five-second sampler observed 4.4G free, below the future 5.2GB admission requirement; the 4GB stop floor remains required. No native run was attempted.

Cause remains `UNKNOWN`. No product/test/source edit, pin, generated file, manifest, registry, queue, or Git metadata was changed.
