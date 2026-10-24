## Report

Read-only investigation complete. Worktree is clean; no product/test edits.

### Evidence

- Current service run: `agt-F-final-source-join-0816-authoring-current-becfe-nodes-1024085217-20732`
- Exact selector: `tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`
- Result: **1 failed in 40.19s, exit 1**
- Failure at line 1090: expected `transport_error`, observed `transport_timeout`.
- Agent source: `0c2c28d`; test blob `e55be12f`; Runtime: `becfe6db`.
- Historical WC6 passing proof: **1 passed in 14.35s** on Runtime `7f6dd89`, with durable receipt/history assertions.

### Boundary findings

`TimelineSession.undo` creates `timeline.inverse`, persists the exact flight, then sends it through `WorkspaceClient` to Runtime’s authenticated commit route. Runtime evaluates `commit(...)` before deferred `_send(200, ...)`.

The hook source sets `lost['done']` only if its match branch runs, and does so before raising `ConnectionError`. However, the failed artifact contains no hook-state print, captured body, receipt, or retry evidence. Therefore:

- Hook execution and `lost['done'] = True` are source-level conditional facts, not directly retained runtime evidence.
- The log proves only a status-0 transport failure, classified as timeout.
- It does not prove durable acceptance or produce a receipt.
- The run stopped before outbox replay, daemon shutdown/restart, retry, history, or receipt assertions.

The unowned seam is the Runtime HTTP close/error classification between `RuntimeHandler._dispatch`/`_send` and generated-client mapping of `TimeoutError` versus `URLError`. No causal pin or timing explanation is proven.

### Next owner

Viewing owns the verdict and next source attempt. Treat this run as **unqualified for lost-ack acceptance**; resolve the `becfe6db` timeout-versus-retained-`7f6dd89` transport boundary before claiming the hook or receipt path. No competing Agent product author is indicated.

No tests were run by this worker. Required commit message and empty `DONE` marker were created.