# Runtime M2 Gate 2 and Gate 4 proof

Date: 2026-10-21 UTC (restart reconciliation)

## Current disposition and final6ef affected proof

The current Runtime integration is `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree `6abc2f117391de8e7e35c0283f575a002199894d`. It descends from the immutable published Runtime 0.2.14 producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree `d3a290b407fa61e6ab2d476f50c068073f70df00`; the published `all76` artifact set remains byte-identical. Agent adopted that producer in `091aa23ec83ea05ffd3b0115a640230d51c8c429`, tree `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`, and App adopted it in `3be3c116610c4ffdf019cba447464280fd7b8e06`, tree `d030e4b8b41a1d5ec46de1c0c245111cafa7e98a`. Those pins are ancestors of the current integration descendants: Agent `7ab6cbae273f133b3adf2a7bae9f2439f02ce71e`, tree `075339b2c6d5e57c1b0e76754457d053b51edf2c`; App `1557c312b999ddc0a21c1728acbc64052ef6491f`, tree `cf94daef960fe1426f6f50e4000b00c0fc42867e`.

The current Runtime full is `runtime-full-retained-owned-temp-integration-1021035028-28646`: **6002 passed, 26 skipped, 15 xfailed, 12 warnings**, exit 0, on tree `6abc2f117391de8e7e35c0283f575a002199894d`. This is current Runtime evidence, not a new Gate 2/4 targeted run. App's native `timeline.init` activation is separate: App `1557c312` and `real7782` prove the initializer create/init, lost-response, reload/restart, history, and immutable-readback path, not Gate 2/4 or all remaining App publication consumers.

The initial final6ef affected run was **not green**:

```text
rt-m2-gate2-final6ef-affected-http-crash-gate2-final6ef-affected-http-crash-1021004534-27309
Runtime tree d3a290b407fa61e6ab2d476f50c068073f70df00; 7 collected: 5 passed, 2 failed.
```

Its exact command was:

```sh
env ASTRID_RUNTIME_CHECKOUT=$PWD ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6efc8150 PYTHONPATH=$PWD:/home/user/work/wt/agt-pin-6efc8150 PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m "not darwin_native and not live" tests/test_timeline_commit_integration.py::test_real_move_rebases_disjoint_clip_and_conflicts_on_same_clip tests/test_timeline_commit_integration.py::test_real_door_concurrent_disjoint_moves_accept_and_rebase tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary
```

The five passing cases were the concurrent disjoint real-door move and the four parametrized crash cases (commit/restore before/after acceptance), including rollback/no-partial-write assertions. The rebase/conflict and lost-ack selectors failed only at their final baseline assertion because the copied legacy `parent_composition.publish` receipt had expired and compacted to `__runtime_idempotency_result_expired_v1`; this was not a `timeline.commit` expiry or history failure.

The approved successor `da022f252a0f11537e1391f30bb402aeec9349c7`, tree `c3c1e0ddb8efe4a236d9744e8bcdea9220894a4c`, changed only test files and kept all product, generated-client, schema, lock and 76-artifact bytes equal to 95bd. Its named run reran only the two failed selectors:

```text
rt-m2-gate2-final6ef-two-aged-fixtures-gate2-final6ef-two-aged-fixtures-1021005203-2115
env ASTRID_RUNTIME_CHECKOUT=$PWD ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6efc8150 PYTHONPATH=$PWD:/home/user/work/wt/agt-pin-6efc8150 PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m "not darwin_native and not live" tests/test_timeline_commit_integration.py::test_real_move_rebases_disjoint_clip_and_conflicts_on_same_clip tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider
```

Preflight passed and the result was **2 passed in 3.67s**. The fixture helper refreshes only copied legacy receipt timestamps before startup; receipt bodies, accepted rows, history/events, and production expiry guards remain untouched. Thus final6ef Gate2 is green for these **seven affected cases across 27309 + 2115**, not a blanket final6ef 51-case result.

The retained normal Agent `e35ad5e72ed9acc61d659a6b4b9c32d69208ab8d`, tree `a2454c2cb472fa5404289c9f48bb7779d330879e`, against Runtime95 passed **51 in 25.12s** in `rt-m2-gate2-final-main014-current-proof-gate2-final-main014-normal-agent-e35ad5e7-proof-1021002537-14311` (central snapshot tree `e0cb9b7a56b88e0ed6555d930793eaa0f963a34b`). That is historical/parent-source evidence, not final6ef evidence. No full51 or previously passing final6ef node was rerun after restart.

## Current Gate 4 disposition

The retained named door proof `rt-m2-gates2-and4-parallel-proof-track-gate4-door-integration-1020213206-10752` passed **29 Python in 16.01s and 61 TypeScript generated-client tests**, exit 0, on central Runtime snapshot tree `183dbcf45a6b3a25f7437415df10100101ef8bbd`. The exact command is the `gate4-door-integration` line in `ORCH/tests/suites.conf`; it covers the commit-route and response-lock files, door origin/auth/preflight nodes, real commit admission/project-scope and lost-ack nodes, two-project isolation, Python generated-client/parity nodes, and `cd packages/typescript && PATH=/home/user/work/app/node_modules/typescript/bin:$PATH npm test`.

This proves `/v1` route/door admission, origin and browser-credential refusal, project route/body scope, two-project isolation, response-lock behavior, exact retry, and generated Python/TypeScript client contracts within that named scope. Source-diff audit against candidate95bd found only an unselected door-audit assertion change and the added Gate2 concurrency test in the relevant files; selected Gate4 node bodies are unchanged. The result transfers only to the named transport source scope. Its Python source is bound to current b92 and the current full covers that Runtime side; the TypeScript generated inputs changed from 0.2.13 to the published 0.2.14 package, so the **61 TypeScript tests remain historical 0.2.13 evidence**. The current 0.2.14 TypeScript evidence is handled separately by `rt-m2-gate4-main014-ts-evidence-0407`; no current 61-test result is claimed here. Candidate qualification separately records full `31902` (**5,988 passed, 26 skipped, 15 xfailed**) and scoped `5889` (**6 passed in 2.75s**) on the 95bd contract tuple.

## Remaining requirement

No additional Runtime Gate2/4 run is justified by this record. The current integration full is recorded above; the adopted Runtime/Agent/App tuple and the separate App native activation are no longer pending adoption claims. The remaining Gate 2/4 qualification boundary is the current 0.2.14 TypeScript generated-client result owned by task 0407. No browser, render, macOS, owner-film, final ZIP, or coordinated four-product result is claimed here.

The original sections below retain the historical proof snapshot and exact commands for audit; their 2026-10-20 source labels must not be read as public013 or final6ef adoption.

## Source

- Current Runtime integration: `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree `6abc2f117391de8e7e35c0283f575a002199894d`. It contains the approved launcher and Speech merges plus the current Runtime full evidence above.
- Gate2 proof snapshot used by the central test service: `36082cf3701de2328d47855bb4cd37455ef4cf57`.
- Gate4 proof snapshot used by the central test service: `183dbcf45a6b3a25f7437415df10100101ef8bbd`.
- Actual Agent provider checkout: `/home/user/work/agent`, `7ab6cbae273f133b3adf2a7bae9f2439f02ce71e` (tree `075339b2c6d5e57c1b0e76754457d053b51edf2c`).
- Shared environments were referenced read-only. The TypeScript check used the existing `/home/user/work/app/node_modules/typescript` path; no dependency or cache files were changed.

### Current-file binding check

The allow-listed suite lines are still present in `ORCH/tests/suites.conf` at lines 135–137. They retain explicit selected integration nodes and the existing `not darwin_native and not live` filter; no broad/full command replaced them.

- Gate2's selected integration functions have identical AST/source hashes in current `b92d3e7` and the recorded `36082cf` snapshot: `test_real_move_rebases_disjoint_clip_and_conflicts_on_same_clip`, `test_real_door_concurrent_disjoint_moves_accept_and_rebase`, and `test_real_door_lost_ack_restart_exact_retry_never_executes_provider`.
- Gate4's selected integration functions have identical AST/source hashes in current `b92d3e7` and the recorded `183dbcf` snapshot: `test_real_door_commit_admission_checks_origin_auth_and_project_scope` and `test_real_door_lost_ack_restart_exact_retry_never_executes_provider`.
- The current merged file adds only the complementary Gate4 admission node relative to the Gate2 snapshot and the Gate2 concurrency node relative to the Gate4 snapshot; both are named on the appropriate suite line. The current Gate2/Gate4 source selections therefore remain bound to the recorded **51 Python** and the historical **29 Python / 61 TypeScript** evidence without rerunning either suite.
- The later baseline/fixture and boundary changes did not remove transport or custody assertions: current object IDs for `tests/test_timeline_commit_baseline.py`, `tests/precut_realm_fixture.py`, `tests/timeline_commit_film_fixture.py`, `tests/test_runtime_boundary.py`, `tests/test_zero_shim_boundary.py`, `tests/test_door_transport.py`, `tests/test_http_response_lock.py`, and `tests/test_timeline_commit_routes.py` are identical to the proof snapshot. The relevant current-to-proof diff is empty.

## Changes

- Added Runtime-owned suite entries `gate2-atomic-integration` and `gate4-door-integration` to `ORCH/tests/suites.conf`; all prior lines remain unchanged.
- Added `test_real_door_commit_admission_checks_origin_auth_and_project_scope` to `tests/test_timeline_commit_integration.py`. It exercises a real `/v1` commit through the browser door, rejecting foreign origin, browser bearer credentials, and route/body project mismatch without writes before accepting the valid request.
- Added `test_real_door_concurrent_disjoint_moves_accept_and_rebase` to `tests/test_timeline_commit_integration.py`. It captures two independently keyed disjoint moves from one original head, sends simultaneous authenticated real-door `/v1` requests, and uses a test-local barrier around the installed Agent provider's preparation call to prove overlap. It asserts one accepted and one rebased result, both intents in the final document, two unique history/receipt edges, and no duplicate ledger rows.

## Gate 2: `gate2-atomic-integration`

Exact command:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m "not darwin_native and not live" tests/test_timeline_commit_execution.py tests/test_timeline_commit_acceptance.py::test_atomic_acceptance_exact_recorder_projection_and_same_content_edge tests/test_timeline_commit_acceptance.py::test_identical_retry_after_restart_and_head_advance tests/test_timeline_commit_acceptance.py::test_changed_payload_and_publication_only_cas_refuse_without_writes tests/test_timeline_commit_acceptance.py::test_invalid_prepared_values_are_atomic tests/test_timeline_commit_acceptance.py::test_failure_after_receipt_rolls_back_every_row tests/test_timeline_commit_acceptance.py::test_failure_between_projection_steps_rolls_back_and_restart_retry_publishes_once tests/test_timeline_commit_acceptance.py::test_complete_recorder_roundtrip_and_replay_after_restart tests/test_timeline_commit_integration.py::test_real_move_rebases_disjoint_clip_and_conflicts_on_same_clip tests/test_timeline_commit_integration.py::test_real_door_concurrent_disjoint_moves_accept_and_rebase tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary
```

Result on the proof snapshot: **51 passed in 24.39s** (central run `rt-m2-gate2-real-http-concurrent-proof-gate2-atomic-integration-1020213848-10497`).

Evidence includes concurrent same-key waiters and different-key CAS races, stale-head rebase versus real conflict through the installed Agent provider, crash before and after acceptance durability (the parameterized commit/restore boundary cases), exact retry after restart/head advance, changed-payload refusal, and rollback/no duplicate revision or event assertions.

## Gate 4: `gate4-door-integration`

Exact command:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m "not darwin_native and not live" tests/test_timeline_commit_routes.py tests/test_http_response_lock.py tests/test_door_transport.py::test_admission_order_host_origin_and_route tests/test_door_transport.py::test_browser_credentials_are_refused tests/test_door_transport.py::test_preflight_allows_listed_request tests/test_door_transport.py::test_preflight_refusals tests/test_timeline_commit_integration.py::test_real_door_commit_admission_checks_origin_auth_and_project_scope tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider tests/test_timeline_commit_acceptance.py::test_real_provider_two_projects_keep_local_ids_and_commit_authority_isolated tests/test_generated_client.py::test_generated_client_smoke_and_scoped_handshake tests/test_generated_client.py::test_acquisition_selected_python_renderer_parity tests/test_client_parity.py::test_product_clients_match_canonical_contract_projection tests/test_client_parity.py::test_recoverable_snapshot_client_projection_is_canonical && cd packages/typescript && PATH=/home/user/work/app/node_modules/typescript/bin:$PATH npm test
```

Result on the proof snapshot: **29 Python tests passed in 16.01s; TypeScript generated-client suite 61 passed, 0 failed**.

Evidence includes normal `/v1` commit transport, origin and browser-credential rejection, route/body project scope, two-project isolation through the real provider, response-lock behavior, lost-ack exact idempotency, Python generated-client/parity checks, and the generated TypeScript client build/typecheck/tests.

## Gaps and next steps

- Gate 2 now includes a simultaneous two-request HTTP-door race using the real Agent provider. The coordinator-level race tests remain complementary coverage for same-key waiters and different-key CAS behavior.
- No Gate 2/4 full, render, or separate browser/e2e suite was requested or run; the current Runtime full `28646` is recorded above. The Gate 4 door tests are the required retained Runtime transport coverage.
- Gate 4's retained historical result is **29 Python tests passed in 16.01s; TypeScript generated-client suite 61 passed, 0 failed**, on proof snapshot `183dbcf45a6b3a25f7437415df10100101ef8bbd`; it was not repeated on current b92. The current 0.2.14 TypeScript generated-client lane is owned by `rt-m2-gate4-main014-ts-evidence-0407`.
- Retired publication/D04 consumers remain held and are not silently counted as current Gate2/Gate4 coverage. When the held integration-marked public publication tests are ported, the exact deferred allow-list addition is `tests/test_timeline_public_s2_mixed_cli_journey.py` on the existing Runtime `commit-integration` line (or its exact qualified node, if the port narrows the file). Do not add or run that line now: the current suite already has the historical pinned lines, and this task deliberately avoids duplicating their run.
- No external blocker remains. The remaining gate gaps are outside this Runtime Gate2/Gate4 proof: Gate 3 renderer-independent save evidence, Gate 5 adversarial App journey, Gate 6 one-writer/one-viewer parity and legacy-endpoint rejection across representative gestures, and Gate 7 delivery/ZIP/owner-film evidence.
