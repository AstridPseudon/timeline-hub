# OPS D137 installed custody review

Verdict: **PASS**. This is a post-install receipt and byte-custody review, not
a new permission gate for an already-authorized normal Agent received-kit
request.

## Exact identity

- Source commit: `cf80cfcb918ee9e311a294fb7291ad5e11c48d0b`.
- Source tree: `363a551a00e9dc081da9760e21a6383296135c06`.
- Source, installed target, and candidate hash: `f07b80937dde807d9aa5dad1deed278d831e7f56fb3810708e955926b45b969f`, 75,541 bytes, `0755`, regular single-link file.
- Required backup: `backups/make-child-venv.20261025T211101Z.bak`, hash `4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36`, 75,503 bytes, `0755`, regular single-link file.
- The receiving lock is absent after readback.
- `STORE_PY`, `STORE_VERIFY`, `bench_store.py`, and `verify_dependency_seed.py` match the protected hashes.

## Receipt review

Consumed the exact permanent evidence from source/security worker
`rt-OPS-D137-shell-security-review-2103` and installer worker
`rt-OPS-D137-shell-CAS-install-2110`. Their receipts agree on source commit,
tree, candidate, preimage, protected helpers, manager-only CAS route, and the
withdrawn/`NOTRUN` fixture gate. The installer receipt records descriptor-bound
lock, no-follow/no-clobber backup, identity CAS, atomic rename, helper
readback, and lock cleanup. No publication or production acceptance claim is
made.

The public caller is the dispatcher’s `CHILDVENV` branch:
`prov CHILDVENV make-child-venv`, which invokes the installed shell from
`orch/bin/make-child-venv`. No alternate caller was inferred.

## Checks run

```text
bash -n <installed target>                                      PASS
in-memory compile of seven embedded Python blocks                PASS
in-memory compile of nested retention helper                    PASS
source/installed/backup/protected identity and mode reconciliation PASS
bounded installed-byte Store smoke                              PASS
```

The bounded smoke used temporary private roots only, the installed shell’s
serialized stage functions, and the read-only installed `bench_store.py`. It
covered a nonzero stage (`17`) and timeout (`124`), retained private stderr at
`0600`, preserved exit status, removed staging, kept payload out of the public
failure marker, and created no Store entry. It did not create a production
child, acquire packages, register a Store entry, or touch the installed kit.

The source diff from the supplied base contains only the intended
`STORE_CONTEXT` closure export. Fullv2/C0 sections 1–7 wire fields and the
Composition contract/schema/generated surfaces were not touched. PLAN §3 F
was respected: no broad/full suite, fixture whole-make, provider/core, Farm,
D130, browser, live-socket, or production request was run.

## Limitations

This proves installed-byte custody and bounded shell/Store failure handling.
It does not claim fixture E2E, production acceptance, Store registration,
publication, or a full suite; the owner’s fixture gate remains withdrawn and
`NOTRUN`.
