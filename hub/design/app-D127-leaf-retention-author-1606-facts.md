# D127 facts

- Base Runtime: `453b3e6f92045980219ec4948419ee5ad25c817d`.
- Only the two authorized files changed.
- The helper now counts the nearest safe frame per 20 ms sample in `top_leaf_frames`, while retaining `top_inclusive_frames` and the existing allowlist.
- Lifecycle output is observed-only: `completed`, `raised`, `returned_without_response`, or `pending_at_stop`.
- `buffer_complete` is separate from lifecycle; the existing `complete` field remains its compatibility alias for buffer completeness.
- Raised and pending requests do not receive inferred handler or request-wall durations.
- Existing max requests/events/bytes, rolling/request buffers, watchdog cancellation, 0600 sink, hashes, PID birth, UTC, request binding, privacy boundary, and unsupported boundaries remain unchanged.
- Prior element 10721 history remains honest: request 3 had 352 samples, 3 lost samples, last phase `authorization`, and no provider leaf, response, wall denominator, or final duration.
- No product hook, collector, activation, body capture, raw-frame publication, schema, pin, or generated file was changed.
