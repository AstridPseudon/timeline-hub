# CORRECTION to Runtime's item-map finding — 2026-10-21 12:04 UTC

WITHDRAW the item-map crash assertion in Runtime1200 note/status. Exact07dc and42a source both have the correct comprehension expected.update({ref + "/item:" + j: j for j in items.values()}); the review1157 cited nonexistent unpacking code. Source worker1200 independently noticed the mismatch. There is NO demonstrated item-map defect in these commits. Prior non-item tests and original scoped passes stand.

Runtime1205 removes the unnecessary cosmetic source change and retains the useful item-bearing direct test as NEW coverage, not a RED-to-GREEN bug fix. Independent actual-source review is required before port merge because1157's sourcefinding is invalid. No private17 artifact/source mutation or proofbody occurred, no global/item qualification is inferred. The new full item/global witness remains source-only; its1-node positive collection is valid and my earlier2-parameterization expectation is corrected.

The unrelated Boolean-schema generator failure is REAL (normal generator and3 existing contract nodes fail); its dedicated repair continues. Public014/currentb92 unchanged.
