Fixed the proven R2 product defect in `inverse.py`. Nested redo now authenticates its restored root against the accepted command input, accounting for native writes before deletion. Owner, deletion, restoration and exact-input guards remain strict. No existing tests or fixtures changed.

- **Targeted qualification: 46 passed**, including the unchanged original failure, all ten recreation/forgery controls, provider fork coverage and 11 new codec tests.
- The retained capture also passes through production `RuntimeCommitService.commit` preview.
- Against the exact base codec, both new positives reproduce the original identity error; all nine negative controls pass.
- Scoped Ruff: PASS. Qualified typecheck-v2 mypy: **1902/1902**, PASS. `git diff --check`: PASS.

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-captured-history-sol-1112/evidence/commands.txt) · [JUnit](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-captured-history-sol-1112/evidence/qualified-targeted.xml) · [Original body hashes and origins](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-captured-history-sol-1112/evidence/source-hashes.json)

No blockers. `inverse.py` remains 1,208 lines; no rationale update needed. Full/gate suites and persisted acceptance of the captured redo were not run. Next: independent whole-path/source review.

Commit message and `DONE` written; no git writes performed.