# Validation

- Read-only Git object comparison: PASS. `a4e016b6` and `96df3f5b` have equal
  relevant blobs for `host_bootstrap.py`, `remotion_runtime.py`, and the exact
  host test.
- Retained source-manifest and preflight receipts: PASS for the declared current
  tuple, expected origins, schema digest, Runtime lock, Node, profile, and
  launcher controls.
- Retained 18455 log parse: PASS for the shared first host boundary and the
  `PYTHONNOUSERSITE` rejection path.
- Retained bounded 1345 XML parse: PASS, 14 tests / 0 failures / 0 errors.
- Retained pristine 26621 XML parse: PASS, 14 tests / 0 failures / 0 errors.
- No tests, collection, provider, package/profile acquisition, sockets,
  browser, render, or production writes were run by this worker.
- Raw XML/log payloads and private environment values were not copied into this
  evidence; the prior complete 1345 environment receipt is EXACTMISSING.
