# OPS inventory maker installation preparation

This is a preparation package only. It does not initialize a Store, acquire
packages, write permissions, or touch a production `ORCH/bin`. The command
below is manager-only and refuses unless the machine-readable D137 decision
input is supplied and accepted:

1. The fixture E2E gate is explicitly `WITHDRAWN` and its result remains
   `NOTRUN`.
2. The input binds this candidate and source to the reviewed installer1826 CAS
   route and marks production installation as manager-only.

This substitution does not claim E2E PASS or authorize this worker to install.
No alternate route is permitted. Independent review of this source follows;
the later install worker must receive a fresh manager decision before running
the route.

## Exact inputs

| input | value |
| --- | --- |
| reviewed source commit | exact 40-hex final source commit bound by the D137 decision |
| candidate SHA-256 | `4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36` |
| candidate bytes/mode | `75503` / `0755` |
| installed preimage SHA-256 | `0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39` |
| installed preimage bytes/mode | `68351` / `0755` |
| protected `bench_store.py` | `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2` |
| protected `verify_dependency_seed.py` | `116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2` |
| normal child reserve | `5905580032` bytes |
| runtime/diagnostic reserve | `8589934592` bytes |
| source floor / stop line | `4600000000` / `4000000000` bytes |

The candidate is extracted from the exact source commit into a fresh private
`TMPDIR` directory. `TMPDIR` must be an existing physical directory owned by
the invoking user, not broadly writable, and outside both `ORCH` and the source
checkout. The created extraction root is checked again before extraction. The
source checkout and all of its ancestors must be physical, clean, and owned by
root or the invoking user; the checkout itself must be owned by the invoking
user. `ORCH`, `ORCH/bin`, and `ORCH/backups` must be existing physical
directories owned by the invoking user and not broadly writable. The target,
candidate, backup, and temporary replacement must each be regular,
non-symlink, single-link files owned by that user and mode `0755`.

## Manager-only live command

Run from this checkout only after the D137 decision above. `ORCH` must be the
already approved orchestration root and `SOURCE_CHECKOUT` must resolve to the
reviewed Composition checkout. This script is intentionally not run by this
worker.

```sh
ORCH=/approved/orch/root \
SOURCE_CHECKOUT=/approved/composition/checkout \
TMPDIR=/approved/private/tmp \
D137_DECISION=/approved/gates/d137-decision.json \
bash ops-child-custody/install-prep/apply-reviewed-maker.sh
```

The script performs, in order:

1. exact D137 decision JSON checks, including the withdrawn/NOTRUN E2E state,
   candidate hash, source commit, and manager-only CAS route;
2. source commit, clean-checkout, regular-file, owner, mode, byte, and hash
   checks; source extraction is private and does not chmod the source checkout;
3. target regular-file/symlink/hardlink/owner/mode checks and exact preimage
   CAS (`0857a5e0…e57b6d39`); protected helper checks;
4. an atomic receiving lock, then a second target identity/hash check;
5. timestamped backup creation using an `O_EXCL|O_NOFOLLOW` descriptor-bound
   reservation and copy, with an existing-path refusal and byte/mode readback;
6. candidate replacement creation using the same descriptor-bound reservation,
   followed by an identity-preserving, directory-descriptor-bound atomic rename;
7. target and protected-helper shape/owner/mode/link/hash readback plus `cmp`.

The lock is the approved manager receiving boundary: every allowed receiving
writer must take the same lock. The target device/inode is checked again while
that lock is held and the rename refuses if it differs. An uncoordinated writer
is not an allowed manager route; the installer does not claim to serialize an
out-of-band writer that ignores the receiving boundary.

A guard failure exits immediately. It must not retry, use an alternate
installer, initialize or reuse a Store, send a child request, change a daemon
or permission file, or enter D130 SWAP/WAL. If the atomic rename has committed
but a later readback fails, the script exits with `INSTALLED_BUT_UNVERIFIED`;
that state is not a refusal and must be handed to the manager without retry or
alternate replacement.

The gate verifier accepts only a D137 JSON with `authorization=D137`,
`fixture_e2e_gate=WITHDRAWN`, `e2e_result=NOTRUN`, `e2e_pass=false`,
`install_route=CAS_MANAGER_ONLY`, `production_install=false`, this post-D137
candidate SHA-256/byte count and an exact 40-hex final source commit, and
`reviewed_installer=installer1826`. Missing,
malformed, symlinked, hardlinked, foreign-owned, or broadly writable artifacts
are refused before any receiving-tree write.

## Private offline controls

The control creates a fresh replica below `TMPDIR`, materializes the exact
parent and candidate bytes from Git, and exercises the route without reading
or writing the live ORCH tree:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B ops-child-custody/install-prep/dry_run_controls.py
```

It must report PASS for candidate match and atomic replacement, wrong-preimage
refusal, no-clobber backup refusal, descriptor reservation under adversarial
symlink replacement, target identity CAS refusal, helper invariance, and
symlink/hardlink shape guards. It does not claim the Agent E2E or a live
installation.

## Validation after a qualified live install

The separate installer must record the exact candidate, preimage, backup,
target readback, protected helper hashes, and source commit. It must then run:

```sh
bash -n ops-child-custody/make-child-venv
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v
/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests
git diff --check
```

No product typecheck applies: this preparation has no Python product change
and Composition has no configured mypy/pyright baseline.

## Receiving message template

```text
OPS inventory maker install gate

D137 decision: WITHDRAWN / NOTRUN — decision path: <...>
Candidate: 4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36 / 75503 bytes / 0755
Preimage required: 0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39 / 68351 bytes / 0755
Protected helpers: bench_store.py 123bb93c…7adfe2; verify_dependency_seed.py 116b4e6…d7bfe2
Admission: normal reserve >=5905580032; stop line >=4000000000; source floor >=4600000000
Decision: INSTALL|HOLD — D137 decision input is not E2E PASS and this worker does not install.
```

