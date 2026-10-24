## Result

Fixed the offline verifier’s AJV schema-reference regression in `verify.mjs`. Registry validation now preserves the vendored `definitions` namespace, allowing `AssetEntry`’s `Meta` references to resolve.

## Evidence

- Retained Appfull16138: 33 offline-verifier failures, all caused by `MissingRefError: #/definitions/Meta`; mutation tests never reached their intended checks.
- Current source: `cca3deb361e8fbbc62ddf491d5fd09c7e542b99f`
- Actual full-suite tree: `3311baa327c8963d007cfc3a1b2f04617085f3b3`
- Frozen upstream App ref: `8f0c2484463e9b666d184a744d52e252984e551a`
- Upstream verifier source was byte-identical pre-fix; upstream schema lacked the current `Meta` definition, so this is an App regression, not proven upstream behavior.

All 33 nodes classified `core / ours-regression`:

- Lines 65, 80, 86, 92, 106, 114, 122, 133, 141, 182, 196, 204, 212.
- Lines 163 and 172 for every variant: `sourceUrl`, `sourceURL`, `assetPath`, `resourceUrl`, `videoURI`, `SourceURL`, `URLSource`, `source_url`, `source-url`, `source.url`.

## Tests

- `node scripts/astrid-landing/offline-verifier/verify.test.mjs` — **33 passed**
- `git diff --check` — **passed**
- `node --check scripts/astrid-landing/offline-verifier/verify.mjs` — **passed**

No full suite or browser/service run was requested.

Independent security review is still required before merging this validator change. Commit message and `DONE` marker were created.