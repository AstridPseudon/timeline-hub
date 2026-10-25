# F-D108/D69 original predicate map — partition 0

Status: **SOURCE_ONLY_EXACT_PARTITION_WITH_PARTIAL_APPROVALS**.

The authoritative membership is `original-membership.json`, SHA-256
`1bd9b4c08c1ade951f28983172c6e76205401c93af5943abc2c3d924ddb6e7d0`. Records were sorted by `(record.path, record.function)` and
assigned by `enumerate(index) % 2 == 0`: **65/129 functions**, with **46/113
removed** and **109/287 added** assertion multiplicity. The complement is 64
functions, 67 removed, and 178 added. JSON contains all 65 function records,
including zero-delta changed bodies; TSV contains the 65 function summaries and
155 distinct assertion rows.

## Decisions

- `approvedreplacement`: 9 rows, only exact G5/D72 selectors and reviewed
  source blobs.
- `preservation`: 25 rows, only exact added assertions within those same
  reviewed selectors/body hashes.
- `approvedretirement`: 0 rows. No retirement was newly approved.
- `UNCLEARED`: 121 rows. These have exact source membership and per-row source
  receipts, but no exact approval receipt; D69 decision-conflict reports remain
  conflicts, not approvals.

D72 is credited only for
`test_native_window_layer_is_materialized_once_with_pin_hold_and_alpha` at new
blob `3c0bfbaaa7b7a8b73ee0d90f1b2a20b58aec6efd`. G5 is credited only for the
exact checkout and store selectors at new blobs `75a9fae98485d8b0e71261039664c4bdcaf9f7a5`
and `dfd1de6876a44f580350120199066aa2a0be799d`. Every credited row names the
review receipt, exact function source/body hashes, membership item, and current
normal `d0ecf1d69a7b37f86034bc52004f73f6c6231603` blob. No selected path has a
later-source-only mismatch.

## Limits and next decisions

Unknown rows stay `UNCLEARED`; aggregate/operator counts, lexical resemblance,
and passing tests do not clear them. Existing D07/b943, Windows/d0ec,
D107/2e3331ee, and D18 owners remain separate. The exact remaining decision
need is an independent selector/body/fingerprint review or owner decision for
the 121 uncleared rows. No old-applied-tree presence, semantic pairing across
unrelated functions, product behavior closure, or authority change is claimed.

Validation recorded in the JSON/evidence: JSON parse, in-memory structure
compile, exact partition arithmetic, and Git/source reads passed. Product
tests, imports, collection, helpers, probes, services, browser, install,
typecheck, and lint were not run (N/A for this source-only task).
