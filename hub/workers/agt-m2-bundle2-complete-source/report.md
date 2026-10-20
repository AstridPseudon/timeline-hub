Composed the required scalar, root, pack/PARAM, trim, and split overlays, preserving popup provenance guards and M1/parent-label bytes. Optional free-moves excluded.

Verification:

- Bounded local lanes: **1,553 passed**, 4 existing skips.
- PARAM direct pair: **15 passed**.
- Frozen Runtime direct pair: **45 passed, 12 xfailed**.
- Final HTTP proof: **95 passed, 13 xfailed**.
- Schema union, 47 byte/delta checks, focused lint and mypy passed. Broader lint findings are documented.

[Report with exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-bundle2-complete-source/notes/report.md) and [absolute Bundle2 handoff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-writer-bundle-2.md) are ready. Both commit-message files are written.

Harness commit remains pending; the handoff includes a helper to verify and publish its exact SHA afterward. PARAM release, official Runtime generation, and M2 integration remain held.