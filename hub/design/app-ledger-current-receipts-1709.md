## Report

Read-only ledger correction completed. No product, test, generated, pin, ledger, or design files changed.

### Verbatim replacement text

Replace standalone D70 block at `design/deletion-ledger.app.md:99–105` with:

```md
D69 — Current App home `c3d79ef88a3dba948fe6e12fbde667e96ada055b`, tree `6576ed365e153dcbff2199762fe210409e35d5c4`; D69 source `2eab0fb8f0df8972a3f02804b1ac25cc8df0f142` is merged at home, with frozen upstream `3881e9440688f774878e18806da2dc5c993a9b00` ancestral. Reverse audit: 1,403 cleared / 67 cited intentional / 4 restored / 0 remaining. Placement restoration: old RED = 5 added controls failed; new home PASS = 41/41. Exact restoration scope is `src/shared/lib/placement/placementService.ts`, `src/shared/lib/placement/__tests__/placementService.test.ts`, and `src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts`; source `61f0fb613a` before → `2eab0fb8f0` after. SHA-256 before → after: `placementService.ts` `74c12bb82895cae28902e71735662851989424c854954b0672973b2de624df0f` → `aa290545d19630ddbebfe2a0d16346d079bba17fa8c35fb3b8158e395e3c4d30`; `placementService.test.ts` `77dfb5e80a848e44e239aca27f2c82b35f4a2ea2ed97063080649258a4c672fa` → `4035cab35caf56fb27f7c31d782467d816e6e9f885af8d6bd71f25849f67ad23`; `placementService.workspaceV1.test.ts` `aeb366ef8d91c7ffbc8c8bad9f277e4cb78633e1011e9336652f33af047cb5f2` → `14d1492668ebc9e76b2a25956e4a597c67300be0b3cb084dac0923c560cce8ca`. Frozen placement declarations remain `fcf8e413ce400977be026208d424ea211f4e464cf68db8fd2d7eece5fce8dd0d` and `80bd6c080820a5855c56fdc48e9ed988627b0d7fbf8fda32afc18957d6a1183b`. C0 §§1, 4, 7 semantics remain: pre-authoring head races may re-read once; submitted Runtime 409 conflicts remain durable as one intent. No live Runtime/browser/service/original/full receipt is claimed.

D70 — Actual home is `c3d79ef88a3dba948fe6e12fbde667e96ada055b`, tree `6576ed365e153dcbff2199762fe210409e35d5c4`; D70 merge `aaddaf12d2401760b75f6fb54e9e624883434447` is an ancestor. The approved `cc64db` line is present: mounted V1 parent move emits `label: Edit timeline`, `intent: Move ${seed.appClipId} on V1`, and `tags: []`. Full-spec SHA-256 `95d9a3e728509ad95b591b94bece0fc4942d040a0b160afa654815c0b3dd296c` → `a6468188ff21c4fd8bd397ff242b0260ee92ab6f2f90ac94786973eaf3c1e99a`; setup helper `28f7f84e141022740bd4bc6cc465579a8285fae16aecbf09ec77ea9d405fb962` → `77c10439a9b1d8287853d325bec82088e65e7401542a5380f8f361d4a9feb6f4`. Gate-5 body is unchanged at `d47d55265b3905a1882ffb370df033cf92b35c3492d4bec366d8da0272b9fb20`; reset block unchanged at `980b4cbe2c1d7a05840c8419fd55991ff73783784c89df6c717e2721a212fe62`; canonical tail unchanged at `5ede6f374857a66a327da3cea0e85de0457a04267003f3f66e3d40ee4f380912`. C0 §§1, 4, 7 and D13 source path are proven by `timelineLocalSaveHandoff.ts:572–577`, `localSaveSession.ts:168–199`, and `three-products.spec.ts:941–1055`. This is source qualification, not a live P3/browser/service/original/full GO.

P2-receipt-publication — Request idempotency and receipt publication identities remain distinct; authoritative `receipt.receipt_id` governs history/head/inverse/undo joins; strict v2 and zero-legacy assertions remain retained. C0 §§4, 5 and `commit-v2.md:703–711,1565–1577`. Author `52f1ee5111be78644b4b7d625217bb5dc3b0a54d`, reviewed tree `89ae790b40f928754a53b9120d3c64319d3010cf`; actual merge `0971c645ba113fab54d1da568550542b94f75e6c`, tree `60cdf06f0688066307dd5020567d15a8563baf7e`; current qualified home `c3d79ef88a3dba948fe6e12fbde667e96ada055b`, tree `6576ed365e153dcbff2199762fe210409e35d5c4`. Author hashes: P2 spec `2e8fc72bcf29870299a13aab50258a0528f727909125099b53a8aa13bc530a8d` → `67662468d0b4e2951b629154fb30f15764de2b797afe7788a97793872c9cd0e0`; oracle `a0bfad5dfa9c2ae14c36508543ccce00c53d459a5c4c3569198c2411407dfc5f` → `225a4c4358f9c115b04b0aea4e969a9b56fe8a0418450f20bb89eff1cdf47e90`. Current-home continuation hashes: `67662468…` → `07fe3d84831e2e5977405811ceaa7a592614871e15ec108d812eb024ebed2f3c`; `225a4c4358…` → `98934eceeb9ac2ae8d6170913abf57ff4503b6f426cfd31739006bbc94d1d272`. Status: PASS for source/merge/home qualification; no live original P2 journey or GO credit.
```

The current ledger’s P2 row at line 90 is therefore corrected from “Pending merge proof” to the PASS status above. The current ledger contains no explicit D69 row; insert the D69 line beside D70 rather than claiming an existing physical row was replaced.

### Verification

Read-only commands run:

- `git show`, `git diff`, `git ls-tree`, and `sha256sum` against the exact source refs.
- Verified D70 merge is ancestor of D69 home and D69 home is ancestor of integration `281c9f1cf9`.
- Verified P2 merge `0971c645ba...` is ancestor of current home.
- Confirmed worktree remains clean.

No tests were run, per the task’s read-only/no-browser/service/original/full constraint.

Commit message written: `U3-P3-ledger`. `DONE` marker created.