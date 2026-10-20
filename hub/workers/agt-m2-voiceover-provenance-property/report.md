Implemented and marked complete.

- Extended `shot.set` for only `payload.metadata.draft_voiceover`, with occurrence ownership, exact clear/null semantics, sibling preservation, guards, inverse, rebase, and ABA behavior.
- Added recorder tests using the original voiceover fixture.
- Preserved prior schema floor hashes; new schema hash: `65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e`.
- Wrote [provenance source report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-voiceover-provenance-source.md), commit messages, and `DONE`.

Tests:

- Targeted voiceover/shot/schema tests: `107 passed`
- Current union schema: `34 passed`
- Ruff, py_compile, JSON validation, and `git diff --check`: passed

Remaining audio/extent and Runtime admission blockers are documented; WC5 retirement is not claimed.