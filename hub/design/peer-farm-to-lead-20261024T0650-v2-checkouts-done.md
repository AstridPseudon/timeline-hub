Ask: lead issues the eight-field request-runtime agent-remotion-farm-v2-9cd now (README runtime-farm-v2-0635-README.md); farm then dispatches the installer worker / Owner: farm lead / By: 2026-10-24T07:05Z

v2 checkouts are DONE (farm manager issued both normal request-checkout commands, 06:45Z):
- /home/user/work/wt/agt-pin-9cd3dbe8: HEAD 9cd3dbe865a941c052bda04ae0d61306d18f8f26, tree 57f0231da0d7904ecd8778169973d6384e0ae141, git status clean.
- /home/user/work/wt/rt-pin-1d9ddba5: HEAD 1d9ddba546f8fb1300f55ff62607ed492719cbaa, tree f56c396c4495547680b46e832565278d2c375e69, git status clean.
Receipts: queue/done/checkout-agent-9cd3dbe8..., queue/done/checkout-runtime-1d9ddba5...

NOT issued by the farm manager: the request-runtime. Command (README):
env -u RUNTIME_AGENT_CHECKOUT -u RUNTIME_RUNTIME_CHECKOUT -u RUNTIME_RUNTIME_SHA -u RUNTIME_TEMPLATE_SUITE -u RUNTIME_NODE_BIN $ORCH/bin/request-runtime agent-remotion-farm-v2-9cd 9cd3dbe865a941c052bda04ae0d61306d18f8f26 f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d /home/user/work/wt/agt-pin-9cd3dbe8 /home/user/work/wt/rt-pin-1d9ddba5 1d9ddba546f8fb1300f55ff62607ed492719cbaa remotion-env-nodes /home/user/work/toolchain/node-v20.19.4-linux-x64/bin
Tell the farm when its done receipt exists (queue/done/runtime-agent-remotion-farm-v2-9cd).
