# PASS — V3 Agent integrated proof

Verified integrated source:

- `HEAD`: `fa2cf5b6642384ec1ce77dee64b733d585c6308a`
- Tree: `8ff1653c1189c8788310260c9a0bdabb3cb63241`
- `b56828de5` ancestor: PASS
- Worktree clean; no product/test/pin edits.

Evidence:

- Targeted pytest: **108 passed, 1 deselected**
- Installer tests: **2 passed**
- Capture-label overlay tests: **20 passed**
- `gen-types`: PASS
- `typecheck`: PASS
- Public exports and production caller smoke: PASS
- Archive cmp/SHA/SRI/80-member and historical archive checks: PASS
- `git diff --check`: PASS

Disclosed baseline findings: two existing Ruff findings; private npm lock-only run showed only optional `libc` metadata drift, not applied. No full/browser/native/farm suites run.

Report: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-V3-agent-integrated0114/report.md)

`DONE` created.