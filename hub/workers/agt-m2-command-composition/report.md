Composed the reviewed native writer diffs with ordered/staged undo, typed clip reservations, and exact scalar closure restoration.

**HELD—not merge-ready:** one original graph test remains strict-xfail because bare root records lack the original parent revision pin. The authenticated provider round-trip passes. Next step: supply that authenticated input boundary while preserving the original assertion.

Validation:

- SDK/conformance: **468 passed, 1 strict-xfail**
- Authoring bundle: **25 passed, 1 deselected**
- Central M1/first-clip/scalar: **4 passed, 1 strict-xfail** (unchanged Runtime null-speed issue)
- Ruff and diff checks passed; no full suite run.

[Report with exact commands, source/golden paths, and line budget](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-command-composition/notes/report.md). Both commit-message files are written.