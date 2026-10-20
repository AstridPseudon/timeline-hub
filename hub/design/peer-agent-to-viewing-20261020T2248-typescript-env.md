# Agent to Viewing: TypeScript probe environment repair

Date: 2026-10-20 22:48 UTC

Source: `/home/user/work/wt/agt-m4-layer-tail-typescript-env`, branch `tl/agt-m4-layer-tail-typescript-env`.

Changed only `tests/packs/rendering/test_remotion_layer_tail_compat.py`: the callback probe resolves `typescript/lib/typescript.js` from `ASTRID_TEST_NODE_MODULES`, retaining `/home/user/work/app/node_modules` as the fallback. No production code, package authority, or shared install changed.

Exact central test source/environment: C13 named suite `full-c13-a8a40afd-integration`, Node `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node` (v20.19.4), `ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0013`, `ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0013/node_modules`, Python `/home/user/work/venv-agent-child-c13-a8a40afd/bin/python`.

Exact requested nodes: all eleven node IDs in `tests/packs/rendering/test_remotion_layer_tail_compat.py` covering the three scalar positives, two legacy window parameters, the middle native window, three unlayered native window parameters, and two support/locked-props parameters. The exact command and node list are recorded in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m4-layer-tail-typescript-env-full-c13-a8a40afd-integration-1020224740-4451/log.txt`.

Result: `11 passed in 11.97s`, exit 0. No neighbors or full suite were run. The pre-tail/native/legacy/clock assertions remain unchanged.
