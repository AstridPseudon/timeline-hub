# P2 D105a placement original submission

## Submission

- Selector: `p2-automatic-child-placement`
- Unique suite: `p2-d105a-placement-0644`; preflight: `p2-d105a-placement-0644-preflight`
- Host: `app-pin-51239c79`
- Source preflight: PASS, `app-pin-51239c79-p2-d105a-placement-0644-preflight-1025064319-2816`
- Actual body: `app-pin-51239c79-p2-d105a-placement-0644-1025064349-31962`
- Actual body status: FAIL, exit 1, 144 seconds
- No retry or second body was submitted.

## Immutable tuple and receipts

| repo | commit | tree | detached checkout | receipt |
|---|---|---|---|---|
| App | `51239c79e26ff743623218b9c09fdce1629ec90c` | `8469ab6218ea7e45247043d658d271fbe7d77283` | `/home/user/work/wt/app-pin-51239c79` | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/queue/done/checkout-app-51239c79e26ff743623218b9c09fdce1629ec90c` |
| Agent | `8c88ea8f06b65f9b79fb7810af04720845c5cc6f` | `cd2a51721f07b447215f4084980d385de3842fd9` | `/home/user/work/wt/agt-pin-8c88ea8f` | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/queue/done/checkout-agent-8c88ea8f06b65f9b79fb7810af04720845c5cc6f` |
| Runtime | `1daca2a33f6d7b10053e07c539a54843e3984e19` | `a522511414947e48e317a5e5c2103483b121a750` | `/home/user/work/wt/rt-pin-1daca2a3` | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/queue/done/checkout-runtime-1daca2a33f6d7b10053e07c539a54843e3984e19` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | `/home/user/work/wt/vw-pin-635f4de0` | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/queue/done/checkout-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40` |

The byte-exact durable submit plan is [here](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-P2-D105a-placement-original-0644-submit-plan.json>), SHA-256 `eb81b941e4924e477669cba44bcb0c58ebfb49b2a4fa18c96055f54cbe9b8a4b`. The submission copy is under `workers/app-P2-D105a-placement-original-0644/submission/p2-placement/`.

## Source and helper hashes

- Placement/oracle spec: `tests/e2e/local/three-products.p2-elements-assets.spec.ts`, SHA-256 `9b8791e6e3b71155daab01440466987de406b23e2b6269dcc67872cc75c807c7`.
- Mounted readiness: `tests/e2e/local/three-products.mounted-readiness.spec.ts`, SHA-256 `2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593`.
- Receipt helper: `tests/e2e/local/support/p2-elements-assets-receipt.test.mjs`, SHA-256 `8247e9a60d4c46c8ada16dbbf330fd93d8f01d7c59421a11e4e5d7347b7c2f8f`.
- D66 launcher: `scripts/testing/d66-plain-stack.mjs`, blob `1f7c196a1f2beca17475bf9aa03442b29f3a69cc`.
- Harness: `tests/e2e/local/support/harness.ts`, blob `9fccbff7ca874d5c86fa71daf85587a036d5f0ba`.
- Runtime schema digest: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`.
- Node/npm: `v20.19.4` / `10.8.2`; Runtime server `AstridRuntime/0.1 Python/3.13.16`.

## Result

Readiness was `1 passed, 0 failed, 0 skipped` in `d66/readiness.xml`. The original XML was `1 test, 0 failures, 0 skipped, 1 error`; the original test did not reach the placement gesture or any placement POST. Its first unmet setup predicate was:

`P2 Runtime phase sink already exists` at `tests/e2e/local/support/harness.ts:122`, called by `prepareP2CommitPhaseCapture()` from `DirectHarness.start()` at `tests/e2e/local/support/harness.ts:631`, for the original `tests/e2e/local/three-products.p2-elements-assets.spec.ts:1199`.

Intended placement POST/status: NOT REACHED; HTTP/status UNKNOWN. The setup error occurred before the real embedded managed file drop and before `occurrence.add-media` could run. The actual service manifest and source-preflight manifest are retained under the submission directory; the original XML remains at the central result path recorded in the handoff JSON.

Existing D102 safe context is bounded separately: prior ADD observed intended Undo POST with HTTP 503, public `code=not_ready`, `reason=runtime_unavailable`; internal reason/class/location and ring correlation were not retained and remain UNKNOWN. The separate A/B source diagnosis identified the old `request_id`/strict `CommitContext` schema regression, fixed in Runtime `1daca2a33`; it is not attributed to this placement setup failure. No inference is made from absent retention.

The D105a protected review and merge-scope review passed after the pin comparison correction. The product remains upstream; no ZIP note applies. No gate GO is claimed; an independent App reviewer must consume this terminal setup failure.
