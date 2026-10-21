# PRIVATE017 placement diagnosed-run report

Date: 2026-10-21 UTC

## Disposition

The fresh prerequisite preflight **passed**. The one authorized central test
request was made exactly once, but it targeted `integration:agent` rather than
this worker snapshot. The service therefore failed before executing the test
body: pytest reported no matching parameterized node and ran zero tests.
Per instruction, there was no retry. Placement remains **unqualified** and
this worker is blocked on a correctly targeted future authorization.

## Exact tuple and preflight

- Agent: `86d1e6da200884ba660ea435c90dac801f8f1c7e`, tree
  `5b6dc1c4eed688bdfc2c7f53b21607b0f169683d`.
- Runtime: `/home/user/work/wt/rt-pin-42a7203f`, commit
  `42a7203f49bb89f299ec854cfbf2b1444e815a7c`, tree
  `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`.
- Agent worktree and Runtime42a checkout were clean.
- `runtime.lock.json` SHA-256:
  `a9046ae72a4ee1ff9cb7e8062f301d599803f826eb6f2dbb025e7cc5b1d27a6c`;
  source commit was exactly Runtime42a and producer version was
  `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.
- The normal client lock checked `15/15` Agent files against both the Agent
  worktree and Runtime42a sources. Runtime `contract/artifacts.json` checked
  `76/76` artifacts. Its producer was `astrid-runtime`, version
  `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0`.
- Agent and Runtime EditCommand schemas were byte-identical and both had raw
  SHA-256 `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`;
  the approved tuple's canonical schema identity remains
  `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d`.
- Isolated imports selected `/home/user/work/venv-agent/bin/python`, Agent
  modules from this worktree, `runtime_protocol` from Runtime42a, and the
  shared schema only from the venv. Contract metadata was `0.2.17` with
  health/schema digest `a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd`.
- The fresh fixture shape probe found source `shot-1` with `items=[]` and
  `source_mapping.shots[shot-1].item_id_map == {}`. This is shot-only; global
  and item allocation remain unqualified.
- Disk free space was `12,552,648` KiB; both worktrees remained clean after
  the probe. No shared dependency was modified.
- Exact collection command, with no body execution:

  `env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-42a7203f PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-42a7203f" ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-42a7203f" /home/user/work/venv-agent/bin/python -P -B -m pytest -q --collect-only -o addopts= -p no:cacheprovider -m integration 'tests/editing_conformance/test_commit_runtime_identity.py::test_fresh_shared_placement_materializes_own_slot_reload_inverse_and_exact_retry[fresh]'`

  Result: **1 test collected in 0.96s**.

## Single central request

Requested exactly once with:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:agent private017-placement-one42a-integration`

Result ID:
`agent-private017-placement-one42a-integration-1021111648-17355`

The service ran the exact named suite command and returned **fail, exit 4,
2s**. First and only failure:

`no tests ran in 0.17s`

`ERROR: not found: /home/user/work/wt/.test-agent-private017-placement-one42a-integration-1021111648-17355/tests/editing_conformance/test_commit_runtime_identity.py::test_fresh_shared_placement_materializes_own_slot_reload_inverse_and_exact_retry`

The central target was `integration:agent` (the integration worktree), not
this worker's exact `5b6dc1c4` snapshot. The parameterized node was therefore
absent from the service snapshot. No RuntimeService/provider admission,
readback, restart, own-slot reuse, inverse, or exact-retry body assertion ran.

## Boundary and retained failures

The existing failures remain retained and diagnosed, not converted to passes:

- `...1021102411-25065`: failed before admission at
  `next(iter(item_id_map.values()))` because the fixture map is empty.
- `...1021103708-3710`: reached acceptance/readback/restart, then failed at
  the old reload expectation of source `S`; the corrected oracle now expects
  the physical projection `D` while accepted history retains `S` and owner
  `O`.

The corrected test still contains the accepted `id_map`, source pin, owner
binding, physical placement, restart, own-slot, inverse, and ledger-first
exact-retry assertions. No product, pin, schema, fixture, or test file was
changed in this worker. No global/item allocation, ordered12634, or RT03 claim
is made.

## Recommended next step

Do not retry automatically. If qualification is still required, the
orchestrator must explicitly authorize a new single central request targeted
at this worker's exact snapshot/worker name, then classify that independent
result. The present run is a dispatch-target failure, not placement evidence.
