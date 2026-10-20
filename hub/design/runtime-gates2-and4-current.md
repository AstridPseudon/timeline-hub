# Runtime M2 Gate 2 and Gate 4 proof

Date: 2026-10-20

## Source

- Runtime base: `86ce14f` (`tl/rt-m2-gates2-and4-parallel-proof-track`), with the focused door-admission regression below.
- Runtime proof snapshot used by the central test service: `183dbcf45a6b3a25f7437415df10100101ef8bbd`.
- Actual Agent provider checkout: `/home/user/work/agent`, `d30894a7abfa6e3163c13a59175b4a0d298c7fea`.
- Shared environments were referenced read-only. The TypeScript check used the existing `/home/user/work/app/node_modules/typescript` path; no dependency or cache files were changed.

## Changes

- Added Runtime-owned suite entries `gate2-atomic-integration` and `gate4-door-integration` to `ORCH/tests/suites.conf`; all prior lines remain unchanged.
- Added `test_real_door_commit_admission_checks_origin_auth_and_project_scope` to `tests/test_timeline_commit_integration.py`. It exercises a real `/v1` commit through the browser door, rejecting foreign origin, browser bearer credentials, and route/body project mismatch without writes before accepting the valid request.

## Gate 2: `gate2-atomic-integration`

Exact command:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m "not darwin_native and not live" tests/test_timeline_commit_execution.py tests/test_timeline_commit_acceptance.py::test_atomic_acceptance_exact_recorder_projection_and_same_content_edge tests/test_timeline_commit_acceptance.py::test_identical_retry_after_restart_and_head_advance tests/test_timeline_commit_acceptance.py::test_changed_payload_and_publication_only_cas_refuse_without_writes tests/test_timeline_commit_acceptance.py::test_invalid_prepared_values_are_atomic tests/test_timeline_commit_acceptance.py::test_failure_after_receipt_rolls_back_every_row tests/test_timeline_commit_acceptance.py::test_failure_between_projection_steps_rolls_back_and_restart_retry_publishes_once tests/test_timeline_commit_acceptance.py::test_complete_recorder_roundtrip_and_replay_after_restart tests/test_timeline_commit_integration.py::test_real_move_rebases_disjoint_clip_and_conflicts_on_same_clip tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary
```

Result on the proof snapshot: **50 passed in 23.88s**.

Evidence includes concurrent same-key waiters and different-key CAS races, stale-head rebase versus real conflict through the installed Agent provider, crash before and after acceptance durability (the parameterized commit/restore boundary cases), exact retry after restart/head advance, changed-payload refusal, and rollback/no duplicate revision or event assertions.

## Gate 4: `gate4-door-integration`

Exact command:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m "not darwin_native and not live" tests/test_timeline_commit_routes.py tests/test_http_response_lock.py tests/test_door_transport.py::test_admission_order_host_origin_and_route tests/test_door_transport.py::test_browser_credentials_are_refused tests/test_door_transport.py::test_preflight_allows_listed_request tests/test_door_transport.py::test_preflight_refusals tests/test_timeline_commit_integration.py::test_real_door_commit_admission_checks_origin_auth_and_project_scope tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider tests/test_timeline_commit_acceptance.py::test_real_provider_two_projects_keep_local_ids_and_commit_authority_isolated tests/test_generated_client.py::test_generated_client_smoke_and_scoped_handshake tests/test_generated_client.py::test_acquisition_selected_python_renderer_parity tests/test_client_parity.py::test_product_clients_match_canonical_contract_projection tests/test_client_parity.py::test_recoverable_snapshot_client_projection_is_canonical && cd packages/typescript && PATH=/home/user/work/app/node_modules/typescript/bin:$PATH npm test
```

Result on the proof snapshot: **29 Python tests passed in 16.01s; TypeScript generated-client suite 61 passed, 0 failed**.

Evidence includes normal `/v1` commit transport, origin and browser-credential rejection, route/body project scope, two-project isolation through the real provider, response-lock behavior, lost-ack exact idempotency, Python generated-client/parity checks, and the generated TypeScript client build/typecheck/tests.

## Gaps and next steps

- Gate 2’s concurrent race tests exercise the Runtime commit coordinator with a prepared provider; the real Agent-provider integration covers rebase/conflict, crash recovery, and retry, but there is not yet a simultaneous two-request HTTP-door race using the real Agent provider.
- No full suite, render suite, or separate browser/e2e suite was requested or run. The Gate 4 door tests are the required Runtime transport coverage.
- No external blocker remains for these two current proof results.
