Implemented P3 D53 in the three allowed paths:

- Transferred cumulative `82cb..bd08` helper delta.
- Applied strict mounted Gate5 `[A,A]` identity guard.
- No donor ancestry, product changes, or protected Gate5 body/reset/tail changes.

Tests passed:

- Node support tests: 23/23.
- Serialized TypeScript checks: root, app, node.
- Scoped ESLint: passed.
- Playwright list-only: 15 tests.
- `git diff --check`: passed.
- Reverse-removal reconstructed exact `82cb` bytes.

Hashes:

- Full spec: `26c1ae764013f8907ff7f3664dbcee016c88bc17a797f66800d012e618165d5b` → `95d9a3e728509ad95b591b94bece0fc4942d040a0b160afa654815c0b3dd296c`
- Gate5 body: unchanged `d47d55265b3905a1882ffb370df033cf92b35c3492d4bec366d8da0272b9fb20`
- Reset block: unchanged `980b4cbe2c1d7a05840c8419fd55991ff73783784c89df6c717e2721a212fe62`
- Protected canonical tail: unchanged `5ede6f374857a66a327da3cea0e85de0457a04267003f3f66e3d40ee4f380912`
- Downstream protected tail: unchanged `6bfdd99dfddf9608d24da81345884e4d32329b3414bd43eeb55ffe3bdde18f74`
- Fault helper: `2b5640862fb5ee4200131ce03974020e235ab963e7bb51326162278a8148c2da` → `3e896066737d9e8f07eccfdcb25f88f16d6e8e48457281f1b986af0b1cab7434`
- D53 guard: `15b580777856fb3d4b6494fbb52f8dcc8c83712ce3ce0c7f6a1cda19431bdfd5` → `1c080595fbb1dd5fb6ecc7387e9bf01744e0b08e61473d3994383e226b60a9e0`

Decision: changed only the mounted-document Gate5 path; all other original before-B guards remain intact.

Behaviour ledger: `D53 | fullspec 26c1ae764013f8907ff7f3664dbcee016c88bc17a797f66800d012e618165d5b→95d9a3e728509ad95b591b94bece0fc4942d040a0b160afa654815c0b3dd296c; guard 15b580777856fb3d4b6494fbb52f8dcc8c83712ce3ce0c7f6a1cda19431bdfd5→1c080595fbb1dd5fb6ecc7387e9bf01744e0b08e61473d3994383e226b60a9e0; branch tl/ap2-P3-D53-clean-apply-1123; home/integrated pending harness commit and App integration.`

Browser/live/full suites were intentionally not run.