# R2 report

- Ran the exact occurrence `True` original once on Agent `d4ba9916…` + Runtime `ab1e4f61…`.
- Result: **1 failed**, exit 1, 8.188s. Retained failure: `provider occurrence alias is outside its boundary` during `redo-birth`; attribution remains **UNKNOWN**.
- Command used: exact `pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short --junitxml=.../original.xml` selector.
- Admission passed: 5,130,645,504 bytes free; no concurrent heavy body.
- Verified clean immutable Agent, Runtime, App, and Composition identities and module origins before/after.
- No product, test, pin, route, registry, profile, or D130/SWAP changes.

Evidence written under:

`/tmp/.../workers/rt-Agent-R2-original-True-after-ab1e-1713/evidence/`

Includes `manifest.json`, `admission.json`, `source-map.json`, `result.json`, `original.xml`, and `validation.md`.