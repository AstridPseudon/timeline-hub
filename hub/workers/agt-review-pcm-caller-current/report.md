**APPROVE the exact four-file caller patch.** No product changes; worktree clean. Report and required completion files written.

[Review report, exact commands and logs]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-pcm-caller-current.md)

Results:

- Caller and neighboring tests: **210 passed**.
- Source/service probes: **7 passed**.
- Compiler/projector tests: **81 passed, 2 existing xfails**.
- Central HTTP tests: **26 passed**, including four real host-served fade-phase comparisons.
- Ruff and diff checks passed.

No full suite ran. Runtime admission, actual encoder/MP4 output, Three.js PCM, Player/export parity and owner-film behavior remain unqualified. Recommended next step: land only the caller patch on the integrated extent/public12/kernel base.