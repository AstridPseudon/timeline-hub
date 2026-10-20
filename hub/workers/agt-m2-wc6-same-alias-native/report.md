Implemented the private same-alias native media rebind path.

- Reused existing `occurrence.swap-media` v1; no schema/public pin/HTTP DTO changes.
- Preserved alias identity, opaque fields, payload/raw data, inverse, and ABA guards.
- Removed the strict xfail after the original positive test passed.
- Local tests: `158 passed, 1 deselected`; Ruff and compile checks passed.
- Central real Runtime session journey: `10 passed`.
- Same-alias Runtime acceptance is blocked by the supplied Runtime candidate’s retired direct-shot fixture route; no fallback was added.

Reports:

- [Design report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-wc6-same-alias-native.md)
- [Worker report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-wc6-same-alias-native/notes/report.md)
- [Commit message](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-wc6-same-alias-native/commit-msg)

`BLOCKED` was written with the exact external blocker.