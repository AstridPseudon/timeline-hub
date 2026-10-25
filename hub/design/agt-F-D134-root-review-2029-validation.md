# Validation

Independent read-only validation completed for the finished2022 packet.

Commands used:

- `sha256sum tests/agent-agent-core-full-1025191128-18455/log.txt`
- Python read-only parser over the retained log, `root-clusters.json`, and `per-id.tsv` for status, ID, group, fixture-frame, production-frame, exception-type, and finite-classification checks.
- Python read-only SHA-256 checks for the ten `source-manifest.json` input files.
- `git show -s --format='%H %T' a4e016b6a9f91fbe372672bdcf382c630bf59186` in the frozen Agent repository.
- `git show -s --format='%H %T' 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` in the frozen Runtime repository.
- Read-only `git ls-tree` checks for all 64 current source blobs and all referenced test files.
- Read-only retained-directory inventory to confirm XML, raw receipt, disk witness, and other private artifacts remain absent.

Results:

- PASS: retained log hash `65def166348d4ffde949d530bff1a7bcba820ad674ca85b8ccc3e708c781ae8e`.
- PASS: 370/370 raw IDs, 370/370 TSV rows, and 370/370 unique IDs; 190 failed plus 180 error.
- PASS: 370/370 first fixture frames; 370/370 Agent production frames; 370/370 Runtime production frames.
- PASS: 52 groups conserve 370 members with no duplicate, missing, or extra IDs; all group fields are consistent.
- PASS: 1937 and finished2022 ID sets are identical.
- PASS: all ten manifest input hashes, frozen Agent tree `60d45288145414ee4702fcce61af7c7810c2a3df`, and frozen Runtime tree `de2954a0ceadb4455903d9abdfec3b773318a50f`.
- PASS: 132/0/212 finite OURS_NEW_FILE equation, plus 14 REG and 12 prior UNKNOWN; no product or ship credit.

No tests, lint, typecheck, control, collection, service, browser, socket, or body run was performed.
