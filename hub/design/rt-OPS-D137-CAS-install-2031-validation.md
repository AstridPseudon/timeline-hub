# D137 guarded CAS installation validation

## Decision and route

The manager-supplied decision is the physical, regular, single-link file
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-D137-CAS-install-2031/evidence/d137-decision.json`.
It records `authorization=D137`, `fixture_e2e_gate=WITHDRAWN`,
`e2e_result=NOTRUN`, `e2e_pass=false`, `install_route=CAS_MANAGER_ONLY`,
`production_install=false`, source commit
`0c4170e42d2ff435ea855a54c940299619f6a285`, candidate
`4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36`, and
`reviewed_installer=installer1826`.

The only live command was:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch \
SOURCE_CHECKOUT=/home/user/work/wt/rt-OPS-D137-CAS-install-2031 \
TMPDIR=/tmp/rt-OPS-D137-CAS-install-2031.aeMRVD \
D137_DECISION=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-D137-CAS-install-2031/evidence/d137-decision.json \
bash ops-child-custody/install-prep/apply-reviewed-maker.sh
```

Result: `PASS: candidate installed with CAS preimage, no-clobber backup,
atomic replacement, and helper readback` (exit 0). The normal request status
boundary had no provisioning entries and no receiving lock before invocation.

## Exact postinstall checks

- Target `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-child-venv` is a regular, non-symlink, single-link, owner `0:0`, mode `0755`, 75,503 bytes, SHA-256 `4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36`.
- New backup `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/backups/make-child-venv.20261025T203242Z.bak` is a regular, non-symlink, single-link, owner `0:0`, mode `0755`, 68,351 bytes, SHA-256 `0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39`.
- `cmp` candidate-to-target: PASS. Backup matches the required preimage: PASS. No-clobber backup and atomic identity-CAS route: PASS.
- `bench_store.py`: SHA-256 `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2`, 43,403 bytes, mode `0755`, single link: unchanged/readback PASS.
- `verify_dependency_seed.py`: SHA-256 `116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2`, 52,731 bytes, mode `0755`, single link: unchanged/readback PASS.
- `bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-child-venv`: PASS.
- In-memory `ast.parse`/`compile` of five installed Python payloads (`RETAIN_STAGE_STDERR`, `STORE_PY`, `STAGING_INVENTORY`, `RELOCATE`, `STORE_VERIFY`): PASS.
- Isolated installed logging control: PASS for nonzero and timeout cases; retained stderr and status were checked without Store initialization, child request, package acquisition, or fixture E2E.
- Receiving lock cleanup: PASS; `.make-child-venv.install.lock` absent after the successful installation.
- Independent reviewed handoff controls: `PASS_SOURCE_SECURITY`; 44 controls reused from `rt-OPS-D137-retention-review-2026` and installer1826 review. No full suite was run or requested.

## Limits

The fixture E2E gate is withdrawn, so this evidence does not claim E2E PASS,
production acceptance, a production request, or hub publication. The install
receipt is ready for separate manager/lead publication only.
