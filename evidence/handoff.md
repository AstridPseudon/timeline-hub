# D141 cut census review handoff

Review result: **FAIL for finite preparation custody; census and selector evidence PASS.**

- The retained cut is `runtime-full-d141-cut-1026005231-18778`, with 7,392 unique cases and 53 exact bad IDs. Keep its raw XML, request, snapshot, summary, log, exit, D66 witnesses, and `KEEP` marker unchanged.
- All 15 exact-pristine-eligible mappings are AST-identical to the frozen pristine functions. All 38 `NEW_OURS` mappings remain source-only provenance; the bounded rename check found no candidate. Missing source is not behavioral evidence.
- The pristine request `rt-pin-fa9cd546-full-d141-pristine-1026005231-8912` is still queued after a low-disk safety denial. It has no outcome; do not classify any case as REG, preexisting, product-fault, or zero-REG.
- Custody action required before comparator use: reconcile the source-manifest hash for the retained pristine `why` file and replace the literal `HEAD^{{tree}}` placeholders with immutable tree values. No alternate run or workaround is authorized by this review.
