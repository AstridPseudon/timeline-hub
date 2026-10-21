# REQUEST CHANGES

Reviewed `8e7b828d5dbe2f0356d5b63047c20697d961b583` (`b32d35b0d08b97d3f822e84c3bc946cc69e851cf`), source-only. Changed paths are `astrid/packs/video_editing/shared/draft_voiceover.py` and `tests/packs/video_editing/test_draft_voiceover.py`.

## Blocking findings

1. **Outer producer authority is a newly invented, caller-settable attribute.**
   `_trusted_outer_producer()` at `draft_voiceover.py:555-577` accepts any mapping assigned to `client.trusted_execution_context`. `rg` finds this attribute only in the changed shared code and its fake tests; `AstridClient` does not define it, and `AstridClient.open_from_launcher()` returns the ordinary client without installing it. The normal action wrapper at `actions/sync_draft_voiceover/run.py:54-67` supplies no authenticated host context. Therefore this is neither an existing host-authenticated carrier nor a proof of the outer task/attempt; a caller can set the five strings/integers and mint the producer pin. The current normal action actually fails at this check after doing the expensive preparation. Keep this refused until a host-owned/private adapter injects an authenticated immutable context; do not treat a client attribute or inner Speech identity as authority.

2. **The outer action and requester outbox flow are not implemented or qualified.**
   `run.py:52-70` still returns only `report`/`receipt`; it does not settle a declared `timeline/authoring-proposal` managed output and does not call `TimelineSession.queue_proposal()`/`flush()`. `pack.yaml` still declares only `report` and `receipt`. The shared function returns an in-memory `authoring_proposal` at `draft_voiceover.py:698-699`, but no requester owns it, persists its original base, forwards the exact first guard, retries a persisted flight, or performs guarded undo. Thus the required outer producer custody is not executable.

3. **The genuine Runtime media-selection proof is absent.**
   `runtime_synthesizer()` verifies the manifest text/hash and hashes bytes read at `draft_voiceover.py:456-462`, which is a useful byte check, but it never obtains the Runtime-authoritative exact five-field `MediaSelection` or verifies the settled publication/association against it. `_settled_media()` at `489-511` accepts selection, duration and positive `size` from `result['output']`, `result['media_selection']`, or the copied managed-output row. It only checks that `object_id` equals the returned audio digest; it does not tie `generation_id`, `variant_id`, `catalog_digest`, intrinsic duration, or size to an authoritative Runtime selection read (nor compare size to the bytes). The old-media path at `678-687` similarly trusts a candidate `size` and locally derived clip duration. The pure native capture enforces the five-field shape, but cannot establish Runtime custody. The changed coordinator tests inject a synthetic `output` row and never exercise the normal settled selection path.

4. **The refreshed-head race checks only the revision, not the admitted publication pair.**
   The initial `head`/`base_publication_id` are read at `612-615`, and the proposal correctly retains the original publication at `587-592`, but the in-flight check at `658-660` compares only `current['summary']['head_revision_id']`. Executable probe: with the changed test fixture, keep the refreshed revision at `h` and change only its publication to `pub-new`; `sync_draft_voiceover(...)` returns `proposal_ready` and emits the original `pub-h`. The final check must compare the complete `(head_revision_id, head_publication_id)` pair and preserve the original admitted pair through the eventual requester request.

5. **Existing positive behavior was converted to no-publish readiness instead of being preserved one-to-one.**
   The former `test_coordinator_publishes_once_with_provenance` is replaced by `test_coordinator_returns_outer_proposal_without_publishing` (`test_draft_voiceover.py:264-275`). The former CAS-failure assertion is also neutralized: the fake `Bound.publish()` is configured to fail, but the changed code never calls it (`249-261`). The missing-audio positive now only asserts `published == False` (`288-295`). These are not requester successes and do not preserve the prior publish/receipt/history behavior. Restore the original 22 positive expectations on their existing routes, then add a separate real requester-positive with proposal queueing, commit/retry/undo and the outer identity distinct from inner Speech.

## What is locally sound but insufficient

`_build_voiceover_proposal()` computes the existing digest over the six-key proposal shape, and `build_producer_batch()` creates the existing first `producer.guard`; the proposal/guard contract neighbors pass. That proves only local construction, not authoritative outer settlement or exact outbox forwarding. `capture_draft_voiceover()` remains a pure native lowering helper and its exact source/timing checks are not a substitute for the required Runtime selection and host-custody proof.

## Evidence

- `/home/user/work/venv-agent/bin/python -m pytest -q tests/packs/video_editing/test_draft_voiceover.py` — **23 passed**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/video_editing/test_draft_voiceover.py tests/sdk/test_timeline_producer_guard.py tests/sdk/test_timeline_native_frontends.py` — **50 passed**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_settled_proposal_contract.py tests/sdk/test_timeline_producer_guard.py` — **82 passed**.
- Read-only probes reported `AstridClient` has no `trusted_execution_context`, the wrapper source contains no `queue_proposal`, and same-revision/new-publication refreshed state was accepted as `proposal_ready`.

No full/live/contract-generation suite was run. No repository files were changed by this review.

## Minimal repair / next step

Provide a host-authenticated outer context through an existing or explicitly private host adapter, obtain the exact Runtime five-field selection plus intrinsic duration/byte/source proof, compare the full original head pair, declare/settle the outer `authoring_proposal`, and hand that unchanged proposal to the existing `TimelineSession` outbox. Then restore the 22 original positives and add the one normal requester success with lost-ack/restart retry and guarded undo. The required action/host composition and exact native proof remain unqualified.
