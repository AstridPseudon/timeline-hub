# Agent F — bounded diagnosis of unconfirmed host/installer failures

This is the source-backed companion to `Externalreport.md`. The sole full4249 run was the `fcc33e0eb964dd48d422673e8f692f195c88748c` snapshot (Agent commit `d24da4af0f1ca83880b4b9ef57559e28ebe52a2a`): exit 1, `240 failed`, `16388 passed`, `140 errors`, `40 skipped`, `5 xfailed`, `4269.86s`.

The exact bounded service rerun was `agt-F-unconfirmed-env-0900-targeted-1023090053-24359` on Agent tree `6f7649a4e0b8f1d936dc94a5fa0bb7c5fb3db276`: 13 collected, **9 passed / 4 failed**, exit 1, `23.44s`, using the durable 0856 projection and Node `v20.19.4`. This is bounded evidence only; independent post-exit durability review remains pending.

## Owner map

- Farm/installer environment: D13 is blocked on its exact profile, binding file, wheel/source digest, native executable digests, browser, and node_modules contract. The two installer nodes are blocked earlier because `Backend.run` launches `version.python -I -m astrid_runtime`, while the selected `venv-agent` has no isolated `astrid_runtime` installation. No repair assertions were reached.
- Agent generic-host owner: the legacy assembler node is a real current source-backed failure at `_renderer_selection` (`generic_host.py:1639`) dereferencing `record.adapter` on the test's intentionally minimal capability record. The expected immutable-publication admission refusal is therefore masked. Upstream 431 status was not tested.
- Farm durability owner: the seven idle/host nodes pass together under the durable environment. This is an environment-sensitive classification, not a source-fix or full-suite claim; the exact variable responsible for the full4249 behavior is not isolated.

## Exact evidence and limits

The durable service command used the existing Agent `targeted` row with `PYTHONPATH=$PWD:/home/user/work/runtime:/home/user/work/agent-runtime-projection-0856/site-packages`, `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`, `ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-composition14-255b6856`, `ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, `ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages`, and `ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-composition14-255b6856/node_modules`.

The exact origin probe found Agent and client modules in this worktree, `runtime_protocol` in `/home/user/work/runtime/runtime_protocol`, and shared schema in `/home/user/work/venv-agent/lib/python3.13/site-packages`. Node reported `v20.19.4`; the Composition lock digest was `b7c4ab2e3c3f466d9d1c0c8d7472a40101d37b6288d52b930067dc663a17feb0`.

No full suite, browser/render journey, P1/P4 HTTP, native14, crash24, source/test/fixture/pin/shared-dependency modification, or upstream baseline was run. Nothing was deleted. The D13 tuple must not be invented or admitted from the ordinary renderer environment. Full qualification is explicitly not claimed.
