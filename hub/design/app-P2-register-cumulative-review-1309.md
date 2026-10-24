## PASS — branch-only cumulative review

Reviewed `dbbaa7b54a9ed2e166046eb074377a515af8bc22` (`tl/app-P2-register-cumulative-review-1309`).

- Tree: `50a631133ded3219e0c1e939132dc6beb3ea2e9b`
- Parent: `778ea320c53734c9df9733174899dd6aad5cefdf`
- Base: `73aa558266e04cae80ea23c50a4bd4722abcda6b`
- Scope: exactly the helper fixture plus registerAsset case; no production code changed.
- Protected element hash: `38653860f747be6851ce2825ec67a94f2051467cf8fcbc66f6415c746cbd6324`
- Protected placement hash: `d409f4ad318bdb84d12b1cba9e214ee042b02e0b0387983d5c47c294663662af`
- Register case hash: `4132b2776b1894e90cc8a739724a08d293795459553385933bd7d3fe97d4c7ce`
- Control hash: `485391d69112cdfef7b33edf36a7361cd4c575a8354548f7183c651b3f496371`

The fixture now positively proves UUID-shaped request keys, `txn-` plus 32-hex receipt IDs, distinct identities, and wrong receipt/key/head/history/inverse/undo rejection. This matches C0 §4 lines 703–711 and undo lines 1565–1577. Runtime producer `becfe6db88b2cc034dba3fafa6c050117cdf2b06` independently uses `txn_id` as `receipt_id` and idempotency key for retry lookup.

Checks:

- Node receipt controls: **3/3 PASS**
- Semantic Vitest: **25/25 PASS**
- Locked TypeScript checks: root, App, Node — **PASS**
- Scoped ESLint — **PASS**
- `git diff --check` — **PASS**
- Reverse patch validation — **PASS**
- Playwright static list: **8 tests across 3 files, PASS** with `--reporter=line`
- Full/browser/service/original journey: **not run**, prohibited by brief.

### Worker behavior ledger

| ID | Behavior | Full-file/helper hashes | Branch | Branch status | Integrated status | Evidence |
|---|---|---|---|---|---|---|
| P2-D58-register-receipt | Distinct request idempotency and publication receipt identities preserved through acceptance, history, head, inverse and undo; strict UUID/`txn-` fixture controls retained | Spec `5f82ec…9ae71 → 1f015b…73177`; control `5fcd39…7ff24 → 485391…96371`; protected element/placement unchanged | `tl/app-P2-register-cumulative-review-1309` | **PASS; branch-only**, `dbbaa7b5`, tree `50a63113` | Pending merge; no live credit | C0 §4, Runtime `becfe6d`, targeted checks above |

Commit message and `DONE` marker were written.