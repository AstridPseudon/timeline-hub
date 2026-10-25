## D123 review report

Verdict: **SOURCE_PASS**

- Restored assertion exactly matches `b545b616`:  
  `assert 'Hidden' not in service.render('win32', version, data, log)`
- All six current-normal paths match `b545b616`; 3,571-source inventory and tree hash verified.
- Protected predicates: **173/173 retained**, none missing/weakened.
- Packaging patch: **12,072,718 bytes**, SHA-256 `b0ff420595441fccb3d0a37b70715e5b2bff373cecd9d2e51c82be51cbe58f6b`; reverse apply passed.
- Only product delta from the failed review is the one assertion line; remaining change is D123 metadata.

Checks:

- Targeted Windows test: **1 passed**
- Mypy, compile, vendor lock, artifact manifest: **PASS**
- Ruff: inherited `I001` and `BLE001` only
- Clean/repair `git diff --check`: **PASS**
- Base diff retains 157 inherited whitespace diagnostics

Unverified as required: full C0 matrix, wheel fixture (`astrid.core`), full/browser/render/stage/download/P4/final suites, and actual Windows-host execution. Candidate remains held for D59; no integration/gating merge.

Evidence: `.../workers/rt-F-D123-predicate-review-1317/evidence/`. `DONE` and commit message are present.