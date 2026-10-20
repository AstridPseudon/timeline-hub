# Direct operation connector: real Runtime integration

2026-10-20 — completed on Runtime base `c1fb9ef2f7736459ceaaaaf85b5f9650e32c942d`. Final central source tree **`173fbf029116b48ffa789ee9613162dfc1ccfc5b`**: **12 passed**, including three new cases and all nine existing commit-integration cases. Local adjacent route/lock/release checks: **20 passed**. No production change or discovered production defect.

Two added test/support files:

- `/home/user/work/wt/rt-m2-connector-live-commit-integration/tests/test_operation_handle_integration.py`
- `/home/user/work/wt/rt-m2-connector-live-commit-integration/tests/fixtures/operation-handle-live.mjs`

The test reuses the captured music-film, renderer-unavailable Agent fixture, `Editing` and SQL snapshot helpers from `tests/test_timeline_commit_integration.py`, and ordinary owner-authenticated product credential provisioning from `tests/door_helpers.py`. A real `RuntimeDaemon(authoring_profile="astrid")` loads the actual Agent provider at startup. Node imports a private build of the unchanged public TypeScript package, including its generated `WorkspaceClient` and handwritten `OperationHost`/`OperationHandle`. It uses the daemon's direct HTTP endpoint; this test starts no browser door or App proxy.

The only server interception delays normal `_send` output after the route has returned from real commit acceptance. One case holds response headers; another sends the real headers and holds the real body, with an observer confirming native `Response.arrayBuffer()` has started. Native fetch dispatches immediately with the handle's supplied target, headers and options; no request or response DTO is substituted. A separate read-only SQLite connection sees the accepted history edge and the exact persisted command result under the original receipt before release.

The same initial handle/client/base/credential performs health, handshake, realm, timeline read and commit. While its ACK remains unobserved, the owner provisions a fresh credential for the same actor, retires the original handle and binds a distinct handle/client. Real negotiation returns the same actor/realm. The old ACK continuation rejects; captured identity/recovery callbacks remain retired and attempted old reads/transmits make no transport dispatch. Retrying the exact original serialized body and key through the new handle returns the original complete result/receipt, with the entire SQL dump unchanged and exactly one added history edge. Disposal during a subsequent real pending read fences that completion and all later use, at both response and body waits.

Real server authorization also rejects invalid credentials at handshake and commit, rejects requesting a write scope from a read-only credential, and rejects a commit after successful read-only negotiation. The refusal details come from the real server; the wrapper correctly retires. All SQL remains unchanged. Credentials use a private stdin pipe and never appear in argv, stdout or the reports.

Published client producer remains **`2c4ac180c2220bdad966bc01e95ad230e99ce26a`**, contract **0.2.13**, schema **`sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`**. `git diff --exit-code 2c4ac180c2220bdad966bc01e95ad230e99ce26a -- packages/typescript` passes; the complete package tree is `8aa87257e045f12a07834e25fb484ea6c397bf96` at both sources. There was no generated artifact mutation, pin, publication, merge, new API or dependency installation. TypeScript output stays in private pytest temporary directories; shared dependencies are only read.

Central request:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
R=$("$ORCH/bin/request-test" rt-m2-connector-live-commit-integration marked-integration --files "tests/test_operation_handle_integration.py tests/test_timeline_commit_integration.py")
"$ORCH/bin/wait-test" "$R" 1
```

Result: `rt-m2-connector-live-commit-integration-marked-integration-1020121543-20963`, **exit 0, 12 passed in 16.81s**. Actual service command:

```sh
env ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q -n 3 -m integration tests/test_operation_handle_integration.py tests/test_timeline_commit_integration.py
```

Agent during the final run: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, tree `75354d38c898729bac09619679f5421faba319ed`; the service external-source record and the post-run HEAD agree. Full exact commands, source hashes and the initial test-runner cleanup failure are in [DetailedReport.md](../workers/rt-m2-connector-live-commit-integration/DetailedReport.md).

This closes the bounded direct-owned-transport accepted-commit/lost-ACK/reconnect gap. It does not qualify the App's hidden-credential proxy, automatic requester activation, native capture, browser outbox/restart durability, arbitrary deferred fetch adapters or macOS. The new tests renew a connection, not the Runtime process; the unchanged adjacent commit tests also exercise Runtime restart. No full suite was requested. No blocker or settled-decision deviation. Next: orchestrator review and normal integration queue; retain the separate App activation prerequisites.
