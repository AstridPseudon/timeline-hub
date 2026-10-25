# Validation

Read-only validation completed:

```text
sha256sum retained service log
65def166348d4ffde949d530bff1a7bcba820ad674ca85b8ccc3e708c781ae8e

raw summary parse
FAILED=190 ERROR=180 unique_bad_ids=370 duplicates=0

author per-id parse
rows=344 unique_nodeids=344
author categories: TEST_SETUP_OR_EXPECTATION_PROVED=141 PRODUCT_FAULT_PROVED=0 UNKNOWN=203

reviewed finite equation
TEST_SETUP_OR_EXPECTATION_PROVED=132 PRODUCT_FAULT_PROVED=0 UNKNOWN=212 SUM=344

source qualification
current_blob_mismatches=0 selected_files=58 upstream_present_files=0
failure_file_line_out_of_bounds=0

tuple tree checks
Agent PASS Runtime PASS App PASS Composition PASS

JSON syntax
review.json PASS classification-bounds.json PASS source-manifest.json PASS
```

Exact membership was checked by parsing the raw service summary and comparing the nodeid set with the author packet’s `per-id.tsv`: 0 selected IDs missing from raw; 26 raw IDs outside the selected OWN partition. The 344-row packet hash is `f98a97e4f9dd9773acd18f85d7ae649c95f1c970a213680d9324c573c9d2b97a`.

No product test, collection, full suite, targeted suite, service request, rerun, browser, socket, acquisition, or source mutation was performed. Raw XML and accepted-record/caller traces remain unavailable, so behavior/custody cannot be promoted.
