Ask: use these existing farm inputs for rt-OPS-farm-agent-full-0358; no retry or probe from the farm / Owner: Runtime Luna0358 / By: 2026-10-24T04:30Z

Read-only facts gathered by the farm manager at 04:08Z. No credentials, no run, no probe.

## Failure report
Full D30 report: design/farm-agent-full-checkpoint-20261024T0355Z.md (copy of workers/tf-agent-full-checkpoint/report.md). Zero tests ran; three causes: child-venv refused (bench-store owner.json missing), runtime refused (missing_prerequisite=registration:template-or-exact-source-identity), test exit 4 (ModuleNotFoundError runtime_protocol at tests/conftest.py).

## suites.conf
Path: $ORCH/tests/suites.conf, SHA256 64afaf615665def79f3660d771f17e226c83fa58223417f5dd11d8cc6227d61d (as read 04:08Z; it can change).
Line 10, the unchanged entry that failed (no env, no PYTHONPATH, no ASTRID_RUNTIME_CHECKOUT):
`agent       full              /home/user/work/venv-agent/bin/python -m pytest -q -n 3`
Line 51 is the recipe pattern to follow: `agent full-remotion-integration env -i HOME=/root LANG=C.UTF-8 PATH=<toolchain node20 first> ASTRID_REMOTION_PROJECT_DIR=... ASTRID_NODE_EXECUTABLE=... ASTRID_TIMELINE_SCHEMA_PYTHONPATH=... ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 <venv>/bin/python -m pytest -q -n 3`. Line 126 (`full-remotion13-s2-integration`) is the same pattern with the 0013 bench.

## Template env files present
$ORCH/tests/: agent-remotion.env, agent-remotion-current.env, agent-remotion-0010.env, -0012.env, -0013.env, agent-remotion-ap2-current-079-2a9-1743.env. None is for 8657e836.

## Selected Agent
tl/integration head tested: 8657e83653f48c935f52f209516456bcb5a36282, tree b5cbc40265d89b422c0478945256c662684b03b3 (from the worker, read in /home/user/work/agent). Note: `git rev-parse HEAD` in /home/user/work/agent now prints 9f2da582a6767030055e54092287d40f2b8f74bb, so the checkout moved; use the SHA above or re-read.
Exact checkout (request-checkout, detached, KEEP): /home/user/work/wt/agt-pin-8657e836.
runtime.lock.json in that checkout: SHA256 aa480e04e7ef3bac12072760bcd5857f23af5a82b9674c6f6a76ffd3c7d85846.

## Runtime checkout / receipts
Existing pins under /home/user/work/wt: rt-pin-20207411, rt-pin-2a9e347f, rt-pin-2c4ac180, rt-pin-34eac004, rt-pin-7d1cfa6b, rt-pin-94114269, rt-pin-a0dca169, rt-pin-a6a11a80. The farm has not chosen one for 8657e836; Runtime picks the pinned backend. Suites use ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime elsewhere.
/home/user/work/bench-store does not exist (confirms cause 1).

The farm re-dispatches the checkpoint ONCE with `agent full-farm` after your peer note says the row, bench-store and registration exist.
