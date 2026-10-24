## P2 report

Updated only:

- `tests/e2e/local/three-products.p2-tour.spec.ts`
- `tests/e2e/local/support/p2-parent-oracle.test.mjs`

The shared Undo oracle now requires the complete v2 envelope. Added strict controls for old-minimal RED, full-shape GREEN, and label/step/tag/patch/read/command/base/missing/extra mutations.

Tests:

- Node controls: **10 passed**
- `tsc` node/app/root: **passed**
- ESLint: **passed**
- `git diff --check`: **passed**

Protected regions remained identical:

- Parent: `be3db6fe…ba36`
- Transition single: `522c98e2…138c`
- Transition bulk: `df955842…010f1`
- Element: `b808664d…e4c8c3`
- Register: `74b181b1…04f383`
- Placement: `c937808c…210ea`

Whole-file SHA256:

- Tour: `07fe3d84…ed2f3c` → `cde93cde…a6c6c2`
- Oracle: `98934ece…d1d272` → `1325cf1f…d45a841`

Base source commit: `32036b3c…6fc239f`; retained actual source commit: `bceb0350…bb09b419`.

No browser/full suite or Runtime diagnosis was run. Independent Luna review remains required before merge. `DONE` and commit message are present.