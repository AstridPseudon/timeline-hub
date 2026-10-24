Ask: use these read-only farm facts for the 0600 request / Owner: Runtime / By: 2026-10-24T06:45Z

Read at 06:20Z. No process probe, no provisioning, no credentials.

## Registry and row
$ORCH/tests/suites.conf SHA256 1a8d349ae6428f447061b13fe96665ff56049a9f3c02644e4c379ccb5de3b5e3 (199218 bytes, 161 lines; baseline before the maker was 64afaf61...; after the maker 7baf5254...).
Line 161, the only `agent full-farm` row (unmanaged, 188 bytes):
agent full-farm env ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-45c3a7f4 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-45c3a7f4" /home/user/work/venv-agent/bin/python -m pytest -q -n 3
Note: the row carries NO Remotion/Node env (no ASTRID_REMOTION_PROJECT_DIR, ASTRID_NODE_EXECUTABLE, Node 20 PATH, ASTRID_TIMELINE_SCHEMA_PYTHONPATH); this is why the 187 setup errors occurred in run 26511. The maker also added a managed line for suite agent-remotion-farm-8657e836-nodes and tests/agent-remotion-farm-8657e836.env.

## Normal receipts
- queue/done/runtime-agent-remotion-farm-8657e836 (04:56Z): status=created, registration_template=remotion-env-nodes identity=validated, requested Agent 8657e83653f48c935f52f209516456bcb5a36282 / Runtime 45c3a7f476e1c5f74fafc15956a58b9871eee21f, build_origin_agent_sha=8657e836..., remotion_tree_sha=b01dca9b3b24f54093c20b7c5657316f997725db, lock_sha256=f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d, component_identity=22888dcf93bab96b97843b6096ad432610f9aa92e8f9210050f352a435fd66d6, key=5ca5c561b7be7069051ac8769432cc1edf29060bed39384cd3c4ecab1736e690, reuse=verified, node v20.19.4 / npm 10.8.2.
- Managed root: /home/user/work/bench-store/entries/runtime-5ca5c561b7be7069051ac8769432cc1edf29060bed39384cd3c4ecab1736e690 (Store owner 90c899284ebd474685cd278b8ce06255).
- Node20 carrier: /home/user/work/toolchain/node-v20.19.4-linux-x64/bin (the eighth request field).
- queue/done/checkout-runtime-45c3a7f476e1c5f74fafc15956a58b9871eee21f: created /home/user/work/wt/rt-pin-45c3a7f4 (detached, KEEP).
- queue/done/checkout-agent-8657e83653f48c935f52f209516456bcb5a36282: created /home/user/work/wt/agt-pin-8657e836 (detached, KEEP).
Both pins were clean (git status empty) when checked at 04:50Z.

Not provided: the Agent working row/env (requested separately from Agent). Checkpoint 26511 stays terminal; the farm reruns only on an explicit handoff.
