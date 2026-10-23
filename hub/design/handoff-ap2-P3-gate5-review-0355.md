# P3 Gate-5 independent source review

Source review of App target `7116a8e2898585fb1e685322a397fd6f0f641f9a` (tree `245f150acdd0950c8a023595e0472ce8dad426c2`, parent App9eda) is **FAIL / request changes** for test-coverage strength, not for a production behavior regression.

The one-file diff preserves the original Gate-5 reset, lost ACK, A/C/B ordering, restart, exact retry, full raw/immutable closure, C preservation, mounted Undo, history/zero-legacy checks, and the original exact-selector collect-one assertion. It correctly retains historical `rebased` tolerance while requiring the new dependent replay to be `merged`; cursor pages now also verify a pinned history head.

Concrete findings in `expectV2History` (`tests/e2e/local/three-products.spec.ts`, roughly 846–948):

- declared request/history `reads` are not asserted;
- step `patch` and `dependencies` are only `expect.any(Array)`, so complete authoritative step reads/dependencies and patch contents are not proved;
- `document_digest` is checked only for shape, not against a recomputed/authoritative digest.

The helper does check request scope/base, commands/label/steps/merge/dry-run, idempotency-key-to-receipt identity, accepted/merged heads, canonical closure shape, receipt, history publication linkage, publisher, labels, merge mode, records, and command-record categories. Conflict/invalid/preview families are not claimed by this one journey. The current registered row reviewed was only `ORCH/tests/suites.conf:36`, `ap2-P3-gate5-h6-0348`; no global selector/launcher change was found.

Checks all passed: exact selector `--list` collected exactly 1 test; `npm exec tsc -- --noEmit`; `npx eslint tests/e2e/local/three-products.spec.ts --max-warnings 0`; and `git diff --check`.

P3 actual qualification remains **UNQUALIFIED**. Service `19140` failed before browser launch during hosted build with missing `@banodoco/timeline-composition/effects.generated` (`ENOENT`). Do not infer journey PASS; environment repair and the successor service run are separately owned.
