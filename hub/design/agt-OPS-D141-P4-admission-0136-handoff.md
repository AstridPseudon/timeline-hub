# D141c P4 admission handoff

Install-ready candidate:

- `ops-d141-p4-admission/test-run`, mode `0755`, SHA-256 `8aa75771f6d3b3e7b65570580131a4866f3e65440d9d815a717c1189e323f5ce`.
- `ops-d141-p4-admission/admission-controls.sh`, mode `0755`, SHA-256 `6fd4462e62a1962db9b298f9f03dae3ba842d7ea818b24f67968ed0c76813737`.
- `ops-d141-p4-admission/source-manifest.json`, mode `0644`, SHA-256 `8b5cda45aaeaeedde34a8836ffe27d42abad63131c5afdfe4b7891b6cb98e2e1`.

Canonical preimage: `/home/user/timeline-hub/hub/kit/bin/test-run`, mode `0755`, 14,962 bytes, SHA-256 `0be17b74ad1e324bc84e50e61e50e3e07390b262b7abe17a37ad22b9bd10d0fe`. The candidate's scoped diff is recorded in `source-manifest.json`; no outside bytes changed.

Required next step: an independent review worker must run the same private control script against the candidate and record PASS before normal separate CAS installation and publication. This worker did not install the canonical kit, add a suite row, submit a request, or run a service body.

No product pytest, typecheck, lint, full suite, or live service run was required or run. The existing queued service remained queued under the old light classification and was not re-requested.
