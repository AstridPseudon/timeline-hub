# Runtime S2 post-merge qualification

## Merge identity

- Approved source: `f7081c14efd9a5b834987e7a1e2abf597b66313b`
- Approved tree: `7ab412cc4bcbe517efcfa806e092336390312e18`
- Integration result: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Merge queue result: `merge-rt-m2-release-s2-final-compose` — merged into `tl/integration`.
- Verified integration tree: `7ab412cc4bcbe517efcfa806e092336390312e18` (exact match).

## Requested integration lanes

All lanes were requested against `integration:runtime` after the merge. The commit and TypeScript lanes snapshot the exact tree above; the full lane was queued while that tree was current but started after later integration merges.

| Lane | Result | Evidence |
| --- | --- | --- |
| `full-restore-integration` | fail, but non-qualifying source | `runtime-full-restore-integration-1020112501-27435`: 7 failed, 5491 passed, 18 skipped, 24 xfailed |
| `commit-integration` | pass | `runtime-commit-integration-1020112501-17354`: 9 passed |
| `ts-client-check` | pass | `runtime-ts-client-check-1020112501-16056`: 61 passed, 0 failed |

Commands executed by the central test service:

- Full: `env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -n 3`
- Commit: `env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/test_timeline_commit_integration.py`
- TypeScript: `cd packages/typescript && PATH=/home/user/work/app/node_modules/typescript/bin:$PATH npm test`

The full lane was the one permitted full request for this task. It was queued while the integration branch was correct, but the central service took its snapshot after later integration merges. Its request snapshot and summary both record tree `330ea3969cb9cce77271404f31793c21abd5993f`, not the approved `7ab412cc…`; therefore its failures cannot qualify the approved S2 tree.

## Full-run node classification

The non-qualifying run reported exactly these seven nodes. All seven match the previous baseline node set, but this is not a blanket inheritance: the current run's observed error signatures are recorded below, and the source mismatch blocks using them as approval evidence.

| Node | Observed signature | Baseline relation |
| --- | --- | --- |
| `tests/test_runtime_boundary.py::test_token_signal_exit_race_uses_only_retained_child_exit` | `AttributeError: '_CustodyChild' object has no attribute 'returncode'` | exact baseline node/signature |
| `tests/test_runtime_boundary.py::test_unverifiable_live_owner_retains_cleanup_uncertainty` | `AttributeError: '_CustodyChild' object has no attribute 'returncode'` | exact baseline node/signature |
| `tests/test_runtime_boundary.py::test_primary_start_error_retains_cleanup_uncertainty_as_cause` | `OSError: ready reply failed`, followed by `_CustodyChild.returncode` `AttributeError` | exact baseline node/signature |
| `tests/test_runtime_boundary.py::test_unowned_handle_does_not_infer_termination_from_poll` | `AttributeError: '_CustodyChild' object has no attribute 'returncode'` | exact baseline node/signature |
| `tests/test_runtime_boundary.py::test_runtime_spawn_retains_owner_and_wires_escrow_before_seal` | `DID NOT RAISE RuntimeCustodyLaunchUncertain` | exact baseline node/signature |
| `tests/test_runtime_boundary.py::test_retained_stop_owner_reclaims_release_before_term_kill_and_positive_wait` | `AttributeError: 'Child' object has no attribute 'returncode'` | exact baseline node/signature |
| `tests/test_zero_shim_boundary.py::test_start_does_not_inject_checkout_into_child` | `KeyError: 'pid'`, followed by `FakeProcess.returncode` `AttributeError` | exact baseline node/signature |

The approved-tree full gate is therefore blocked: this worker was limited to one full request, and that request was consumed by a later tree after the integration branch advanced.

## Baseline

Previous Runtime 860 full baseline: `runtime-full-restore-integration-1020095412-22308` — 5194 passed, 7 failed, 18 skipped, 25 xfailed.

Its seven failures are six nodes in `tests/test_runtime_boundary.py` and one in `tests/test_zero_shim_boundary.py`; the current non-qualifying run reported the same seven nodes and signatures.

## Scope and decisions

- No product edits, dependency pins, publication, branch operations, or local full-suite execution were performed.
- The merge was not performed by this worker; the completed queue result and the integration worktree were independently checked.
- The accidental `request-merge --help` probe was refused by the dispatcher and changed no branch or worktree.
- After the merge equality check, `tl/integration` advanced from `2c4ac180`/tree `7ab412cc…` to `129493b2`/tree `330ea396…` through later queued merges. The full-run snapshot followed that later tree, so no approved-tree full qualification is claimed.
