## Verdict: FAIL / HOLD

Review is read-only; no production/test code changed.

- Commit: `778ea320c53734c9df9733174899dd6aad5cefdf`
- Tree: `0f0779413bf88b2b1828ddc3fb6691748d15da15`
- Parent: `73aa558266e04cae80ea23c50a4bd4722abcda6b`
- Diff: exactly two permitted files; working tree clean.
- Protected element and placement region hashes are byte-identical:
  - Element: `38653860f747be6851ce2825ec67a94f2051467cf8fcbc66f6415c746cbd6324`
  - Placement: `d409f4ad318bdb84d12b1cba9e214ee042b02e0b0387983d5c47c294663662af`

The receipt correction correctly uses `receipt.receipt_id` for publication/history/head/undo joins and `receipt.idempotency_key` for the request key. This matches C0 §4 ([lines 703–711](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/commit-v2.md:703)) and undo requirements ([lines 1565–1577](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/commit-v2.md:1565)). Runtime `becfe6db88b2cc034dba3fafa6c050117cdf2b06` independently records `txn-` receipts and looks up retries by idempotency key ([store.py:3415](/home/user/work/runtime/runtime_protocol/store.py:3415), [timeline_commit_store.py:1421](/home/user/work/runtime/runtime_protocol/timeline_commit_store.py:1421), [timeline_commit_store.py:389](/home/user/work/runtime/runtime_protocol/timeline_commit_store.py:389)).

Blocking finding: the three new controls use `request-1` / `publication-1`, while the helper only requires arbitrary strings via `expect.any(String)`. They do not positively exercise the required UUID-shaped idempotency key and `txn-`/UUID receipt. Wrong receipt/key/head/history/undo negatives are present and pass, but the required positive identity-shape proof is missing.

Commands:

- `/opt/node20/bin/node tests/e2e/local/support/p2-elements-assets-receipt.test.mjs` — **3/3 PASS**
- Qualified Vitest semantic neighbor with runner preload, `--configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism` — **25/25 PASS**
- Three serialized locked TypeScript checks (`tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`) — **PASS**
- Scoped ESLint — **PASS**
- `git diff --check` — **PASS**
- Reverse patch validation — **PASS**
- Full/browser/service/original journey — **NOT RUN**, prohibited by task.

Hashes:

- Spec before: `5f82ec9064abf15e1beada27e3c7905556cbcf66a63bc0a843f685729cb9ae71`
- Spec after: `1f015b178460a5ca5b474bb26ada0f1ec04033b689cb33f91d7f483b81c73177`
- New control file: `5fcd397e16128332caff02552005598436ccf91030e150356424c7ba22b7ff24`

| id | what(paths) | contradicts | replacedby | owner | ms | status | evidence |
|---|---|---|---|---|---|---|---|
| P2-D58-register-receipt | `three-products.p2-elements-assets.spec.ts`; `support/p2-elements-assets-receipt.test.mjs` | `post.key` used as publication identity | `receipt.receipt_id` joins; `receipt.idempotency_key` request identity | App/P2 | branch-only `778ea320` | REVIEW FAIL | Source correction and all scoped checks pass; positive UUID/`txn-` receipt control missing |

Commit message written and `DONE` created.