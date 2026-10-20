# D13 requester and declared proposal output: exact remaining handoff
2026-10-20; Agent source `1441bdf1a4795aad318cf27e8b26331146bc0d92`.
Runtime main read-only `9f9b25c`; candidate authority inspected with `git show 8a8dcde`.
PLAN/producer-commit-port.md govern; M2 integration and old-writer retirement HELD.

## Actual request seams and the blocker
- Agent `astrid/packs/rendering/shared/runtime_stitch.py:27` build_stitch_admission
  emits publication.timeline_id/expected_version/render, with no original head pair or outputs.
- `astrid/core/contracts/runtime_orchestration.py:12` maps BOTH stitch names to
  rendering.render, NOT rendering.assemble_timeline. Do not add assembler ports to render.
- `astrid/packs/video_editing/shared/runtime_orchestration.py:399` admit_runtime_stitch
  forwards these settings through admit_runtime_task -> supplied client.tasks.create;
  only tests call it. No existing App/CLI production requester/consumer was found.
- `astrid/sdk/invocation.py:2480` _kernel_invoke serializes outputs supplied by its caller
  into spec.outputs; it does not copy pack output declarations or capture a target pair.
- `astrid/core/execution/generic_host.py:6600` _materialize_inputs stages ONLY family,
  continuation_id, resolved_children, edges, aggregation. It drops publication and
  supplies no producer attempt/executor/fence/epoch to the assembler JSON envelope.
- `astrid/packs/rendering/actions/assemble_timeline/run.py:309` still emits whole
  timeline/registry/publication, not SettledProducerProposal commands/pin/digest.
  Host :9631 publishes BEFORE normal upload/settlement. Keep that behavior until qualified.
No safe actual-caller change exists within this slice: an unused parameter/declaration
would not bind an authorized requester or make the existing assembler a proposal producer.

## Existing normal output contract (no new Runtime public output type needed)
- Registered `astrid/packs/rendering/pack.yaml:69`: authoring_proposal, type:file,
  artifact_type:timeline/authoring-proposal, path_template:{out}/authoring-proposal.json.
  Existing main writes that file plus a normal hashed manifest (:451-479).
- Host _typed_outputs (:7064) verifies declared port/path/hash/size; _upload_outputs
  (:7716) sends file bytes via upload_object, retaining attempt-bound output identity.
- RuntimeProtocolClient.upload_object (:4839) binds project/run/task/attempt/executor,
  lease/fence/persisted epoch/output key/port/filename to ordinary object ingestion.
- Settlement row is kind:object, name:authoring_proposal, digest:sha256:<raw bytes>,
  size:<integer>, media_type:application/json, filename:authoring-proposal.json;
  normal role/ordinal metadata remain. Pack type:file is NOT a new settlement kind.
  artifact_type is declaration metadata, not an extra settlement descriptor field.
- Runtime service.py:7479 settle_attempt stages outputs, then store.py:5201 settles
  result.outputs and task completed + attempt settled atomically with managed associations.
  service.py:6716 exposes succeeded task + immutable spec/current attempt/result.
- Candidate 8a8dcde timeline_commit_producer.py ProducerReads.capture joins tasks->runs
  project, current attempts.task_id/executor/fence/epoch/settled, immutable stored spec,
  unique result.outputs name, exact managed task/attempt/project/port/ordinal association,
  durable available/promoted lifecycle and project_objects/object/CAS size/SHA bytes.
  Require spec.outputs.authoring_proposal={type:file,artifact_type:timeline/authoring-proposal}
  and spec.runtime_dependencies.publication.admitted_target EXACTLY equal the pin/request.
  Runtime rechecks captured custody at acceptance; no inline caller authority.

## Required owner handoff, preserving the existing requester/outbox
1. Agent/App owner identifies the real authorized request entrypoint. Before slow work,
   resolve canonical project/timeline IDs and capture ONCE the session's original
   {project_id,timeline_id,base_revision_id,base_publication_id}; retain it unchanged in
   immutable admission spec.runtime_dependencies.publication.admitted_target.
   Freeze the registered file declaration in that SAME actual assembler task spec.
   Numeric expected_version, labels or completion-time head never supply either pin.
2. Agent producer/host owner supplies admitted target + host-owned attempt identity and
   native captured registered-media commands, writes canonical proposal JSON/digest through
   that declared file, and settles normally. Do not select this using caller toggles.
   Missing/mismatched target refuses replacement. No renderer projects:write/tasks:write.
3. Requester reads task/managed outputs through existing tasks.show/list_managed_outputs
   and authorized object read; queues the unchanged proposal via TimelineSession.queue_proposal
   then flush. Pending unrelated intent must finish first; retain ORIGINAL base after head C.
4. Separate ACK/recovery work: sync.py:309-325 currently advances base and clears flight;
   atomically retain verified receipt + pending historical-render body/key BEFORE clearing.
   Recover receipt from exact commit replay/existing publication checkpoint; admit accepted A
   with the approved historical selector after C/restart. Never recapture or recommit at C.
Tests here prove serialization/requester refusal only; actual custody/one-shot/render recovery
still require the coupled Runtime descendant + registered producer + authorized requester journey.
