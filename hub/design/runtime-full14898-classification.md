# Runtime full `14898` classification

## Result

The completed artifact `runtime-full-restore-integration-1020160931-14898`
targeted `integration:runtime`. Its exact Runtime source was commit
`6ab3243972f8dc49105819e6d7ba7aef1a2888b8`, tree
`c225a680c645c67c3fe1f43b5e564b2a77a05d80`; the snapshot key was
`234cd8b43da0e24a87be6e48dacae3d5`. The external source record was Agent
`f133a87986d839d7716d3efac2c2ba25fe036098`, App
`a04f90cf60eac69a5079f0ab03188abcbd1571fc`, and Composition
`5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`.

The exact source includes catalog promotion `81f8c7e0`, selected-media CAS
`a51af88`, catalog text `9f211fc`, and native clip `6ab3243`. It excludes the
unmerged audio, ordinary014, carrier, and strict-marker patches.

| Result | Count |
|---|---:|
| Passed | 5515 |
| Failed | 7 |
| Skipped | 18 |
| Xfailed | 18 |
| Warnings | 12 |
| Pytest duration | 684.66s (0:11:24) |
| Service elapsed | 687s |
| Exit | 1 |

The summary command was:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
```

## Failure classification

The seven current failure nodes are exactly the established baseline cohort.
There are **0 new failure nodes** and no other failure to classify.

| Failure node | Classification from the raw log |
|---|---|
| `tests/test_runtime_boundary.py::test_token_signal_exit_race_uses_only_retained_child_exit` | Known baseline. Linux `platform._stop_linux_tree` reaches `process.returncode` on `_CustodyChild`, which has no `returncode`. |
| `tests/test_runtime_boundary.py::test_unverifiable_live_owner_retains_cleanup_uncertainty` | Known baseline. Same Linux cleanup/test-double `returncode` `AttributeError` before the expected `BootstrapError`. |
| `tests/test_runtime_boundary.py::test_primary_start_error_retains_cleanup_uncertainty_as_cause` | Known baseline. Same Linux cleanup/test-double `returncode` `AttributeError` while preserving the primary `OSError` scenario. |
| `tests/test_runtime_boundary.py::test_unowned_handle_does_not_infer_termination_from_poll` | Known baseline. Same Linux cleanup/test-double `returncode` `AttributeError` before the expected sole-reaper refusal. |
| `tests/test_runtime_boundary.py::test_runtime_spawn_retains_owner_and_wires_escrow_before_seal` | Known baseline. The fake custody broker path did not raise the expected `RuntimeCustodyLaunchUncertain`. |
| `tests/test_runtime_boundary.py::test_retained_stop_owner_reclaims_release_before_term_kill_and_positive_wait` | Known baseline. Linux cleanup reaches `process.returncode` on the fake `Child`, which has no `returncode`. |
| `tests/test_zero_shim_boundary.py::test_start_does_not_inject_checkout_into_child` | Known baseline. The mocked identity first raises `KeyError: 'pid'`; cleanup then reaches the same fake-process `returncode` `AttributeError`. |

The baseline designation is supported by the prior untouched-main targeted
proof and repeated completed full results recorded in
`design/runtime-baseline.md`; the node IDs match exactly. This classification
does not weaken, skip, delete, or rewrite any test expectation.

## Gate interpretation and non-results

The raw default full remains **RED**. “0 new” means no regression nodes were
introduced relative to the known baseline; it does not mean the suite is green
or that a gate passed. No private-floor result is used as gate proof. The
request/snapshot/extension/summary/log contain no storage-floor exception or
resource evidence, so no storage exception is attributed; the raw run remains
RED for the seven baseline failures.

This worker analyzed only the completed request, snapshot, extension record,
summary, and log. No test request, full rerun, targeted rerun, product/test
change, shared-dependency write, or new skip was made.
