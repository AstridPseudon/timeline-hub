# Runtime full `30033` classification

## Result

The completed artifact `runtime-full-restore-integration-1020181908-30033`
ran against target `integration:runtime` with suite
`full-restore-integration`. The service request was recorded at
`2026-10-20T18:19:08Z`; its immutable snapshot records Runtime tree
`a0f8c953d9cc046c2ab5a9f9926bc0dd6e547e5d` and snapshot key
`66daf8e4585d4b75ac69f91f84abbdb5`. That tree resolves in the captured
Runtime checkout to commit
`7e160c5d254a9b3d42a28672a2d7e2ac1acd5ca8`.

The post-snapshot external tuple recorded by the service is Agent
`6f0cdc7df95fe3c9b2d491d6fcb39b754fa212bd`, App
`ed48d92d2a8bb8d9f013060e420eba646d88ace4`, and Composition
`5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`. The Runtime source includes the
current merged batch `WAV4ec`, `script285`, `markeracd`, `generatorcc`,
`PCMfixture2ef`, and `observer7e`. Private `952`, carrier, `RT07cut`, and
visibility branches are excluded. This classification is bounded to the
service snapshot; later source changes are not relabeled as snapshot evidence.

| Result | Count |
|---|---:|
| Passed | 5524 |
| Failed | 7 |
| Skipped | 18 |
| Xfailed | 18 |
| Warnings | 12 |
| Pytest duration | 573.93s (0:09:33) |
| Service elapsed | 576s |
| Exit | 1 |

The service ran:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
```

## Comparison with the previous manager full

The previous manager full `runtime-full-restore-integration-1020160931-14898`
was `5515 passed / 7 failed / 18 skipped / 18 xfailed`. The current result is
`+9` passed with no change to the failure, skip, or xfail counts. All seven
current failure node IDs are exactly the established baseline cohort: six
Runtime boundary nodes and one zero-shim boundary node. Therefore this is
**PASS with the known baseline**, with **0 new failure nodes**.

The raw default full remains RED (exit 1); this is not an all-green result and
does not close an all-green gate.

## Failure cohort

The seven failures are unchanged from the prior baseline:

| Failure node | Classification and trace |
|---|---|
| `tests/test_runtime_boundary.py::test_token_signal_exit_race_uses_only_retained_child_exit` | Known baseline. Linux cleanup reaches `process.returncode` on `_CustodyChild`, which has no `returncode`. |
| `tests/test_runtime_boundary.py::test_unverifiable_live_owner_retains_cleanup_uncertainty` | Known baseline. Same Linux cleanup/test-double `returncode` `AttributeError` before the expected `BootstrapError`. |
| `tests/test_runtime_boundary.py::test_primary_start_error_retains_cleanup_uncertainty_as_cause` | Known baseline. The primary `OSError("ready reply failed")` is followed by the same cleanup/test-double `returncode` `AttributeError`. |
| `tests/test_runtime_boundary.py::test_unowned_handle_does_not_infer_termination_from_poll` | Known baseline. Same Linux cleanup/test-double `returncode` `AttributeError` before the expected sole-reaper refusal. |
| `tests/test_runtime_boundary.py::test_runtime_spawn_retains_owner_and_wires_escrow_before_seal` | Known baseline. The fake custody-broker path did not raise the expected `RuntimeCustodyLaunchUncertain`. |
| `tests/test_runtime_boundary.py::test_retained_stop_owner_reclaims_release_before_term_kill_and_positive_wait` | Known baseline. Linux cleanup reaches `process.returncode` on the fake `Child`, which has no `returncode`. |
| `tests/test_zero_shim_boundary.py::test_start_does_not_inject_checkout_into_child` | Known baseline. The mocked identity first raises `KeyError: 'pid'`; cleanup then reaches the same fake-process `returncode` `AttributeError`. |

The concrete follow-up cohort remains the existing Linux custody/fake-process
boundary group, especially the cleanup access at
`runtime_protocol/platform.py:698` and the custody identity setup. Keep these
seven nodes as the known baseline until a separately authorized Runtime fix
and full result resolves them. No product change or full rerun is requested
by this classification.

No storage-floor exception or resource evidence appears in the artifact. No
test expectation was weakened, skipped, deleted, or rewritten.

## Scope and pin safety

This worker read the request, snapshot, external tuple, summary, status, and
completed log only. It did not run local tests, request another suite, mutate
integration, change product code, write shared dependencies, or alter the
public generated-client producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
(`0.2.13`). No historical pin is moved.
