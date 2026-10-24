## P3/D75b current submission

Submitted once with the existing D66 plain-stack submit command from `/home/user/work/app`.

- preflight ID: `app-pin-3c29d553-d75b-p3-current-1855-preflight-1024185442-20128`
- normal ID: `app-pin-3c29d553-d75b-p3-current-1855-1024185512-26908`
- preflight status: `pass`, exit 0, 3s
- normal status: `fail`, exit 1, 471s
- service target: `app-pin-3c29d553`
- submit plan: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P3-D75b-submit-produce-1855/submission/p3-submit-plan.json`

Captured source pins and trees:

| repo | commit | tree | detached checkout |
|---|---|---|---|
| App | `3c29d553a7af0b0e0876760052855818ea834658` | `2f0aa476b5cd40e2b80b5f4dec37571b7152a55f` | `/home/user/work/wt/app-pin-3c29d553` |
| Agent | `831df37ffdfbb7cf802c95f91eac30681efdbb45` | `52213c5a56f332532759826f04be6659d8ddd34a` | `/home/user/work/wt/agt-pin-831df37f` |
| Runtime | `1bae0e8ccb8f912d50ad16e80d2e42f8e2ea603f` | `4feab0185b3750a55b8f0c21c92c6015aaf8e2f7` | `/home/user/work/wt/rt-pin-1bae0e8c` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | `/home/user/work/wt/vw-pin-635f4de0` |

The preflight manifest is retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-3c29d553-d75b-p3-current-1855-preflight-1024185442-20128/d66/manifest.json`

It records the service snapshot as App tree `2f0aa476b5cd40e2b80b5f4dec37571b7152a55f`, one parent `3c29d553a7af0b0e0876760052855818ea834658`, and all four detached source identities above. The normal result directory is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-3c29d553-d75b-p3-current-1855-1024185512-26908`

Observed source-only and service facts:

- Node `v20.19.4`, npm `10.8.2`
- Runtime server `AstridRuntime/0.1 Python/3.13.16`
- protocol `workspace.v1`
- provider `astrid-v1`, compiler `authoring-bundle-1`
- schema digest `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`
- service snapshot head `88ab2b2ab44ce7f8844cd5d746dd4d44df289c6f`, tree unchanged at `2f0aa476b5cd40e2b80b5f4dec37571b7152a55f`, sole parent App `3c29d553a7af0b0e0876760052855818ea834658`

Protected test hashes were unchanged before/after the run:

- `tests/e2e/local/three-products.spec.ts`: `8661fc919714d292c567844dc4f423855923077ca6a679a1398ec2a46154315b`
- `tests/e2e/local/three-products.mounted-readiness.spec.ts`: `2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593`

Verdict from the retained JUnit:

- readiness: PASS, 1/1, 0 failures, testcase 26.288s; `readiness.xml`
- original Gate5: FAIL, 0/1, 1 failure, testcase 201.824s; `p3.xml`
- no skipped or errored tests
- no downstream credit: the original journey failed at its first unmet recovery assertion

First failure/stage:

`tests/e2e/local/three-products.spec.ts:1773` in the Gate5 recovery-retry stage. After `wire.armRecoveryRetry()`, the unchanged 90,000ms poll ceiling expected `wire.observed.length === 4` but observed `3`; the retained error context and trace are under `d66/p3/three-products-M2-real-gat-710b3-rt-and-undo-preserve-intent/`.

Evidence:

- manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-3c29d553-d75b-p3-current-1855-1024185512-26908/d66/manifest.json`
- readiness JUnit: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-3c29d553-d75b-p3-current-1855-1024185512-26908/d66/readiness.xml`
- original JUnit: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-3c29d553-d75b-p3-current-1855-1024185512-26908/d66/p3.xml`
- normal log/summary: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-3c29d553-d75b-p3-current-1855-1024185512-26908/d66/` (`log.txt`, `p3/three-products-summary.json`)

The 1843 core/protected controls and 1848 same-blob home receipt were reused; no source, test, product, generated, pin, or suite-body change was made by this submission worker. No retry or second request was submitted after the normal ID existed.
