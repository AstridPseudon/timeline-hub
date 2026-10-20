# Runtime connector live integration gates

Status: PASS

The independently approved tests-only commit `b26e922125362f2294dfdc23feb44b64adf19a58` was applied exactly to current Runtime `2cb9bb62c88d91fdab03df230ef0b2a3bd81f513`. The worktree changes are limited to:

- `tests/fixtures/operation-handle-live.mjs`
- `tests/test_operation_handle_integration.py`

No product code, package pins, publication, merge, or App proxy/activation work was performed.

## Frozen source and package identity

At start, Runtime was `2cb9bb62c88d91fdab03df230ef0b2a3bd81f513`, tree `ec90ae8c6472316eea0101369314fcbef6907334`. The central test snapshot including the two untracked additions was tree `330ea3969cb9cce77271404f31793c21abd5993f`. The actual Agent checkout used by the run was source `9cb1090458428fb09067e359be92cdbb6608a206`, tree `43005ea2e18c7b017b927ad4220209a33aaeb27b`. No credential token values are recorded here.

The published 0.2.13 TypeScript package subtree remains tree `8aa87257e045f12a07834e25fb484ea6c397bf96`, equal to producer `2c4ac180c2220bdad966bc01e95ad230e99ce26a`; `git diff --exit-code 2c4ac180c2220bdad966bc01e95ad230e99ce26a -- packages/typescript` passed.

## Evidence

Central test ID: `runtime-marked-integration-1020123549-29716`.

Exact command:

```text
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -n 3 -m integration tests/test_operation_handle_integration.py tests/test_timeline_commit_integration.py
```

Result: **12 passed in 8.74s** (central suite exit 0).

The run exercises real Runtime HTTP, the startup-loaded Agent provider, and the compiled TypeScript/Node client. Both lost-ACK observation phases remain present: response-level withholding and body-level withholding after native response body consumption begins. The assertions retain the original accepted response/receipt, the exact original retry payload, one additional SQL history edge, and the idempotency result stored for that receipt. Real credential and scope refusals remain covered, including invalid credentials and read-only authority refusing write operations.

No broad/full suite, package-unit repeat, App proxy, App activation, remote relay, or macOS claim is included.

