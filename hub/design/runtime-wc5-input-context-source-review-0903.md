# Runtime WC5 settled speech input/context source review

Date: 2026-10-21 UTC

## Decision

**SOURCE ACK — bounded carrier fit only.** The exact Agent source
`a4da7cbe417aa4a3c0f90681020db6e5fd55b757` / tree
`f009d028cbeeb76dba954808db1ecea217afc3fa` can use the existing Runtime
execution-request input contract for an optional `settled_speech_input` file.
This is not approval for registration, generation, pinning, activation, native
execution, public adoption, or a live outer requester/outbox workflow.

The source proposal’s wire shape is correct:

```text
execution_request.inputs: [
  {name, object_id, digest, filename, required}
]
input_object_ids: [the same object_id, in the same order]
```

The field is an ordered descriptor array, not a mapping. No Runtime DTO,
endpoint, mode, action family, scope, or current017 extension is needed.

## Runtime custody/contract verification

The existing Runtime path supplies the required immutable boundary:

- `runtime_protocol/store.py:_normalize_execution_request` requires each
  descriptor to have a canonical SHA-256 `object_id`, rejects duplicate names
  and object IDs, and requires `input_object_ids` to be the exact ordered
  mirror.
- `RealmStore._validate_task_inputs` requires every admitted object to exist in
  CAS and to be associated with the task project before task/run rows are
  created.
- `runtime_protocol/remote_worker_deployment.py:deployment_binding_from_task`
  repeats the ordered descriptor/object-ID check, rejects conflicting digests,
  and freezes request/spec/admission digests in the read-only deployment
  binding.
- The Agent normalizer accepts only the existing safe descriptor fields. The
  generic host fetches the admitted CAS bytes, verifies SHA-256, and writes an
  attempt-local materialized path. A caller path, arbitrary materialized root,
  or hash-mismatched object is not an authority source.

This means the proposed JSON bundle is ordinary immutable input custody. Its
content is not trusted merely because it is present in the file; the managed
consumer must re-read Runtime authority before using it.

## Settled Speech rechecks and identity boundaries

The exact Agent consumer preserves the intended checks:

- The requester invokes the existing `generation.generate_speech` capability
  with text/settings only. It does not pass caller duration or generation
  intent, and the bundle does not carry claimant duration, media selection,
  producer identity, outer target, or commit identity.
- The requester performs the existing authoritative media read before import.
  The consumer performs it again for each entry and requires the exact
  five-field media selection, project/output association, `audio/wav`, positive
  verified size, finite positive intrinsic duration, exact object bytes, and
  matching hash.
- The consumer rechecks the Runtime task/run/attempt tuple, project,
  `generation.generate_speech` capability, completed state, planned text and
  settings, completed output association, and exactly one managed Speech row
  bound to that same task attempt. The H3 result coordinates are locators, not
  authority and not a fabricated selection.
- The outer managed action receives only the host-materialized file. Its
  `_ActionContext` supplies the trusted outer producer tuple and admitted target;
  the proposal must match those values. Inner Speech task/attempt IDs are not
  copied into the outer producer identity.
- The managed read client is limited to the existing worker read scopes. The
  preparation adapter rejects publication. The action emits the existing outer
  `timeline/authoring-proposal` artifact; settlement must finish before the
  requester forwards the exact proposal through the existing durable outbox.

The worker therefore has no Speech-root write authority and no timeline commit
authority. No inner/outer alias, caller duration, latest/gallery selection,
raw-object adoption, or new commit path is introduced.

## Caller and original-22 status

The exact registered outer action remains
`video_editing.sync_draft_voiceover`; the inner action remains
`generation.generate_speech`. In the exact Agent source, the optional action
input is declared and passed through the managed runner, but
`_prepare_requester_speech_inputs` has no non-test production caller. There is
therefore no live requester admission of this descriptor, no captured outer
settled proposal, and no requester/outbox commit, retry, or undo proof.

The baseline `tests/packs/video_editing/test_draft_voiceover.py` is unchanged
by the exact source diff. The exact source archive ran that suite successfully,
but that offline result is only preservation evidence; it is not the missing
live outer workflow proof. The original 22 successes/paths remain strict and
must stay on their existing routes until the one real outer qualification is
completed. No original positive was converted to refusal or weakened here.

## Evidence

Runtime targeted checks on this worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_schema_validation.py tests/test_timeline_producer_guards.py \
  -k 'schema_validation or admitted_utf8_script_input_stays_pinned_after_source_update_and_restart or settled_proposal_capture_is_verified_detached_and_read_only'
25 passed, 40 deselected in 5.78s
```

Exact Agent source archived to a private temporary directory, with Runtime
source supplied read-only:

```text
tests/packs/video_editing/test_settled_voiceover_input.py
tests/packs/video_editing/test_voiceover_requester.py
tests/core/execution/test_python_action_context.py
tests/packs/video_editing/test_sync_draft_voiceover_action.py
-k 'consumer or requester or managed_read_client or existing_file_descriptor or context_has_read_only_identity or request_cannot_replace_host_context or output_spool or optional_settled_input or declaration_keeps_existing or action_uses_private_managed_entry or advisory or existing'
33 passed, 33 deselected in 5.35s

tests/packs/video_editing/test_draft_voiceover.py
24 passed in 0.47s

tests/sdk/test_execution_request_binding.py
-k 'full_contract or input_manifest or caller_cannot or malformed_canonical or workspace_admission_derives or remote_task_create_derives or frozen_inputs'
7 passed, 35 deselected in 0.33s
```

The independent Agent custody report also records three compact refusal probes
(outside-attempt path, direct symlink, and host CAS hash mismatch) as passed.
No HTTP/live socket, native, browser, render, full suite, generation, pin,
registration, activation, or public source-adoption test was run for this ACK.

## Remaining proof

Agent owns the next proof: one normal outer
`video_editing.sync_draft_voiceover` admission retaining the original target /
head pair and ordinary script input; one completed outer proposal; then the
requester’s existing outbox submits the exact digest-bound producer guard and
demonstrates accepted commit, lost-ack retry/restart, and undo. The inner
Speech task’s independently verified selection/duration must remain separate
from the outer producer identity throughout.
