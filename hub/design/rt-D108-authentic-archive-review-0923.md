# D108 authentic archive independent review

## Verdict

**PASS — custody and handback only.** The existing archive is present at the
exact absolute source path below, has the expected size and SHA-256, and is
byte-identical to the retained ORIGINAL0912 archive. The prior safe metadata,
hash file, and report were copied byte-for-byte into the requested flat
handoff names.

## Verified archive

- Source path: `/home/user/timeline-hub/hub/design/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz`
- Size: `26543` bytes
- SHA-256: `2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`
- Existing comparison path:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/evidence/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz`
- `sha256sum -c`: PASS for both source and comparison archive.
- Exact byte comparison (`cmp`): PASS.
- No archive extraction, acquisition, reconstruction, or archive mutation was
  performed by this review.

## Receipt and source facts

The copied ORIGINAL0912 safe JSON records the normal receipt
`txn-11c90075be6c4c8bb9e2627366f0fe4f` for `parent_composition.publish`, event
`3`, content digest
`sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb`,
revision `a3e671256f1c42b8837d3e118c97b21b`, and predecessor receipt
`txn-55c0651b2cd64255ae06e73f9708220a` / revision `film-parent-v1`.

The same safe metadata records Runtime source commit
`d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`, old source commit
`0ba9622a3e98a85577ef893be85988ba7f203b88`, and old source tree
`c0bbd76656ac21439d11bf928eb970d60fe6e690`. No credentials or private
payload/body content were copied into the handoff.

## Preserved boundary

The historical setup gap remains unchanged: 27 authenticated-legacy-restore
rows plus 16 current-pair-reader rows = **43 ENV errors** caused by absent
`ASTRID_AUTHENTIC_LEGACY_ARCHIVE`. No reader behavior is credited. This review
does not approve semantic behavior, body behavior, relabel behavior, or any
new archive/input; the existing 43ENV row remains open until corrected-input
proof.

## Handoff files

- `handoff-rt-D108-authentic-archive-0923-source.json` — byte-copy of
  ORIGINAL0912 safe metadata JSON.
- `handoff-rt-D108-authentic-archive-0923-source.sha256` — byte-copy of
  ORIGINAL0912 checksum file.
- `handoff-rt-D108-authentic-archive-0923-source-report.md` — byte-copy of
  ORIGINAL0912 report.

Product worktree is clean. Tests, typecheck, and lint are N/A for this
artifact-only, read-only review.
