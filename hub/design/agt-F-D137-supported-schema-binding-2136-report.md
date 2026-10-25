# D137/F report

- Qualified the supported binding: `ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages`.
- Verified frozen four-repo tuple, registered child key, interpreter/origin partition, direct-URL schema source, and 12-entry RECORD hashes.
- Ran exactly one unchanged-launcher positive/poison control:
  - Positive: exit `17`, calls `1`.
  - Poisoned `agent_sha`: exit `1`, calls `0`.
- Retained prior import failure, poison refusal, and preparation failure; no unchanged retry.
- No product, test, launcher, guard, child, shared-venv, package, or Git changes.

Validation:

- `bash -n evidence/core-command.sh` — PASS.
- JSON validation for all six JSON packets — PASS.
- Frozen source SHA/tree/parent/origin/dirty checks — PASS.
- No tests, full suite, request-test, or core body run.

Evidence is under the assigned worker evidence directory. Actual fullbody remains pending independent review of this PASS control packet.

Commit message written and `DONE` marker created.