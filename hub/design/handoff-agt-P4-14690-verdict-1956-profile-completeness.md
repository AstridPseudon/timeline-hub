# Profile custody and completeness

- Raw handler profiles: 54 files, 54 unique SHA-256 values.
- Merged profile: `handlers.prof` present.
- Events: 111 lines; 54 `handler_begin` and 54 `handler_end` records with
  matching sequences, one profile per end event.
- Actual handler origin: `runtime_protocol.server.RuntimeHandler._dispatch`,
  `/home/user/work/wt/rt-pin-e89eb8c7/runtime_protocol/server.py:1171`.
- All observed handlers used one PID and one calling thread. The two daemon
  instance IDs are retained as captured; no daemon substitution is inferred.
- Selected handler/server/service/caller module hashes matched before/after:
  server `aa82d81b…`, service `94591ec2…`, store `a2db29e4…`, port
  `0d44b5a5…`, Agent commit `6c2fc6c8…`, runtime client `d095328f…`.
- The full import inventory was 122 modules before and 124 after; only lazy
  Agent modules `_selected_param_authority` and `commit_session` were added to
  the after inventory. This is recorded, not treated as a source mutation.

Authoritative XML outcomes and durations:

| selector | outcome | duration |
| --- | --- | ---: |
| `test_cli_sheet_v2_runtime_preserves_document_and_reads_back` | PASS | 2.821s |
| `test_http_ten_note_commit_per_step_inverse_and_redo` | FAIL: `p4-ten-note-undo-note-01`, `error_type=Failed` | 45.407s |
| `test_http_note_conflict_reruns_public_function_from_verified_peer_document` | PASS | 9.630s |

Captured profile method-entry totals are not receipt totals: history 71,
`_verify_accepted` 64, accept calls 1, and `commit_timeline` calls 2. The
shared initial ten-note commit is one shared boundary: history 5, verify 6,
accept 1, commit 1, wall 3.553s. `undo-note-01` is a separate boundary:
history 49, verify 48, accept 0, commit 1, wall 33.992s, `error_type=Failed`.
No per-note allocation of the shared commit is made, and no later redo/note
operation is claimed.

The existing merged-pstats top ten was recomputed read-only and matched the
producer's `profile-facts.txt`; this review does not interpret it causally.
