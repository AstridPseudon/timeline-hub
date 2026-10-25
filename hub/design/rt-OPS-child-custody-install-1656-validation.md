# OPS child custody exact installation validation

Result: `PASS_INSTALL`.

## Installation

- Reviewed source: commit `9428f515fcd8dccaef26193438b3ac89f903f5aa`; maker SHA-256 `0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39`; `68351` bytes; mode `0755`.
- Live target preimage CAS: `1243cb6c203b7f9c23015f2fc0e3fe4722eb53c1c703f171b89123cf9c8afd0b`; `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/backups/make-child-venv.20261025T165744Z.bak` preserves the exact `68506`-byte, `0755` preimage.
- Installed live target equals the reviewed candidate byte-for-byte and mode-for-mode: `0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39`, `68351` bytes, `0755`.
- Method: CAS-guarded backup followed by same-directory atomic replacement. No semantic edit, permission change, store/dependency/trust/queue change, or worktree change.

## Exact controls

Commands and results:

```text
bash -n ops-child-custody/make-child-venv                         PASS
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v
                                                                   PASS (29 tests)
/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests
                                                                   PASS
git diff --check                                                   PASS
```

The unittest run used a real private `TMPDIR` directory at the assigned evidence path because the harness worker `tmpdir` marker is a regular file. It exercised the unmodified embedded verifier, in-memory compilation of all seven embedded Python blocks, the parent-RED/candidate-GREEN modeled source/install control, exhaustive modeled refusal paths, and retention lifecycle controls. No actual maker, diagnostic, child build, package acquisition, registration, store initialization, request/body, full/provider/browser/P4, or SWAP WAL/recovery action was run.

## Byte and block checks

All embedded blocks match candidate-to-live after installation. `STORE_PY` and `STORE_VERIFY` retain their protected hashes; `STORE_BUILD` is the sole changed production block relative to the live preimage, as reviewed:

| block | candidate/live SHA-256 | result |
| --- | --- | --- |
| `STORE_PY` | `0889b24010e67bd31f28f5efbaec37fed43adf1a0d5ebe8c4fcd57a8248ca50c` | exact |
| `STORE_VERIFY` | `f7c7ebcc26221958ce24e36025faad167c6015a2889202752d267e03d5eda209` | exact |
| `STORE_BUILD` | `a3d9b63f5b99ce4e3ae5b72be93e5140000f99dc4e50e954a00777e420d09409` | exact candidate/live |
| `STAGING_INVENTORY` | `4c98ffcf6de7bd0314cc0e4790d4ffaeb206c03fb905f143e013cc57f631c6f1` | exact |
| `RELOCATE` | `cf189024a79d12481c0629d3815c794c805dcd3fb4de6e9c3640ec242693cd98` | exact |
| `PROVENANCE_SCRIPT` | `6ab4e64766e6df6996035fdf984b3c50efa169ffa982c5f4df6633964a0781cf` | exact |
| `DIST_METADATA_SCRIPT` | `54ea91773be42a9f5a513cb10cc1706ab89d2c061a0d0a4c3ba2c392153b8d67` | exact |
| `IDENTITY_SCRIPT` | `05f8c82c7ea9b28f6f12ac8cad3557a08b0885e455ee22719c9e3ddebc3ccf77` | exact |

Protected live sources remain exact: `bench_store.py` `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2`, `verify_dependency_seed.py` `116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2`. D131 reserves remain `5905580032` normal-child bytes and `8589934592` runtime/diagnostic bytes. Default-off retention and registration barriers are covered by the 29-test control suite and unchanged outside the reviewed maker block.

## Provenance note and limits

The review JSON records candidate tree `7952f3e9e155320720664ea9d151fe79114bd6`, which is malformed at 38 characters and does not equal the commit-resolved 40-character tree `7952f3e9e15532072066474ea9d151fe79114bd6`. The exact candidate commit, maker hash/size/mode, author manifest, and independent review maker hash all agree; this metadata discrepancy is recorded and no source hash mismatch was found.

Actual retained-layout acceptance remains `UNVERIFIED / EXACTMISSING`. Real child acceptance is not claimed: the Store input is absent and the unchanged 8 GiB runtime/diagnostic admission is unavailable. Typecheck is N/A because no configured Python mypy/pyright baseline exists and no product TypeScript changed.
