# OPS-bench-store core projection 1915 — independent Luna review

## Verdict

**SOURCE PASS (scoped). COMBINED FAIL / UNQUALIFIED / NO INSTALL.**

The staged core is a coherent, byte-preserving extension of frozen1858 for the
fixed `tests/provision/<validated-name>.txt` report projection and for
conservative leasing of a genuine unmanaged suite row. This is source/private
evidence only. It does not qualify the creator/child combined path, readonly
publication/deletion, installation, HOST, or the test service.

## Evidence reviewed

- Final core source SHA256: `88ae9e5af3425639b7eba0b79aa6b84e78a319fe810c0c6a2d3ceece1be8b5f3`.
- Frozen1858 source SHA256: `53d90fb3108b24253a29416214ec5fa8f69402f50a515f0399b7464ec39a2e14`.
- The packet hash manifest passed (`9/9` packet files); its 35 frozen input hashes passed, including the immutable1858 source and the unchanged1850 lease seam.
- Runtime assigned and integration worktrees are clean at `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`; `git diff --check` passed.
- Staged Python compilation passed for core, both test files, lease seam, and validator. `bash -n` passed for the four creator wrappers and the lease test-run wrapper.
- Creator1912 statically declares exact verified `.provision-report` bytes as `report`, calls `store.ensure(..., report)`, and verifies persisted fixed-path bytes/receipt fields. Lease1918's caller seam remains `names_for_suite(...)` followed by `acquire(names)`; this is compatibility evidence only, not combined behavior.

## Test results

Commands used private writable TMPDIR `/tmp/w-2921f440f8/rt-review-1923`; no
readonly or combined fixture was run.

```text
python3 -I -B handoff-runtime-OPS-bench-store-core-projection-1915-test-projection.py
PASS: 15 tests, 0.847s, exit 0

python3 -I -B handoff-runtime-OPS-bench-store-core-projection-1915-test-core.py
RED: 17 PASS / 1 FAIL, 18 tests, 1.509s, exit 1
```

The projection suite covers exact UTF-8/CRLF bytes, reuse and empty/absent
compatibility, fixed-path ownership/type/hash/collision/tamper controls,
owned-only eviction, held retention, creation/eviction crash recovery, and
the custom unmanaged suite case. The custom case returned both registered
managed names and held both real inherited flock leases; missing/tampered
managed rows refused. Unknown legacy benches were not adopted.

The preserved core RED is
`test_reclamation_is_real_before_callback_and_failure_preserves_eviction`.
Its `any(...st_ino == old_inode...)` assertion requires an inode number never
to reappear anywhere under the store. A bounded private probe against the
staged source showed `old_path_exists=False`, no matching path for the old
payload inode, and no pending eviction journal before the failing build; the
assertion's inode identity is therefore an OS allocation expectation, not a
reclamation failure. Preserve the RED and the test unchanged. This is a
small worker-owned test-expectation correction for the manager to route; do
not skip, xfail, or weaken it in this review. No orchestrator disposition is
needed for this ordinary defect.

The packet validator was invoked after seeding its documented private patch
replay target with frozen1858 `bench_store.py`:

```text
python3 -I -B handoff-runtime-OPS-bench-store-core-projection-1915-validate.py
exit 1: all packet/source/caller/hash assertions through “Runtime assigned +
integration clean” passed, then the validator referenced the absent historical
worktree `/home/user/work/wt/rt-OPS-bench-store-core-projection-1915`.
```

This is a packet path/staging mismatch, not a Runtime diff: the current review
worktree and `/home/user/work/runtime` both independently passed clean status,
diff-check, and the expected HEAD check; patch replay plus `cmp` passed.

## Boundaries and next steps

No product source, tests, generated files, schemas, pins, benches, queues,
configs, installations, network, HOST, chmod, denied-path retry, cleanup, or
full/gate suite was run or changed. D21c tuple-keying and D25 triage policy
remain acknowledged. The original readonly EACCES/pending disposition remains
the blocker to any combined qualification. A later authorized run must use the
exact pinned Agent SHA + backend SHA + client tuple, after the inode test
expectation is corrected without weakening reclamation assertions and after
the permission stop is resolved.
