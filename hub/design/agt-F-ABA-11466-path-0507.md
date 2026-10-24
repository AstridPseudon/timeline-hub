## Report

- Read PLAN §3 and `contract/commit-v2.md`; no product edits made. Worktree remains clean.
- Traced the production path:
  - `timeline_document.emit_document_publish_commands`
  - `capture_occurrence_swap_media`
  - `TimelineSession.commit_many`
  - `TimelineSession.undo` → `_flush` → Runtime commit.
- Source owner: `astrid/sdk/timeline/native_occurrence_media_commands.py::_replace_payload_media`.
- Candidate cause: this seam emits numeric-index paths such as `payload/items/<index>/media_id` and `payload/assets/<index>/...`. Runtime’s strict `location()` accepts only uniquely identifying item paths; it rejects missing identity tokens or non-unique matches with the observed “ambiguous item path” conflict. This is a static causal hypothesis, not proof of the actual failing path.
- Bounded existing seam: emit one complete changed collection (`payload/items`, `payload/assets`, or `payload/audio_bindings`) rather than numeric leaf paths, or explicitly normalize and validate unique item identities before emitting identity-token paths. No Runtime waiver or byte-equivalence fallback is appropriate.
- The existing forwarding machinery does retain source-level original/landing records through `commands.execute → Closure → private capture`; however, the manager-copied 11466 artifacts do not retain the actual failing private capture, native packet, exact path, bindings, or Runtime response detail. Therefore the actual duplicate/missing identity condition cannot be distinguished from the traceback alone.

### Tests

Not rerun by this worker, per task restrictions. Existing service artifact reports:

```text
tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba
1 failed in 29.28s
```

Failure: `test_authoring_media.py:1088`, `TimelineSession.undo`, Runtime `CommitConflict: provider observation has an ambiguous item path`.

No full suite, live probe, browser run, or additional original/body run was performed.

Required commit message and `DONE` marker were created.