Implemented the bounded fixture fix.

- Added `_check_core = check` to the two affected fake checkout fixtures.
- Preserved all forwarding, default, gap, and argument assertions.
- No product code or test weakening.

Tests:

- Affected files: **4 passed**
- CLI neighbors + working-copy tests: **254 passed**
- Ruff selected rules: **passed**
- `git diff --check`: **clean**
- Full suite: **not rerun**

Historical classification and handoff:

- [Classification](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-full24995-classification.md>)
- [Handoff](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agt-tests-full24995-three-cli-fixes.md>)
- [Worker report](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-tests-full24995-three-cli-fixes/report.md>)

Patch SHA-256: `415744518d1223940e6e1588ebe9c6eee0a26250b7696063f36771ad387bd45b`

Commit message and `DONE` marker written.