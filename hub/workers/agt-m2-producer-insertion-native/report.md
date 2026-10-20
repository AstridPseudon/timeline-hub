Implemented both native operations, assembly lowering, registry storage preservation and canonical inverse dependency checks. Promoted all 24 spike cases; 66 permanent cases now cover the native path.

- Final focused run: **268 passed**.
- Broader focused runs: **577 passed**, **361 passed**.
- Ruff and `git diff --check`: passed.
- Unequal dual registries refuse under main’s existing policy.
- Product delta: 125 added / 20 removed lines, net105.

[Report with exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-producer-insertion-native/notes/report.md). Design/Runtime handoffs and both commit-message files are ready.

Runtime pairing remains unverified pending official generated artifacts and authentic settled outputs. No writer cut or settlement change was made.