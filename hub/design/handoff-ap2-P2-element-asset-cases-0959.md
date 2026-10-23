# Handoff: ap2-P2-element-asset-cases-0959

Added the sole allowed product file:

`/home/user/work/wt/ap2-P2-element-asset-cases-0959/tests/e2e/local/three-products.p2-elements-assets.spec.ts`

The spec contains three real mounted cases: published `am-burst` apply plus parameter edit; parent file-drop registration with exact media selection and registry assertions; and embedded child file-drop placement using `occurrence.add-media`. They assert v2 request metadata, reply/receipt shape, `/commits` records, canonical closure/digests, opaque sibling preservation, reload, guarded Undo, and no legacy save/composition or `/doorlog` writes.

Static evidence:

- scoped ESLint: PASS;
- `git diff --check`: PASS;
- Playwright discovery with `playwright.three-products.config.ts`: PASS, 3 tests;
- `npx tsc -p tsconfig.json --noEmit`: PASS.
- Supplemental direct-file `tsc` reached existing diagnostics in `timelineDraftIndexedDb.ts`, `types/index.ts`, and `support/harness.ts:749`; it reported none in the new spec.

No browser, HTTP/body/socket/service, build, full suite, or `request-test` was run, as required. The child case deliberately does not launch the separate operation-proxy/image-generator executor; that is the remaining seam if “automatic placement” means that separate generator journey rather than mounted automatic child ownership. Farm execution and independent review are next.
