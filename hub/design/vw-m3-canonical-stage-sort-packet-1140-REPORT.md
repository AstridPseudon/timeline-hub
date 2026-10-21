# Canonical stage-sort packet 1140 READY

The corrected operational packet is published at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-canonical-stage-sort-packet-1140/packet`

`stage-audit.mjs` now delegates graph serialization to the frozen App0d43
controller `hashTree` (`15e7a670adfc914fca2eed54b9c1c70d53f5df1e1ff16534247d0e6841767469`, full controller `f536eff2773cd1ffd87678d647b99facd01c7cfa6d649d98ae7a0b7387038c27`) and uses direct gzip/tar parsing for the 77-member archive guard. The exact functional and namespace diff against 1120 is published at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m3-canonical-stage-sort-packet-1140.patch`

Local actual audit PASS: source and stage both `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c / 21455`; all existing filesystem, inode, link, closure, lock, manifest, source, and bundle guards ran. Direct tar parsing: 77 unique regular members. Planted changed-byte and missing-file negatives both refused. Static prerequisites and checksums all pass. No Composition worktree source changed.

The independent review and `grant-canonical-stage-sort-1140.md` are not yet present, so no central preflight or physical request was made. See the worker report for exact commands and hashes.
