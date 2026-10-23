# Runtime G5/R2r fixture export

## Result

Published the existing authentic fixture evidence as eight flat regular files
under the absolute ORCH design directory for normal hub-sync. The source
evidence files under `design/evidence/` were not altered. The flat export is
described by
`handoff-runtime-G5-fixture-export-1641.manifest.json`.

The archive is
`g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz`, 26,543 bytes, with SHA256
`2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`, matching
the authentic-capture handoff.

## Custody

- Each of the eight named files was copied from `design/evidence/` to the
  flat `design/` directory with the same basename.
- `cmp`, SHA256, and byte-size checks passed for every source/destination pair.
- All exported files are regular files and are below the 50 MB custody limit.
- The archive was not regenerated, restored, or changed; no key material was
  exported. The existing public fixture-key identity remains referenced only
  by the source handoff/evidence.
- The unrelated `g5-sdk-authentic-capture-20261023-sha256sums.txt` was not
  exported because it is not named by the handoff.

## Credential scan

A signature scan covered the eight exported source files plus the existing
source checksum file. It found no private-key headers or recognized cloud,
GitHub, OpenAI, Slack, or Google credential signatures. Secret values were not
printed. No Codex credential access was used.

## Boundary

This is custody/export evidence only. No product files, tests, service,
provisioning, daemon, hub-sync, Git writes, archive regeneration, key
creation, or original FOUR behavior run was performed. Export alone does not
prove Agent body/authority readiness; the independent review and the planned
downstream original FOUR run remain separate gates.

## Verification commands

- `cmp` plus SHA256 and size comparison for all eight source/destination pairs:
  PASS.
- Finite JSON parse and manifest/hash/size validation:
  PASS (after export).
- Credential signature scan without printing values:
  PASS.
- Bash/syntax-only checks: not applicable; no shell or product code changed.
