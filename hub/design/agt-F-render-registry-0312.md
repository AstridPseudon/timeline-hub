Implemented F-render-21.

- Reused the already-loaded default `ElementRegistry` for production type membership checks.
- Preserved the independent catalog guard for explicit/caller-supplied registries.
- Added focused load-count, override, foreign-membership, and transition-guard tests.

Tests/checks:

- Resolver controls: 6 passed
- Resolver/catalog/lazy neighbors: 27 passed
- Installed registry security: 26 passed
- Scoped Ruff, mypy, vendor lock, artifact manifest, and `git diff --check`: passed

The reviewed-source control files were absent from this worktree and were not imported. The original 45-second timeout remains unknown and unqualified; no original/full/renderer probe was run.

Commit message and `DONE` marker written.