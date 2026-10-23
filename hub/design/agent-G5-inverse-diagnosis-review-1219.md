# G5 inverse diagnosis review

## Verdict

**BLOCKED — the real Runtime whole-commit inverse still returns the exact 503 `not_ready` / `runtime_unavailable` outcome.** This review made no Agent, Runtime, test, fixture, client, schema, pin, or dependency changes. G5 is not qualified, and no failed positive was rewritten as a refusal.

## Identity and evidence boundary

- Agent candidate: commit `b9092fe27e3e0bc5febb9c4c62586e122a10a84f`, tree `08ce16f3ea192c35fb7c919e99beb2b0b187fb47`.
- G5 production parent: `ee7f0b809266690f5c46d6824af1e6ee82f03714`, tree `4305240b13e6eefbfdf9a4e34c8a04d9127b2645`.
- Runtime: commit `3b926efab2eed122d374540baee297d4cdcec62a`, tree `b794170504544b259781e50d7ca4d61b6729e67c`.
- The prior 605 KB capture is not treated as present or as durable evidence. The only durable prior facts used here are the 1210 worker log/report and source inspection.

## Exact result

The permanent new test uses the real `Checkout.publish(restructure=True)` caller, the real Agent provider, the real Runtime commit service/store, and the public `TimelineSession.undo()` caller. The restructure itself was accepted before inverse dispatch: it produced the expected three-root restructure and preserved the authored opaque value containing explicit null, ordered null/false/zero values. The target then sent one whole-commit `timeline.inverse` request for the accepted restructure receipt, with the normal base revision/publication pair, command, label, v2 step metadata, `merge: fields`, `dry_run: false`, and `source: {via: python}`.

The inverse did not produce an accepted, merged, or conflict reply. Runtime surfaced `WorkspaceClientError: Timeline commit outcome unavailable; retry the exact request`, with `code=not_ready` and `details={reason: runtime_unavailable}`. At the Runtime service boundary this is status 503. The in-process bridge normalizes the error into `WorkspaceClientError` with status 0 while retaining code/details. No inverse receipt was accepted, so undo, redo, and the later-overlap refusal/no-write assertions were not reached.

## Causal trace and ownership

The mapping is deterministic and Runtime-owned at the surfaced boundary:

1. Agent `sync.py:_flush` freezes the request in the outbox and calls `RemoteTimelines.commit`; ambiguous errors are deliberately left in flight.
2. The public bridge routes to Runtime's canonical timeline commit endpoint.
3. Runtime `service.py:_execute_timeline_commit` invokes `CommitExecutionCoordinator.execute`.
4. `timeline_commit_execution.py` catches provider, port verification, and port-close failures, performs a durable idempotency lookup, and re-raises the underlying error when no accepted winner exists.
5. Runtime service converts any otherwise-unhandled exception to `CommitUnavailable` (503, `not_ready`, `runtime_unavailable`), and the server/bridge expose the envelope above.

The Agent inverse handler is reached by the installed provider at `astrid/sdk/timeline/commit.py:924+`. It validates the inverse, loads the authenticated target/history boundaries, selects inverse records, executes the inverse plan, prepares the full canonical/records result, and calls `port.accept`. It translates `AuthoringBundleError` and `CommandError`, but an unhandled provider exception, a port verification exception, a close exception, or a failed durable lookup can all be collapsed by the Runtime boundary into this same 503. Source and the surviving log therefore identify the precise failure boundary and owner of the public disposition, but not the underlying exception. I did not attribute it to Agent R1 or claim a Runtime semantic bug.

### One permitted causal probe

I ran one external-only observability wrapper around this same test case. It wrapped the already-created Runtime coordinator/provider and attempted to record the actual context, request, port captures, history, canonical head, traceback, and module origins without changing predicates, guards, source, or acceptance state. The tracing observer exceeded the bounded probe window and was interrupted; it emitted no evidence file and no usable underlying trace. This is explicitly a failed diagnostic extension, not a second qualification run. No further inverse body was sent.

## Test fidelity and fixture limits

The target test retains the accepted restructure shape/equivalence checks, opaque null/order preservation, the intended whole-undo and redo assertions, and the later overlapping authored write expected to refuse. It also verifies the restructure request's full v2 metadata and uses a narration-media failure only to keep the restructure as one publication; that setup does not fake an acceptance.

Two limits remain material:

- The refusal block currently checks the `CommitConflict`/“intervening” result only; it does not explicitly assert unchanged head, history, and canonical document after refusal. That no-write property remains required and is unverified, not a reason to weaken the test.
- The shared `restructure_runtime` fixture's `open_bundle` seam calls the Runtime store's private `revision_closure` and ignores the publication argument. Thus the test is a genuine public commit/inverse service test and does not falsely turn the 503 into a product refusal, but it cannot by itself certify the separate public exact revision/publication-pair read-authority boundary.

The inverse request construction is source-faithful: `TimelineSession.undo` creates the `timeline.inverse` command and v2 label/step metadata, while `_flush` adds the exact base pair, commands, source, dry-run flag, and stable idempotency flight. The accepted full-v2 inverse reply remains unverified.

## Checks

- The 1210 real-Runtime targeted case: **1 failed** in 11.67s with the exact `runtime_unavailable` boundary result; no undo/redo/refusal qualification.
- External causal-probe invocation: **interrupted after exceeding the bounded observer window**, no result/evidence artifact.
- Scoped Ruff on the target: **passed** (`All checks passed!`).
- `git diff --check HEAD^ HEAD`: **passed**.
- Source identity checks for Agent and Runtime: **passed**; Runtime worktree is at exact 3b/tree b794.
- No full suite, browser, HTTP journey, native matrix, P1/P4, D17 duplicate, daemon, shared-install mutation, or known-failed inverse rerun was made.

## Disposition and handoff

Keep G5/P1 blocked. Runtime owns the surfaced 503 and should add observability at the coordinator/provider/port boundary to identify whether the underlying exception is Agent-provider, Runtime-port/store, or close/verification. Once that exact cause is known, apply only the bounded existing owner fix; do not waive guards, broaden the inverse matrix, or alter C0 metadata. If the cause is Agent-owned, it should be a precise provider-handler fix; if Runtime-owned, the handoff facts above identify the coordinator boundary. After a reviewed fix, rerun the original permanent test once and require accepted equivalent undo, redo, overlapping-write refusal, and explicit no-write assertions before G5 integration.
