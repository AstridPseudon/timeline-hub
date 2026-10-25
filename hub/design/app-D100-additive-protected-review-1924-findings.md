# D100 protected source-purpose review

Verdict: **PASS_SOURCE_PURPOSE**.

No finite source-purpose finding requires a return. The approved candidate is
exactly one additive test-file change from `9486cbb06e2ab53402086772e6c2bc18bc4849fc`
to `92eb2dafc6a3d4735253b14882fd336faa79837c` (final tree
`7a03ee6731d10d024419a3fd8c2383e5b2c29e44`). The protected product file
`astrid/sdk/timeline/_command_state.py` is SHA-256
`018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3` on
both base and candidate.

## Independent delta audit

The candidate changes only the following purposes:

1. In `test_first_physical_item_preserves_custody_and_opaque_fields`, it
   replaces the over-broad whole-`source_mapping` equality with exact equality
   for authoritative `shots`, `placements`, and `_runtime_document`; asserts
   that the only extra top-level key is `_doc_patch_images`; and asserts the
   complete cache projection for owner `occurrence:occ-a`, including physical
   `shot_id`/`internal_timeline_id`, source revision IDs, authored payload, and
   authored internal timeline.
2. In `test_registered_shared_owner_uses_the_same_physical_custody_without_alias_birth`,
   it authors the new direct shared-owner fixture with `source_offset: 0` and
   recomputes the authored parent payload digest. It then applies the same
   authoritative/cache split and asserts both explicit owner keys
   (`occurrence:occ-a`, `occurrence:shared`) with the exact source physical IDs,
   source revision IDs, payload, and internal timeline.

The expected cache values are derived from the authored `document`/`replacement`
inputs, never from `plan.bundle` or the result under test. Owner keys and all
cache fields are explicit; no owner guessing, optionalization, weakening, or
post-output circular derivation is present.

## Preserved predicates and inputs

The diff deletes only the two broad cache-inclusive equalities and the
unadmitted shared-owner setup assignment. It preserves the existing input
fixtures, command envelopes, patch paths, previous values, aggregate and
non-aggregate variants, and all other assertions: `item_id_map == {}`;
canonical shot payload; opaque item fields; internal revision equality;
wrong physical owner/revision/digest; duplicate/empty/malformed IDs;
wrong-previous-value whole-patch refusal; copied-placement birth/missing/
duplicate/owner/map refusals; copied payload physical identity; existing-owner
switch refusal; original bundle immutability; and the registered Runtime
first-birth acceptance plus wrong-previous no-write refusal.

The registered behavior test remains a real RuntimeService `commit_timeline`
caller with the C0 request envelope and idempotency key. The mounted App
boundary is independently present as `localSaveSession` durable outbox →
`DataProvider.commitTimeline`; Runtime enforces the canonical route and
startup-only registered Astrid provider. The local `execute()` shared-owner
case is not used as production-path credit. D66 diagnostic hooks are unrelated
to this custody predicate and are not credited.

## Evidence boundary

The author packet's static checks passed. Actual1837 and independent1843
retained the meaningful registered-provider RED→PASS but did not establish
whole-candidate GREEN. This review therefore records **source-purpose PASS only**;
behavior bodies, corrected own27, original9, App projection, fixture receiving,
provider/socket/browser/full suites, and source release remain **NOTRUN/HELD**.
