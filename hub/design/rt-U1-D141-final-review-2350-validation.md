# U1 D141 validation

## Identity and scope

- Reviewed commit: `24107e83b096264e59f64ed5bd65e00650567f22`.
- Parents in actual order: `0ca306dfd3cf4e21976271cc4b2e779b10e025b0`, then `fa9cd5464a8b37b02f971de375e56be846cd69e2`.
- Both parents are ancestors of the reviewed commit.
- Merge-base: `dbcdb97c50afc72bd5e2599cb7ead0fe56bc7c4f`.
- `git diff --name-status 0ca306dfd3cf4e21976271cc4b2e779b10e025b0 24107e83b0` has exactly six paths, identical to the frozen upstream patch path set.
- `git diff --check 0ca306dfd3cf4e21976271cc4b2e779b10e025b0 24107e83b0` passed.
- Worktree was clean; no unmerged index entries or conflict-marker additions were found.

## Functional receipt

No test body or full suite was rerun by this independent review. The authentic author receipt was read and hash-checked:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-D141-final-join-2345/evidence/targeted.xml`
- Receipt SHA-256: `c059937a1d50375b5e8cf39c4ce0ab636dd9e7b8696b2c9e11b7d082001a1653`.
- XML summary: 119 tests, 0 errors, 0 failures, 0 skipped, 21.171 seconds (reported as 21.18 seconds).
- The six current committed file SHA-256 values match `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-U1-D141-final-join-2345/evidence/source-manifest.json`.

## Static and predicate evidence

- Author in-memory compile: PASS for all six changed Python files.
- Author scoped Ruff: 93 inherited diagnostics; no new diagnostics claimed and no fixes applied.
- Author Pyright: 432 baseline diagnostics to 428 final diagnostics; zero new diagnostics.
- Current final delta introduces no skip/xfail markers and no conflict markers.
- Four targeted test modules preserve every base test; `/home/user/work/wt/rt-U1-D141-final-review-2350/tests/test_task_storage_estimate.py` adds only the two intended reserve tests.
- The protected client/schema/generated/pin set is byte-identical; all non-six paths are unchanged.

## Storage behavior reviewed

- `/home/user/work/wt/rt-U1-D141-final-review-2350/runtime_protocol/store.py:2865` uses `storage_preflight` for admission and passes the task estimate.
- `/home/user/work/wt/rt-U1-D141-final-review-2350/runtime_protocol/store.py:3904` validates task/capability estimates, reads live free bytes, applies the default one-GiB reserve from `/home/user/work/wt/rt-U1-D141-final-review-2350/runtime_protocol/storage.py`, and returns `insufficient_storage` without a reclaim command.
- `/home/user/work/wt/rt-U1-D141-final-review-2350/runtime_protocol/store.py:3979` repeats the same storage admission at claim time.
- `/home/user/work/wt/rt-U1-D141-final-review-2350/runtime_protocol/service.py:5594-5598` carries the production request estimate into Runtime storage admission.
- The estimate model uses the intended current opaque-JPEG/alpha-PNG selection, Runtime-owned inputs, 1.10 allowance, and one-GiB free-space reserve.

## Disk disclosure

The only disk witness used was `df -BG`, which reported rounded `5G` free space. The precise byte start was unavailable; this review does not invent a precise >=5GB witness and did not rerun an underfloor test.
