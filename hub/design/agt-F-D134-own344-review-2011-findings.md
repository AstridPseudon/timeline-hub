# F/D134 independent OWN-344 review

## Verdict

FAIL for the author packet as a classification artifact. The raw service and exact 344-member selection are reproduced, but the author’s `141 + 0 + 203` proof count overstates setup/expectation proof by nine projection records. The reviewed finite partition is:

`TEST_SETUP_OR_EXPECTATION_PROVED (132) + PRODUCT_FAULT_PROVED (0) + UNKNOWN (212) = 344`.

The original author packet is retained byte-for-byte and is not silently rewritten.

## Independent checks

- The retained service log hash is `65def166348d4ffde949d530bff1a7bcba820ad674ca85b8ccc3e708c781ae8e`; its terminal summary is 190 failed, 180 errors, 8926 passed, 86 warnings, and 173 passed subtests.
- Parsing raw `FAILED`/`ERROR` summary lines gives 370 unique bad nodeids, 190/180 by status, and no duplicate IDs. The author packet’s 344 nodeids are an exact subset: selected-minus-raw 0; raw-minus-selected 26.
- All 344 current test-file blobs match the author packet’s recorded hashes. The 58 selected files are all absent at named upstream `08e6b905...`; this is provenance only, not causality.
- All four tuple commit/tree pairs match their git objects: Agent `a4e016b6/60d452...`, Runtime `5e9ad1c6/de2954...`, App `d8a1cd40/dd2afd...`, Composition `635f4de0/5ab519...`.
- The current C0 contract is Runtime commit `5e9ad1c6`, `contract/commit-v2.md`. Its recorded predicates support the retained route/label/closure checks; it does not provide product behavior credit by itself.

## Correction

The author’s `projection_fixture_missing_item` cluster contains nine IDs whose first boundary is `source_payload["items"][0]` at `tests/sdk/test_timeline_capture_projection.py:316`. The product assertion is never reached. Because these projection cases depend on the protected existing D100 first-birth/source authority, a missing item in this setup frame cannot be called a test bug from the frame alone. These nine are therefore UNKNOWN, not proved setup/expectation errors.

Exact correction guidance: keep the nine IDs in the same 344-member universe, move only their category to UNKNOWN in a reviewed derivative, and obtain a retained/qualified D100 first-birth plus source-authority record before any further promotion. Do not retarget these cases to App proof 27, substitute a new capture, or rewrite the author packet.

## Boundaries retained after review

- The 102 managed-edge records remain setup/expectation-proved only because source inspection shows the shared fixture actually submits generic `doc.patch` changes to `parent/occurrences`, while C0 requires semantic closure creation/attachment/per-occurrence operations. The managed guard refusal alone would not be enough; no product fault or faithful migration is inferred.
- The 11 source/hash/pin records are direct explicit assertions against historical literals. The qualified current tuple was independently hashed and differs. This is an input/expectation boundary; it is not permission to silently refresh pins, and raw hash failure is not itself causal product evidence.
- The 2 missing-argument, 4 detached-preflight, 1 missing-client, 1 retired-route, 3 v2-label, 7 mirror-guard, and 1 legacy-shape records each have direct source and retained first-boundary evidence. C0 uses `merged` for new non-base v2 landings, preserves historical `rebased`, and excludes overwrite routes. Mirror and legacy classifications rely on explicit test purpose/source, not the guard text alone.
- The remaining 203 author UNKNOWN records stay UNKNOWN. This includes protected Gate3/D133, D23/D14, D100 first-birth and missing-authority/live-authored-input cases, and all unresolved failures without an accepted record and legitimate caller trace. Guard text, failure status, new-file provenance, or a setup frame cannot promote them.

No `PRODUCT_FAULT_PROVED` record is legitimate from the retained evidence. The 14 prior REG records remain `UNVERIFIED_CURRENT_REG`; the 12 prior UNKNOWN records remain UNKNOWN; retirement remains 0.

No tests, collection, service request, rerun, browser, socket, acquisition, source fix, or product migration was performed.
