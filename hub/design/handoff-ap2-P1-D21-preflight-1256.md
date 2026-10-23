# AP2 P1 D21 preflight handoff

Status: NOTREADY pending manager-owned fresh dispatcher receipts.

Prepared the existing `ap2-P1-chain-h6` row with report-all preflight and preserved the original two-test P1 body byte-for-byte (`221d05890ba9f42d50520c9b655c21338aece782`, SHA-256 `f28334c1f52d145ae66792ef419ba8138a1ec013f82fd982c4633de7f3a64133`). Gate-5 remains byte-locked at blob `37caf28577d42fbe98afd2320dffa3c72e6e74b1`.

The row requires App `419d5e3b4bf03ef77f8cbba5975691f17f19757c`/tree `4027d3845298a9f31cc86af0c06260afb27d55be`, Agent `5b1b4db8253f46e0e085908e79f309d492877386`, Runtime `3b926efab2eed122d374540baee297d4cdcec62a`, exact proof/remotion lock hashes, and successful future `queue/done` child-venv/Remotion receipts. It rejects the known refused `5b1-1253` requests and reports `NOTREADY` when future receipts are absent; no artifact path was invented.

The only source change is the allowed `ASTRID_RUNTIME_PYTHON` support in `tests/e2e/local/support/harness.ts`, with executable-file validation and unchanged `.venv` fallback.

Evidence: TypeScript, targeted ESLint, diff check, suite-row `bash -n`, and explicit valid/invalid interpreter probes pass. The bounded direct preflight correctly reports all current setup blockers and does not enter the body/browser/build/live service. Manager should queue fresh receipts, reconcile exact source trees, then request the existing `ap2-P1-chain-h6` row once; the row itself performs the real runner `--list` two-test check and then the original P1 command.

