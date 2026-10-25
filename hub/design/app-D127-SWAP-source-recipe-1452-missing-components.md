# D127 exact missing components

The following are absent from the retained safe custody and must not be inferred:

- Original3250's exact SWAP POST body, including its concrete project/timeline IDs, immutable `base_revision_id` and `base_publication_id`, request `Idempotency-Key`, generated `shot-fork-*` ID, and exact command/step bytes as received by Runtime.
- Original3250's exact pre-SWAP history page and canonical closure payload, including the concrete old/new `asset`, `generation_id`, `variant_id`, `object_id`, and `catalog_digest` values.
- The registered Agent provider's original3250 output: accepted/conflict phase data, exact native receiver/provider identity, record dependencies, reads/selections, effect bindings, and closure bindings.
- The exact Runtime history/receipt records and the lower private cause for the public `history_unavailable` response. D125/D127 retain only the public static tag and report the lower binding as `UNKNOWN`.
- Any historical replay authority. The source recipe supplies deterministic construction and current production call order only; it does not establish identity with the old realm or old request.

Safe substitutes are intentionally not proposed: Runtime must use its existing retained source pointers and current registered provider, with the request's actual CAS/media-selection values supplied at execution time.
