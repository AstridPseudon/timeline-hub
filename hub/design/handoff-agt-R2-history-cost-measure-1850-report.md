SOURCE MEASUREMENT PASS

Measured the existing Runtime control:

`tests/test_timeline_inverse_sequential_authority.py::test_inverse_sequential_scope_round_trip[v2-whole-restore]`

- Result: `1 passed in 6.87s`, exit 0.
- `store.history_entry`: 258 calls; max recursive depth 6; 4.400s inclusive / 0.581s exclusive.
- `_verify_accepted`: 254 calls; 4.126s inclusive / 0.651s exclusive.
- `store._inverse_stage_history`: 259 calls.
- `auth._inverse_stage_history`: 106 calls.
- `auth._capture_records`: 106 calls; `Recorder` validation: 106 calls, 1.470s.
- `PreparedCommit` validation: 55 calls, 0.863s.
- `json.loads`: 6,299 calls; digest: 3,136; canonical JSON: 5,696.

The smallest measured seam is `runtime_protocol.timeline_commit_validation.validate_commit_value(value, definition)`, handed to owner `rt-P4-validation-dispatch-1827`. Proposal only: inspect reuse/dispatch cost for repeated `Recorder` and `PreparedCommit` validation. No fix applied; D47 remains held. Timings are profiler-inclusive and overlap; they do not establish original-45s causality.

Evidence:

- [profile.json]( /home/user/work/wt/agt-R2-history-cost-measure-1850/evidence/r2-history-cost-measure-1850/profile.json)
- [JUnit XML]( /home/user/work/wt/agt-R2-history-cost-measure-1850/evidence/r2-history-cost-measure-1850/runtime-v2-whole-restore.xml)
- [run log]( /home/user/work/wt/agt-R2-history-cost-measure-1850/evidence/r2-history-cost-measure-1850/runtime-v2-whole-restore.log)

Checks passed: harness `py_compile`, `git diff --check`. No product/test changes; no full suite run. The requested `handoff-agt-R2-tail-wholepath-1840-*` artifact was unavailable in mounted paths/refs. Commit message and `DONE` marker written.