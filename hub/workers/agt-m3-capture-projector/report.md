Added `project_capture(document, *, authoring_preview=None) → {config, registry, expansion}` using the existing core projector. Save behavior remains unchanged.

- Focused tests: **184 passed, 1 strict xfailed**.
- Real candidate goldens: **6 passed**.
- Ruff and whitespace checks passed.

Blocked: exact saved expansion parity needs `created_at` metadata absent from `CanonicalDocument`. The full golden remains strict xfail; Runtime acknowledged the blocker.

[Report with exact commands, hashes, and decisions](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m3-capture-projector/notes/report.md). Both commit-message files are ready.

Next: orchestrator resolves graph metadata semantics, then Runtime qualifies paired admission and all twelve forgeries. **M3 remains held.**