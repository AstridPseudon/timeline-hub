# Receiving note — OPS inventory maker installation

Do not dispatch the live installer from this preparation. First receive the
single genuine Agent E2E result, then obtain an independent result review.
There is no duplicate E2E and no alternate route.

```text
OPS inventory maker install gate

E2E1800: PASS|NOTRUN|FAIL — result path/hash: <...>
Independent result review: PASS|HOLD — reviewer/result: <...>
Candidate: c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e / 69516 bytes / 0755
Preimage required: 0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39 / 68351 bytes / 0755
Protected helpers: bench_store.py 123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2;
  verify_dependency_seed.py 116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2
Admission: normal reserve >=5905580032; source floor >=4600000000; stop line >=4000000000
Decision: INSTALL|HOLD — D125b remains binding unless both PASS gates are attached.
```

## Exact post-gate action

From the prepared Composition checkout, set `ORCH` to the approved
orchestration root and `SOURCE_CHECKOUT` to the clean physical checkout at
`09ed4999741b822fba7e8b3033ca28db6bcf8fa1`, then run exactly:

```sh
ORCH=/approved/orch/root \
SOURCE_CHECKOUT=/approved/composition/checkout \
bash ops-child-custody/install-prep/apply-reviewed-maker.sh
```

The command refuses a source/hash/mode/owner/symlink/hardlink mismatch, a dirty
checkout, a missing protected helper, an occupied backup name, or a changed
installed preimage. It performs no alternate action on refusal. On success,
record the backup path and exact target/helper readback before the manager
dispatches the normal child-venv route.

The production caller remains the installed `make-child-venv` through the
normal dispatcher route. No C0 protocol or trust change is part of this
installation preparation; C0 request/reply shapes remain as already settled.
