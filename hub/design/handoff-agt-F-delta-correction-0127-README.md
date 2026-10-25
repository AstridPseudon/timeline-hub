# F-D89 private incremental successor packet

This private packet corrects the earlier F-D89/0118 eligibility without modifying the historical evidence. It is derived from authentic F-D86/0055 and F-D89/0118 artifacts plus exact normal-home/source receipts.

## Submission sets

- Existing MAIN submitter0107 first subset: **289 selectors**, the exact 0055 set of 298 minus the exact numeric9 exclusion in `first-subset-exclusions.tsv`. Its flat input is `first-subset-selector-argv.txt`. It must run independently of this successor packet.
- New successor delta: **2 graph-redo2 selectors only**, in `selector-argv.txt` / `successor-selector-argv.txt` and `successor-membership.tsv`. They are `SOURCE_EXACT_BEHAVIOR_PENDING`; no behavioral PASS is claimed.
- Later delta held: **11 scalar11 selectors**, in `later-delta.tsv`, because Runtime0110 returned `FAIL_SOURCE`: the scalar seed lacks genuine media admission (`verified_media`/`media.admit`) and Runtime rejects the empty-bootstrap manifest before acceptance.

The 0118 historical 13-row packet remains available byte-for-byte as `historical-0118-membership-delta.tsv` and `historical-0118-source-manifest.json`; `historical-0118-status.tsv` explicitly marks its prior eligibility as superseded by this correction. The original worker evidence at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-incremental-delta-0118/evidence` was not modified.

## Source identity

The captured 0118 source tuple is Agent `219b9ca8b196bcf4ee6fda6e08c2e50ae251ae4b`, tree `9d26efc30836abb7ae3a19882e6e917405db2f89`. The final captured normal Agent home snapshot is `c6c3158d333dca1158683757cfe92101262a2b74`, tree `d0b26805fade4371c5936de08e60803141eb708c`, with current merge subject `Merge tl/agt-F-cli-trim-return-0122`. All six relevant source contents match the captured 219b commit; this is recorded in `source-manifest.json`.

A historical manifest discrepancy is preserved explicitly: its literal for `test_commit_runtime_scalar.py` is 65 characters and does not equal the verified current/captured-commit SHA-256. The malformed historical literal was not changed; see `source_hash_discrepancies` and `validation.json`.

Scalar's Agent source merge receipt is retained but does not qualify the family after the independent Runtime FAIL_SOURCE. Graph remains source-exact only. Runtime release is `a3cd1a3214fa1632879c21d82d1abb9ea720b1de`.

## Preservation and validation

`dispositions.tsv` preserves all 550 original rows and original columns, then appends successor overlays for graph2, held scalar11, excluded numeric9, retained first-subset rows, and the remaining historical/retired rows. `original550-rollup.tsv` is the exact 0118 rollup copy. Counts and exact set differences are in `set-accounting.json`; no sum is used as proof.

Only JSON/TSV/set/hash/source identity checks and `bash -n` of the proposed existing-runner recipe are in scope. No pytest, collection, helper/function/fixture execution, service, build, browser, render, install, checkout, profile creation, or D73 receipt was performed.
