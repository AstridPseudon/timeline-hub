# PASS_INSTALLED_SOURCE

The actual installed `ORCH/bin/make-child-venv` is a regular `0755` file,
68,351 bytes, SHA-256
`0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39`.
The file is byte-identical to
`ops-child-custody/make-child-venv` at author commit
`9428f515fcd8dccaef26193438b3ac89f903f5aa`.

The CAS backup exists at
`ORCH/backups/make-child-venv.20261025T165744Z.bak` and is a regular `0755`
file, 68,506 bytes, SHA-256
`1243cb6c203b7f9c23015f2fc0e3fe4722eb53c1c703f171b89123cf9c8afd0b`,
matching the old preimage. The install receipt was parsed as JSON and its
candidate, backup, replacement, embedded-block, reserve, and scope fields
match the current paths. The receipt result is `PASS_INSTALL`.

The resolved commit tree is
`7952f3e9e15532072066474ea9d151fe79114bd6`. The receipt/source review’s
recorded tree is the known malformed 38-character value
`7952f3e9e155320720664ea9d151fe79114bd6`; this is a metadata-only discrepancy,
not a source mismatch.

Protected dependency sources remain exact:

| source | SHA-256 | bytes | mode |
| --- | --- | ---: | --- |
| `bench_store.py` | `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2` | 43,403 | 0755 |
| `verify_dependency_seed.py` | `116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2` | 52,731 | 0755 |

`STORE_PY` (`0889b24010e67bd31f28f5efbaec37fed43adf1a0d5ebe8c4fcd57a8248ca50c`)
and `STORE_VERIFY`
(`f7c7ebcc26221958ce24e36025faad167c6015a2889202752d267e03d5eda209`) are
unchanged from the backup. `STORE_BUILD` is the only changed production
block, and its diff only reuses the existing authenticated source-archive
installation path for unseeded builds. All seven embedded Python blocks
compile in memory.

## Validation commands

- `bash -n ORCH/bin/make-child-venv` — PASS.
- Read-only JSON/hash/metadata assertions over the source manifest, author
  commit, installed target, backup, receipt, protected helpers, reserves, and
  embedded blocks — PASS.
- In-memory compilation of `STORE_PY`, `STORE_VERIFY`, `STAGING_INVENTORY`,
  `RELOCATE`, `PROVENANCE_SCRIPT`, `DIST_METADATA_SCRIPT`, and
  `IDENTITY_SCRIPT` — PASS, 7 blocks.
- `git diff --check` — PASS; worktree remains clean.
- Author, independent review, and installer reports/logs were read. Their
  exact private custody suite result is PASS, 29 tests, including the seven
  embedded compilations and modeled parent-RED/candidate-GREEN controls. No
  duplicate 29-test run was made because no code changed and no actual
  discrepancy was found.

Actual Main layout and actual child acceptance remain `UNVERIFIED / EXACTMISSING`
and `UNVERIFIED`, respectively. No live child/build/diagnostic, Store,
package acquisition, registration, body, provider, full, browser, P4, or
SWAP action was performed.
