FULLPASS for assigned artifact scope; production qualification remains unverified.

Implemented:

- `ops-handoff/remotion-toolchain.patch` — maker-only patch accepting explicit eighth `NODE_BIN` argument.
- `ops-handoff/remotion-toolchain-manifest.json` — hashes, command, evidence, and limits.
- Commit message written to the required harness path.

Validation:

- Fixture: `/home/user/work/venv-runtime/bin/python "$TMPDIR/test-node-carrier.py"` — PASS.
- Counts: `cases=12`, explicit=1, legacy=4, refusals=7, store=1, build=0.
- `bash -n`, Python compile, private patch apply/cmp, JSON validation, and diff checks — PASS.
- Baseline maker: 26,508 bytes, SHA-256 `99cca067…e4e28`.
- Patched maker: 27,925 bytes, SHA-256 `99cc8673…033a0`.
- Patch: 3,119 bytes, SHA-256 `0e665467…8ad3c2`.
- Manifest: 3,358 bytes, SHA-256 `1d90cf95…a89204`.
- Preserved request/daemon hashes: `f13a1d07…591f7b1` / `f18bc20b…892c15`.

Production request command is recorded in the manifest and was not queued. The exact approved Node path was absent in this sandbox, so actual installed Node/npm hashes and production caller smoke remain unverified. No daemon, queue, build, install, network, restart, or source checkout was modified.