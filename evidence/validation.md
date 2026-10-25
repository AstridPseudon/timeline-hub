# D137 installed source custody validation

## Result

Installed integrity: **PASS**. Source custody: **PASS**. Acceptance remains
**UNVERIFIED**; the authorized D137 decision remains `WITHDRAWN / NOTRUN` for
the fixture E2E gate. No production request or acceptance is inferred.

## Read-only checks

The live target is a regular single-link mode `0755` file of 75,503 bytes and
SHA-256
`4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36`. It
matches `ops-child-custody/make-child-venv` from commit
`0c4170e42d2ff435ea855a54c940299619f6a285`, whose tree is
`b43a840b75bf895f9789732c56585175c4b367bf`, byte-for-byte.

The retained backup is a regular single-link mode `0755` file of 68,351 bytes
and SHA-256
`0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39`. It
matches the reviewed preimage source at commit
`9428f515fcd8dccaef26193438b3ac89f903f5aa`, byte-for-byte.

Protected live helper hashes match the required pins: `bench_store.py`
`123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2` and
`verify_dependency_seed.py`
`116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2`.

Exact checks run in this review:

```text
read-only Git/source/target/backup/helper comparison: PASS
bash -n /tmp/.../orch/bin/make-child-venv: PASS
in-memory compile of 7 embedded Python blocks: PASS
git diff --check: PASS
```

The installed receipt's normal CAS, identity, lock, no-clobber, atomic
replacement, helper readback, and lock-cleanup controls are accepted as
`PASS_INSTALL` evidence; they were not rerun. The independent source/security
review's 44 controls plus one real Store cleanup-boundary control, and the
installed logging receipt's two cases, are reused as directed; no Store,
fixture, child, or production body was started here.

## Boundaries and decision

The public evidence contains no private stderr payload, authentication data,
or raw diagnostic output. No live write, process probe, normal hub
publication, Git mutation, credential access, second installation, or product
edit occurred. D130 remains held. Agent receiving and its one real request do
not depend on this optional parallel receipt check.

Installer receipt SHA-256: `a75fe7c5f9b7c7e1f2829d4eeb1fcfbd463008b6366b8cfe69d2723f42da4785`.
Installer report SHA-256: `aead9740885172a4926551eb2846c4ab43d4150946a8dd77209386c11389bf7c`.
