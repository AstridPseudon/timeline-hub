# D139a combined guarded kit installation

Result: `PASS_INSTALL_COMBINED_WITH_ACCEPTANCE_LIMITS`.

## Exact installation

The worktree was the authorized exact source commit
`0921ec1c8eb7cab668203963c5a5eeb0e4616c00`, tree
`577a3cca4e23c94d051e839eb47d7b1bd7a1c9c3`. The joined source review was
`PASS_SOURCE` with 63/63 source controls; the independent request-carrier
review was `PASS_PRIVATE_SOURCE_CONTROLS_REAL_CHILD_NOTRUN` with 5+33+6
focused controls. Both reviews were read before installation.

Maker installation used the approved command and route:

```text
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
SOURCE_CHECKOUT=/home/user/work/wt/rt-OPS-D139a-combined-CAS-install-2309
TMPDIR=/tmp/d139a-install-controls
D137_DECISION=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-D139a-combined-CAS-install-2309/evidence/d137-decision.json
bash ops-child-custody/install-prep/apply-reviewed-maker.sh
```

Result: PASS. Maker target is the exact candidate
`fd83c9e2017f75fb0d76a2d633d4a63aed090df37c4d7417b03152e7a4fc22b5`,
111171 bytes, mode 0755. Backup is
`make-child-venv.20261025T231036Z.bak`, the exact f07 preimage, 75541 bytes,
mode 0755. Existing backups were not changed. Protected helper hashes remained
`123bb93c…7adfe2` and `116b4e6…d7bfe2`.

Before wrapper replacement, the approved generic helper was run against
private fixtures for wrong preimage, symlink destination, and existing-backup
no-clobber controls. All three refused as expected.

The reviewed wrapper was installed with `install_atomic.py` copy/rename under
`.request-child-venv.install.lock`, after exact source and bdda preimage checks.
Result: PASS. Target is the exact candidate
`60d2238a748cb21789db5f35174a5186609fc511496701e1327e946fa0412504`, 18066
bytes, mode 0755. Backup is
`request-child-venv.20261025T231055Z.bak`, the exact bdda preimage, 15435 bytes,
mode 0755. No wrapper target drift or lock remained.

The checker target was initially absent. It was installed exactly once using
the approved helper's O_EXCL/O_NOFOLLOW copy into the owned receiving
directory under `.check-child-imports.install.lock`; no backup was needed.
Result: PASS. Target is the exact 8215 checker, 14033 bytes, mode 0755.

## Post-install commands

| Command/control | Result |
| --- | --- |
| `bash -n` on installed maker and wrapper | PASS |
| Installed maker embedded Python compile, seven blocks | PASS 7/7 |
| Installed maker serialized shell smoke: nonzero 17 and timeout 124 | PASS; exact statuses, private stderr mode 0600, bounded public marker |
| Read-only installed schema admission using genuine `/home/user/work/venv-agent/.../banodoco_timeline_schema-0.0.2.dist-info` | PASS; 18 RECORD rows, 12 hashed, `tree_tie=UNAVAILABLE` |
| Exact installed wrapper private queue/parser suite, 5 tests | PASS 5/5 |
| Exact installed checker canonical CLI with Agent 2149 census | Expected exit 1; PASS diagnostic: 1146 rows, 12 missing canonical names, 12 failures, 0 missing installed distributions |
| Installed target/protected helper/backup regular-file, single-link, mode, hash and byte readback | PASS |
| `git diff --check` | PASS; source worktree unchanged |

The serialized maker smoke deliberately did not initialize Store, create a
venv, acquire packages, request a child, or mutate a live queue. Consequently
full Store rollback cleanup and real-child acceptance remain unverified.

## Scope limits

No package acquisition, real child/venv, Store/registration, provider,
browser, Farm, D130, render, production acceptance, or publication ran.
Publication remains the manager/lead's normal hub-sync responsibility. The
D137 fixture decision remains genuine `WITHDRAWN` / `NOTRUN` with
`e2e_pass=false`.
