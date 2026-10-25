# Validation

Prior review was read from `workers/rt-OPS-inventory-install-review-1815/evidence/review.json`.
Its original `FAIL_SOURCE_SECURITY` remains recorded. No live destination was
used.

## Static and scoped checks

```text
bash -n ops-child-custody/install-prep/apply-reviewed-maker.sh                 PASS
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/install-prep/*.py
                                                                            PASS (All checks passed!)
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B - <<'PY' ... AST parse ... PY
                                                                            PASS (3 install-prep Python files)
git diff --check                                                               PASS
```

The protected candidate remains SHA-256
`c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e`; no
candidate maker, verifier, existing tests, or protected helper was edited.

## Private controls

```text
TMPDIR=/tmp/w-faa5e10967/rt-OPS-inventory-install-return-1821-tmp \
PYTHONDONTWRITEBYTECODE=1 python3 -B ops-child-custody/install-prep/dry_run_controls.py
PASS: private candidate, preimage, no-clobber, descriptor race, identity CAS, helper, symlink, and hardlink controls
```

The controls use fresh private replicas only. They cover positive replacement,
wrong preimage, no-clobber backup, adversarial symlink reservation for backup
and replacement, changed-target identity refusal, helper invariance, symlink
shape, hardlink shape, and private TMPDIR ownership/boundary.

## Private installer route

The route was run once against a disposable ORCH replica, a private TMPDIR,
the frozen clean Composition checkout, and synthetic gate artifacts. This is
route evidence only; the synthetic gates do not qualify D125b or Agent E2E1800.

```text
E2E_RESULT=<private gate JSON> INDEPENDENT_REVIEW=<private review JSON> \
ORCH=<private replica> SOURCE_CHECKOUT=/home/user/peteromallet/timeline-composition \
TMPDIR=<private TMPDIR> bash ops-child-custody/install-prep/apply-reviewed-maker.sh
PASS: exact E2E and independent review gates accepted
PASS: candidate installed with CAS preimage, no-clobber backup, atomic replacement, and helper readback
target=c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e
backup=0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39
helpers=123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2,116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2
```

Private shell refusals also passed for missing gate artifact, wrong preimage,
protected-helper symlink, target symlink, target hardlink, and a pre-created
receiving lock. No full suite, live install, Agent E2E, package acquisition,
Store initialization, child request, or production write was run.
