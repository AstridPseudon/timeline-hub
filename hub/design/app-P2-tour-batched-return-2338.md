# P2 report

Implemented source-only corrections in:

- `tests/e2e/local/three-products.p2-tour.spec.ts`
- `tests/e2e/local/support/p2-parent-oracle.test.mjs`

Changes:

- Preserved parent8232 full Undo-envelope correction and controls.
- Corrected single/bulk transition intent to exact authored form: `Clear transitions: <ids>`.
- Strengthened step assertions and added exact single/bulk request controls.
- Added RED/GREEN and negative mutation controls; dedicated oracle passes 13/13.
- Bulk `None` failure is a product display defect, not a test issue. Owner: `BulkClipPanelBody.tsx:541–560`, with sentinel behavior from `PropertiesPanelBody.tsx:245` and `select.tsx:36–42`. Test assertion remains unchanged.

Source evidence: pinned commit `bceb0350326f22beefdde5c5ba275412bb09b419`; relevant blobs include handoff `bf167a51…`, bulk panel `066fcc46…`, primitives `5a7f064e…`, select wrapper `c9ca9929…`.

Tests:

- Node oracle: 13 passed
- Node TypeScript check: passed
- App TypeScript check: passed
- Root TypeScript check: passed
- ESLint scoped checks: passed
- `git diff --check`: passed

Protected-spec comparison against predecessor: only the tour hash changed (`07fe3d84…` → `da55dba9…`); other five protected specs unchanged.

No browser/full suite run. Independent Luna review remains required. Commit message and `DONE` marker are present.