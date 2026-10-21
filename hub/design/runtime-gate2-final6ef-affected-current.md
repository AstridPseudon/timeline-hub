# Runtime Gate2 affected-node run: Agent 6ef / Runtime 95bd

Date: 2026-10-21

## Scope

This is the one narrowly scoped current6ef Gate2 run. No Runtime source or
test files were changed. The central service suite ran exactly these four
node selectors:

```text
tests/test_timeline_commit_integration.py::test_real_move_rebases_disjoint_clip_and_conflicts_on_same_clip
tests/test_timeline_commit_integration.py::test_real_door_concurrent_disjoint_moves_accept_and_rebase
tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider
tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary
```

The crash selector is parametrized by operation (`commit`, `restore`) and
stage (`before`, `after`), so the four selectors represent seven collected
cases. The existing assertions and tripwires were left unchanged, including
before/after acceptance, no-write rollback, exact replay, and forbidden
provider execution on retry.

## Exact source and artifact tuple

- Runtime product: commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Agent checkout: commit `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`, clean.
- Runtime client contract: `0.2.14`.
- Client schema digest:
  `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`.
- Normal Runtime artifact digest:
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.

The suite preflight imported `runtime_protocol` from the Runtime snapshot and
`astrid_runtime_client` from the pinned Agent checkout, then passed all commit,
tree, cleanliness, contract, schema, lock source, and artifact assertions.

## Central service command and result

Named suite: `gate2-final6ef-affected-http-crash`

Run ID:
`rt-m2-gate2-final6ef-affected-http-crash-gate2-final6ef-affected-http-crash-1021004534-27309`

The test body was:

```text
env ASTRID_RUNTIME_CHECKOUT=$PWD ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6efc8150 PYTHONPATH=$PWD:/home/user/work/wt/agt-pin-6efc8150 PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m "not darwin_native and not live" tests/test_timeline_commit_integration.py::test_real_move_rebases_disjoint_clip_and_conflicts_on_same_clip tests/test_timeline_commit_integration.py::test_real_door_concurrent_disjoint_moves_accept_and_rebase tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary
```

Preflight: **passed**.

Pytest: **5 passed, 2 failed in 19.06s** (7 cases collected).

Passed coverage:

- concurrent disjoint real-door moves: accepted + rebased, distinct receipts
  and revisions, final document contains both moves, no duplicate ledger rows;
- all four process-death cases: commit/restore × before/after acceptance,
  including rollback/no-write and restart behavior;
- the lost-ack test reached exact replay and provider-forbidden retry checks
  before its final baseline assertion.

## First failure and qualification status

The first failure was:

```text
tests/test_timeline_commit_integration.py::test_real_move_rebases_disjoint_clip_and_conflicts_on_same_clip
tests/test_timeline_commit_integration.py:132
assert baseline["receipt"] == self.film.publication["receipt"]
```

The receipt differed only in its result payload: Runtime had compacted the
historical result to `__runtime_idempotency_result_expired_v1`, while the
fixture retained the original publication result. The fixture's recorded
publication timestamp is `2026-10-19T23:31:30.900+00:00`; this run was after
the 24-hour idempotency result window. The same stale-fixture expiry symptom
was present in an earlier current-Runtime neighbor run. The second failure is
the same baseline assertion in the lost-ack selector, after its retry and
provider tripwires passed.

This run therefore does **not** qualify a green current6ef Gate2 result. No
expected-failure marker, skip, guard weakening, or duplicate run was added.

Central log:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-gate2-final6ef-affected-http-crash-gate2-final6ef-affected-http-crash-1021004534-27309/log.txt`

No full, browser, render, normal 51-case, rational/PARAM, or valid-window
hold suite was run.
