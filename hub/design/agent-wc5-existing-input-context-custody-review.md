# Agent WC5 existing input/context custody source review

Date: 2026-10-21 UTC

## Decision

**APPROVE** the exact committed Agent source for source staging only:

- commit: `a4da7cbe417aa4a3c0f90681020db6e5fd55b757`
- tree: `f009d028cbeeb76dba954808db1ecea217afc3fa`
- parent: `722535178627d08bf706c3dd4327eb757c5fa960`
- subject: `feat(video-editing): join settled speech through dormant file input`

This is not approval for native execution, a live Runtime workflow, pinning,
registration, public activation, source adoption, or requester outbox/retry/
undo qualification. The source remains dormant and requires the separately
reviewed peer ACK and later real workflow proof.

## Corrected exact source proposal

The existing proposal is substantively correct, with one wire-level precision:
`execution_request.inputs` is the existing ordered array of descriptors, not a
mapping. The future requester/session integration must place the returned
descriptor in that array and set the task-level `input_object_ids` to the
matching one-element list. No new request field or Runtime route is proposed.

The source delta is exactly these nine files:

- `astrid/core/execution/executor/_action_context.py`
- `astrid/packs/video_editing/actions/sync_draft_voiceover/run.py`
- `astrid/packs/video_editing/pack.yaml`
- `astrid/packs/video_editing/shared/draft_voiceover.py`
- `astrid/packs/video_editing/shared/voiceover_requester.py`
- `tests/core/execution/test_python_action_context.py`
- `tests/packs/video_editing/test_draft_voiceover_managed.py`
- `tests/packs/video_editing/test_sync_draft_voiceover_action.py`
- `tests/packs/video_editing/test_voiceover_requester.py`

The requester helper runs the normal `generation.generate_speech` capability
with the planned text and speech settings, waits for a successful H3-shaped
result, requires the Runtime task/run/attempt coordinates and exactly one
managed `speech` output, and performs the existing authoritative media read.
It then imports one immutable JSON bundle under requester authority. The
returned ordinary descriptor is:

```json
{
  "name": "settled_speech_input",
  "object_id": "sha256:<bundle-bytes>",
  "digest": "sha256:<bundle-bytes>",
  "filename": "settled-speech-<content-prefix>.json",
  "required": true
}
```

The future request carrier is therefore, without any new schema:

```text
execution_request.inputs: [<the descriptor above>]
input_object_ids: [<the descriptor's object_id>]
```

The bundle root is exactly `{"entries": [...]}`. Each ordered entry contains
only `occurrence_id`, `text`, `settings`, and the closed H3 result envelope
(`schema_version`, `input_digest`, `result_digest`, `result`). It carries no
outer target, producer, requester authority, duration, media selection, or
commit identity. The inner H3 coordinates are locators only.

## Custody trace and refusals

The existing execution-request normalizer requires an array of safe named
descriptors. Runtime admission requires the descriptor object ID and the
task-level `input_object_ids` to agree. The generic host then requires the
descriptor digest to be admitted, fetches the CAS object, verifies its SHA-256
bytes, and writes the materialized file under the exact attempt's `inputs/`
directory. A caller-local path or unauthorized/hash-mismatched object is
refused before action dispatch. The new action port is optional and only
receives that host-materialized path; the source does not add a caller path,
worker speech root, child delegation, or write scope.

The consumer performs a second boundary check on the path: a direct symlink,
an unavailable/non-file path, and a resolved path outside the managed attempt
are refused. Its H3 envelope and result digest are closed and verified. It
then reads the Runtime task and requires matching task/run/attempt, project,
capability, completed state, task inputs, task output, and exactly one managed
speech association bound to that task attempt. The claimant's duration and
media metadata are never used.

For every accepted inner output, the existing Runtime media reader is called
again with the exact claimed selector. It requires the exact five-field media
selection, matching project/output claims, verified `audio/wav`, positive
verified size, finite positive intrinsic duration, exact object bytes, and
matching SHA-256. The same authoritative read is repeated before native
capture/proposal construction, so a changed pin or duration refuses.

The managed action obtains the host worker read connection only through the
existing environment/handshake path. The handshake actor must equal the
outer executor identity and the scopes must be exactly:
`worker:execute`, `projects:read`, `tasks:read`, and `objects:read`. Actor or
scope substitution refuses. The `_PreparationClient` checks the ephemeral
host context on delegated reads, and its target wrapper refuses publication.

Outer identity is never derived from the JSON file or inner speech result.
The host-only `_ActionContext` supplies the producer tuple
`task_id/attempt_id/executor_id/fence/runtime_epoch` and the admitted target
tuple `project_id/timeline_id/base_revision_id/base_publication_id`. The
managed source checks the selected project/timeline/base pair against that
trusted target before preparation and builds the existing proposal with that
same outer identity. The inner speech task is only provenance for the
Runtime-verified media row.

The action context is read-only, rejects missing/inconsistent runtime context,
wrong project or invocation, nested/reused/copied/lifetime-expired context,
PID/thread changes, output-root replacement, and symlinked/replaced output
directories. The materialized input path is additionally fenced to the
attempt root. These checks are source guards only; they do not constitute a
real worker or native execution proof.

## Preserved floors and evidence

The public `sync_draft_voiceover` path is unchanged: its existing publication,
receipt, revision/CAS, timing, and failure behavior remain on the public
helper. The new port is dormant and does not activate a caller. The existing
schemaed5/65-37 floors and public014 remain untouched; the target diff has no
schema or Runtime files and no public caller adoption. The prior native
companion source44 and the worker's current141 report are not treated as
real end-to-end workflow evidence.

Focused checks run against a private archive of the exact target tree, with
the shared Runtime source supplied read-only:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<target>:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/packs/video_editing/test_settled_voiceover_input.py \
  tests/packs/video_editing/test_voiceover_requester.py \
  tests/core/execution/test_python_action_context.py \
  -k 'consumer or requester or managed_read_client or existing_file_descriptor or context_has_read_only_identity or request_cannot_replace_host_context or output_spool'
  23 passed, 21 deselected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<target>:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_execution_request_binding.py \
  -k 'full_contract or input_manifest or caller_cannot or malformed_canonical or workspace_admission_derives or remote_task_create_derives or frozen_inputs'
  7 passed, 35 deselected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<target>:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/packs/video_editing/test_sync_draft_voiceover_action.py \
  -k 'optional_settled_input or declaration_keeps_existing or action_uses_private_managed_entry or advisory or existing'
  9 passed, 13 deselected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<target>:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/packs/video_editing/test_draft_voiceover.py
  24 passed

Ad hoc custody probes: 3 compact negatives passed (outside-attempt path,
direct symlink, and host CAS hash mismatch).
```

No full suite, HTTP/live socket, private-body, native, browser, render,
install, generation, pin, registration, public activation, or source adoption
was run. The next step is the separately authorized peer review and then one
real workflow qualification using the exact source pair; this review grants
neither authorization.
