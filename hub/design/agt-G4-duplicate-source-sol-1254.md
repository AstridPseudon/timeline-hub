Implemented explicit `occurrence.duplicate` reservations through the production helper and caller. The provider preserves legacy placement metadata only for an authenticated exact copy; residual patch order and final validation remain intact. No Runtime change was needed.

Verification, with exact commands and output:

- [Acceptance log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-duplicate-source-sol-1254/evidence/acceptance-green.log): **78 passed**, including both previously failing originals.
- [Focused controls log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-duplicate-source-sol-1254/evidence/controls-green.log): **71 passed, 1 integration test deselected**.
- [Check commands/results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-duplicate-source-sol-1254/evidence/checks.json): Ruff, corrected vendor-lock invocation, artifact manifest, and diff checks passed. Mypy retains exactly two baseline errors at `timeline_editing.py:525`; no new errors.

OldRED/newGREEN XML is retained. Original test hashes and exact ASTs are unchanged. Commit message and `DONE` are written.

No blocker remains for this authoring task. Full, gate, and live Runtime validation were not run. **Independent cumulative core review is required before merge.**