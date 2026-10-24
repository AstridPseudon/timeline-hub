## F/D54a report

- Compared all assigned 33 selectors against upstream XML `9244377`, old `9758` evidence, D52 package/current receipts.
- Result: 33 upstream FAIL; 33 old FAIL; 0 cause-identity-qualified; 0 exact-env-qualified.
- Four old tracebacks were retained but had different causes from upstream. The other 29 were summary-only and remain UNPROVEN.
- Current status: all 33 `NOT_RUN_CURRENT_CORE159`; no current failure or PASS receipt inferred.
- Durable evidence: [d54a-paired-cause-1458.json](/home/user/work/wt/agt-F-D54-paired-cause-a-1458/evidence/d54a-paired-cause-1458.json), 29 KB.
- No product, test, source, dependency, or environment changes.

Validation:

- `python3 -m json.tool ...` — PASS
- Exact 33 ID/order/category/status parity check — PASS
- `git diff --check` — PASS
- Full/targeted tests — not run per read-only scope.

Commit message and `DONE` marker created. No blockers; remaining facts needed are retained old tracebacks for 29 rows and an authorized current-core run.