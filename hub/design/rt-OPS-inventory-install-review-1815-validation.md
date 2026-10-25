# OPS inventory installation-prep independent security review

Result: `FAIL_SOURCE_SECURITY`.

The exact candidate and receiving preimage are conserved: candidate
`c3226b93…`, 69,516 bytes, mode `0755`, from source commit
`09ed4999741b822fba7e8b3033ca28db6bcf8fa1`; expected preimage
`0857a5e0…`, 68,351 bytes, mode `0755`, from parent commit
`9428f515fcd8dccaef26193438b3ac89f903f5aa`. Read-only inspection of the
actual1656 installation and independent1659 review agrees with those values.
Protected `bench_store.py` (`123bb93c…`) and
`verify_dependency_seed.py` (`116b4e6…`) were read-only and unchanged.

## Required checks

Executed in a private `/tmp/w-0388168f05/rt-OPS-inventory-install-review-1815`
area. No live ORCH/bin, Store, package, permission, provider, socket, E2E, or
D130 path was used.

```text
bash -n ops-child-custody/install-prep/apply-reviewed-maker.sh
PASS

bash -n ops-child-custody/make-child-venv
PASS

PYTHONDONTWRITEBYTECODE=1 python3 -B ops-child-custody/install-prep/dry_run_controls.py
PASS: private candidate match, wrong-preimage refusal, no-clobber backup,
helper invariance, and shape guards

/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/install-prep/dry_run_controls.py
PASS (All checks passed)

PYTHONDONTWRITEBYTECODE=1 python3 -B <in-memory AST/compile check>
PASS: controls AST plus 7 maker embedded Python blocks

<in-memory hash/tree conservation check>
PASS: exact candidate/preimage hashes, sizes, Git modes, and trees

git diff --check
PASS
```

The original 40 tests were not repeated: the touched candidate source is the
installer/runbook/control package, and no product maker source changed. The
existing author validation already records 40/40 for the preparation package.

## Blocking findings

- `F1`: `apply-reviewed-maker.sh:72-74,86-88` uses predictable temporary names
  with check-then-`cp`; destination symlink replacement can redirect writes.
- `F2`: `apply-reviewed-maker.sh:16-17,33` validates `ORCH` but not physical,
  owned `ORCH/bin` and `ORCH/backups` parents, allowing path redirection.
- `F3`: `apply-reviewed-maker.sh:82-91` has a TOCTOU window between the final
  digest and rename, so it is not descriptor/identity-bound CAS.
- `F4`: `apply-reviewed-maker.sh:91-97` may report `REFUSED` after replacing
  the target, and helper readback omits shape/owner/mode/link checks.
- `F5`: `apply-reviewed-maker.sh:62-63` trusts caller-controlled `TMPDIR`
  without physical/ownership/separation checks.

Additional limits are recorded as `F6` (source checkout ownership is stated
but not enforced) and `F7` (D125b E2E/independent gates are procedural only).
The private runner does not model these races, parent path redirects, or
post-replacement helper shape changes; its own replacement copy is also
check-then-copy.

## Gate and scope limits

Agent E2E1800 is still pending and independent result review is required after
that E2E. D125b therefore remains binding. This review does not qualify a live
install, child acceptance, Store initialization, package acquisition, or any
production write. No alternate route was attempted after the finding.
