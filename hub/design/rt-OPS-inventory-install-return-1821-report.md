## Report

Implemented the private installer first return for F1–F7.

- Added descriptor-bound `O_EXCL|O_NOFOLLOW` copies and identity-checked atomic rename.
- Added receiving lock, parent/source/TMPDIR ownership and physical-shape checks.
- Added exact D125b gate artifact verification.
- Added honest `INSTALLED_BUT_UNVERIFIED` postcommit state.
- Expanded private controls for race, CAS, symlink, hardlink, preimage, and no-clobber cases.
- Preserved candidate maker hash: `c3226b...e7142e`.

Validation passed:

```text
bash -n .../apply-reviewed-maker.sh                         PASS
ruff check --no-cache ops-child-custody/install-prep/*.py   PASS
Python AST parse                                             PASS
git diff --check                                             PASS
dry_run_controls.py                                          PASS
Private installer replica route                              PASS
```

No live install, full suite, Agent E2E, Store initialization, package acquisition, or production write was performed.

D125b remains HOLD because genuine E2E1800 and independent review artifacts are still pending.

Evidence written to the requested `evidence/` files. Commit message written to the requested path; `DONE` marker created.