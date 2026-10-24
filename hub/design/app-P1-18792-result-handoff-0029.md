## Result

- Retained suite: `app-P1-reviewed-leaves-caller-sol-0013-ap2-P1-chain-h6-1024002459-18792`
- Status: `pass`, exit `0`, retained duration `141s`
- Playwright: `2 passed (56.3s)`, `0` failures, skipped count `UNKNOWN` (not reported)
- No test rerun or product/test/artifact changes made.

| Selector | Duration | Result |
|---|---:|---|
| `tests/e2e/local/three-products.p1-chain.spec.ts:1393:1` — accepted split, merged trim, lost ACK/restart/retry | 24.5s | PASS |
| `tests/e2e/local/three-products.p1-chain.spec.ts:1561:1` — stale trim refusal and rollback | 20.4s | PASS |

## Source and custody

- App source: commit `f8b15af0a66ed14e7711a4bb7f1ed5b62b4988b5`
- App tree: `dde63bed393f716033baaa3512cd5be379a095c1`
- App worktree: clean; current checkout matches retained snapshot tree.
- Agent pin: commit `78738040d72ce74c42ddf7731221aecb06f9246d`, tree `e77ea239789dd8ae9103c68fef79b49329cf2c6e`
- Runtime pin: commit `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, tree `f79a2355cfb39d9ada7721978bd20d5702105778`
- Composition pin: `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`
- Bench lease: `complete`, SHA256 `37a40f08d8548dba289b9b0bb35bcf63b359f6d37ee86044ebc6b6da080b9ec1`

Key source guards:

- P1 spec blob `5a2029d5f61a5cb665e1fb59c9fe13c9fff0bfde`
- P1 spec SHA256 `50960dd2efadc8350b8647a1f7e88a6cad2b44907bf36a7108832ee0ea9ebf17`
- First case SHA256 `eecdb2b41f66ecfe16a3d564f701c3138e39dd214b473c98635c6f7da51cbd72`
- Second case SHA256 `4d614d4c8f01e5a53abfa34ff3dd4b59f7dd63908c5d62028158834fcf3eb075`
- Gate-5 blob `37caf28577d42fbe98afd2320dffa3c72e6e74b1`

## Verified behavior

The unchanged source and completed run cover:

- v2 request fields, step patches, reads, merge mode, `dry_run: false`, source, and nonempty `Idempotency-Key`.
- Accepted split and merged trim replies, canonical document, digest, id map, steps, dependencies, and receipt identity.
- Lost acknowledgement, persisted request/key, reload ownership continuity, runtime restart, exact retry, idempotent replay, drained outbox.
- Agent move accepted; stale App trim refused with `409/value_conflict`; rollback to Agent canonical document; history tail reaches expected lengths.
- Legacy write traffic is empty in both cases.

Failure-only diagnostics are absent/UNKNOWN by scope; no successful diagnostic artifact is claimed. Fields such as `rationale`, `group_id`, `historical_rebased`, `undo_steps`, `preview`, and invalid-response detail fields are not asserted by this two-case evidence and remain unverified.

No final JSON artifact was published because the retained safe files do not contain a complete security-qualified request/reply artifact. A4 GO is not declared.

Created:

- Required commit message at the assigned `commit-msg` path.
- Empty `DONE` marker.
