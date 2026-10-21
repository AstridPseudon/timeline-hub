# Runtime Gate2/Gate4 current-command readiness

Date: 2026-10-21 UTC. Scope is the Runtime gate-track command and evidence
reconciliation only. This is not an all-gates claim.

## Current tuple and command status

- Runtime current integration: `b92d3e7a05eec65c142294ef4873edd059e9b31d`,
  tree `6abc2f117391de8e7e35c0283f575a002199894d`.
- Published Runtime/client producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`,
  tree `d3a290b407fa61e6ab2d476f50c068073f70df00`, client `0.2.14`,
  schema `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`,
  artifacts `76/76`, version
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
- Public014 Agent source used for the retained-text pair: commit
  `afe37906433773a29b5928b35abd8075be8a7ecf`, tree
  `f2cedd08a01b1a360df79046e4b9c2a5cb101dd5`.

The existing Runtime named suites remain runnable on current b92. Collection
checks found all paths and selectors present:

- `gate2-atomic-integration`: **51 tests collected**. The current command is
  the line in `ORCH/tests/suites.conf` and includes the full execution module,
  the named atomic/retry/refusal/rollback/recorder cases, concurrent disjoint
  door moves, rebase/conflict, lost-ACK retry, and the parametrized crash case.
- `gate4-door-integration`: **29 Python tests collected**. Its current command
  includes the route/lock/transport, real-door admission/retry/isolation,
  generated Python client, and parity selectors, followed by
  `cd packages/typescript && PATH=/home/user/work/app/node_modules/typescript/bin:$PATH npm test`.
- Public014 retained-text pair: **2 tests collected**, both original bodies.

The exact current Runtime selector tails are:

```text
tests/test_timeline_commit_execution.py
tests/test_timeline_commit_acceptance.py::test_atomic_acceptance_exact_recorder_projection_and_same_content_edge
tests/test_timeline_commit_acceptance.py::test_identical_retry_after_restart_and_head_advance
tests/test_timeline_commit_acceptance.py::test_changed_payload_and_publication_only_cas_refuse_without_writes
tests/test_timeline_commit_acceptance.py::test_invalid_prepared_values_are_atomic
tests/test_timeline_commit_acceptance.py::test_failure_after_receipt_rolls_back_every_row
tests/test_timeline_commit_acceptance.py::test_failure_between_projection_steps_rolls_back_and_restart_retry_publishes_once
tests/test_timeline_commit_acceptance.py::test_complete_recorder_roundtrip_and_replay_after_restart
tests/test_timeline_commit_integration.py::test_real_move_rebases_disjoint_clip_and_conflicts_on_same_clip
tests/test_timeline_commit_integration.py::test_real_door_concurrent_disjoint_moves_accept_and_rebase
tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider
tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance-boundary
```

Gate4's exact current Python selectors are the two full files
`tests/test_timeline_commit_routes.py` and `tests/test_http_response_lock.py`,
plus `test_admission_order_host_origin_and_route`,
`test_browser_credentials_are_refused`, `test_preflight_allows_listed_request`,
`test_preflight_refusals`, `test_real_door_commit_admission_checks_origin_auth_and_project_scope`,
`test_real_door_lost_ack_restart_exact_retry_never_executes_provider`,
`test_real_provider_two_projects_keep_local_ids_and_commit_authority_isolated`,
`test_generated_client_smoke_and_scoped_handshake`,
`test_acquisition_selected_python_renderer_parity`,
`test_product_clients_match_canonical_contract_projection`, and
`test_recoverable_snapshot_client_projection_is_canonical`, in their respective
files as recorded in `ORCH/tests/suites.conf`.

The public014 command had one real readiness defect: its preflight required
Agent `HEAD == afe379...`, but the central service snapshots a target tree into
a synthetic commit before execution. I repaired only that owned suite line to
assert the immutable Agent `HEAD^{tree} == f2cedd...`; the exact Runtime HEAD,
Runtime tree, schema digest, published lock source, 76-artifact count, and
import-origin guards remain. A planted invalid selector exited nonzero (pytest
rc 4), while the real pair collected positively.

## Recorded green evidence

- Gate2 exact normal 51-case tuple:
  `rt-m2-gate2-final-main014-current-proof-gate2-final-main014-normal-agent-e35ad5e7-proof-1021002537-14311` — **51 passed in 25.12s**, Runtime producer `95bd`, Agent `e35ad5e7`.
- Final6ef affected follow-up:
  `rt-m2-gate2-final6ef-two-aged-fixtures-gate2-final6ef-two-aged-fixtures-1021005203-2115` — **2 passed in 3.67s** after the initial affected run's 5-pass/2-baseline-failure result. The failures were expired copied legacy idempotency receipts; the helper refreshed only copied fixture clocks. This is historical 95bd/6ef evidence, not a fresh b92 replay.
- Earlier parallel named Gate2 command:
  `rt-m2-gates2-and4-parallel-proof-track-gate2-atomic-integration-1020213050-20082` — **50 passed in 23.88s** on proof tree `183dbcf...`. The current b92 collection is 51 because the current selector set includes the concurrent-disjoint-door case; no claim is made that this old 50-count result covers that extra current node.
- Gate4 Python historical named result:
  `rt-m2-gates2-and4-parallel-proof-track-gate4-door-integration-1020213206-10752` — **29 passed in 16.01s**, plus its TypeScript segment **61 passed**; the Python bodies are source-identical to current b92, but that snapshot's generated package was 0.2.13.
- Gate4 current TypeScript result:
  `rt-m2-gate4-main014-ts-evidence-0407-ts-client-check-1021040813-12394` — **61 passed, 0 failed**, on current b92 tree `6abc2f...`, command `cd packages/typescript && PATH=/home/user/work/app/node_modules/typescript/bin:$PATH npm test`.
- Public014 exact b92 pair after guard repair:
  `rt-m2-public014-text-pair-execute-0903-public014-retained-text-original-pair-integration-1021090630-11357` — **2 passed in 1.78s**, exact Agent tree `f2cedd...` and Runtime b92/tree `6abc2f...`.
- Current Runtime broad evidence (not a gate replacement):
  `runtime-full-retained-owned-temp-integration-1021035028-28646` — **6002 passed, 26 skipped, 15 xfailed, 12 warnings**, b92/tree `6abc2f...`.

Reproducible named invocations are:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:runtime gate2-atomic-integration
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:runtime gate4-door-integration
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-public014-text-pair-execute-0903 public014-retained-text-original-pair-integration
```

The first two are commands to run at M4; their current b92 direct bodies were
not rerun here because unchanged passing bodies are explicitly out of scope.
The public014 pair was the one previously blocked before body execution and
was run once after the guard repair.

## Limits and remaining qualification boundary

Evidence is Linux-only. No macOS or `darwin_native` tests were run or claimed;
no browser, renderer, live-socket, full-suite repeat, private017 body, or
four-product journey was run here. Gate2's exact 51-pass result is bound to
Runtime95/e35, with final6ef only covered by its recorded seven-case
5+2 follow-up; current b92 has source/collection/full evidence but no fresh
direct 51-case b92 result. Gate4's current TypeScript 61-pass result is b92;
the 29 Python result is historical source-identical evidence plus current
positive collection. These boundaries are concrete and intentional.
