Implemented the private Agent fix; no Runtime/App changes or public adoption.

- Enforced canonical outer keys, 256 UTF-8-byte limit, reserved-key rejection, and App size/count limits.
- Preserved nested `__proto__`/`constructor`/`prototype` JSON data.
- Fixed absent/null/empty namespace disjoint rebases while preserving exact inverse and ABA protections.
- Added focused regression coverage.

Tests: `209 passed`; Ruff, schema parse, and `git diff --check` passed. No full/Runtime/App suites run.

Private schema SHA-256: `89ed90ce0a4a95559a6d086d57f851fbcc6d224c9e7658f41467dfa9280eb0c3`

Artifacts: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-project-data-main-limits-fix/report.md), commit message, and `DONE` marker created.