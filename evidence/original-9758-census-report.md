## Report

Completed evidence-only checkpoint census.

- Service result: exit 1; 231 failed, 45 errors, 17,673 passed, 4 skipped, 85 warnings, 566 subtests.
- Source verified: commit `ba55ac1e9e…`, tree `c13d368666…`; Runtime `/home/user/work/runtime` at `becfe6db…`.
- Parsed 276 unique terminal bad IDs: 231 failures and 45 errors.
- Retained traceback sections: 119; absent offsets: 157.
- Skip markers: 4 located; node IDs/reasons were not retained.
- Reconciliation: 64 historical-closed bad, 3 historical-open bad, 1 historical-open unknown, 200 original IDs not listed as bad/unknown, 209 new or different bad nodes.
- Preserved all 267 D32 records unchanged.

Evidence:

- [census JSON](/home/user/work/wt/agt-F-full9758-census-1052/evidence/agent-full-1024095047-9758-census.json)
- [terminal CSV](/home/user/work/wt/agt-F-full9758-census-1052/evidence/agent-full-1024095047-9758-terminal.csv)
- [traceback extract](/home/user/work/wt/agt-F-full9758-census-1052/evidence/agent-full-1024095047-9758-tracebacks.txt)
- [manifest](/home/user/work/wt/agt-F-full9758-census-1052/evidence/agent-full-1024095047-9758-census-manifest.json)

Validation commands passed:

- `python3 -m json.tool` on both JSON artifacts
- JSON/CSV/node-list parity and count validation
- Manifest SHA-256 validation
- `git diff --check`

No product tests, lint, typecheck, full retry, or test body rerun. Evidence totals 5.9 MB. Setup-cause classification remains owned by the separate worker; no regression causes or closures were inferred.