## Report

Implemented D96 fixture migration.

- `seedThreeProducts(..., occurrenceHostWindow = 12)` now derives occurrence duration, full plate hold, and expected occurrence shape from one value.
- Only `three-products.p2-elements-assets.spec.ts` opts into `14`; all other 16 callers retain default `12`.
- Added source-driven caller/seed control.

Tests:

- `p2-placement-seed-window.test.mjs` + receipt control: 3 passed.
- D66 source/list control: 24 passed; aggregate P2 = 8, isolated placement = 1.
- Embedded Python compile/AST: passed.
- App and Node TypeScript checks under `.app-tsc.lock`: passed.
- Scoped ESLint: passed, 0 warnings.
- `git diff --check`: passed.

Hashes:

- Harness: `92f126...1956` → `bcefb8...16bd`
- Seed source: `6120be...efe9` → `9fba1a...1a6a`
- Protected placement body: unchanged `ea9c04...c5b7`
- Protected waits: unchanged `320cb6...9a28`

No browser/service/body execution performed. Independent review and normal merge remain next steps.