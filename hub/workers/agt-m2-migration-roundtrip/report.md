Fixed both gaps: created-root bindings validate at the correct inverse stage, and the exact legacy provenance path preserves opaque data. Original and opaque-variant reload → inverse → same-ID redo tests pass.

- Targeted tests: **603 passed, 1 deselected, zero xfails**.
- Ruff, whitespace and inverse mypy checks pass.
- Graph mypy retains **13 verified pre-existing errors**.
- No loader/compiler change was needed.
- Runtime seed/schema gaps remain unresolved; **all M2 merges remain HELD**.

[Report with exact commands and next steps](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-migration-roundtrip/notes/report.md). Both commit-message files are written; local caches removed.