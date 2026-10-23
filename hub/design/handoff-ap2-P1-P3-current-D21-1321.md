# AP2 P1/P3 D21 current tuple handoff

Status: **NOTREADY**; no body or live-service qualification.

Only the existing `ap2-P1-chain-h6` and `ap2-P3-gate5-h6-0348` rows in `scratchpad/orch/tests/suites.conf` were updated. Both now guard App `4282d776497f651bce3870d1d9e6a37a5eaa2030`/tree `2e0ef95cc03f4d620180d9473973587412d97b0c`, Agent `f6116e1b658514021cbbf08d5a6f16a240523f1a`/tree `26f260e0674161f9f786bf93b15a1477a5e63a86`, and Runtime `8592822fd11275540f596562f43c715676f2bc0f`/tree `ed9856f43a4e44a058bf2230badea2c4c7080050`.

The P1 row refreshes the exact source/tree/pin/interpreter and fresh bench names. The P3 row replaces held Runtime `9345…`, uses the same explicit child-bench interpreter contract, preserves the normal hosted-build/runtimePython/source-vs-synthetic guards, and adds a full original native `seedThreeProducts()` preflight before the unchanged Gate-5 body.

Required receipts and installed artifacts are absent, so both D21 preflights stop before global setup, harness boot, selector collection, and body. Exact list checks passed: P1=2 selectors; P3 original Gate-5 selector=1. Original body identities are unchanged:

- P1 blob `221d05890ba9f42d50520c9b655c21338aece782`, SHA-256 `f28334c1f52d145ae66792ef419ba8138a1ec013f82fd982c4633de7f3a64133`
- Gate-5 blob `37caf28577d42fbe98afd2320dffa3c72e6e74b1`, SHA-256 `0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14`

Row SHA-256 values including newline:

- P3 `ec6221cba13426ec7eac7c5b3b7bb3bd4d55aa107264980347f1c0ecc408631b`
- P1 `129c8cab17c880bdeb936249346b922757691b48c13a6902f27d191580664b52`
- outside both rows `8846047343c8ab529adcde5c22c2d8b658641cc2877b9d03f0fe8b963b88e34a`

See the worker report for exact commands, NOTREADY output, and limits.
