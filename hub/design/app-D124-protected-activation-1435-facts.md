# D124/D126 protected activation facts

Verdict: `PASS_PROTECTED_ACTIVATION`.

The current App head is `84857c45347539c7820bb054b69e2e5ad4079081`, tree
`7feb5b12a1ad9629f096700c40c393d5b3998217`. The worktree remained clean and
no App source, test, assertion, guard, environment-policy, package, profile, or
generated file was changed.

Both authorized controls used Node v20.19.4 and completed a fresh Runtime
lifecycle. Each selected exactly two tests and passed both, with 40 unrelated
tests skipped and zero failures. The normal control had helper overrides unset.
The reviewed control used only the D66 helper path and SHA override, with the
canonical basename `p2_commit_phase_capture.py` and SHA256
`6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760`.

The reviewed capture had 102 rows, was not truncated, retained all 102 events,
and stayed below the 128-event/65,536-byte bounds. It recorded observed
accept, authorization, coordinator admission and lock, dispatch queue, handler
entry, provider, receipt, and HTTP response phases. Sampling used the 20 ms
interval with bounded denominators; sampler errors were empty. Unsupported
boundaries remained explicitly marked as unsupported rather than inferred.
The normal capture likewise retained 102/102 events without truncation.

Raw captures stayed private with mode `0600`. Published evidence contains only
safe counts, phase names/status, bounds, unsupported-boundary declarations,
tool/source hashes, and verdict metadata. It contains no raw request, auth,
idempotency key, private URL, or stack export.

The request-correlation limit remains unchanged: public HTTP `request_id` and
logged service diagnostic `request_id` are distinct sources. The existing
lowercase SHA256 of the exact `Idempotency-Key` bytes is an exact browser/helper
join only when those bytes match; it is not an exact join to current service
error logs because those logs do not carry the key hash. No equivalence was
invented and no Runtime correlation change was made.

No full, original/P2/browser/native, or broad suite was run, per task
instruction. Full-tour authorization remains a manager decision after this
independent protected activation PASS.
