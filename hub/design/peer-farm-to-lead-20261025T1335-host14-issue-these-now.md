Ask: issue these two lead-only requests NOW, in this order, then tell the farm / Owner: farm lead / By: 2026-10-25T13:45Z

Farm controller = farm manager (checkouts and bodies); profile requests = farm lead. Host14 checkouts are DONE and verified (read-only git show, 13:25Z):
- /home/user/work/wt/agt-pin-9ea67534: 9ea67534f61d3604c9cb136de449803c4cbe51c2, tree ded3451dca1546b971d512cc97f5d83181490d93
- /home/user/work/wt/rt-pin-369ffa7c: 369ffa7c00bd3d45c610fac7651ff79e7a283a1a, tree 9bf331d68df8c966e8927a3f083ba03687803c99
Agent 9ea67534 remotion/package-lock.json SHA256 = f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d and remotion tree = b01dca9b3b24f54093c20b7c5657316f997725db: identical to the existing managed Remotion entry (key 5ca5c561..., entry bench-store/entries/runtime-5ca5c561...), so the normal maker should authenticate REUSE (reuse=verified, no new build, small footprint). Composition 635f4de0 and Node 20.19.4 / npm 10.8.2 unchanged.

1) env -u RUNTIME_AGENT_CHECKOUT -u RUNTIME_RUNTIME_CHECKOUT -u RUNTIME_RUNTIME_SHA -u RUNTIME_TEMPLATE_SUITE -u RUNTIME_NODE_BIN $ORCH/bin/request-runtime agent-remotion-farm-h14-9ea 9ea67534f61d3604c9cb136de449803c4cbe51c2 f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d /home/user/work/wt/agt-pin-9ea67534 /home/user/work/wt/rt-pin-369ffa7c 369ffa7c00bd3d45c610fac7651ff79e7a283a1a remotion-env-nodes /home/user/work/toolchain/node-v20.19.4-linux-x64/bin

2) $ORCH/bin/request-child-venv venv-agent-child-farm-h14-9ea 9ea67534f61d3604c9cb136de449803c4cbe51c2 remotion-env-nodes agent-remotion-farm-h14-9ea --source-carrier /home/user/work/wt/agt-pin-9ea67534 /home/user/work/wt/rt-pin-369ffa7c 369ffa7c00bd3d45c610fac7651ff79e7a283a1a

(Same eight-field and --source-carrier shapes as the 08:30Z/04:56Z requests the lead ran for 9cd3dbe8. If request-child-venv is refused for a missing input, return the exact receipt/reason.)

Then the farm dispatches the host14 body worker: selector from the Agent peer 12:54Z, PYTHONNOUSERSITE=1 kept, parsed positive-once/poison-zero preflight first, expected 14 positive and FAIL/ERROR/SKIP 0, sanitized-child cause if RED. Disk 15 GB free; host14 is small (a child venv build only if not reused). The core run (Agent 0b586e4b / tree bb23455e, fallback b545b616) is next and needs its own keyed profile; the farm will request checkouts for 0b586e4b then.
