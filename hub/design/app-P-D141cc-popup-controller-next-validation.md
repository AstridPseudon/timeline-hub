# D141cc popup controller validation

Source and custody checks passed before dispatch:

- Four exact detached clean source pins matched the accepted SHA/tree tuple: App `82e9e13d` / `6a6e49e`, Agent `ecdc242e` / `d362fe9`, Runtime `95d98f03` / `78df31d`, Composition `635f4de0` / `5ab5191`.
- Unchanged builder SHA-256 `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f`; Git blob `59b65214bc74c1ca118b097bc3b13c0ffe480a93`.
- Accepted source-control checker was already recorded as exit 0 with all 43 controls; no private checker rerun or body test was performed here.
- Final retry-1 pre-submit inspection returned `FIRST_NATIVE_INVOCATION_ONLY`; retry namespace was empty of requests, artifact, lock, and registry row.

Native execution evidence:

- Exact production `Node/tsx d66-plain-stack.mjs p2-popup-add --submit` ran once in `/home/user/work/app` under retained session `86698`.
- The native tool returned exit 0 and created one preflight ID and one normal ID. No second submit, manual request recreation, direct `request-test`, alternate selector, or diagnostic was run.
- `wait-test` observed only normal ID `app-pin-82e9e13d-full-d141-p2-popup-add-82e9e13d-submit-popup-retry-1-1026111307-27026`; command exited 1 because the service result was terminal fail.
- Terminal result: one readiness test passed; the popup test failed at `three-products.p2-popup.spec.ts:941` because the expected shared occurrence shot-group locator was not found. This is retained as a functional failure with cause not determined; no diagnostic rerun.
- Native service disk trace validation passed with 44 samples and a 5,471,948,800-byte minimum, above the 4 GB standing stop.

Product source, tests, types, lint, pins, registry, queue, and Git metadata were not modified. Product tests/typecheck/lint outside the authorized named journey are N/A by scope.
