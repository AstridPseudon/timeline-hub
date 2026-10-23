# R2r client guard repair

## Result

PASS for the requested Runtime source repair against base `21482a416d1f0f976ec563b9e1bf96a765f80e56` (tree `7a182a69`). The public generated Python and TypeScript commit clients now accept contract-valid `merged` replies while retaining `accepted` and legacy `rebased` compatibility. Preview replies still require `status: preview` and a null receipt.

Diff: `e3d1645520ceec003a060c6b912f372ab2b1e35ce0d11ef37853042fb78eadb7`.

## Changes

- Widened the canonical Python template guard and regenerated `packages/python/.../generated.py`.
- Widened the canonical TypeScript client guard in `packages/typescript/src/generated.ts`.
- Added contract-valid public-client regressions for accepted/merged live replies, accepted/merged previews, full result/receipt preservation, and malformed status/missing/array receipt refusal.
- Refreshed `contract/artifacts.json` through the normal manifest tool.

Successor producer tuple: schema `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`; contract `0.2.14`; artifacts version `sha256:b0a15d84defb5528f75d846413df8e575a0f4e18cd89855d486ee0ce54a83085`; Python generated `sha256:f4ee7ce3919c12b3baae3cbf202c2df2afc16616be733dbd2cab89fbc4472f18`; TypeScript generated `sha256:607ece1c559cc3465b9cc560bf2a9bada0e10047caa7bd66269c73a0a58df1ef`.

## Evidence

- Central targeted service `rt-R2r-client-guards-0233-targeted-1023023409-13438`: **PASS**, 124 passed in 33.86s.
- Direct public-client subset: **PASS**, 8 passed.
- `npm run build --prefix packages/typescript`: **PASS**.
- `python generators/generate.py --check`: **PASS**.
- TypeScript conformance generator `--check`: **PASS**.
- `python scripts/artifact_manifest.py --check`: **PASS**.
- `git diff --check`: **PASS**.
- Ruff comparison: touched Python files have the same finding counts as exact base (template 2, generated client 1, test 14); no findings occur on added Python test lines. Scoped Pyright reports only inherited diagnostics; no diagnostic was emitted on the added helper/regression lines.

## Limits / blocked checks

- `npm test --prefix packages/typescript` is **FAIL** before test execution: installed TypeScript reports TS5112 for the existing `tsc --noEmit ... test/public-api.mts` command. The package's existing `client.test.mjs` also has a baseline Node syntax error at EOF; this file is unchanged by the task. The generated-client TypeScript regression ran successfully through the Runtime targeted service.
- No real provider acceptance, full/native/browser/live-socket suite, or integrated consumer proof was run. This is transport/client-envelope proof only; adoption still requires independent review, merge, and integrated proof.
