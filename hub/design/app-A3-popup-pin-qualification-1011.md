# A3/A2 qualification report

- Qualified held App packet at `5bafd247e8426bf5ca03b7aa841fbb037b6c20d5`.
- Agent pin: `333b44b1a1b8be72d4d101391b7636c508419109`; Runtime pin: `37eb6c7bdb79dcae2523883e66b5cea5be721ffd`.
- Exact mounted recipe: **67/67 tests passed** (accepted and merged popup flows included).
- Overall qualification: **PASS**.
- No product/test edits were needed; worktree remains clean.

Command used: Node `20.20.0`, Vitest `4.1.5`, runner loader, no cache, one worker/file serialization, actual `A3_AGENT_SOURCE`, `A3_RUNTIME_SOURCE`, and qualified Agent Python override.

Additional checks passed:

- `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`
- Scoped ESLint
- Private Python compilation
- `git diff --check`
- Protected source blob identity

Exact App SHA/tree/parent:

`5bafd247e8426bf5ca03b7aa841fbb037b6c20d5` / `dd6ed3c5261c918c6947fa7589b35c02948be99d` / `d99fd1a0bc9fc3112219415159eaec87494a09b6`

Agent and Runtime source checkouts were clean and stable. No browser, HTTP, live Runtime, database, build, or full suite was used; provider/direct-fixture coverage is not original gate credit.

The required `commit-msg` and `DONE` markers were created. Recommended next step: proceed with the independent cumulative App review and merge queue.