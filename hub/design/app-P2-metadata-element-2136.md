## Report

- Ran one isolated original D66 `p2-element` submission from normal App.
- Tuple: App `245742dc…`, Agent `840a58a7…`, Runtime qualified `bc04caa2…`, Composition `635f4de0…`.
- Host: `app-pin-245742dc`
- Preflight: PASS, request `…preflight-1024213610-23701`
- Normal request: `…-1024213640-11589`
- Result: FAIL, exit 1, 190 s.

Evidence:

- Readiness: 1/1 PASS, 26.3 s.
- Original element: 1 test, 1 failure, 23.454 s; failure at `three-products.p2-elements-assets.spec.ts:412`, waiting 5 s for `status` text `applied`.
- Same Runtime boundary: request ordinal 3, `provider` phase, `validate_commit_value` at `runtime_protocol/timeline_commit_validation.py:173`, category `historical_sequential_capture_jsonschema_validation`.
- Pending window: 4,558 ms to test outcome / 4,626 ms to page close, versus prior 4,526 / 4,592 ms.
- One private 0600 watchdog dump retained; SHA-256 `4dc124762e2b47ff41ce36b32d8e8dfb1effd346dcf0022c6f8bdf84a4f71269`.

Artifacts remain private. Manifest SHA: `d0ec1e61…`; original XML SHA: `82b76c53…`; readiness XML SHA: `c4638e1d…`. Protected test hashes were unchanged.

No product changes, retries, other cases, full tour, or diagnosis loop. `DONE` and commit message were created. Next step is a meaningful Runtime fix before further cases.