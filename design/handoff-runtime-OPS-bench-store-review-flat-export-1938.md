# Runtime OPS-bench-store flat export 1938

Documentation-only BYTEEXACT publication from the completed worker reports.
No source, proof rerun, integration merge, or tracked deletion was performed.

## Exported files and provenance

| Destination | Exact source path | Or commit / source revision | Bytes | Lines | SHA-256 | `cmp` |
| --- | --- | --- | ---: | ---: | --- | --- |
| `design/handoff-runtime-OPS-bench-store-core-test-review-1937.md` | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-bench-store-core-test-review-1937/handoff-runtime-OPS-bench-store-core-test-review-1937.md` | Runtime2a9 base `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` | 1,310 | 22 | `877da8e709bdb3d7e884fb18376c916efab7af90fe970da7b819a87ad14b51d0` | PASS |
| `design/handoff-runtime-OPS-bench-store-leases-custody-review-1935.md` | `tl/rt-OPS-bench-store-leases-custody-review-1935:docs/handoff-runtime-OPS-bench-store-leases-custody-review-1935.md` in `/home/user/banodoco/banodoco-workspace-runtime` | branch commit `de1c9da4338385084e005b7bc8486850625a326e` | 3,831 | 66 | `c0ce343964ce807b9fc09f971b8cdeb0b5d8924b0321bdbe39a0e2f5606e3d69` | PASS |
| `design/handoff-runtime-OPS-bench-store-core-test-review-1937-summary.md` | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-bench-store-core-test-review-1937/report.md` | worker artifact; review base `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` | 837 | 8 | `247eace663d4fdfebf848c9ccdb97457f815903eb8c0c384afd2921a6d5c33f4` | PASS |
| `design/handoff-runtime-OPS-bench-store-leases-custody-review-1935-summary.md` | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-bench-store-leases-custody-review-1935/report.md` | worker artifact; review base `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` | 1,039 | 21 | `c3c7ad14e8c00d8dec67b8b3f49607ace65f01faf326d25c186fda4ada9c96bd` | PASS |

The two detailed handoffs are copied byte-for-byte from their named sources;
the two `-summary.md` files are likewise exact worker `report.md` copies.
`cmp -s` was run against every source after export and returned success. No
existing destination bytes were present or overwritten.

## Source status and limits

- Export worktree base: `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.
- Source reports preserve the settled combined status: **FAIL / UNQUALIFIED /
  NO INSTALL**; permission1905 remains **STOPPED**.
- Core detailed source: worker artifact, with base/runtime commit recorded above;
  its report records scoped 18/18 core, 1/1 oracle, and 78/78 validator PASS.
- Lease detailed source: historical branch doc, whose branch revision is
  recorded above; it records package-only custody PASS and explicitly says the
  retained 24/24 behavioral result was not rerun.
- No validator, fixture, test suite, Store.ensure, combined-child,
  readonly-publish, delete, HOST, test-service, chmod, denied-path retry,
  cleanup, install, queue, provision, network, Git, product/test/generated,
  or pin action was taken by this export.
