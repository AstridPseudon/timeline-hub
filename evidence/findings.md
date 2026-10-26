# D141 cut census review

## Decision

**FAIL, scoped to finite preparation custody.** The census, exact ID join, parameter preservation, AST selector mapping, and privacy checks pass. The package is not clean enough for an unqualified preparation PASS because one retained control hash differs from `source-manifest.json`, and the manifest records unresolved tree placeholders.

This is not a behavioral, REG, preexisting, product-fault, or zero-REG verdict. The pristine request `rt-pin-fa9cd546-full-d141-pristine-1026005231-8912` remains `queued`; it has no comparator body, XML, exit, or summary. All 53 bad cases therefore remain `UNCLASSIFIED_NO_SAME_ENV_COMPARATOR` / `NONE`.

## Independent checks

- Parsed the retained XML: 7,392 testcase elements and 7,392 unique exact IDs; 7,300 pass, 35 failure, 18 error, and 39 XML skipped. The service summary reconciles as 26 skipped plus 13 xfailed = 39 XML skipped.
- Joined the 53 published bad IDs to XML exactly: 53/53 present once, with class, name, status, and full bracketed parameter selector preserved. The 35/18 failure/error split matches.
- Rechecked all 53 selector mappings with Python AST. All 15 `exactmappedPRISTINE_ELIGIBLE` entries reproduce the recorded cut/pristine AST hashes. All 38 `NEW_OURS` entries received one bounded frozen-pristine test-function name/body-text check: 0 name matches and 0 body matches. Dynamic parameter uncertainty remains UNKNOWN.
- Verified Runtime cut 6a011d5, Agent cut 28e56ca, Runtime pristine fa9cd54, and Agent pristine 8b6ed21 commit/tree identities and clean worktrees. Present listed Git blobs match; the listed pristine paths for cut-only modules/tests are absent as expected by the `NEW_OURS` mapping.
- Rehashed every retained cut control artifact and the XML; they match the source manifest, and the cut `KEEP` marker is unchanged. The pristine `why` artifact does not: claimed `186892...da2905`, actual `9bbf75...d971`.
- The source manifest’s Composition tree is the literal `HEAD^{{tree}}`, while commit 635f4de’s actual tree is `5ab519...a148`; all four `worktree_tree` fields are also unresolved literals. These are custody metadata defects, not evidence of a product delta.
- Published JSON contains only safe identity/selector, exception class, file/line, hashes, and custody metadata; no failure messages, runtime payload bodies, user content, credentials, or URLs.

## Test policy

No product lint, typecheck, test, import, collection, provider, or full-suite rerun applies to this evidence-only review. No files were deleted or changed in the product/source repositories, and the retained `runtime-full-d141-cut-1026005231-18778` artifacts were not modified.

## Handoff

Keep all raw cut artifacts unchanged. Before any same-environment comparison, refresh or reconcile the mismatched `why` control hash and replace unresolved tree placeholders with immutable commit/tree values. Then run the single authorized pristine comparator through the central service; do not infer an outcome from the queued safety denial.
