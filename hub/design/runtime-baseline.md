# Runtime M0 Linux baseline

Runtime main snapshot: tl/integration `8c1830d1ca64a3934c37611a28ffe8db7df879ea`. Shared dependencies-only environment: `/home/user/work/venv-runtime` (Python 3.13.16). Worker installed the test extra dependencies from pyproject/README without installing its disposable worktree. Run from a Runtime worktree, selecting that worktree source; no Agent or renderer dependency was installed. No product changes or baseline fixes. All listed failures occurred on the unchanged main snapshot (worker HEAD = base 8c1830d, git diff/status clean); none are introduced by a Timeline port. They were not separately reproduced in another main checkout because it would be the same source.

## Required default lane — RED, recorded

From `/home/user/work/wt/rt-m0-env`:

```bash
/home/user/work/venv-runtime/bin/python -m pytest -q -n 2
```

Completed captured run: **3391 passed, 9 failed, 18 skipped**, 12 warnings, 320.31s, exit 1. `/tmp/rt-m0-default.log`.
Another completed run of the same default lane (setsid wrapper): **3392 passed, 8 failed, 18 skipped**, 12 warnings, 247.48s, exit 1. `/tmp/rt-m0-default-setsid.log`. The door audit case passed in this run; the other eight failures repeated. These were baseline diagnostics, not fixes, and neither run is green.
Default collection: 3418/3463 tests selected, 45 deselected by main's `not integration and not darwin_native and not live` lane. All 18 runtime skips report native Windows APIs. The 45 integration/darwin_native/live cases were only collected, not executed. No macOS or live coverage claimed.

Failures, exactly:

- `tests/test_door_transport.py::test_audit_lines_without_credentials` (first captured run only): expected three audit entries immediately after responses, saw two. Intermittent across completed runs; scheduling/audit-completion race is a hypothesis, not a proven fix.
- `tests/test_runtime_boundary.py::test_token_signal_exit_race_uses_only_retained_child_exit`
- `tests/test_runtime_boundary.py::test_unverifiable_live_owner_retains_cleanup_uncertainty`
- `tests/test_runtime_boundary.py::test_primary_start_error_retains_cleanup_uncertainty_as_cause`
- `tests/test_runtime_boundary.py::test_unowned_handle_does_not_infer_termination_from_poll`
- `tests/test_runtime_boundary.py::test_retained_stop_owner_reclaims_release_before_term_kill_and_positive_wait`
  These five reach Linux `platform._stop_linux_tree` with test child doubles lacking `returncode`. This establishes the failing Linux fixture/cleanup interaction, not that weakening production process ownership is safe.
- `tests/test_runtime_boundary.py::test_runtime_spawn_retains_owner_and_wires_escrow_before_seal`: expected `RuntimeCustodyLaunchUncertain`, did not raise on this Linux path. Requires review of intended platform behavior/fixture before any fix.
- `tests/test_second_client_e2e.py::test_second_client_core_journey_is_executable`: `npm ci --ignore-scripts --no-audit --no-fund` in packages/typescript exits 226. Test captures npm output, so pytest traceback does not establish installation vs concurrency cause. Do not claim a client protocol failure or green TS journey.
- `tests/test_zero_shim_boundary.py::test_start_does_not_inject_checkout_into_child`: attempts default `/root/.local/state/astrid-runtime/logs`, denied read-only filesystem. Sandbox writable XDG_STATE_HOME is a plausible targeted rerun prerequisite, not a source fix already performed.

## Required door/lock/idempotency coverage — PASS

```bash
/home/user/work/venv-runtime/bin/python -m pytest -q -n 2 \
  tests/test_door_*.py tests/test_http_response_lock.py tests/test_idempotency_compaction.py
```

**1332 passed in 41.47s**, exit 0, `/tmp/rt-m0-target.log`. The passing run includes the intermittent audit case. Manager independently checked collection from integration at the same SHA: **1332/1333 selected (1 deselected)**. Breakdown: door_chat 16, door_lifecycle 18, door_routes 1276, door_transport 16, http_response_lock 3, idempotency_compaction 3. These prove main transport only; no new commit route exists yet, so gate 4 extension is not claimed.

## Existing generated-contract checks — PASS

Design worker rt-m0-contract ran, all exit 0:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python generators/generate.py --check
node tools/generate_typescript_conformance.mjs --contract contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json --component-manifest contract/component-manifest.json --fixture-root conformance/fixtures --check
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check
```

No changed wire/client implementation or new atomic-acceptance/renderer-off/App-journey proof is claimed. No TS package suite was separately completed by this manager.

## Worker process note

rt-m0-env started redundant full-suite diagnostics after mistaking asynchronous tool/process namespace visibility for pytest termination. Completed logs above contain trustworthy pytest summaries; partial ongoing runs provide no additional aggregate claim. Orchestrator confirmed it stopped the redundant worker and its pytest descendants outside sandbox, preserved logs/worktree and released its heavy slot. Serial/supervised partial runs were interrupted and supply no completed result. Runtime manager authored this reviewed baseline from the completed logs; the terminated worker has no final report. No further broad baseline rerun is needed for M0. Any interrupted later diagnostic is not a success. Baseline failures remain recorded for narrow follow-up under authorized milestone work.

## M1 merged full result — 2026-10-19T20:59Z

Central runtime-full-1019194117-7355, final tree28f8877e1c97e03a9fb79a199f2c8738a8dc5eea (integration82df3cf), command `/home/user/work/venv-runtime/bin/python -m pytest -q -n 3`: **3693passed37failed18skipped**,12warnings,147.42s. Exact37nodes/tracebacks in tests/runtime-full-1019194117-7355/log.txt; no new full submitted. This is RED, not a gate-complete claim. All new commit/acceptance/input/door/client/contract tests pass in this default lane; real Agent integration tests remain separately proven5+10, not run by default selection.

Failure classification after reading actual tracebacks:
-22 historical-fixture failures: realm-admission5/operator-upgrade3/spec-dedup1/spec-reference1/workspace-adopt12. Helpers build CURRENT v31 then relabel25–28 without removing4new history/input tables and2new parent columns; strict historical admission correctly refuses them. New rt-m1-schema-fixture-fix owns authentic old-layout fixture repair (existing test_runtime_upgrade.py walk-back already does it), preserving ALL safety/manifest/rollback/source-unchanged assertions. No production admission relaxation.
-7 restore regressions in test_shot_composition_runtime.py: kept old endpoint calls lack required publication guard; one generated method fails Python signature first, six service calls fail strict body validation. Current Agent provider explicitly reports unsupported_operation 'restore adapter is not installed'; restore is M2 backlog. Original restore behaviour expectations remain unchanged/RED and must be restored through sole provider/path plus exact-head-pair callers during M2. No old writer fallback, assertion deletion, or M1 restore-complete claim.
-1 installed wheel probe: ALL wheel members/exactsourcebytes/WORKER_SCOPES pass, child origin assertion fails because central PYTHONPATH=$snapshot leaks into installed subprocess. rt-m1-wheel-isolation makes probe truly isolated while retaining origin/source/byte assertions; no product import change.
-7 old-name baseline failures persist:6 runtime_boundary Linux test-double/launch cases listed above +zero_shim start-does-not-inject. Current zero_shim now reaches incomplete fake identity (missingpid) instead of the earlier sandbox log permission failure; underlying product/test files unchanged from8c1830d. No claim same traceback. Original audit race and npm second-client failure pass in this central outside-sandbox run. Main-only baseline not rerun.

Test-only worker branches remain held until App frozen tuple proof is released; no Runtime product/ABI/schema change intended. Initial dispatch names rt-m1-legacy-fixtures and rt-m1-wheel-probe were refused (relative brief path), no worker/source ran; replaced by absolute-path requests rt-m1-schema-fixture-fix and rt-m1-wheel-isolation. No new full until a later reviewed batch justifies it.
