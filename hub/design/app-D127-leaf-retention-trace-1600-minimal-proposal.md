# D127 minimum existing-helper proposal

Disposition: do not author a leaf-cost conclusion and do not activate another profile from the current packet. The current helper safely retained the exact pending request, but its inclusive top-10 projection censored the useful leaf and the request never reached a completed provider/response boundary.

## One seam revision, before any activation

Make one bounded revision to the existing `tests/helpers/p2_commit_phase_capture.py` helper only. Keep the current trace hooks, 20 ms sampler, watchdog, request-local buffer, rolling ring, private sink, and source hash pin. Do not add a Runtime hook, App collector, browser probe, request-body capture, raw stack publication, or new persistence route.

The revision should make these explicit, using the same safe-frame observations already available:

1. Maintain one nearest-safe-frame counter per sample (`leaf_counts`) in the existing per-request counter state. Publish at most ten `top_leaf_frames` rows, with the same `sample_total`, `lost_samples`, and optional dispatch-wall share fields. Retain the existing `top_inclusive_frames` rows for continuity. If no safe leaf exists, publish an explicit empty/UNKNOWN projection. This prevents routing wrappers from consuming the only ten rows without claiming that the leaf was expensive.
2. Separate lifecycle state from byte retention. Keep the request-local buffer priority and 64 KiB bound, but label its current `complete` meaning as buffer-complete (or add an equivalent `buffer_complete` field). Add a terminal state with only these truthful outcomes: `completed` (response observed), `raised` (request-scope exception observed), `returned_without_response` (dispatch returned but no response hook), and `pending_at_stop` (capture stopped while dispatch was active). For an active request, record only elapsed observation-to-stop time if useful; never call it handler duration or request-wall duration. Keep provider, response, and final duration UNKNOWN when their end hooks were not observed.
3. Preserve teardown behavior: cancel the request-owned watchdog before finalization, mark a live request `pending_at_stop`, and flush the final snapshot after summaries. Record a request-scope raised/aborted return separately from a normal dispatch return; a connection/cancellation path without a response must not be classified as `complete`. The existing helper must remain unable to replace the original operation exception.

## Required acceptance of that revision

- Exact joined request remains bound only by key hash plus namespace/PID birth/request/UTC tuple.
- Existing `max_requests=8`, `max_events=128`, `max_bytes=65536`, watchdog cap, and 0600 sink limits remain unchanged unless a protected review explicitly re-approves the original budgets.
- Output contains counters, safe relative frame labels, phase names, statuses, and hashes only. No raw frame dump, body, header, key preimage, credential, private URL, or new raw/private publication.
- Existing offline tests in `tests/test_p2_commit_phase_capture.py` cover buffer priority, byte-limit incompleteness, pending shutdown, raised/aborted teardown, watchdog cancellation, and the new leaf/lifecycle projection. No live/socket/browser/profile rerun is part of this proposal.
- The App caller remains the mounted IndexedDB outbox -> registered Runtime provider -> canonical generated-client POST. C0 request/reply fields, idempotency, auth, previous-value/ABA behavior, and no-write behavior are untouched.

This is a diagnostic qualification seam only. A bounded author and protected review must approve the helper revision and its source/hash custody before any helper activation. It does not establish provider dominance, native-vs-Python cost, final duration, SWAP outcome, or product readiness.
