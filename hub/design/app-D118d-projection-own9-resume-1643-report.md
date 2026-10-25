# D118d report

- Verified source custody: test blob SHA-256 `6e41a5...a1436`, empty diff from reviewed commit.
- Verified Runtime pin `5e9ad1c6`, tree `de2954a0`, clean; provider registration resolves to pinned Runtime.
- Live free space: `4,993,753,088` bytes initially, falling to `4,992,692,224`; below required `5,000,000,000` floor but above `4,000,000,000` stop.
- Exact nine-node pytest was **not run**; pytest never started. Static checks were not repeated per instructions.
- Evidence written under the assigned worker evidence directory, including `facts.json`, `source-custody.json`, `commands-results.md`, `verdict.md`, and `own9.log`.
- Blocked reason recorded in `BLOCKED`. No source, dependency, cache, or shared worktree changes.