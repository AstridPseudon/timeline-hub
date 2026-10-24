## Report

Investigation complete; no product, test, source, pin, ledger, or design files changed.

Exact captured sources and receipts:

| Role | Commit | Tree | Checkout |
|---|---|---|---|
| App | `255f9f1218765f9a407354cf230aab9a452c8073` | `3f6d3df601452eb00ac0a664590c45f28a0f3734` | `app-pin-255f9f12` |
| Agent | `d6e84eb0e404a902c7d48da00cba11863592a63a` | `e54c73834ff8f259db4a12f868b005d9f11cc2f9` | `agt-pin-d6e84eb0` |
| Runtime | `327da207ed30880fe2ae0cd0b116722bb2c6f7a6` | `0140a9ab2bf8582c4712dbf84498a6d5dcb132cf` | `rt-pin-327da207` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | `vw-pin-635f4de0` |

D73 path traced through:

- `request-checkout` queues the exact SHA.
- `make-checkout` resolves it, creates the detached checkout, writes worker metadata, and emits the genuine receipt.
- `request-test` resolves the target worker metadata and records the source tree.
- `test-run` creates the service snapshot with `git commit-tree $tree -p HEAD`.
- D73 submit/receipt validation records the four exact source pins.
- `selectPinnedSources` rejects the actual service root before build or gesture execution.

20321 identity:

```text
App pin:       255f... tree 3f6d...
Target worker: 4a12... parents 3c2d... 255f... tree 3f6d...
Test snapshot: aeac... parent 4a12... tree 3f6d...
```

The request failed correctly in 2 seconds with no build, readiness, service, browser, or case execution:

```text
selected aeac.../3f6d...
pinned   255f.../3f6d...
```

The minimum stable route is the genuine detached `app-pin-255f9f12` checkout as the test target. Its generated service snapshot should be admitted only when:

- the snapshot is detached and clean;
- its tree equals the pinned App tree;
- it has exactly one parent;
- that sole parent is the exact pinned App SHA.

Same-tree alone, arbitrary ancestry, grandparent matching, multiple parents, missing parents, and the `4a12` worker-finalization parent must fail closed. The existing `4a12` target is therefore invalid despite sharing the pinned tree and containing `255f` as an ancestor.

No tests were run, per the read-only brief. Verification consisted of read-only `git show`, `git status`, metadata, receipt, and existing 20321 result inspection. The required next step is an actual-source `--preflight` against the exact App checkout target, followed by only the single focused body if preflight passes.

Commit message and `DONE` marker are prepared.