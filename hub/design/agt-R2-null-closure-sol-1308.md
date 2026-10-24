Fixed retained null clip mirrors across final validation, timing validation, emission and patch execution. Changed three authorized source files and added one focused regression file.

Results:

- Original shapes: **2 failed / 3 passed → 5 passed**
- M1: **126 passed**
- Authoring cohort: **336 passed**
- Strict refusals: **17 passed**
- Focused regressions and validation neighbors: **46 passed**
- Ruff, qualified mypy, vendor-lock, artifact-manifest and diff checks passed.

Preserved raw null shapes, validated the authoritative list, and retained scalar, contradictory-mirror and new-null refusals. All original **46 M1 test ASTs** remain exact; protected files are unchanged.

Exact commands and durable XML: [evidence index](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-null-closure-sol-1308/evidence/test-commands.txt).

No blockers. No full or gate suites run. Commit message and `DONE` written. Next: independent core/security review before integration.