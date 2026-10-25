# D72(2) ledger-entry proposal: D103 CLI trim/move media setup

## Scope and source identity

- Writable source delta: `tests/editing_conformance/test_cli_trim_runtime.py` only.
- Original source blob: `c1899ab070` (the `tl/integration` file before this
  worker's delta).
- Candidate source blob: `793ab7efc7` after the source-only patch.
- Genuine media source: tracked
  `tests/fixtures/reshape/hype_regression/main.mp4` (Git blob
  `c54c64cdc532ef4d08752ee01983966e58726531`; SHA-256
  `a13a68e512b6fae7fa4edd71b68266b33d1f7581be3fa199031809ec14d2f95e`).
- The fixture is an ISO Base Media MP4. Its repository media manifest declares
  `expected_duration_seconds: 42.0`; the test reads the exact bytes at runtime.

## Exact containment audit

All values below are rational seconds. No float residue, epsilon, clamp, or
rounding guard was added; authored values in the test are unchanged.

| live sequence | source window(s) | occurrence ends reached |
| --- | --- | --- |
| trim, disjoint peer | `[1, 6)`, then `[1, 5000001/1000000)`, dependent `[1, 4)` | `5/2`, `4000001/2000000`, `3/2` |
| trim, relevant peer | `[1, 6)`, then `[1, 5000001/1000000)`, conflicting peer `[1, 3)` | `5/2`, `4000001/2000000`, `1` |
| move | `[1, 6)` | initial `5/2`, moved `3 + 5/2 = 11/2` |

The retained text title is non-media and ends at `5 + 1 = 6`. The genuine
video's declared 42-second duration contains the largest source endpoint `6`
and largest occurrence end `11/2`.

## Unchanged predicate/input map

- `from=1`, `to=6`, `hold=5`, `speed=2`, `app.astrid.for=2.5`, row identity,
  track, opaque values, and the explicit registry duration setup remain.
- All three selectors remain live: the two `relevant_peer` parameter cases of
  `test_cli_trim_exact_retry_restart_dependent_suffix_and_peer`, plus
  `test_cli_move_exact_retry_restart_and_undo_over_real_http`.
- Trim/move command inputs, lost-ACK handling, exact retry, restart, peer
  conflict/rebase branches, dependent suffix, inverse/undo, history,
  publication, canonical-document, physical-identity, and no-write assertions
  are unchanged.
- Only the invalid PNG media object setup changed: exact genuine MP4 bytes,
  `video/mp4`, and the matching `.mp4` original name. No product/schema/guard
  or shared seed changed; the former `PNG` constant had no callers outside
  this file.

## Current route and proof recipe

The fixture uses the existing `runtime` fixture's in-memory HTTP transport and
current Runtime service. The setup path is
`service.import_media` -> media selection -> verified media ->
`capture_clip_add_media` -> `TimelineSession.commit`; commit handling remains
the registered `commitTimeline` provider path. No synthetic history, pins,
manual SQL, CAS authority, or admission bypass is introduced.

Meaningful MAIN3 recipe after protected review: run the three original
selectors unchanged on the integrated Agent/Runtime route, covering both trim
parameter cases and the move case; retain the existing exact-retry,
lost-ack/restart, peer, dependent, inverse/undo, history, and no-write tails.
