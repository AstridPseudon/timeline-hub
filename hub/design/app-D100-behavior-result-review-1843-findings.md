# D100 independent result finding

Result: PASS for the meaningful registered-provider first-physical-item behavior, with a precise boundary. Whole-candidate GREEN is not established: the retained exact 27-node run is 24 passed / 3 failed.

## Verified custody

- Candidate `9486cbb06e2ab53402086772e6c2bc18bc4849fc`, tree `0919e511bd28b3d3af76bb18155efda12c3e94f6`, is clean.
- The only candidate paths relative to parent are `astrid/sdk/timeline/_command_state.py` and the additive D100 test.
- Candidate product SHA-256 is `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3`; protected test SHA-256 is `be2c9d054d94fe741fa2c53552ec59de1510bf82dbf704018e0bc49f3218ec58`.
- Runtime is clean at `ab1e4f6141987706132916e2da16477f5a019464`, tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`; the projection receiving fixture is unchanged.

## Retained behavior

Parent: 27 nodes, 23 passed, 4 failed, exit 1. Candidate: 27 nodes, 24 passed, 3 failed, exit 1. The real registered-provider node `test_registered_runtime_first_source_item_birth_and_no_write_refusal` is the meaningful first-birth comparison: parent reaches the old physical-item correspondence refusal; candidate accepts the first physical item and retains the refusal/no-write check.

The two custody failures are not a candidate product regression. Both reach the post-execution assertion at test line 49. The only extra value is `_doc_patch_images`, added by `_doc_patch_materialize.remember()` for compiler projection. The implementation comments and C0 boundary identify this as a private projection cache, not historical/source authority; canonical document conversion does not expose it. The failure is therefore an over-broad internal-map equality expectation, not a source-custody failure. The assertion remains protected and was not weakened.

The shared-owner failure is also not caused by the candidate delta. It is a direct `execute()` test, not the Runtime/provider integration. Parent and candidate both fail before the item patch at the existing authoring compiler guard for a non-default placement `source_offset`. This is a setup/contract question for the Agent/provider owner, not an App fault and not evidence against the new physical-source branch.

## Boundary and blocker

No App projection9, own9, fixture receive, browser, service, full, family, tour, retry, lint, or typecheck run was performed. The whole candidate remains red at the retained test-file level, and the App whole-path proof is consequently unverified. The smallest authorized next question belongs to the Agent/provider owner: use an admitted default-source-offset fixture for the direct shared-owner test, or explicitly support the existing source trim in `occurrence.place-shared`. No App change or automatic test weakening is justified.
