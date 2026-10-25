# F/D134 independent final review

## Verdict

PASS for the firstreturn2016 classification derivative, classification-only.
The independent2011 packet correctly identified that the author2003 packet
overstated setup/expectation proof by nine records. The returned derivative
applies exactly that correction and nothing else.

The prior packet dispositions remain distinct: author2003 and independent2011
are `FAIL_AUTHOR_PACKET_OVERSTATES_PROOF`; this final review is PASS because
the derivative is the corrected, bounded artifact.

## Findings

- The original2003 packet is preserved byte-for-byte.
- All 344 memberIDs are conserved: 344 author rows, 344 reviewed rows, zero
  additions, zero removals, and 344 unique nodeids on each side.
- Exactly nine rows differ, and the only changed field is
  `causal_category`. They are the complete original
  `projection_fixture_missing_item` cluster, moved from
  `TEST_SETUP_OR_EXPECTATION_PROVED` to `UNKNOWN`.
- Every other row preserves its status, failure type/file/line, test file,
  source blob, provenance, cluster, and source evidence.
- Cluster and category totals conserve to
  `TEST_SETUP_OR_EXPECTATION_PROVED (132) + PRODUCT_FAULT_PROVED (0) +
  UNKNOWN (212) = 344`.
- The retained service log hash, tuple, and all source fields match the
  original2003 packet exactly. Permanent worker evidence and flatdesign copies
  match byte-for-byte.

## Boundaries retained

`UNVERIFIED_CURRENT_REG` remains 14; prior UNKNOWN remains 12; missing XML and
final count remain UNKNOWN; retirement remains 0. No product fault is proved.
The nine projection records remain UNKNOWN because protected D100 first-birth
and source-authority evidence is absent; a setup-frame missing item does not
prove a test bug or product fault.

This PASS qualifies classification only. It grants no migration, source fix,
test rewrite, route change, or product-fault credit.
