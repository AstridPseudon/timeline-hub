# Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D141gg-parent-notes-1148/evidence/check_notes.py` → exit 0, `PASS_PRIVATE_D141GG_CANDIDATES`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m json.tool .../rt-F-D141gg-parent-notes-1148/evidence/source-manifest.json` → PASS.
- Independent 568-entry recomputation → 568/568 before and after; maps equal; every full path, regular/non-symlink mode, byte count, and SHA-256 matched.
- Canonical target and backup mode/hash/prefix/suffix/candidate checks → PASS.
- Conservation checks → PASS: 32 IDs, ledgers, witnesses, limits, old gaps, popup/history, placeholders, and balanced fences.
- Function-only `render_readme` with four controlled repository records and missing-gate fallback → PASS; caller and production bin both hash `ef9cd915a4c64f45c179e9ed8aa2ded6e29123847e8018db88ba8b0b680fd9ca`.
- Own durable sampler: 2 samples, minimum available bytes `5603184640` above `4000000000`, PID `4`, exit `-15` after SIGTERM, wait/reap observed.

The raw installation log was inspected for CAS ordering and the checker-interpretation correction. No files in the Composition worktree were changed.
