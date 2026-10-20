# Runtime Gate2 corrected Main014 live acceptance

Date: 2026-10-20. No source, test, or artifact files were changed.

## Exact source/import tuple

- Runtime worker: commit `6e845a187684919c162b29568496c015bda1a591`, tree `7f11d7e159d46a88a22111c414aa7bdf7b599d9d`.
- Agent checkout used by the HTTP/provider tests: `/home/user/work/agent`, commit `b43cd95717a5018940f5ffa4123d2db3ff34b8f0`, tree `1d44801de4aa27559d39bc30c35800a13db5ad49`.
- Runtime integration head was clean at `9d1c43c647301da48a6e86ad82e466b501bd2418` (tree `50e74e3243c5da4cf77b6e6cc76605fae8aeb649`).
- Imports resolved to the worker's `runtime_protocol` and `runtime_protocol/timeline_commit_provider.py`, plus `/home/user/work/agent/astrid_runtime_client/__init__.py`. Contract metadata was `0.2.13`, schema `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`.
- The selected function source hashes match the prior 51-case proof snapshot (`36082cf…`); the corrected Main014 tree only carries the already-proven test-file delta.

## Exact bounded service run

The default full suite excludes `integration`. The existing `gate2-atomic-integration` named suite hardcodes all 51 cases, including regular nonintegration coverage, so a temporary selector was necessary to pass exact nodes; it was removed after the run.

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m "integration and not darwin_native and not live" tests/test_timeline_commit_integration.py::test_real_move_rebases_disjoint_clip_and_conflicts_on_same_clip tests/test_timeline_commit_integration.py::test_real_door_concurrent_disjoint_moves_accept_and_rebase tests/test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider tests/test_timeline_commit_crash.py::test_real_process_death_at_acceptance_boundary
```

Central result `rt-m2-gate2-corrected014-concurrency-current-gate2-actual-http-crash-corrected014-1020225848-28982`: **7 passed in 18.22s**.

Coverage mapping:

- simultaneous durable live-door commits: concurrent disjoint moves, accepted + rebased, both receipts/history revisions, no duplicate ledger rows;
- stale disjoint rebase versus same-clip conflict: direct real-provider acceptance path;
- crash before/after acceptance boundary: commit/restore × before/after, four cases;
- exact replay and changed body/key refusal: live-door lost-ACK restart retry, provider forbidden on replay, same-key changed rationale refused;
- no partial projection/duplicate revision: asserted by the selected concurrency, retry, and crash cases.

## Gaps

The prior fixed 51-case proof remains `51 passed in 24.39s` on its recorded snapshot; regular nonintegration cases were not duplicated here. No full, Gate4, render, or browser suite was run. This report records the corrected-source live HTTP/concurrency/crash acceptance evidence and does not claim broader gate completion.
