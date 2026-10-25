# D132a protected verdict

Source review: PASS.

The complete pure construction from `document_fixture()` through the existing create-roots operation and `document_from_bundle` produced a schema-shaped `PreparedCommit` candidate. Against frozen Runtime `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`, the pre-edit census found exactly one error at `$.canonical_document.shot_revisions[1].payload.metadata`: `None` is not an object. The after-state candidate has zero errors after the approved authored `null -> {}` setup-slot migration.

The cumulative source delta against `20177e66564f9f91735ed1a11bac821682d60edf` is limited to six v2 request metadata lines and the one approved authored setup input. Fixture counts remain 22 test bodies/90 assertions/6 parametrizations; graph counts remain 11/33/7. Test-body, assertion, and parametrization ASTs are unchanged. Actual D60 `92443771676ef2bbb547d0a103d708fa8bec4c63` and frozen R4 SDK `11caf1d9de291d76f491cf69f7942606b7471d7a` both lack the fixture and graph paths; the unavailable `d11417a59` object was not treated as absence proof.

No Runtime, Agent product, schema, generated, pin, caller, guard, or assertion changes were found. No source fix was made after PASS.

Own9 then ran exactly the authorized nine nodes with 5,019,459,584 bytes available, against clean Runtime `5e9ad1c6`/tree `de2954a`, using the registered `astrid` provider. All 9/9 failed at the genuine Runtime route with the first safe refusal: `invalid_records` / `CommitRejected`, “provider executed a different command,” first node `test_typed_roots_are_valid_local_creations_and_retired_roots_are_reserved`, frame `runtime_protocol/timeline_commit_auth.py:337`. Raw XML/log remain private in `own9.xml` and `own9.log`. No retry, second body, alternate route, or extra suite was run.
