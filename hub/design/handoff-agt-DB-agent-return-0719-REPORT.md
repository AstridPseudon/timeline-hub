# Agent delivery dry-run return — exact tuple qualified

The missing current delivery inputs were created as operational drafts:
`ORCH/delivery/README.template.md` and `ORCH/delivery/gate-results.md`.
They state only current evidence: H3/P1 **NO-GO (partial)**, G5 **gated**,
V4 **cut**, P4 **partial**, Agent full 24,096 **failed/no pass credit**, and
final readiness **not ready**. No v1 approval was copied and no ZIP was made.

The sanctioned `delivery-build --dry-run --repos agent` run at
`build-20261023T072111Z` qualified the exact source tip/tree
`4edc4b321cae5cfc58252d7ed89e3f0408238646` /
`f17b84c48bae3461dd11cedb8719bd17495a8210` against base
`431681a6d3cfa0bba2c8c9baa03f152d33032df1`. Patch and bundle verification
passed with all trees equal to `f17b84c48bae`; the patch is 8,206,362 bytes
(SHA-256 `97615e10ff7913aeb79d4ad680694ea1e88bc7a14f79de015b4d1efd651a4c1b`)
and the bundle is 2,839,300 bytes (SHA-256
`c4a3384688b5105da20feae4c7ac0004aae81fcaecc4a6cbc23df9fd8babff11`).

The retained patch was applied to a worker-owned fresh clone. The exact
targeted Agent command passed **93 tests**. `astrid` and
`astrid_runtime_client` imported from the fresh clone; `runtime_protocol`
imported from `/home/user/work/runtime`. Ruff `2149=2149`, private mypy
`1912=1912`, vendor lock, artifact manifest, and `git diff --check` all passed.

The live integration ref subsequently moved to `d24da4af` / tree `fcc33e0e`.
A later dry-run saw that movement and is deliberately not used to replace the
qualified exact tuple or trigger a new qualification cycle.
