## Result: PASS

- Added harness-only [run-d13-wheel-input-0039.sh](/home/user/work/wt/agt-F-D13-wheel-input-0039/tools/run-d13-wheel-input-0039.sh).
- Built authentic Agent c36 wheel from exact commit/tree using normal `build 1.4.0 --no-isolation`.
- Verified c886 installed payloads, RECORD/direct URL, `python -I` origins, source digest, Node20/819acf resources, and original D13 body hash.
- Bound a new four-field profile carrier to immutable c886; no product, test, pin, schema, or managed-environment changes.

Tests/checks:

- `tools/run-d13-wheel-input-0039.sh` — report-all preflight PASS; original D13 preflight **1 passed in 13.92s**.
- `bash -n tools/run-d13-wheel-input-0039.sh` — PASS.
- `git diff --check` — PASS.
- No native/runtime/render/full suite run.

Evidence:

- Wheel SHA256: `5d9440099ffce5882a9e1cc568cb06b574f80812c684d4478f1898b78cbb437a`
- Source commit/tree: `c36ca8c94b695b0e25b7d42c89f194661f187423` / `50689a445fcae5ca54ba2e7e8f1d99e9a2c43c92`
- Evidence manifest, bindings, and profile are under the worker evidence directory; wheel remains in TMPDIR because its 57.7 MB size exceeds the 35 MB evidence cap.
- `DONE` and commit message written.