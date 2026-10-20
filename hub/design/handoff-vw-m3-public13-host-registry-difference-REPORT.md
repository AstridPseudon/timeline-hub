# Report: `vw-m3-public13-host-registry-difference`

Status: `exactRootDiff`; not `HOSTREADY`.

- Reproduced the existing b70 registry comparison with 15 workers.
- Cause: worker processes retained an external `ASTRID_PACKS_PATH` and `PYTHONPATH`, while the host used the current source root.
- Effects registry differed:
  - Host hash: `84b2d658…652e7`
  - Worker hash: `b5d65c61…341a`
  - Only `$.content_hashes.effects` differed semantically.
- Worker loaded 22 extra shadow owners from the alternate root, producing the mismatch.
- Repeated with both sides on the same root: zero semantic, registry-entry, and owner differences.
- Captured sanitized provenance, module origins, pins, paths, and process custody in:
  - [registry-comparison.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-public13-host-registry-difference/registry-comparison.json)
  - [registry-comparison-fixed.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-public13-host-registry-difference/registry-comparison-fixed.json)

Tests: no product tests run; no source changed, and broad/install/browser/render/network suites were prohibited. Diagnostic probes exited successfully with cleanup/custody checks passing.

No core or helper changes were made. The owner fix remains unapplied: bind host and workers to one authoritative source/install root, then rerun actual catalog/launch validation. Pins remain unchanged. Commit message and `DONE` marker written.