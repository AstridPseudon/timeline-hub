# P1 custody review

Result: **PASS_CUSTODY_TEST_PASS**.

No custody finding was identified. The review independently loaded `dispatches[5]`, matched the recipe hash, builder SHA/blob, exact four detached clean pin pairs, 12 pin fields per recipe, exact command/row hashes, genuine preflight and normal IDs, raw `KEEP` markers, request/snap/status/exit files, XML counts, and the same-ID wait.

The normal body result is the original `32161` only: two P1 cases passed, with one readiness case. The accepted path includes split, dependent trim, intervening Agent edit, lost acknowledgement, reload/restart, exact retry, merged reply, drained outbox, history cardinality, and zero legacy traffic. The refusal path includes a real Agent move, stale trim conflict details, rollback/message, canonical-parent equality, history cardinality, and zero legacy traffic.

Limits retained honestly:

- No product, browser, service, full-suite, private-control, typecheck, or lint rerun occurred.
- An older `867cb273` P1 result was present but is a different historical target and was excluded; it was not retargeted or repeated.
- The reviewer’s first sampler shell command failed to parse before side effects; the corrected foreground sampler ran from the second tool invocation, produced three samples, and was explicitly stopped/reaped. This does not alter the author’s native custody or terminal result.
