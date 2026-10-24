# F-ABA capture proposal review

## Verdict

**FAIL — actual Agent-only proposal is insufficient.**

The proposal correctly identifies the retained packet as inconclusive, but its `_send` hook cannot cover the missing facts:

- `RuntimeHandler._send` at [test_authoring_media.py:1057](/home/user/work/wt/agt-F-ABA-capture-review-0945/tests/timeline/test_authoring_media.py:1057) runs only after `commit_timeline` returns. It cannot observe `port_factory` failure, a blocked provider, the coordinator’s saved provider/close exception, or final lookup authorization.
- The exact original blob is `e55be12f…`; the target function contains 59 assertions. Assertion 42 is the original transport-error code assertion; assertions 43–59 did not execute in the retained run.
- Adding `client.timelines.history(...)` before assertion 42 adds a live request inside a run that already consumed 40.19s of the 45s test budget. It can block, alter timing, produce another timeout, or replace the original failure. It must not be added.

The retained packet is finite: 37,751 bytes. It records only the 40.19s failure (`transport_timeout` versus expected `transport_error`), with no request-correlated provider, port, close, authorization, receipt, retry, or history outcome.

## Required smallest correction

Runtime owns the required observer at:

[runtime_protocol/timeline_commit_execution.py:69](/home/user/banodoco/banodoco-workspace-runtime/runtime_protocol/timeline_commit_execution.py:69), `CommitExecutionCoordinator.execute`.

Add an opt-in, observer-only, request-correlated diagnostic sink around the existing stages:

- initial lookup;
- port-factory entry/result;
- provider entry/result or exception;
- close result or exception;
- final authenticated lookup authorization result and replay result/exception.

Flush a bounded partial record before provider invocation so a provider block is distinguishable from a port-construction failure. Capture provider/replay data only when naturally available from the authenticated Runtime path. Preserve the full v2 request/reply facts through the existing outbox and returned envelopes: IDs, commands, labels/steps, merge/reads/dry-run/source fields, canonical closure, digests, `id_map`, records, dependencies, effects, bindings, undo/history/publisher, receipts, and structured conflict/invalid fields. Store only request length/hash and non-secret authorization status in the diagnostic record; never dump credentials, raw authorization headers, or unbounded bodies/payloads.

The observer must be best-effort and must not change semantics, authentication, timeout budgets, exception categories, response handling, or error precedence. Do not perform a second HTTP history request. If a history item is needed, Runtime should capture it from the existing authenticated store lookup (`timeline_commit_store.py:172-200`) during the same coordinator operation.

Agent owns only the test-local packet retention and must preserve the exact 59-assertion AST/order, 30s/45s budgets, all pins/origin/module guards, and the genuine mounted `TimelineSession.undo` → Runtime `/commit` production path. No original test rerun under a new filename is justified.

## Checks

- `git diff --check` — PASS.
- Exact local test blob hash — `e55be12f88d23fddba3dd36614eb91745c1f8adf`.
- AST inspection — 59 assertions; original assertion order confirmed.
- Runtime source inspection — coordinator stages confirmed at lines 83, 87, 93–98, and 101.
- No tests, service runs, product edits, Runtime edits, or original-body reruns performed.
- Worktree clean; required commit message and `DONE` marker created.