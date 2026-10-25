# OPS D108b pin audit handoff

Submitted the one authorized light host-scope audit through the normal test service.

- Service ID: `agt-OPS-D108b-pin-audit-0826-ops-agent-pin-audit-1025082803-15709`
- Request: `bin/request-test agt-OPS-D108b-pin-audit-0826 ops-agent-pin-audit --no-cache`
- Suite: `composition ops-agent-pin-audit`
- Script: `workers/agt-OPS-D108b-pin-audit-0826/evidence/host_pin_audit.py`
- Script SHA-256: `87f5525a8624637a1cd21bb3fd4e7e355ba3339985ff8bcbd839c5b2039b76b0`
- Registration CAS: `suites.conf` pre `209e00c24a97aeb6b3b97cc359314a537eabe2328519b36cf4c8dbcfcd4f8708`; temporary post `b62baea4e47065c4bc2ed1eec0a7c20289c0d3870b6cb992cf8c136496d7ab77`; predecessor backup `209e00c24a97aeb6b3b97cc359314a537eabe2328519b36cf4c8dbcfcd4f8708`.

The row is temporary and will be restored by hash-checked CAS after the service result. No Composition source or product/test source was changed.

Service result: exit `3` / `fail`, intentionally conservative `LIMIT` because two namespace fields and 24 process metadata reads were unreadable; 83 PID races were recorded. The durable JSON still records the observer ancestor chain through outside `test-run` PID 21916 and visible `dispatcher-daem`, `test-run`, and `wait-test` witnesses. All three candidate worktrees matched exact SHA/tree and were clean; active-reference lists were empty; candidate process hits were empty. Because host-scope completeness was not fully provable, all three decisions remain `KEEP`.

- Result directory: `tests/agt-OPS-D108b-pin-audit-0826-ops-agent-pin-audit-1025082803-15709`
- Service log SHA-256: `fecf86af812e6a5b5368d69a83e3c88af2d943d7929afa0e3b9fae760f25e812`
- Durable audit JSON SHA-256: `e64d2f8547f93f23fc88992eed1cf46be771ba1209d5110263ce51446b543c48`
- Restored `suites.conf` SHA-256: `209e00c24a97aeb6b3b97cc359314a537eabe2328519b36cf4c8dbcfcd4f8708`; owned row count `0`.

Coverage correction: the scanner now matches candidate paths in cmdline bytes while retaining only a safe cmdline hash and candidate-hit field. Corrected script SHA-256: `d8b0815cfdab168e269b3d00f78bc0142b498f94b7b329638dd0877def4a9468`. Corrected light service ID: `agt-OPS-D108b-pin-audit-0826-ops-agent-pin-audit-1025082909-27257`.

Corrected service also returned exit `3` / `LIMIT`; durable corrected JSON SHA-256 is `8158be5871d3cd82253b7d9cbbb9c26f6097cf0f555e2d891bcf66a3ff3aa4f6`, with 84 PID races, 24 unreadable process fields, 2 unreadable namespace fields, zero candidate hits, and zero active references for each target. The output records outside `test-run`, `dispatcher-daem`, and `wait-test` witnesses and retains historical refs separately. All candidate decisions remain `KEEP`.
