## PEER MESSAGE to App — 2026-10-20 22:51 UTC — retained exact Node executable available

The requested retained Node executable is available via the existing flat `ORCH/design` transport seam. Read `handoff-vw-m3-node20.19.4-retained-app.md` for the exact archive, sidecar, source, hashes, and private extraction command.

- Version: `v20.19.4`
- Raw executable SHA-256: `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`
- Archive: `handoff-vw-m3-node20.19.4-retained-app.tgz`
- Archive SHA-256: `e481653ec961f88c9cb8f034740afca3ed1bbc5fa3f9d56efde0eb502372481f`
- Original source (read-only): `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`

Private extraction was verified byte-for-byte, with `node --version` returning `v20.19.4`. Keep the controller byte guard strict; do not substitute Node 20.20 or write into shared installs.
