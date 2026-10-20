Implemented `placement.move` v1 with explicit ownership, shared-root refusal, registry guards, occurrence bounds, and parent/occurrence goldens. It reuses existing move timing and writes.

- Validation: **319 targeted tests passed**; ruff and `git diff --check` passed.
- Legacy pooling/add/replacement semantics remain unsupported. Runtime/App acceptance and full suites were not run.
- Both commit-message files are ready. No merge requested.

[Report with exact commands and next steps](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-placement-native/notes/report.md) · [Contract](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-placement-contract.md)