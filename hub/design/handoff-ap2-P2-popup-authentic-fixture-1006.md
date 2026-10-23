# Handoff: ap2-P2-popup-authentic-fixture-1006

The App proof worker added the new popup spec:

`tests/e2e/local/three-products.p2-popup.spec.ts`

It prepares a faithful current Runtime fixture with a real imported media selection and two occurrences sharing the existing shot/revision closure. The ADD and SWAP bodies use the mounted popup labels/data hooks, require the full-v2 A2 request/reply shape, assert the fork-plus-media command order and canonical preservation, read Runtime `/commits` history/bindings, reload, and issue guarded Undo.

The spec is source-qualified only. The separate A3 product worker must restore the mounted `Add media` / `Swap selected clip` caller and full-v2 request metadata before body execution. No product code was changed here, and the tests intentionally remain strict about that seam.

Static evidence:

- scoped ESLint — PASS
- TypeScript — PASS
- Playwright discovery with `playwright.three-products.config.ts` — PASS, 2 tests
- `git diff --check` — PASS

Browser/service/full-suite evidence is intentionally absent and belongs to the central test service after the A3 caller is merged.
