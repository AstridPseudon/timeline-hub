# D141cc independent review findings

## FAIL — return for correction

The admitted same-author control script passes, but it does not qualify the completed continuation. The source-only review found three blocking issues:

1. `p2-popup-add@popup-retry-1` is not generated from the unchanged production builder. Its candidate command and row bytes are synthetic. Calling the unchanged pure `serviceRecipe` with the admitted tuple gives command SHA `27fcd174df3f214502bbca1e67b0eb366c361c11e1f5ae5c0c48d7a987582501`; the candidate records `809c1a5ed1be729808d335c8c18dbfdee3ccd73d9454e4739b91e256572def37`. The actual retry registry row hashes to `c89f8ac7430f4e5342fbffb23cd5ce4aa54f2151e38b3e46af7035aea13fc6c3`, while the candidate records `17e8a4acc32f21825eb0642d7e7a832889ec10b9591c0a05795e2dfa8cf6a018`. The six original rows do match.

2. The model has a producer/artifact race. If another normal request appears after `create_preflight` and before `_create_normal`, the controller makes a second normal request. The self-test only tests a later recovery after persistence failure; it does not test this interleaving.

3. Same-target/suite requests with matching source but mismatched command or row bytes are silently ignored by `exact_candidates`; the controller then creates a new request. This must fail closed, and the digest-to-byte relationship is not validated.

The unchanged builder, source pins, old cancelled receipts, placement bounded PASS, and present-time disk limitation remain unchanged. No candidate source was repaired and no service operation was run.

Recommended next step: return the packet to the owner to regenerate the retry row and command directly from the unchanged builder, then add fail-closed mismatched-tuple and preflight/normal interleaving controls before any future dispatch. This review does not authorize that dispatch.
