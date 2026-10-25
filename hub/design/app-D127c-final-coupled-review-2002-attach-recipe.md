# Attach and source-review recipe

This is a read-only recipe for the next authorized repair/review. It is not an activation recipe and was not executed against a live body here.

1. Pin Runtime to commit `368f53f4454d5908c86de53d174f0bedcf23781c`, tree `8d5683702f36034f27ee7f49737665d66dbc2b75`; verify `tests/helpers/p2_commit_phase_capture.py` SHA-256 is `095c252b...` and `tests/test_p2_commit_phase_capture.py` SHA-256 is `ee789ec1...`.
2. Pin App to commit `6c0329334797b42565918114f2e760a606b026b6`, tree `8b9a12d2d77708d260db8a9bd6b9fadff611bf44`; verify the final validator blob SHA-256 is `558963eb...`.
3. In `tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`, repair only the source-pin branch so the final helper hash has an explicit reviewed-profiler branch with basename `p2_commit_phase_capture.py`; retain all old arms and exact helper allowlist. Do not broaden acceptance to arbitrary hashes.
4. Run the normal D66 source guard with a private TMPDIR child, checking helper basename/hash, sink 0600, directory 0700, no helper filename leakage, and the existing lifecycle phases. Keep the final body unqualified until this passes.
5. Run the bounded no-live validator controls: supported Node20 profiler-only positive/mutation node and the existing Node22 reviewed-profiler/reviewed-new pair. Do not rerun the known-hanging combined Node20 pattern unless a later decision explicitly requires it.
6. Reuse Runtime central request `30318`; do not resubmit it. Any product or source repair belongs to a separate authorized task, not this evidence-only review.

Actual mounted path reconstructed from final blobs:

`ElementsLibraryPanel.applyElement` → `elementOperationAdapter.execute` → `createElementTimelineRoutes`/`useTimelineSave` → `createLocalSaveSession.send` → `RuntimeDataProvider.commitTimeline` → generated `POST /v1/projects/{project_id}/timelines/{timeline_id}/commit` with `Idempotency-Key`.

The first element request shape is `source.via=app`, one `doc.patch` command, one `list.insert` change with `elementRef`, and one `timeline.apply_element` step. Parameter edit is `doc.patch` with a different `set` shape; undo is `timeline.inverse`.
