# M2 writer bundle 3: render producer contract

Design + feasibility only, 2026-10-20. Governing decisions: PLAN §4.1/4.2,
Agent INBOX “render-producer-authority”, deletion ledger D13. Reviewed Agent
`fc324e838fd668fc06cae906e8bcfccace86ad62`, Runtime
`9f9b25c000485e919f30f1411831fe2d5a3c1316`.
**Old endpoint 410 HELD; all M2 integration merges HELD pending PLAN's M1 record.**
No product code, schema, endpoint, permission, DTO, table or generated client changes here.

## Next implementation slice (one screen)

1. Agent: extend bundle 2's official media insertion to the **parent** owner and
   a separately reserved asset alias. Reuse create-or-require registration;
   preserve `derive_clip_id` / `derive_asset_key` and ordinal order. Do not copy
   R4's registry upsert or let selection's variant ID replace the reserved alias.
2. Agent: add a versioned, deterministic **replace-assembled** command as the
   explicit populated-target intent. It uses the same insertion primitive and
   records the exact removed authored content. No generic whole-document save.
   Unsupported target shapes refuse with the original proposal retained.
3. Agent + Runtime: prove a proposal reaches the **existing caller-authorized
   parent** while the assembler attempt is still live, then `commitTimeline`
   revalidates its authority dependency inside acceptance. This delivery seam
   and guard are absent today: they are prerequisites, not a claimed capability.
4. Agent: add captured batch queueing (the public session currently exposes
   move/inverse), and make ACK handling durably retain the accepted receipt and
   pending revision-pinned render before clearing the command flight. Reuse the
   outbox writer and existing separated task prepare/dispatch. Keep the exact
   admission until its task/run locator is durable. No second journal.
5. Runtime owns the render admission retry regression/fix. Only after the recipe
   below passes may the real host hook and exported publication helpers switch;
   only then can D13/old 410 retire. This task requests no integration merge.

## Verified lifecycle and concrete seams

Paths below are relative to the named checkout; Agent is
`/home/user/work/wt/agt-m2-render-producer-plan`, Runtime is `/home/user/work/runtime`.

| Seam | Existing behavior / required reuse |
| --- | --- |
| Runtime `runtime_protocol/store.py:_admit_continuation` | Two ordered dependency edges; completed children materialized once into `continuation_admissions`. Outputs retain settlement descriptors; unique CAS input list alone cannot represent duplicate child media. |
| Agent `astrid/packs/rendering/actions/assemble_timeline/run.py:build_authoring_proposal`, `_candidate_outputs` | Exactly ordinal 0/1, distinct task IDs bound to succeeded fenced edges; one primary video each. Ignores `is_primary:false` and metadata `status:superseded`; rejects ambiguity. Child completion/list order does not choose clip order. Emits visual track, clips at 0/first duration, source [0,duration), two continuation-derived clip IDs and two asset aliases even for identical media. Registry entries include media ID, unprefixed SHA, type, duration, `origin:immutable-public`. |
| Agent `astrid/core/execution/generic_host.py:run_task`, `_publish_assembled_timeline` (~8401, 9632) | Validates attempt-local proposal path; target/version/render come from immutable admitted spec, not proposal labels. Calls publication **before** uploading/settling assembler outputs; lease pump still runs. Key is `timeline-publication-<author task ID>`. |
| Runtime `runtime_protocol/service.py:publish_timeline_render` (~7613) | Checks worker/executor identity. Exact published checkpoint replay wins before live lease checks, even after cancellation; changed semantic payload refuses. Unfinished work checks lease/fence/epoch, running/current attempt, admitted two-child continuation and target project; prepares durably, rechecks after prepare, then atomically updates projection config/registry/version, creates frozen render task and publishes checkpoint. It does not create an EditCommand parent revision/history. |
| Agent `astrid/sdk/invocation.py:_invoke_local_orchestrator`; `astrid/packs/video_editing/shared/runtime_orchestration.py:admit_runtime_handoff`, `admit_runtime_stitch`, `read_runtime_events` | Existing parent stays in the caller process and uses its connected client for child admission. Route approvals/proposals through that parent, with its actual authenticated actor/project. The stitch helpers are supported seams, not proof of a live end-to-end coordinator loop: repository search finds no production caller of `admit_runtime_stitch` or `publish_stitched_render`. |
| Authority | `RuntimeProtocolClient.WORKER_SCOPES` (~4412) includes worker execution/CAS, excludes `projects:write`, `tasks:write`, admin. Runtime `server.py:_timeline_commit` requires `projects:write`; ordinary task admission requires `tasks:write`. The parent must already possess those scopes; unavailable parent authority leaves a proposal pending. Never lend its credential to the worker or fabricate an owner client. |
| Official acceptance | Agent `astrid/sdk/timeline/commit.py:RuntimeCommitService.commit` -> Runtime `service.py:commit_timeline` -> `timeline_commit_execution.py:CommitExecutionCoordinator.execute` -> `timeline_commit_store.py:TimelineCommitStore.accept`. Accepted receipt lookup precedes preparation/live dependency reads; acceptance has the outer transaction. `timeline_commit_port.py:RequestCommitPort.validate` rechecks captured media there. |

## Proposed commands and guards (design names, not implemented APIs)

Use the existing `EditCommand`/`CommitRequest` envelope, `args`, recorder,
`AgentDependency(kind="authority", policy="exact", pin=<JSON>)`, and grouping.
No new top-level wire fields or provider ABI are needed by this proposal.

* Empty target: `track.create(parent, visual row)` and two official media-add
  commands in one commit. Each add captures a five-field Runtime selection,
  reserved clip ID **and independent asset alias**, fixed non-ripple start and
  source window. Registration is an insertion or an exact requirement, never an
  upsert. Media bytes remain outside deterministic command execution.
* Populated target: explicit `timeline.replace-assembled` v1, selected at parent,
  takes the approved ordered media insertions. Its schema, not an implicit diff,
  states replacement of the observed config/registry authored content. Capture
  every removed value (including unknown/null fields), collection membership and
  order, target/base publication, occupied IDs and dependencies before work.
  Preserve outer parent metadata; unsupported occurrences/shared content refuse
  until a lossless command lowering exists. Never silently append to a populated
  target, recapture against latest head, or interpret `timeline.restore` as import.
* Both routes record created track/clip/asset IDs, reads/selections, unchanged
  writes and exact media dependencies. Inverse restores removed authored bytes,
  recompiles timing and guards intervening writes including A→B→A and later
  references to newly created entities. No inverse may remove a reused binding.

The coordinator resolves each child's exact managed association through existing
`managed_output_page` / `managed_output` and
`timeline_commit_port.py:MediaReads.selection(association_id,object_id,version)`.
The result is `{asset,generation_id,variant_id,object_id,catalog_digest}`;
`RequestCommitPort.selected_media` captures it and `validate` rechecks it at
acceptance. This proves same project, durable available/promoted lifecycle,
unique registered variant and exact completed settlement provenance. An assembler
role flag, bare CAS digest, or a lookup of today's primary is insufficient. Keep
ordinary generation publication/settlement; do not synthesize missing variants.
The new test's role filter is **not** a registered-lifecycle authorization proof.

## Authority fence and durable handoff

Before sending, parent approval must bind the original head pair, proposal
bytes/digest, ordered child identities/selections, reserved IDs and render intent
in its existing outbox. Freeze exact commit bytes/key under realm/actor/project/
timeline scope. Include an authority dependency for the assembler task/attempt,
executor, fence/epoch and its admitted target/dependency snapshot. Runtime checks
the actual lease row/liveness internally; never put a lease token in history. Runtime
must verify these against real task/admission rows inside
`TimelineCommitStore.accept` through `RequestCommitPort.validate`, **after**
accepted replay lookup and **before** writes. Do not trust a provider-supplied
dependency as authorization. Invalidated lease, cancellation, superseded attempt,
wrong project or changed admitted proposal must atomically refuse without render.
This is internal validation work in the existing commit lane, not a worker scope
grant; ordinary editing commits without producer authority remain unaffected.

Two concrete blockers must be proven away before wiring the producer:

* The port currently has no task-authority validation. Preflight reads cannot
  close the cancel/accept race. `_validate_attempt_lease` explicitly refuses a
  settled attempt: **settle proposal, then commit** is not an equivalent handoff.
  A parent must receive the already-produced artifact while the original attempt
  and lease pump remain live. Existing post-settlement task result downloads do
  not provide that seam. The local candidates to inspect are caller-owned
  `OrchestratorRunRequest.run_root` and `GenericPackHost._allocate_attempt_root`
  (configured attempt base gives `<task>-<attempt>/outputs/authoring-proposal.json`).
  Their accessibility/association is not yet an authenticated handoff. Prove
  delivery using this existing parent/host execution boundary before claiming
  feasibility; do not overload reboot-only
  `checkpoint_attempt` or introduce an endpoint/credential to fill this gap.
* `astrid/sdk/timeline/sync.py:TimelineSession.flush` validates ACK then atomically
  advances base/deletes pending/clears flight, retaining neither receipt nor
  pending render. Extend that **same durable ACK transition** for producers:
  accepted receipt + revision/publication/digest + approved render intent must
  survive before flight clearing. A callback after `flush()` returns is too late.

Recovery order: unknown commit outcome -> exact original commit retry; known
acceptance -> never recommit, resume pending render. Build through
`RemoteTasks.prepare_admission`, durably retain its exact arguments/key using the
existing outbox writer, then `dispatch_admission`; persist task/run identity before
clearing pending admission. `sdk/recovery.py:AdmissionReceipt` demonstrates these
separated admission boundaries; do not stack another journal on top.

Use normal `rendering.render` with `params.timeline_ref`, project/timeline guards
and `canonical_head_revision_id=<accepted revision>`. Runtime owns the snapshot
and authority tuple. Head C before first admission may visibly refuse; keep A's
render pending, never render C or silently repin. Runtime's current reference lane
does not promise arbitrary historical admission. Once A's task was accepted, a
lost ACK + C + restart + exact admission retry must return that **original task**;
Runtime owns the `store.py:create_task` freeze-before-replay bug/test. This worker
does not duplicate it. After commit acceptance cancellation cannot erase accepted
history; retain/recover the pending render and use ordinary task cancellation for
an already admitted task. Exact accepted commit replay must not require a live
producer lease. Until all these transitions are proven, retain the old endpoint.

## Acceptance recipe and evidence

1. Agent conformance: reverse child completion/list order, duplicate media with
   distinct aliases, inactive/superseded output distractors, registered output
   lifecycle/version race, occupied track/clip/asset IDs, exact create-or-require,
   empty insertion and explicit populated replacement. Assert golden authored
   state, recorder reads/order/created IDs, deterministic replay, unknown/null
   round trip, guarded inverse/redo, later dependencies and A→B→A refusal.
2. Paired Agent/Runtime integration: real production worker credential, real
   caller-authorized parent; renderer stopped. Assert worker commit/admission
   denied, parent commit succeeds with correct attribution, zero legacy publish
   calls, reload/show/undo work. Race cancellation after capture/inside acceptance;
   retry stale attempt/epoch/project; assert no partial revision or render task.
3. Fault injection at before send, accepted-before-response, ACK fsync, after ACK
   before admission freeze, after freeze before send, accepted admission before
   response and task-locator fsync; restart parent and Runtime. Assert one accepted
   edit, original IDs/receipt and one task pinned to A. Add head C both before first
   admission (visible refusal retained) and after accepted admission (original
   task on retry). Runtime supplies the latter permanent test. Keep the old
   publication-chain positive behaviors until the replacement passes them.

Executable spike added only to Agent's existing suites:
`test_assembly_keeps_ordered_clip_and_asset_ids_when_inactive_outputs_precede_primary`
(two cases), and
`test_render_publication_worker_has_no_project_or_task_write_scope`.
These prove old role filtering/aliases/order and configured scope limits, not
HTTP denial, cancellation races or completed migration. Existing host-hook,
orchestration and session-recovery neighbors were also run:

```sh
PYTHONPATH=/home/user/work/wt/agt-m2-render-producer-plan PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/packs/rendering/test_assemble_timeline.py tests/packs/video_editing/test_runtime_publication_chain.py::test_render_publication_worker_has_no_project_or_task_write_scope tests/packs/video_editing/test_runtime_publication_chain.py::test_generic_host_hook_materializes_and_publishes_without_local_save_or_invoke tests/packs/video_editing/test_runtime_orchestration.py tests/sdk/test_timeline_sync.py
```

**83 passed in 8.20s.** Steps 1–3 above are the required future acceptance recipe,
not executed evidence. Socket/browser/full suites, production credentials and
Runtime retry were not exercised. Use the central test service for paired/socket
tests, e.g. after implementation:
`request-test <implementation-worker> targeted --files "tests/editing_conformance/test_commit_runtime_m1.py tests/packs/video_editing/test_runtime_publication_chain.py"`,
then `wait-test <returned-result-dir>`; extend these real suites with the cases
above rather than add an isolated fake acceptance harness.
