# Runtime G5/R2r custody review — independent export review

## Verdict

**PASS.** The eight files named by
`handoff-runtime-G5-fixture-export-1641.manifest.json` are byte-identical
between `design/evidence/` and flat `design/`, with matching SHA-256 hashes,
sizes, regular-file types, and finite JSON where applicable.

The three existing independent 1640 proof JSONs were copied to flat `design/`
without changing their bytes. Their source/destination comparisons, hashes,
sizes, regular-file types, and finite-JSON checks pass.

## Archive identity

The existing archive is 26,543 bytes and has SHA-256
`2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`, matching
the independent 1640 review. Archive member paths were safety-inspected; the
archive was not regenerated, restored, or modified.

## Checks

- Export manifest: 8/8 source/destination `cmp`, SHA-256, size, regular-file,
  and finite-JSON checks — PASS.
- Independent 1640 proof copies: 3/3 exact `cmp`, SHA-256, size,
  regular-file, and finite-JSON checks — PASS.
- Credential signature scan over source and flat export/proof files — PASS,
  zero matches; no secret values were printed.
- Runtime base observed read-only at commit
  `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`, tree
  `9b07545cac9a8bbafb16246aaa6f72050ef7cffe`.

## Boundary

This is custody/export evidence only. The independent 1640 current-reader
restore and 10-test qualification are retained as prior evidence and were not
rerun here. No Agent FOUR run, service, daemon, provisioning, archive
regeneration, key-material operation, product/test/generated/pin change, or
authority/body claim was made. No producer gate was added.

Detailed hashes and paths are in
`handoff-runtime-G5-custody-review-1645.manifest.json`.
