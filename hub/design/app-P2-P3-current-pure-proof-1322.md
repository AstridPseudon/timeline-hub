# PASS — readonly current App proof

No product or test files changed. App worktree is clean.

## Exact identities

- App HEAD: `971a29e198c3e384795731f79e39c096abd58845`
- App tree: `349691b03229d6e1f11a164997e29f49dae9f381`
- App parents: `6ab5938d34d75fe9f90f4c21f2518dfd1b6e847d c11d1b31ad39dc1603b147e538b7f618820fa4aa`
- Actual Agent source: `47b744dfe908dba1b9b09251d7fa2da3eb0530a6`, tree `68a7300422373c66b6d314a8b6ba917d0fbddd65`
- Named Agent fact `cba425b61958f380f25b7bdea83d23c92f627761` is an ancestor of actual Agent HEAD; actual checkout has additional null-closure changes.
- Runtime: `becfe6db88b2cc034dba3fafa6c050117cdf2b06`, tree `7edc08e3fe94edcbc8ef695c479f4de301789b89`
- Agent interpreter: `/home/user/work/venv-agent/bin/python`
- Source env: `/home/user/work/agent`, `/home/user/work/runtime`

## Evidence

- Deduplicated Vitest union: **27 files, 704 tests passed**
- Node20 oracle union: **9 files, 9 subtests passed**
- Required diagnostic command: **1 passed**
- Semantic Vitest oracle: **7 passed**
- Current actual Agent/Runtime popup/provider/media witness: **3 files, 67 passed**
- Clip pointer/ClipAction/media controls: **3 files, 79 passed**
- Locked root/app/node TypeScript checks: **all passed**
- Scoped ESLint: **passed with zero warnings**
- `git diff --check`: passed
- Playwright list-only discovery: **8 P2 tests**
- Original Gate5 list-only discovery: **1 test**
- No browser, HTTP, backend, native, realm, live service, or full-suite execution performed.

Exact mandated Node command passed:

```text
/opt/node20/bin/node --import tsx --test --test-concurrency=1 tests/e2e/local/support/p2-element-diagnostic.test.ts
```

The diagnostic source currently contains 26 named controls plus 3 generated terminal-state controls = 29 source controls; the actual evaluated serialized Apply sampler is anchored at line 211. This differs from the brief’s stated count of 28 and is reported, not altered.

## Current behavior ledger

| Row | Current proof |
|---|---|
| Parent | Actual helper validates exact request/reply shape, distinct request/idempotency and receipt identities, authoritative history/head/inverse/undo publication joins; mounted body retained at `three-products.p2-tour.spec.ts:709`. |
| Popup | Actual ADD/SWAP helpers, accepted/merged mounted provider witness, shared occurrence fork, authenticated old/new media; 67 current-source tests plus popup oracle. |
| Register | Actual accepted receipt identity, authoritative history/head and guarded undo joins; register control at `three-products.p2-elements-assets.spec.ts:489`; receipt oracle passed. |
| Placement | Actual placement receipt identity and guarded publication binding; placement control at `three-products.p2-elements-assets.spec.ts:556`; placement oracle passed. |
| Element | Actual catalog/parameter apply path, exact patch/reload/undo behavior, serialized Apply diagnostic; element control at `:398`; 97 element/catalog/parameter tests passed. |
| D53 unchanged | Gate5 fault-order 3 controls + reset-precondition 20 controls = 23; original Gate5 body retained and list-only discovery preserved 1 case. |

## Region hashes

- Parent region `709–740`: `be3db6fe21330addecb797e1defd28361cc40d92130c20e129da627a05cdba36`
- Transition single `741–760`: `522c98e2921916c88ffd2de1751eabf4c374d58c4a453fb433b7166b0de2138c`
- Transition bulk `761–781`: `df955842968d879d786fff7230af2ab56188df2d2fb59f0596048b70218010f1`
- Element `398–488`: `b808664d88799d223b4dfc8a62357bc3e237719005fde47e11f3413e61e4c8c3`
- Register `489–555`: `74b181b199e4c6cfe8dea24590a0e0075e0bc28aa903e749c13824093404f383`
- Placement `556–618`: `2fa3cca29d599fb538bfd8308ac8aae235fd639f467e626d7d96af865335b230`
- Popup ADD `850–857`: `8210dccc8e5d63bab811291de80a91970f7aec2d0b6194e511c20d018474abc1`
- Popup SWAP `858–864`: `e66926998e182b65d877182eda1ab48357c4823abc4f98bd1ada31b92f08c6b0`
- Original Gate5 body `1634–1831`: `d47d55265b3905a1882ffb370df033cf92b35c3492d4bec366d8da0272b9fb20`
- Native/bootstrap body `2235–2417`: `49ccd4a808b60cd3f8818827683ef695be1d792f025519408ef9bc079de893de`

Current source blobs and SHA256s were verified against all six reviewed donor commits; all donor commits are ancestors of App HEAD. The only cumulative changed spec blob is `three-products.p2-elements-assets.spec.ts`, whose current blob is `40119421b81a33b51438e21fd82813689f09b531`.

Control files remain unchanged/current:

- `three-products.spec.ts`: SHA256 `95d9a3e728509ad95b591b94bece0fc4942d040a0b160afa654815c0b3dd296c`
- `p2-element-diagnostic.ts`: `d91eea281af85c8b61e74ba810441059e038ebebce7a8c9eeb366c3cd9fc6c59`
- `p2-element-diagnostic.test.ts`: `797882ac07e61250a54e5d3d315dde653b27581b14cfd7fb76e0a72478d4b607`
- `gate5-fault-order.test.mjs`: `e7235bc7074ddb4c75e4dcd958c0c3cf71f640604d968fd750c4162bbd2ae06b`
- `gate5-reset-precondition.test.mjs`: `430d75012714c7c183f467bba533f1b2122fa834c9711395de935d8ebef02fee`

Commit message and empty `DONE` marker were written. Recommended next step: reconcile the orchestrator’s expected Agent identity with the actual descendant checkout before any live Gate/central-service execution.