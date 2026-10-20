# Runtime current86 corrected full result

## Verdict

The manager-requested corrected run is **baseline-only red**, not a product pass:
it completed the full suite and has exactly the seven established baseline failure
node IDs from `old30033`. There are no new assertion failures and no new
environment failures in this result.

The run was the single authorized central run:
`runtime-full-retained-owned-temp-integration-1020212001-21387`. No additional
full, native, render, dependency, or Git operation was performed.

## Run identity and command

- Requested base/source: Runtime `86ce14f144a740d9002d8758f952bdb4324847d8`
  (`current integration86ce14f`).
- Central snapshot: tree `c3333a08dbb09d51ee4fedd8c7ec455775374315`, key
  `1419e05162aec3ee4293fcddf20cdc5a8`.
- External tuple: Agent `a8a40afd37e5560a14fa5e1a09ace6018596793e`, App
  `8c0e1f799b64e9b6f179018b7dff01479d43c85c`, Composition
  `4f325f1e14f03a3418f04bd81b3635c810a40cf`.
- Service command:

  ```text
  env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-full-temp-retain-all-final/runtime-full-retained-temp.py -- /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
  ```

- The Runtime configuration has `tmp_path_retention_policy = "failed"`.
- The real storage floor was used; it was not overridden.
- The owned retained root was `/tmp/rt-full-084lgh1w`.

Result: **7 failed, 5540 passed, 18 skipped, 18 xfailed, 12 warnings** in
432.35s (service elapsed 433s), exit 1.

## Failure comparison

`old30033` reported 7 failed / 5524 passed / 18 skipped / 18 xfailed. Its seven
failure node IDs are unchanged below. `old8649` reported 36 failed / 5409
passed / 18 skipped / 18 xfailed / 92 errors; its extra failures and errors
were storage-floor environment effects, not evidence against this product
source.

| Current failure node | Classification | Evidence in corrected run |
|---|---|---|
| `tests/test_runtime_boundary.py::test_token_signal_exit_race_uses_only_retained_child_exit` | Existing baseline | Linux cleanup reaches `process.returncode` on `_CustodyChild`; the fake has no `returncode` (`runtime_protocol/platform.py:709`). |
| `tests/test_runtime_boundary.py::test_unverifiable_live_owner_retains_cleanup_uncertainty` | Existing baseline | The same fake-process `returncode` `AttributeError` occurs before the expected `BootstrapError`. |
| `tests/test_runtime_boundary.py::test_primary_start_error_retains_cleanup_uncertainty_as_cause` | Existing baseline | The primary `OSError("ready reply failed")` is followed by the same cleanup `AttributeError`. |
| `tests/test_runtime_boundary.py::test_unowned_handle_does_not_infer_termination_from_poll` | Existing baseline | The same cleanup `AttributeError` occurs before the expected sole-reaper refusal. |
| `tests/test_runtime_boundary.py::test_runtime_spawn_retains_owner_and_wires_escrow_before_seal` | Existing baseline | The fake broker path did not raise the expected `RuntimeCustodyLaunchUncertain`. |
| `tests/test_runtime_boundary.py::test_retained_stop_owner_reclaims_release_before_term_kill_and_positive_wait` | Existing baseline | Linux cleanup reaches `process.returncode` on the fake `Child`, which has no `returncode`. |
| `tests/test_zero_shim_boundary.py::test_start_does_not_inject_checkout_into_child` | Existing baseline | The mocked identity first raises `KeyError: 'pid'`; cleanup then reaches the same fake-process `returncode` `AttributeError`. |

The current log's final `FAILED` list is byte-for-byte the same node cohort as
`old30033`. No current failure has a new node ID, assertion message, or
environment cause. The current platform line moved from 698 in `old30033` to
709 with the source snapshot, but the failure mechanism is unchanged.

## Storage and retention classification

The retention correction prevented the passed-realm accumulation seen in
`old8649` for this run. Evidence:

- `old8649` contains 239 log-line matches for `storage estimate would cross the
  free-space floor` / `insufficient_storage`, and ended with 92 errors.
- The corrected current log contains no `storage estimate would cross`,
  `insufficient_storage`, `free-space floor`, or `available_bytes` matches.
- The corrected run completed all tests with 5540 passes and kept the owned
  retained root at 49M (`du -sh /tmp/rt-full-084lgh1w`).
- The retained root contains the expected failed/diagnostic temporary material
  (including the seven baseline boundary cases and xfailed legacy cases), not
  an accumulating set of passed realms. No storage setting was overridden.

This is evidence that the retention policy fixed the environment failure mode;
it does not convert the seven known boundary failures into passes.

## Decisions and next steps

- Classify this result as **known baseline failures; no new failure**. Do not
  relabel it green.
- Keep `old8649` classified as environment-invalid because of its storage-floor
  exhaustion, not as a product pass.
- No product edit or rerun is warranted from this result. The existing Runtime
  owner follow-up remains the seven-node custody/process-identity boundary
  cohort, especially the fake-process cleanup contract in
  `runtime_protocol/platform.py` and the custody identity setup. Any repair and
  full verification require a separately authorized run.

## Evidence command

The central waiter used was:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test runtime-full-retained-owned-temp-integration-1020212001-21387
```

It returned exit 1 with the result above. No local test suite was run by this
worker.
