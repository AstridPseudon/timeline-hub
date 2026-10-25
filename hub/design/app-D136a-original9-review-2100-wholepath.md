# Whole-path read-only review

## Caller to Runtime

The mounted App outbox/bootstrap path supplies `commitTimeline` through `RuntimeDataProvider` and calls the generated Runtime client. The App adapter checks project/timeline and base revision/publication identity, passes the C0 v2 request plus `Idempotency-Key`, and accepts only a reply with a receipt. The public Agent workspace helper and authoring writer use the same generated `commit_timeline` operation; no local writer or fallback executor was found.

## Runtime to registered Agent provider

The Runtime HTTP route authenticates the actor for `projects:write`, checks canonical route/body identity, requires the idempotency key, and calls `RuntimeService.commit_timeline`. The service validates the request and canonical path, performs authorization and active-timeline checks, then enters the `CommitExecutionCoordinator`. The coordinator preserves invocation identity, checks durable replay before provider execution, calls the startup-registered provider, verifies its outcome, and rechecks replay before returning a refusal or accepted result.

Startup is profile-gated: only the explicit `astrid` profile imports the Agent provider factory; the provider ABI, interface version, contract digest, synchronous signature, and startup-only registration are validated before requests are served. The immutable Runtime pin used by the actual run is the reviewed `ab1e4f...` source, not the mutable integration worktree.

## Provider to first seam

The provider loads the exact base closure, executes the explicit `timeline.init`, and calls final candidate validation before materializing/persisting the canonical document. The stack reaches `validate_final_candidate` → `_validate_fps` → the typed-location equality guard. It does not reach a saved-projection comparator or a later browser/render path.

## Passing comparator and prior evidence

The D100 projection source/test remains byte-exact and the prior 27-pass and source/security reviews remain bounded prior evidence. The receiver's 45 source checks remain source evidence only. Because all nine selectors fail in setup, no comparison assertion is reached in this run; it is incorrect to grant nine behavior or full-scope credit.

## C0/privacy hold

The route preserves the C0 request authority and the accepted/merged, conflict, invalid, and preview reply boundary at Runtime. This review publishes only source locations, hashes, selector/count facts, and the fixed failure reason. It publishes no XML/payload/auth/keys/URLs/frames/raw private paths/private identifiers. D130 SWAP/WAL/recovery/full-tour holds remain untouched.
