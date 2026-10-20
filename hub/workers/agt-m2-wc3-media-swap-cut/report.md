Implemented WC3 native media-swap migration.

- Replaced whole-closure publication in `remote.py` with native `TimelineSession` capture/flush.
- Added exact immutable media selection validation and durable pending-command retry handling.
- Preserved explicit API fields, receipts, errors, source windows, ordering, opaque fields, and isolation.
- Updated direct and Runtime-backed conformance tests.
- Design note: [agent-wc3-media-swap-cut.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-wc3-media-swap-cut.md)
- Commit message written; `DONE` created.

Tests:

- Focused tests: `123 passed`
- Replacement tests: `6 passed`
- Runtime conformance: `2478 passed, 4 skipped, 2 xfailed`
- Focused Ruff and `git diff --check`: passed

No blockers. Qualification ledger remains held until merged.