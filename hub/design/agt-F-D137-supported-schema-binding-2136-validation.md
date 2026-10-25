# D137/F validation

Status: PASS_EVIDENCE.

- bash -n evidence/core-command.sh — PASS.
- python3 -m json.tool on all six JSON packets — PASS.
- Positive/poison manifest structural validation — PASS; both have 36 lines and differ only in agent_sha.
- Frozen Agent/Runtime/App/Composition SHA, tree, parent, origin and clean-status checks — PASS.
- Registered child interpreter/origin probe with PYTHONNOUSERSITE=1, PYTHONDONTWRITEBYTECODE=1, pinned Agent/Runtime PYTHONPATH, and explicit ASTRID_TIMELINE_SCHEMA_PYTHONPATH — PASS.
- External schema RECORD verification — PASS (12 hashed entries).
- bash -n was run before the bounded controls; the unchanged pinned launcher was used.
- No product/core/test/pin/generated/kit file was changed. No pytest, request-test, full suite, service body, child request, package installation, copy or alternate interpreter was used.

The historical D134/1848 control witness remains retained. The D137 prior positive import failure, poison refusal, and rehearsal-stub preparation failure remain retained and were not retried unchanged.
