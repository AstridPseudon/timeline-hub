Implemented the reviewed successor:

- Applied the approved opaque remapper and removed duplicate logic.
- Tightened allocation, reference, typed-birth and boolean/numeric checks.
- Reused the command engine for complete inverse ACK verification.
- Reduced product growth from **+397 to +387 lines**.

Focused tests: **615 passed, 7 deselected**. Scoped Ruff and `git diff --check` passed. Six positive Runtime tests await the official generated pair; actual admission/own-slot qualification remains unverified.

[Report with exact commands, findings and next steps](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-materialization-review/report.txt). Coordination and both commit-message files are ready. The harness must publish the successor SHA after committing.