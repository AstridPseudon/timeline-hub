# Handoff — Runtime G5 inverse boundary diagnosis

The requested bounded diagnosis was attempted once against Runtime `3b926efab2eed122d374540baee297d4cdcec62a` with Agent checkout `77ab3908fbf827fd591f077a3ef00664c073409d`.

The observer was scratch-only and proxied the real coordinator, provider, port factory, port `verify_outcome`, and port `close`, preserving arguments and execution. It flushed bounded JSONL records and module origins/hashes as each seam ran. The evidence is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-G5-inverse-boundary-diagnosis-1305/evidence/g5-observer.jsonl`

The run successfully exercised the real Agent provider through one accepted `inverse-name` `doc.patch` commit. It then stopped before the restructure request. In `astrid/sdk/timeline/publish.py:228-231`, `Checkout._commit_restructure` compares its detached `local` closure with the `TimelineSession._bundle(state)` closure and refuses with:

```text
restructure requires its exact current closure; reopen the timeline
```

Consequently, the evidence has no inverse flight, inverse receipt, inverse provider exception, port verification exception, port-close exception, or Runtime `not_ready/runtime_unavailable` traceback. This is a bounded Agent-side setup/reader-fidelity blocker, not evidence of a Runtime semantic defect.

The candidate inverse body matches the D21 `5dcf78e...` body hash. The older `b9092fe...` body differs because it predates the explicit post-refusal no-write assertions and uses the legacy fixture argument; this discrepancy is retained honestly.

Recommended next step: Agent G5 fixture/test-fidelity owner should explain or repair the exact-current-closure mismatch while preserving the exact revision/publication reader and no-write controls. Then dispatch one fresh, instrumented normal-service invocation. Runtime should not patch coordinator/provider/port code or classify the earlier 503 as Runtime-owned until an underlying exception is captured.
