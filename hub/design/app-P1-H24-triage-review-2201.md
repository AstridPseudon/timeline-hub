## Result: PASS

The submitted report is independently supported. Its causal verdict remains:

**INSUFFICIENTEVIDENCE** — the trim was rejected locally during capture with authentic `source-parent-mismatch`, but the compared operands are unavailable. No product defect or valid refusal can be established.

Evidence:

- App source: `e6d72d3d07d2df485e4f3e86c56d1eb2dd5cd91a`, tree `6513960eb0b2704d02c3b3298ba594b546af7565`.
- Agent pin: `78738040d72ce74c42ddf7731221aecb06f9246d`, tree `e77ea239789dd8ae9103c68fef79b49329cf2c6e`.
- Runtime pin: `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, tree `f79a2355cfb39d9ada7721978bd20d5702105778`.
- Actual run: 1 passed / 1 failed. Case 1 passed in 29.7s. Case 2 timed out at 300001ms; assertion expected two POSTs and observed one.
- Case 2 reached sequence 23: `capture-rejected`, stage `capture`, error code `source-parent-mismatch`, class `TimelineVersionConflictError`.
- No second POST, Agent move, Runtime 409, refusal reply, or rollback was reached.
- Source confirms the rejection condition at `timelineLocalSaveHandoff.ts:78–81`; capture invokes it at line 218. The rejection is created as `TimelineVersionConflictError` at lines 57–59.
- Safe diagnostics show the selected clip changing `sourceIn` 0 → 3, trim patch `{from: 3}`, and absent `to/at/hold/speed` patch fields. The compared config/registry operands are not present.
- Owner/session correlation is consistent: owner alias 1, generation 0, session present, closed false; durable outbox owner generation 1 is separately identified.

Safe artifact audit:

- Path: `.../playwright-output/three-products.p1-chain-P1-c924b-p-rolls-back-with-a-message/p1-diagnostic.json`
- Size: 144,118 bytes
- SHA-256: `faa0df373a0ae84dfd3ba56aab81988a65435c31b339ec91864be1bb299e4b0f`
- Attachment is byte-identical.
- `jq` parsing, exact top-level schema, nested source allowlist, record bounds, and sensitive-key/value scan: PASS.
- 23 records, accepted 23, rejected 0, overflow 0, listener errors 0.
- Request projection contains only body length (3,669 bytes), not raw request data or a reconstructed body hash.
- Unknown/loss markers remain honest: callback/capture resolution unknown and capped console retained.

Protected source checks:

- First P1 case hash: `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f`
- Second P1 case hash: `2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7`
- Gate-5 blob: `37caf28577d42fbe98afd2320dffa3c72e6e74b1`
- Worktree remained clean; no product/test/source changes were made.

Tests: **N/A** — read-only evidence audit as required.

Remaining blocker: obtain a future safe, field-specific comparison projection from the authentic `checkSource` seam. Do not clear the guard, infer a basis mismatch, or propose a product fix from this artifact alone.

Commit message and `DONE` marker were created.