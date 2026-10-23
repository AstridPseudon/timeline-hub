# G2/G5 retained historical basis — 1917

Early finding (source not patched): corrected1907 Runtime is actually
`2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` (tree
`f79a2355cfb39d9ada7721978bd20d5702105778`); configured `d9e2…` is stale.
Both normal moves accepted. `find_version` currently discards each history
row's publication ID and calls `Checkout.open(revision_id=...)`. In contrast,
`store.fetch_bundle` hydrates head opens using the exact revision/publication
pair. The source therefore loses original publication provenance on the
historical path. Checking the captured original canonical closure against both
construction paths before making a product patch. No test body changed, no
original node rerun, no integration activation; P1 NO-GO stays intact.
