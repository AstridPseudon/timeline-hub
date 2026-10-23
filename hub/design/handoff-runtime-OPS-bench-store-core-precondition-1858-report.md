# OPS-bench-store core precondition 1858 — BLOCKED combined acceptance

Source packet exported; product diff is empty. No DONE marker. No installation, real bench changes, queue edits, Git mutations, dependency writes, installed permission changes, or production tests. Core has no chmod, /proc scanning, copying or quarantine. Dedicated-store migration only: unknown existing benches/registrations stay protected and their space is NOT reclaimed by this change.

## Delivered

Updated shared interface before 3 minutes: durable managed eviction rolls forward and really deletes payload plus exact owned registration projections/index before the separate creation callback. Creation failure rolls back only the new creation to its post-eviction baseline. Pending journals block all ordinary API operations; recovery validates journal projection authority before mutation. Tests kill actual processes at journal/projection/index/deletion/publication boundaries.

Fixed policy is latest two per component PLUS all leases. A new tuple may coexist with two older leased tuples when the fixed 8 GiB reserve is available; released superseded entries are reaped on the next ensure policy transaction. Same-key creators serialize and build once. Stable lock identity, cross-component dependency leases, canonical content keys/paths, ownership markers and registration hashes are validated. Directory-FD deletion never follows symlinks. Public signatures and 1854 callable-registration/extensions are retained; the old 1854 source basename is an identical compatibility copy for adapter fixtures. Payload is fsynced before publication.

The stopped 1854 worker had STOPPED/exit/ended and no running marker; its branch remained 2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d. Neither stopped core worker exported source or committed WIP, and their TMPDIRs were recycled. Their log has only the API document. Thus there was no saved implementation to rewrite; this implements the settled interface, including the corrected policies. Root initialization is explicit and never adopts an existing directory.

## Exact checks and results

With D=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design and TMPDIR=/tmp/w-978846aa6c, from this assigned worktree:

- `python3 -I "$D/handoff-runtime-OPS-bench-store-core-precondition-1858-test-core.py"` — PASS, 20 tests in 1.849s. Actual old payload incarnation/path/rows/env gone before callback; statvfs free bytes increase at least 32 KiB for a 64 KiB payload; failed build retains completed eviction; latest2 plus leases; exact projection rollback; killed-process recovery; reserve refusal; duplicate creator serialization; path/symlink/forged marker/index/journal/registration/lock controls.
- `python3 -I "$D/handoff-runtime-OPS-bench-store-leases-1850-test-leases.py"` — PASS, 21 tests in 7.698s on final exported core. Actual staged test-run seam covers setup lease, descendants, SIGKILL/parent death, timeout/cancel, two-component leases, acquisition/eviction race, unchanged cache/slot/source guards. No sockets or real suites.
- `python3 -I "$D/handoff-runtime-OPS-bench-store-core-precondition-1858-validate.py"` — PASS. Runs `bash -n` on the four staged creator shell scripts and staged test-run; scoped `py_compile` on core, core fixture and both adapter fixtures with all bytecode in TMPDIR; `cmp` core versus 1854 compatibility copy; `git -C /home/user/work/runtime status --porcelain`, `git diff --check`, and `git status --porcelain`, all clean/empty.
- `cmp /tmp/w-978846aa6c/bench_store.py "$D/handoff-runtime-OPS-bench-store-core-precondition-1858-bench_store.py"` — PASS.
- `python3 -I "$D/handoff-runtime-OPS-bench-store-creators-1850-test-adapters.py"` — BLOCKED/exit 1. Real staged requester -> exact dispatcher branch -> maker -> core: three runtime calls passed (creation, same-tree reuse, changed Agent/backend retaining true origin). Child call reached readonly sealing, then rename refused with PermissionError. Logs retained. Two tiny fresh fixture runs were used to expose the original creation exception when rollback also failed; refused paths were never retried or permission-modified.

An earlier core fixture compared only inode numbers and hit immediate filesystem inode reuse for new metadata. Corrected to compare (device, inode, ctime_ns) while retaining old-path/registration deletion and free-byte assertions; no behavior expectation was removed or weakened. Final 20-test run above passed.

## Blocker and limits

The child adapter deliberately seals its entire stage read-only before core publication, as required by its existing custody verifier. This sandbox denies renaming that read-only stage into entries, and rollback also cannot unlink files within its read-only nested directories. The core truthfully reports both errors and leaves an explicit creation journal pending. It never reports success. No chmod or retry workaround was attempted. The source also requires deletion permissions inside an owned sealed bench for eviction: production readonly deletion remains UNVERIFIED and may require an authorized trusted-owner mechanism. This is evidence of an unresolved interface/environment constraint; this packet does not relax readonly verification or the no-chmod restriction.

No combined child creator PASS, no production installation/real-bench reclamation claim, no migration of existing legacy benches, no full suite. Public C0v2 and frozen34e wire/product files were untouched (assigned worktree HEAD 2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d, empty tracked/untracked diff/status). The fixed 8 GiB reserve matches the service's heavy-run floor; it does not estimate unknown future installer size. Stable tiny lock files and retired-name metadata are retained, never old bench trash.

## Handoff

Core/source/interface/fixture/validation plus SHA256 manifest: `handoff-runtime-OPS-bench-store-core-precondition-1858-*` in design; identical core at the 1854 adapter import basename. Reports/logs also in this worker folder. Current total TMPDIR footprint is under 20 MiB; permanent packet is under 5 MiB. Adapter sources belong to their original workers and were not edited.

Next: orchestrator dispatch independent Luna review immediately, focusing on transaction/deletion authority and readonly publication/deletion. Resolve the permission boundary through the authorized owner before rerunning the child adapter fixture or installing anything. Re-run source fixture + creator/lease caller proofs after any authorized fix. No module-only DONE claim and no merge request.
