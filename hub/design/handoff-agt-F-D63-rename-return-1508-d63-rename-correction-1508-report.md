# F/D63 rename correction

This is a read-only correction overlay for the prior D63 publication. The original 201-row JSON/TSV and the original folded 276-row summary remain retained at their recorded paths and hashes in `d63-rename-correction-1508.json`.

## Correction

The prior publication correctly found two bounded rename candidates but incorrectly published all 201 missing selectors as `NEW-OURS`. The corrected split is:

- 199 `NEW-OURS` rows after the existing cheap name/body check.
- 2 authenticated upstream counterparts: order 129 and order 181.
- Order 129 is current `PASS`, upstream `PASS`.
- Order 181 is current `OPEN`, upstream `PASS`; it remains a current-proof candidate owned exclusively by `agt-F-D63-env-catalogue-current-1508`. It is not a `NEW-OURS` non-core known gap, and no regression closure is claimed.

The XML records were authenticated against their complete module/class/function identities, not a fuzzy name collision:

- `tests.packs.rendering.test_remotion_render_contract.TextCardVisibleMarkupTest` / `test_text_card_renders_visible_markup` — PASS.
- `tests.test_env_vars_conformance.TestNoBareStringAccess` / `test_no_catalogued_bare_strings_in_core` — PASS.

The other visible known-gap row, order 55 (`test_no_audio_wire_parity - ...`), remains genuine `NEW-OURS`: the retained current selector has a literal suffix and no body hash or authenticated rename mapping. The nearby upstream XML testcase is `tests.core.rendering.test_conformance::test_no_audio_wire_parity` and is a failure, so it is not used as a counterpart or regression closure.

## Folded totals and precedence

The folded total stays 276. The 75 prior normalized-exact matches plus the 2 authenticated counterparts yield 77 qualified counterparts if proved: 66 FAIL and 11 PASS. The nine current-PASS contrasts are the prior eight plus order 129. Order 181 is the one current candidate pending proof. Existing categories remain 78 environment and 2 D23-deferred with existing precedence; the core current rollup remains 152 PASS and 5 OPEN. No zero-regression closure is asserted.

All 201 source IDs and current evidence references are preserved by overlaying this correction on the original artifacts; no receipt was invented or rewritten. The original 276 totals and source hashes are retained.

## Validation and limits

No tests, product source execution, registry/generated-file work, locks, installs, or package acquisition were performed. XML attribute inspection and read-only JSON/TSV invariant checks only. The exclusive order-181 current-proof worker was not run.
