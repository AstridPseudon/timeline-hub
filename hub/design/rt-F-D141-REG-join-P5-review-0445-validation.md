# D141h actual REG join validation

This is a read-only data review. No test, typecheck, lint, collection, import, service, or rerun command was executed by this worker.

| Check | Evidence | Result |
|---|---|---|
| Retained cut identity | `runtime-full-d141-cut-1026005231-18778`, XML SHA-256 `227a6efa...dde31f0`, 7392 cases | PASS |
| Actual pristine identity | `rt-pin-fa9cd546-full-d141-pristine-targeted15-1026044256-11121`, XML SHA-256 `0047e2b8...c094888`, 15 unique cases | PASS |
| Actual result | 15/15 PASS, zero failures/errors/skips/xfails, service exit 0 | PASS |
| Actual XML uniqueness | 15 testcase elements and 15 unique IDs | PASS |
| Actual source controls | Runtime `fa9cd546`, tree `124e10db...f266ed`; Agent `8b6ed211`, tree `0a3691a4...f266ed`; clean checks; `/home/user/work/venv-runtime/bin/python`; no-cache request | PASS |
| Snap and runner custody | normal 32-hex `snap.key`, runner exit 0, retained `KEEP`; raw row retained in place | PASS |
| Resource trace | first and terminal samples retained, continuous trace validation PASS, 5-second policy, 4GB stop, 4.6GB floor decision; heavy marker is empty and no heavy claim is made | PASS |
| Admission and receipts | request admitted by passing service row; recorded D141 decision and controller receipt/trace validators PASS | PASS |
| Source-before/after and validation | Actual service record includes clean source checks, XML validation, trace validation, and retained artifacts | PASS |
| Exact join | 15 census IDs match the 15 actual XML function names after pytest XML filename/module normalization; 38 are `NEW_OURS`; 53 = 15 + 38; no unknown exact IDs | PASS |
| Environment-type pristine failure | None observed | PASS (zero) |
| Product REG verdict | 13 upgrade IDs and 2 TypeScript-generator IDs are `REG_PROVED` from cut failure plus pristine PASS with matching predicate source hashes | PASS |

The 13 upgrade failures retain the same AttributeError frame at `runtime_protocol/timeline_commit_store.py:261`, caused during staged candidate integrity inspection. The two generator failures retain the stale generated-artifact frame for `conformance/typescript/contract-metadata.ts`. Exact census IDs, actual XML names, source paths, body hashes, statuses, and owners are in `reg.json`.

The 38 `NEW_OURS` records receive no product REG verdict. The original P5 result is separately retained as an authentic 38/38 PASS cut proof in `p5-custody.json`; later source applicability remains owed after source changes.
