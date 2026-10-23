# G4/R5 requester handoff (Agent → Runtime)

Status: PASS for the Agent requester interface mapping; NOT an R5 readiness or
Runtime behavior qualification.  This is the handoff for Runtime peer 0354.

## Exact source identities and adoption requirement

- Agent usable source: `5f0fb2edb72aae37ba86e3ffe28f5e79b63aa026`
  (`feat(timeline): compose G2 G3 and G4 current join`).
- Runtime normal dependency: `normal34e` = checkout
  `/home/user/work/wt/rt-pin-34eac004`, commit
  `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Runtime behavior reference, read-only: `ad823e0a0f5be4a7acf1d3006df6f794709da63d`.
  This is the exact Runtime source used for the original publication tests.
- Independent source join `0401` is active; this handoff does not claim that it
  has been merged.

Runtime should port the old publication authority/fence/target/restart/render-pin
semantics onto the normal `commitTimeline` requester path at normal34e, using
the exact ad823 test inventory below as the behavior checklist.  Do not use an
all-410 substitute, alternate executor, mock provider, or the retired
`publish_timeline_render` body as the replacement.

## Public Agent entrypoint and call order

The production caller uses this path:

1. Open the authenticated, scoped requester session:

   ```python
   TimelineSession.open(
       project, timeline, *, client=client, outbox_path=None,
       base_revision_id=None, base_publication_id=None,
   )
   ```

   The session binds realm/actor/project/timeline, pins the revision/publication
   pair, and persists an outbox flight before sending it.  A restarted session
   uses the same outbox and exact flight body/key.

2. Before registered assembler work, freeze the target and ordered child
   closure:

   ```python
   session.admit_assembly(
       child_outputs, *, replace_clips, assembler_digest,
       idempotency_key, rationale="Assemble ordered child visuals",
   )
   ```

   This captures `admitted_target` (`project_id`, `timeline_id`,
   `base_revision_id`, `base_publication_id`) and exact managed child
   association/object/version/media pins.  `queue_assembly(task_id,
   *, attempt_id)` reads exactly one settled native proposal and queues it at
   the admitted base; it calls `read_assembly_proposal` and then
   `queue_proposal` unchanged.

3. The supported production publication entrypoint is:

   ```python
   publish_authoring_proposal(
       client, *, proposal, timeline_id, expected_version,
       runtime_attempt=None, render_capability_digest,
       output_name="hype.mp4", selector="rendering.ffmpeg",
       idempotency_key, requester_session=None,
       label="Assemble timeline", steps=None, merge="fields",
       reads=None, dry_run=False,
   )
   ```

   It requires the original `requester_session`, the same client and timeline,
   and a proposal whose admitted target is in that session's scope.  Its order
   is exactly:

   ```text
   requester session + settled proposal
     → client.tasks.publish_timeline_render(... requester_session=session ...)
     → commit_assembly(session, proposal, ...)
     → normal commitTimeline through the session outbox
     → if non-preview, admit rendering.render pinned to accepted revision /
       receipt publication / canonical content digest
   ```

   `publish_timeline_render` above is the Agent transport adapter name.  It is
   not permission to retain Runtime's retired HTTP publication writer.  The
   adapter validates the exact producer attempt and delegates to
   `commit_assembly`; Runtime is the writer.

4. Video Editing's production wrapper uses the same entrypoint:

   ```python
   publish_stitched_render(
       client, *, project, timeline_ref, expected_version,
       config=None, registry=None, proposal=None,
       requester_session=None, label="Assemble timeline", steps=None,
       merge="fields", reads=None, dry_run=False,
       output_name="hype.mp4", selector="rendering.ffmpeg",
       runtime_attempt=None, render_capability_digest=None,
       idempotency_key,
   )
   ```

   The wrapper requires `proposal`, `requester_session`, and
   `render_capability_digest`; it rejects legacy `config`/`registry` payloads
   for native assembly.  The production caller uses this wrapper in
   `astrid/packs/video_editing/shared/runtime_orchestration.py`, which calls
   `publish_authoring_proposal`.

## Request/reply preservation requirements

The normal request sent by `TimelineSession` must retain the complete v2
request, with no field filtering: `api_version`, `project_id`, `timeline_id`,
`base_revision_id`, `base_publication_id`, `commands`, `label`, `steps`,
`merge`, `reads`, `dry_run`, `source`, `rationale`, `group_id`, and stable
idempotency.  Each step retains `id`, `label`, `intent`, `tags`,
`command_ordinals`, `patch`, and any declared reads.  Commands include the
producer guard followed by the settled proposal commands; the producer guard
retains attempt, fence, runtime epoch, admitted target, and render/media pins.

Every successful `{data, receipt}` must retain the authoritative canonical
document/head/revision/digests, records/effects, steps/dependencies,
history/undo_steps, and accepted/merged status.  Historical accepted
`rebased` receipts remain authentic and replay unchanged; new disjoint-head
success is `merged`, with `rebased_onto` retained where present.  A conflict
retains reason and head.  An invalid result retains code, path, hint, and
suggested command.  Preview retains `status: preview`, no receipt, and
`would_status` of `accepted` or `merged`.  Do not drop fields when the render
admission envelope is built; the render pin is derived from the accepted
canonical revision/publication/content digest.

## Agent fixture and test nodes Runtime can port

The exact source fixture is in `tests/sdk/test_timeline_render_publication.py`:
`requester(tmp_path)` calls the assembly fixture
`tests/sdk/test_timeline_assembly.py::_requester`, `_admit`, and
`proposal_for`; it then installs exact settled task/output/association/object
reads on the transport, wraps the transport with `RemoteTasks`, and spies on
`tasks.admit`.  The generated transport fixture is deliberately only a
transport-boundary fake; it is not Runtime proof and must not become an
alternate provider.

The publication helper is the exact normal call shape:

```python
def publish(session, proposal, **options):
    return publish_authoring_proposal(
        session.client, proposal=proposal, timeline_id="t", expected_version=1,
        render_capability_digest=DIGEST, output_name="chain.mp4",
        requester_session=session, idempotency_key="publish", **options,
    )
```

Agent seam tests (all in `tests/sdk/test_timeline_render_publication.py`) are:

- `test_registered_requester_commits_original_target_then_admits_exact_renderer`
- `test_requester_lost_commit_ack_retries_identical_v2_flight_after_restart`
- `test_lost_render_ack_replays_original_acceptance_after_peer_head_moves`
- `test_preview_never_admits_renderer_or_advances_base`
- `test_runtime_refusal_keeps_full_structured_details_and_never_admits_render`
  (both `conflict` and `invalid` parameters)
- `test_video_editing_production_wrapper_uses_requester_commit`
- `test_accepted_retry_never_rereads_mutable_producer_lifecycle`
- `test_v2_authoritative_fields_survive_the_publication_envelope`
  (preview and commit)
- `test_original_step_reads_and_tags_are_sent_without_filtering`
- `test_landed_peer_state_and_original_merge_spelling_survive_replay`
  (both `merged` and historical `rebased` spellings)

The preceding assembly admission nodes are in
`tests/sdk/test_timeline_assembly.py`:

- `test_admission_freezes_original_target_and_ordered_associations`
- `test_lost_admission_ack_reuses_durable_body_without_recapture`

Targeted Agent result: **15 passed** for these two files.  This confirms the
requester seam and fixture shape only; it does not execute live Runtime render
bodies or claim Runtime readiness.

## Exact ad823 Runtime scenario map

`ad823e0a` collects 20 nodes: 17 authority nodes in
`tests/test_timeline_render_publication_authority.py` and 3 publication nodes
in `tests/test_timeline_render_publication.py`.  The authority parameter set
has nine malformed-target cases, so the 17 count is intentional.

### Authority suite (17 collected nodes)

Port these to normal requester `commitTimeline` plus ordinary exact-revision
render admission, preserving refusal-before-write and scoped authorization:

| ad823 node/scenario | Normal-path assertion |
| --- | --- |
| `test_tracked_target_refuses_without_invalidating_canonical_history` | A tracked canonical target cannot be overwritten by the old publication body; requester commit/CAS must refuse without changing head/history, and no render is admitted. |
| `test_existing_same_project_unadmitted_target_refuses_before_checkpoint` | Same-project but unadmitted timeline is a target mismatch; no checkpoint/publication write. |
| `test_missing_or_malformed_admitted_target_fails_closed[publication0]` through `[publication8]` | All nine `{}`, `False`, `[]`, string, null/empty timeline, and incomplete admitted-target forms fail closed with structured invalid/refusal details before writes. |
| `test_inconsistent_native_target_cannot_override_legacy_admission` | Authority comes from the originally admitted target/producer guard, never a worker-supplied replacement target. |
| `test_corrupt_immutable_spec_cannot_supply_target_authority` | A corrupt/missing immutable producer admission cannot authorize a commit or render. |
| `test_canonical_tracking_after_prepare_refuses_before_publication_writes` | A head/CAS change at the acceptance seam refuses atomically; no publication/render side effect is left behind. |
| `test_exact_published_checkpoint_replays_before_live_target_changes` | Exact idempotency replay returns the durable original `{data, receipt}` after live task/spec/target changes; changed body under another key refuses. |
| `test_tracking_is_scoped_to_the_publication_target` | Project/timeline scope is preserved; another timeline's head cannot affect the target render pin. |
| `test_legacy_head_without_canonical_publication_remains_publishable` | Preserve the explicitly supported legacy-head compatibility case while landing through the normal commit route, not by reviving the old writer. |

### Publication suite (3 collected nodes)

These are the exact ad823 nodes in
`tests/test_timeline_render_publication.py`:

- `test_publication_is_fenced_atomic_and_exactly_replayable`: producer lease
  fence and attempt identity are authoritative; accepted commit is atomic;
  render is admitted only with the exact accepted revision/publication/content
  digest; identical retries replay without a second publication/render task.
- `test_prepared_checkpoint_cannot_publish_after_cancel_or_stale_fence`:
  stale fence and cancellation at the acceptance seam refuse; canonical head,
  publication record, and render task remain unchanged.
- `test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart`:
  a prepared/incomplete operation resumes after Runtime restart with the
  recovered attempt fence and creates exactly one render task.

The ad823 reference was inspected with `git show`; no Runtime render bodies
were executed for this handoff, per brief.

## Actual gap and boundary

The Agent side has the requester entrypoint, exact outbox/restart behavior,
producer guard construction, full v2 envelope forwarding, and render pin
construction.  The actual missing replacement behavior is Runtime-owned: the
17 authority cases and 3 fenced publication cases still describe the old
`publish_timeline_render` service route in ad823.  R5 must port their
semantics to the normal `commitTimeline` producer-guard acceptance plus
ordinary render admission, including the atomic seam and exact replay.  A
route-wide refusal alone is not a replacement, and this handoff does not claim
that it is.  No alternate executor/provider or mock-based substitute is
proposed.

No Agent product, client, pin, render, browser, full-suite, or native14 edits
were made.
