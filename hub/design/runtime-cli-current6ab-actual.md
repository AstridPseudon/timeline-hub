# Runtime current-6ab consumer gate

## Result

The one requested central test-service run passed. No Runtime product files,
Agent files, shared dependencies, fixtures, or assertions were changed.

## Exact source tuple

| Component | Checkout | HEAD | HEAD tree | Clean |
| --- | --- | --- | --- | --- |
| Runtime | `/home/user/work/wt/rt-m2-cli-current6ab-actual` | `6ab3243972f8dc49105819e6d7ba7aef1a2888b8` | `c225a680c645c67c3fe1f43b5e564b2a77a05d80` | yes |
| Agent (sdk) | `/home/user/work/wt/agt-pin-2f8b9cc5` | `2f8b9cc53648a392da8684016c6ee15e589ea060` | `8f15471af6928e166cfbeedf6d00d7cf6454cfbe` | yes |

The Agent checkout was created by the completed `request-checkout` result and
was verified before testing. Import probing with the intended path precedence
resolved `astrid` from `/home/user/work/wt/agt-pin-2f8b9cc5/astrid/__init__.py`
and `runtime_protocol` from
`/home/user/work/wt/rt-m2-cli-current6ab-actual/runtime_protocol/__init__.py`.

## Exact command and result

Test-service request:

```text
request-test rt-m2-cli-current6ab-actual cli-agent2f8-integration
```

Run ID: `rt-m2-cli-current6ab-actual-cli-agent2f8-integration-1020162712-644`

The suite command executed was:

```sh
env ASTRID_RUNTIME_CHECKOUT=$PWD \
  ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-2f8b9cc5 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=$PWD:/home/user/work/wt/agt-pin-2f8b9cc5 \
  /home/user/work/venv-agent/bin/python -m pytest -q -m integration \
  /home/user/work/wt/agt-pin-2f8b9cc5/tests/sdk/test_timeline_commit_provider_runtime.py
```

Result: **2 passed in 1.78s**, service exit `0` (run duration 3s).
The authoritative log is the central result directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-cli-current6ab-actual-cli-agent2f8-integration-1020162712-644/`.

The two existing tests exercised direct Python RuntimeService/provider use:

- structural reservation collision, inverse deletion, Runtime restart, exact
  receipt retry without provider execution, unchanged head, and redo;
- restore, exact restore retry after restart, stale publication refusal,
  restore inverse/redo, historical-ID reuse, and dry-run non-persistence.

## Limits

This named lane is not evidence for HTTP transport or an actual CLI process,
lost-ack response handling, restart-safe queued dependent B, concurrent rebase,
retained-read behavior, or renderer-off tripwires. Those remain covered only if
and when their existing dedicated suites are run. No full Agent/Runtime suite,
M1-neighbor suite, browser/live-socket suite, or render suite was requested.

