## FAIL — P3 same-ID gate is not gateGO

- Preflight PASS: `app-pin-f6a21c28-p3-intermediate-1933-preflight-1024193926-15980`.
- Normal same-ID run FAIL, exit 1: `app-pin-f6a21c28-p3-intermediate-1933-1024193956-14240`.
- No retry or duplicate submission.
- Readiness: 1/1 PASS, 26.282665s.
- Original Gate 5: 0/1, 1 failure, 103.105087s suite / 75.224s testcase.

Pinned heads:

- App `f6a21c285267d6475816adbda74233907ac93911`, tree `1993e3326e515e0a2801810bf087dc60886388d7`
- Agent `3b2db4bdf9014de013338521dd038ebdecd25f02`, tree `c84907010418e1c0a9ca0d46900c106ba771736e`
- Runtime `42855b6401e6683b157164bc332441ffffdffb06`, tree `d7c2f07832f6d5eba3b6c95831d1a856930edb55`
- Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`

The actual run passed both recovery mounts’ strict five-observed/three-forwarded identity, ordering, origin, and prior-wait checks, then reached merged B and history-count assertions. It failed at `three-products.spec.ts:1820`: history’s authoritative B command contained additional `authorship`, `bindings`, `expect`, `reads`, `resolved`, and `selections` fields absent from the submitted command. No downstream history-closure, preview, Agent, undo, or canonical credit is claimed.

Source/hash checks:

- Actual protected spec hash: `736fd381…e491e05`.
- Approved before/after hashes: `8661fc91…6154315b → 736fd381…e491e05`.
- Exactly one reviewed readiness-poll insertion; D79 harness files match the author-tested commit exactly.
- Node 20 syntax check and `git diff --check`: PASS.
- Bare native-control command failed at setup because Node lacked a TypeScript loader; Node 20 with the existing `--import tsx` loader passed all 3 controls.
- Reused unchanged author evidence: D66 21/21, parser 9/9, setup 3/3, typecheck and scoped lint PASS.

No product, test, pin, generated, registry, or source edits were made. Commit message and `DONE` marker created.