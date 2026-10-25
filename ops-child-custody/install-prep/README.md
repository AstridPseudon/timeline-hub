# OPS inventory maker installation preparation

This is a preparation package only. It does not install anything, initialize a
Store, acquire packages, write permissions, or touch `ORCH/bin`. The live
command below is manager-only and is eligible only after both gates in the
receiving note are satisfied:

1. `agt-OPS-inventory-E2E-receive-1800` reports the one genuine candidate E2E
   as PASS.
2. An independent result review accepts that result.

Until then, D125b holds the install. No alternate route is permitted.

## Exact inputs

| input | value |
| --- | --- |
| reviewed source commit | `09ed4999741b822fba7e8b3033ca28db6bcf8fa1` |
| candidate SHA-256 | `c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e` |
| candidate bytes/mode | `69516` / `0755` |
| installed preimage SHA-256 | `0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39` |
| installed preimage bytes/mode | `68351` / `0755` |
| protected `bench_store.py` | `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2` |
| protected `verify_dependency_seed.py` | `116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2` |
| normal child reserve | `5905580032` bytes |
| runtime/diagnostic reserve | `8589934592` bytes |
| source floor / stop line | `4600000000` / `4000000000` bytes |

The candidate is extracted from the exact source commit into a fresh private
`TMPDIR` directory. The source checkout must be physical, clean, and owned by
the invoking user. The target, candidate, backup, and temporary replacement
must each be regular, non-symlink, single-link files owned by that user and
mode `0755`.

## Manager-only live command

Run from this checkout only after the two gates above. `ORCH` must be the
already approved orchestration root and `SOURCE_CHECKOUT` must resolve to the
reviewed Composition checkout. This script is intentionally not run by this
worker.

```sh
ORCH=/approved/orch/root \
SOURCE_CHECKOUT=/approved/composition/checkout \
bash ops-child-custody/install-prep/apply-reviewed-maker.sh
```

The script performs, in order:

1. source commit, clean-checkout, regular-file, owner, mode, byte, and hash
   checks; source extraction is private and does not chmod the source checkout;
2. target regular-file/symlink/hardlink/owner/mode checks and exact preimage
   CAS (`0857a5e0…e57b6d39`); protected helper checks;
3. timestamped backup creation with an existing-path refusal and byte/mode
   readback;
4. immediate pre-replacement CAS recheck and same-directory atomic rename of
   a candidate temporary; and
5. target and protected-helper byte/mode/hash readback plus `cmp`.

A guard failure exits immediately. It must not retry, use an alternate
installer, initialize or reuse a Store, send a child request, change a daemon
or permission file, or enter D130 SWAP/WAL.

## Private offline controls

The control creates a fresh replica below `TMPDIR`, materializes the exact
parent and candidate bytes from Git, and exercises the route without reading
or writing the live ORCH tree:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B ops-child-custody/install-prep/dry_run_controls.py
```

It must report PASS for candidate match and atomic replacement, wrong-preimage
refusal, no-clobber backup refusal, helper invariance, and symlink/hardlink
shape guards. It does not claim the Agent E2E or a live installation.

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

E2E1800: PASS|NOTRUN|FAIL — result path/hash: <...>
Independent result review: PASS|HOLD — reviewer/result: <...>
Candidate: c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e / 69516 bytes / 0755
Preimage required: 0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39 / 68351 bytes / 0755
Protected helpers: bench_store.py 123bb93c…7adfe2; verify_dependency_seed.py 116b4e6…d7bfe2
Admission: normal reserve >=5905580032; stop line >=4000000000; source floor >=4600000000
Decision: INSTALL|HOLD — D125b remains binding unless both PASS gates are attached.
```
