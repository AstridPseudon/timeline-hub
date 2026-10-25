# D137 guarded CAS installation validation

## Result

`PASS_INSTALL` at the exact reviewed source `cf80cfcb918ee9e311a294fb7291ad5e11c48d0b` / tree `363a551a00e9dc081da9760e21a6383296135c06`.

The reviewed candidate `f07b80937dde807d9aa5dad1deed278d831e7f56fb3810708e955926b45b969f` (75,541 bytes, mode 0755) replaced the exact target preimage `4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36` (75,503 bytes, mode 0755). The target and new backup are regular, non-symlink, single-link files. The prior `0857a5e0…` backup was not changed.

## Guarded installation

Exact command:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch SOURCE_CHECKOUT=/home/user/work/wt/rt-OPS-D137-shell-CAS-install-2110 TMPDIR=/tmp/w-9ba5e4b855 D137_DECISION=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-D137-shell-CAS-install-2110/evidence/d137-decision.json bash ops-child-custody/install-prep/apply-reviewed-maker.sh
```

Result: exit `0`, `PASS: candidate installed with CAS preimage, no-clobber backup, atomic replacement, and helper readback`.

The route preserved the reviewed descriptor identity CAS, `O_EXCL|O_NOFOLLOW` reservations, no-clobber backup, atomic rename, and readback. The receiving lock was absent after completion. New backup:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/backups/make-child-venv.20261025T211101Z.bak`, SHA-256 `4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36`, 75,503 bytes, mode 0755. Protected helper hashes remained `123bb93c…` and `116b4e6…`.

## Post-install checks

- `bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-child-venv` — PASS.
- Existing `SourceCallerTests.test_store_cleanup_boundary_keeps_nonzero_and_timeout_evidence`, run with `test_custody.MAKER` set to the live installed target — PASS, 1 test with both nonzero and timeout cases.
- The smoke read the installed target bytes directly, materialized its exact serialized `STORE_CONTEXT`, and exercised the existing bounded `Store.ensure` cleanup control. It did not use a source extraction or a helper superset.
- In-memory compile of all 7 embedded Python blocks from the installed target — PASS.
- Candidate-to-target `cmp` — PASS.
- Backup-to-parent-preimage `cmp` — PASS.
- Target/backup/helper mode, ownership, regular-file, single-link, and SHA-256 readback — PASS.
- `git status --porcelain --untracked-files=all` on the source checkout before install — clean.

## Limits and acceptance

The D137 fixture E2E gate is explicitly `WITHDRAWN` / `NOTRUN`, with `e2e_pass=false`; no E2E or production acceptance claim is made. No child/core request, package acquisition, whole-make run, Farm run, full suite, or Agent next request was performed here. Publication was not performed by this worker, so `publication_ready=false`; the installed hash is recorded for the manager's normal publication and receipt handoff.
