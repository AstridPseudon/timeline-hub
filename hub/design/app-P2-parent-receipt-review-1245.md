## PASS — D56 protected test review

Reviewed commit `52f1ee5111be78644b4b7d625217bb5dc3b0a54d` on `tl/app-P2-parent-receipt-oracle-1240`.

- Parent: `cca3deb361e8fbbc62ddf491d5fd09c7e542b99f`
- Tree: `89ae790b40f928754a53b9120d3c64319d3010cf`
- Only permitted files changed:
  - `tests/e2e/local/three-products.p2-tour.spec.ts`
  - `tests/e2e/local/support/p2-parent-oracle.test.mjs`
- Worktree remained clean; no source fixes or Git mutations made.

The review confirms `receipt.receipt_id` remains the authoritative publication ID while `receipt.idempotency_key` remains the request key. History, head, inverse, and `undo_of` joins use the receipt publication ID. Exact v2 request/reply fields, canonical/raw/opaque/closure/reads/steps/metadata/reload/Undo/zero-legacy assertions remain strict.

Source citations:

- Contract §4: [`commit-v2.md:703-711`](/home/user/timeline-hub/hub/design/commit-v2.md:703)
- Contract undo identity: [`commit-v2.md:1565-1577`](/home/user/timeline-hub/hub/design/commit-v2.md:1565)
- Runtime producer: [`store.py:3415-3467`](/home/user/work/runtime/runtime_protocol/store.py:3415), [`service.py:1840-1844`](/home/user/work/runtime/runtime_protocol/service.py:1840)
- P1 precedent: [`three-products.p1-chain.spec.ts:149-150`](/home/user/work/app/tests/e2e/local/three-products.p1-chain.spec.ts:149)
- P2 receipt assertions: [`three-products.p2-tour.spec.ts:299-302`](/home/user/work/wt/app-P2-parent-receipt-review-1245/tests/e2e/local/three-products.p2-tour.spec.ts:299)
- P2 history/head/undo joins: [`three-products.p2-tour.spec.ts:648-706`](/home/user/work/wt/app-P2-parent-receipt-review-1245/tests/e2e/local/three-products.p2-tour.spec.ts:648)
- Actual-helper positive and wrong-ID controls: [`p2-parent-oracle.test.mjs:182-228`](/home/user/work/wt/app-P2-parent-receipt-review-1245/tests/e2e/local/support/p2-parent-oracle.test.mjs:182)

### Hashes

Full-file SHA-256 before → after:

- `three-products.p2-tour.spec.ts`:  
  `2e8fc72bcf29870299a13aab50258a0528f727909125099b53a8aa13bc530a8d` → `67662468d0b4e2951b629154fb30f15764de2b797afe7788a97793872c9cd0e0`
- `p2-parent-oracle.test.mjs`:  
  `a0bfad5dfa9c2ae14c36508543ccce00c53d459a5c4c3569198c2411407dfc5f` → `225a4c4358f9c115b04b0aea4e969a9b56fe8a0418450f20bb89eff1cdf47e90`

Function-body SHA-256:

- `assertReplyShape`:  
  `eadab56ba880e8951e3e3446b9d46fad95cbc87ea3672507f67599514d6a1ca7` → `419085eb3d0012d76ae81a99c50152a4c6984d897816d9528593ca82a41b49b1`
- `assertAuthoritativeHistoryPublication`: absent → `29f7aabc5b1cde07f54daeba971fe2fdb5ecfa9e64e4e473bf304fa8e51c02dd`
- `assertAuthoritativeHead`: absent → `1b7cafeab971d905651fe592063faf8db12b86458d450f88cd82c6ce92cd824e`
- `assertInverseTargetsPublication`: absent → `4864b0003d06a338f4a2f0d0c8c08878fd7975a5f79bc1365196a99920ba15d9`
- `assertUndoHistoryPublication`: absent → `7aca36348053758423de83cd7f96c3e01ff43a808207503a890a9b4c808525ab`
- `replyFixture`: absent → `dba903512ca6476591e8a2cca9b81a60e64787e940a87bbeccb1895a3b6b8453`

### Verification

Passed:

```text
TSX_DISABLE_CACHE=1 /opt/node20/bin/node --import tsx --test --test-concurrency=1 \
  tests/e2e/local/support/p2-parent-oracle.test.mjs \
  tests/e2e/local/support/p2-transition-oracle.test.mjs \
  tests/e2e/local/support/p2-document-oracle.test.mjs
```

Result: 3 passed, 0 failed.

```text
/opt/node20/bin/node node_modules/eslint/bin/eslint.js \
  tests/e2e/local/three-products.p2-tour.spec.ts \
  --report-unused-disable-directives --max-warnings 0
```

Passed.

Locked TypeScript configs passed:

```text
flock -w 600 /home/user/work/.app-tsc.lock /bin/bash -c \
'/opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.json --noEmit --incremental false &&
 /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit --incremental false &&
 /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit --incremental false'
```

Also passed:

- `git diff --check`
- Reverse-removal check with `git apply --reverse --check`
- Playwright list-only: exactly 3 P2 tests listed
- Protected document/transition/original-owner blobs unchanged

No full suite, browser journey, backend, live GO, or actual journey execution was run.

The standalone reply helper accepts any current-producer-shaped `txn-*` receipt because no externally expected receipt ID exists at that point. The actual helper controls then reject conflated receipt/key and wrong history/head/inverse/undo bindings, so this is not a defect.

### Worker-authored behavior ledger

| ID | Behavior | Full-file hashes | Helper/body hashes | Branch | Branch status | Integrated status | Evidence |
|---|---|---|---|---|---|---|---|
| P2-receipt-publication | Request idempotency and receipt publication identities remain distinct; authoritative receipt ID governs history/head/inverse/undo joins; strict v2 and zero-legacy assertions retained | Spec `2e8fc7…530a8d → 676624…cd0e0`; oracle `a0bfad…dfc5f → 225a4c…47e90` | `assertReplyShape` `eadab5…a1ca7 → 419085…49b1`; new binding helpers and fixture hashes listed above | `tl/app-P2-parent-receipt-oracle-1240` | PASS; reviewed SHA `52f1ee…0a54d`, tree `89ae79…01cf`, parent `cca3de…2b99f` | Pending merge proof; branch-only review, no final GO | PLAN §3 P2/D56; contract §4; P2 spec/support citations above; handoff and author report |

Commit message written to the required path, and `DONE` marker created.