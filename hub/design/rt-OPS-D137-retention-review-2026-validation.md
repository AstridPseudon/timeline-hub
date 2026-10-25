# D137 independent focused final review

Verdict: **PASS_SOURCE_SECURITY**. Acceptance remains **UNVERIFIED** because
the D137 fixture E2E gate is owner-withdrawn and remains `NOTRUN`.

## Source and scope

Reviewed source commit `0c4170e42d2ff435ea855a54c940299619f6a285`, tree
`b43a840b75bf895f9789732c56585175c4b367bf`, and
`ops-child-custody/make-child-venv` SHA-256
`4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36`,
75,503 bytes, mode `0755`, single link.

The change is limited to the D137 stderr handoff, its focused tests, and the
candidate/install pins. `STORE_PY` and `STORE_VERIFY` are byte-identical to
the parent at hashes `0889b240…8ca50c` and `f7c7ebcc…da209`. The protected
`bench_store.py` and `verify_dependency_seed.py` hashes are exactly
`123bb93c…7adfe2` and `116b4e6b…d7bfe2`, with mode `0755` and one link.
No schema, owner, RECORD, inventory, trust, public protocol, D130, or M5
change is present.

## D137-001 review

The original independent-2013 blocker was retained once, as `D137-001`, and
is resolved in this candidate. `run_stage` redirects each producer command's
stderr to the stage file, preserves the exact command return status, and
`failure()` calls the private handoff before writing the bounded public marker
or returning to `Store.ensure`. The handoff writes only to the maker-owned
`tests/provision-stderr/<request>.<stage>.*` route.

The retained stderr is a regular, owned, single-link file with mode `0600`,
bounded to 1 MiB. Metadata records the full observed byte count, retained
byte count, truncation boolean, and SHA-256 of the complete observed stream;
the public failure marker remains payload-free. Request and stage names are
allowlisted. Source and destination opens use `O_NOFOLLOW`; destination files
use `O_EXCL` and existing records are never clobbered. Forged symlink and
hardlink destinations are refused without modifying the outside sentinel.

The cleanup regression is meaningful: the test constructs the real
`bench_store.Store`, calls real `Store.ensure`, executes the exact extracted
maker `run_stage`/`failure` handoff for both a nonzero stage and a timeout,
then observes the real `_roll` cleanup. It asserts the Store staging directory
is empty while the private retained first stderr remains durable. This is not
a test that merely deletes a stage directory. The outer installed dispatcher
and a real child request were not run, so those remain E2E-unverified.

The 1 MiB test verifies exact retention at the bound and truthful metadata for
`1 MiB + 17` bytes. The nonzero and timeout tests verify exact first stderr,
stage attribution, and status `17` / `124`. No public raw stderr is emitted.

## D137 gates and installer handoff

The gate helper accepts only the exact fields `authorization=D137`,
`fixture_e2e_gate=WITHDRAWN`, `e2e_result=NOTRUN`, `e2e_pass=false`,
`install_route=CAS_MANAGER_ONLY`, `production_install=false`, the candidate
hash/size, an exact 40-hex `source_commit`, and `reviewed_installer=installer1826`.
The reviewed installer binds that source commit through `git archive`, checks
the candidate hash/size and mode, checks the installed preimage
`0857a5e0…e57b6d39` / 68,351 bytes / `0755`, and checks both protected helper
hashes before the descriptor-bound CAS replacement. The route preserves the
no-follow/no-clobber backup, identity CAS, atomic rename, and post-commit
readback gates. The runnable manager-only command is:

```sh
ORCH=/approved/orch/root \
SOURCE_CHECKOUT=/approved/composition/checkout \
TMPDIR=/approved/private/tmp \
D137_DECISION=/approved/gates/d137-decision.json \
bash ops-child-custody/install-prep/apply-reviewed-maker.sh
```

This review did not run that installer, install the candidate, initialize a
production Store, or issue a request.

## Commands and results

- `TMPDIR=/tmp/w-00fcb0569b PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m unittest discover -s ops-child-custody/tests -v` — **44/44 PASS**.
- Focused `test_store_cleanup_boundary_keeps_nonzero_and_timeout_evidence` — **1/1 PASS**.
- `TMPDIR=/tmp/w-00fcb0569b PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B ops-child-custody/install-prep/dry_run_controls.py` — **PASS**.
- `/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests ops-child-custody/install-prep/*.py` — **PASS**.
- `bash -n ops-child-custody/make-child-venv ops-child-custody/install-prep/apply-reviewed-maker.sh` — **PASS**.
- In-memory compile of 7 embedded Python blocks and 7 Python files — **PASS**.
- Byte comparison of `STORE_PY`/`STORE_VERIFY` against parent — **PASS**.
- `git diff --check 4932c0f8e2e02ce6a203bf41fe014f9c3a7db5fa..HEAD` — **PASS**.
- Private synthetic D137 decision through `verify_gate_artifacts.py` — **PASS**, E2E remains `NOTRUN`.

No full suite, whole-make fixture, browser/live socket, credentials,
acquisition, production request, or live installation was run.
