## D108 report

- Found existing archive: `/tmp/.../design/evidence/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz`
- Size: 26,543 bytes
- SHA-256: `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`
- Normal receipt: `txn-11c90075be6c4c8bb9e2627366f0fe4f`
- Runtime source commit: `d9e2a71e...`; Git source blobs recorded in [D108-authentic-archive.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D108-authentic-archive-input-0912/evidence/D108-authentic-archive.json).

Preserved the historical gap: 27 restore cases + 16 current-reader cases = 43 `ASTRID_AUTHENTIC_LEGACY_ARCHIVE` environment errors; no reader behavior was credited.

Outputs:

- [Safe metadata JSON](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D108-authentic-archive-input-0912/evidence/D108-authentic-archive.json)
- [Hash file](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D108-authentic-archive-input-0912/evidence/D108-authentic-archive.sha256)

Validation passed: `sha256sum -c`, `jq empty`, `git diff --check`, clean worktree, and output-scope checks. No tests/lint/typecheck run per the readonly artifact-lookup acceptance. Commit message and `DONE` marker written.