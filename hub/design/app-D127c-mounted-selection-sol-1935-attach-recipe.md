D127c is source-only. Do not execute this activation until the final Runtime/App sources pass one coupled independent review and the orchestrator releases the normal/home/body hold.

The canonical helper is the regular, non-symlink file:
`/home/user/work/wt/app-D127c-mounted-selection-sol-1935/tests/helpers/p2_commit_phase_capture.py`

Its final SHA-256 is `095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d`.
The exact corrected source tree is `8d5683702f36034f27ee7f49737665d66dbc2b75`, matching the central service snapshot. The harness owns the final commit; its SHA cannot exist before worker exit. Resolve and verify it afterwards through the ordinary source route (no checkout or ref mutation):

```sh
git -C /home/user/work/wt/app-D127c-mounted-selection-sol-1935 rev-parse refs/heads/tl/app-D127c-mounted-selection-sol-1935
git -C /home/user/work/wt/app-D127c-mounted-selection-sol-1935 rev-parse 'refs/heads/tl/app-D127c-mounted-selection-sol-1935^{tree}'
git -C /home/user/work/wt/app-D127c-mounted-selection-sol-1935 show tl/app-D127c-mounted-selection-sol-1935:tests/helpers/p2_commit_phase_capture.py | sha256sum
```

The supported D66 override takes an exact absolute helper plus its SHA, checks a regular non-symlink file and rejects mismatches. With the independently reviewed App bootstrap-test arm and approved normal D66 cohort in place, the existing source recipe is:

```sh
D66_P2_COMMIT_PHASE_CAPTURE_HELPER=/home/user/work/wt/app-D127c-mounted-selection-sol-1935/tests/helpers/p2_commit_phase_capture.py \
D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256=095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d \
D66_OUTPUT_DIR="$TMPDIR/d127c-approved-element" \
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node \
  --import tsx scripts/testing/d66-plain-stack.mjs p2-element --submit
```

Run location is the reviewed App checkout. This recipe intentionally inherits the orchestrator's approved cohort heads/trees/source checkouts; it does not replace pins or authorize a body run. D66 forwards the reviewed helper identity to the existing harness. The harness adds scripts/testing to the Runtime child's PYTHONPATH and sets ASTRID_P2_COMMIT_PHASE_CAPTURE=1, the private phase sink, and the exact helper path. sitecustomize loads this canonical basename before the normal `python -m runtime_protocol.cli start` worker starts, constructs `P2CommitPhaseCapture(..., enabled=True)`, and stops it at exit. Its thread trace observes the actual HTTP server thread; no alternate collector/server/entrypoint is installed. The helper is inactive unless explicitly enabled and started. Default D66 activation does not request raw pstats; optional raw output is a separate constructor setting, confined to an existing owner-only 0700 non-symlink child of TMPDIR with exclusive 0600 file creation and no shared-parent chmod.

The source-backed mounted path at App d5a1d1ab6550187e377fd7387d300102b8b82ece is:

- VideoEditorProvider owns and registers AstridElementOperationAdapter with the live useTimelineSave elementTimelineRoutes and authority guards. ElementsLibraryPanel.applyElement calls its captured adapter's timeline.apply_element operation (effect placement overlay).
- element-adapter appends a clip with id/at/track/clipType/hold/elementRef. useTimelineSave saves via the mounted local owner. timelineLocalSaveHandoff verifies the original causal operation and emits parent clips collection/field reads plus step intent timeline.apply_element.
- documentPatchIntent emits ONE doc.patch change: list.insert, ref parent, path [clips], before absent, id matching value.id, order_before the original ordered IDs, after_id the previous final item (null for empty), and created [parent/clip:<inserted-id>]. The value carries a pinned effect elementRef (id/kind/revision/packId); clipType equals elementRef.id. No concrete clip/catalog identity is selected by the diagnostic.
- localSaveSession is the actual local-document save branch beside the native commitSession branch. It uses the existing commitOutbox, persists the original command/step/reads/created operands, and sends through useTimelineSave's provider.commitTimeline(request,key). dataProvider.commitTimeline validates scope/base and calls the registered generated Runtime client with the same body and HTTP Idempotency-Key.
- RuntimeHandler._dispatch resets then invokes the bounded real _prefetch_body, routes through _timeline_commit, and forwards the request to runtime.commit_timeline. The helper requires live trace-established dispatch AND direct bounded prefetch completion on that handler/thread, with the same buffer identity, before arming at handler entry. Direct _timeline_commit with manually assigned bytes, or a replacement prefetch, cannot arm or consume selection.

The predicate selects only the FIRST exact insertion. It excludes params (doc.patch set at parent clips/id:<id>/params), Undo (timeline.inverse), setup/native/media requests, other handlers/routes/methods, mixed commands/changes and dry runs. A mounted element-shaped first attempt consumes selection even if mixed/dry-run, so a retry cannot become the sampled request. Profile construction/enable/disable and previous binding restoration remain request-thread scoped; failures do not alter Runtime execution. Existing request ordinal, hashed Idempotency-Key, process birth, UTC anchors and timing joins remain unchanged.

The C0 request remains api_version 1; project/timeline and base revision/publication; commands with schema_version/op/version/select/args/created; label; steps with id/label/intent/tags/command_ordinals/patch/optional reads; merge fields|atomic; reads; HTTP Idempotency-Key; dry_run; source; optional rationale/group_id. The observer does not normalize, drop, add or mutate any live input. Replies retain accepted|merged canonical document/digest, normalized commands, identity/revision/landing/rebased_onto/merge_mode, durable receipt, records/bindings/effects/dependencies/history/undo_steps; conflict reason/head; invalid code/path/hint/suggested_command; preview would_status with null receipt. Authority, validation, guards and history remain exclusively Runtime/provider behavior.

The protected App spec's first Apply assertions are at 1038-1056; later params at 1084 and Undo at 1105. Those bodies and waits were not changed or run. The mounted Runtime unit tests prove selector/provenance on the genuine dispatch/handler methods with a stub commit port; they do not qualify the live element/provider/browser body. No raw request, IDs, keys, credentials, URLs, locals, exception text, raw stacks or pstats are published in this packet.
