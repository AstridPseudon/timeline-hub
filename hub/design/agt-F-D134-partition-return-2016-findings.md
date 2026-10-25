# F/D134 reviewed OWN-344 classification derivative

## Verdict

This is the corrected derivative of author2003’s permanent evidence. The
author packet remains byte-for-byte unchanged. The independent review2011
identified exactly nine `projection_fixture_missing_item` records whose first
boundary is `source_payload["items"][0]` at
`tests/sdk/test_timeline_capture_projection.py:316`. They are moved from
`TEST_SETUP_OR_EXPECTATION_PROVED` to `UNKNOWN`; no record is removed, added,
or promoted to product fault.

The reviewed finite partition is:

`TEST_SETUP_OR_EXPECTATION_PROVED (132) + PRODUCT_FAULT_PROVED (0) + UNKNOWN (212) = 344`.

## Exact membership delta

- Author member count: 344; reviewed member count: 344.
- Added nodeids: 0. Removed nodeids: 0.
- Category changes: exactly 9, all in the `projection_fixture_missing_item`
  cluster, from setup/expectation proved to UNKNOWN.
- The nine changed nodeids are preserved in `partition.json` and are the
  projection cases for `child`, `duplicate`, `new_shot`, `parent`, `remove`,
  `sdk_bundle`, `test_real_saved_entire_expansion_golden`,
  `test_real_saved_projection_config_registry_and_full_pins_golden`, and
  `test_saved_canonical_images_preserve_authored_fields_pins_order_and_read_rows`.
- All 335 outside records retain their author2003 IDs, source/tuple fields,
  member IDs, clusters, and categories exactly.

## Reviewed category totals

| Category / cluster | Count |
| --- | ---: |
| `managed_edge_fixture` — setup/expectation proved | 102 |
| `stale_source_pin_or_hash_expectation` — setup/expectation proved | 11 |
| `fixture_call_missing_required_args` — setup/expectation proved | 2 |
| `detached_fixture_preflight` — setup/expectation proved | 4 |
| `fixture_missing_client` — setup/expectation proved | 1 |
| `retired_save_route_expectation` — setup/expectation proved | 1 |
| `v2_status_label_expectation` — setup/expectation proved | 3 |
| `clip_mirror_fixture_guard` — setup/expectation proved | 7 |
| `legacy_archive_shape_expectation` — setup/expectation proved | 1 |
| `projection_fixture_missing_item` — UNKNOWN | 9 |
| `unresolved_causal_boundary` — UNKNOWN | 203 |
| **Total** | **344** |

No `PRODUCT_FAULT_PROVED` record is legitimate from the retained evidence.
The nine projection records remain UNKNOWN because protected D100 first-birth
and source-authority evidence is missing; the setup-frame absence does not
prove a test bug or product fault. Do not infer closure of the original nine.

## Retained service and source binding

The retained service is
`agent-agent-core-full-1025191128-18455`, with log SHA-256
`65def166348d4ffde949d530bff1a7bcba820ad674ca85b8ccc3e708c781ae8e` and
summary 190 failed, 180 errors, and 8926 passed. The source tuple and all
current source/member IDs are unchanged from author2003.

Author evidence and review input hashes are bound in `partition.json` and
`source-manifest.json`. Author `per-id.tsv` SHA-256 is
`f98a97e4f9dd9773acd18f85d7ae649c95f1c970a213680d9324c573c9d2b97a`.

## REG14 and boundaries

The 14 REG records remain `UNVERIFIED_CURRENT_REG`; the prior UNKNOWN count
remains 12; missing XML and final-count evidence remain UNKNOWN; retirement is
0. The retained XML is unavailable. The derivative does not claim product
fault, current REG closure, original-nine closure, or any migration/fix.

No tests, collection, service request, rerun, browser, socket, acquisition,
source fix, product migration, or author-packet rewrite was performed.
