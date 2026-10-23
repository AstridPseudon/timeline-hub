# R1/A3 current-integration occurrence.fork port

Current integration port report for orchestrator handoff. Source `dc00a764c0c0acc9f613261060b4e5552dd0c1cc` over `9cf0fde2f57603813d81733ee8b0f7117ffd634c`, applied to `bf40d6bb5923210a3f5d210414c9ad737b40403d`.

Source-set SHA256: `e7c96edb911f6a1d89fb218cc951fea6094ee350f2ab62cbf039f951239e6830` (exact match to `design/agent-A3-occurrence-fork-call-0504.json`). Exactly the 13 reviewed paths changed: nine existing provider files and three new conformance tests plus `native_occurrence_fork.py`. No schema/generated/pin/artifact/runtime/App/G234 files changed. Baseline files matched the reviewed source base, so no conflict composition was required.

Runtime provenance: tests used a private read-only archive of `6a6e97506409719b9d3c54984268e7c93c026efa`, whose `runtime_protocol` production tree has no diff from `be5848e17fbf68100286114883f5820fe4755911`. Module origins were verified: `astrid` and fork provider from this worktree, `runtime_protocol` from the private archive.

Evidence: provider/recipe targeted `25 passed in 4.04s`; real RuntimeService integration `1 passed in 3.15s`; author-equivalent source/neighbour lane `244 passed in 24.79s`; scoped Ruff PASS; private mypy PASS10; normal Ruff ratchet `2150/2150`; local vendor lock PASS; artifact manifest PASS; diff/whitespace checks PASS. Normal mypy ratchet was attempted but environment-limited by missing YAML stubs and incompatible NumPy stubs; no baseline or budget change. Mounted App proof remains explicitly unclaimed. See worker report for exact commands and limits.

Commit message: `feat(timeline): port R1-A3 occurrence fork`.

