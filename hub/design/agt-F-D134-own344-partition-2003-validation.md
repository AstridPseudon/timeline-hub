# Validation

- Parsed the immutable 1937 per-ID evidence and retained 18455 log read-only; selected exactly 344 `OURS_NEW_FILE` IDs.
- `per-id.tsv`: 344 data rows, 344 unique nodeids, 11 tab-separated fields on every row.
- Category counts: `TEST_SETUP_OR_EXPECTATION_PROVED=141`, `PRODUCT_FAULT_PROVED=0`, `UNKNOWN=203`; equation is `141 + 0 + 203 = 344`.
- Cluster counts sum to 344: managed-edge 102, stale pin/hash 11, missing fixture args 2, projection 9, detached preflight 4, missing client 1, retired route 1, v2 label 3, mirror guard 7, legacy archive 1, unresolved 203.
- `sha256sum log.txt` matched `65def166348d4ffde949d530bff1a7bcba820ad674ca85b8ccc3e708c781ae8e`.
- JSON artifacts were checked with `python3 -m json.tool`.
- No test suite, collection, service request, rerun, browser, socket, or acquisition was performed; this task is read-only classification.

The 14 prior REG records remain separate as `UNVERIFIED_CURRENT_REG`; the 12 prior UNKNOWN records remain UNKNOWN. No REG0 or retirement deduction was made.
