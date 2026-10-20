Implemented only the valid two-file migration from `2961d3ce`:

- Migrated identity fixtures to public Runtime ingest and trusted acceptance.
- Updated closure seeding to retain existing pinned shot/internal images.
- Preserved all original assertions; Stage 1 changes were excluded.

Tests:

- Identity current Runtime: `3 passed`
- Pinned Runtime `94114269`: `3 passed`
- Capture/trusted-seed integration: `26 passed, 32 deselected, 6 xfailed`
- Ruff and diff checks: passed
- Named projection lane: `3 passed, 2 failed` due unrelated Runtime health schema digest mismatch in M1 tests.

Wrote commit message and `DONE` marker.