# Runtime voiceover carrier shape audit

Date: 2026-10-20 (UTC)

## Exact existing seam

The outer registered action is `video_editing.sync_draft_voiceover`. The
existing `generation.generate_speech` call is inner speech execution only; it
is not an outer action name, and no outer voiceover workflow is qualified by
this audit. Runtime has no generic voiceover/action whitelist.

The private task spec retains the original target at
`runtime_dependencies.publication.admitted_target`, with exactly:

```json
{
  "project_id": "<project>",
  "timeline_id": "<timeline>",
  "base_revision_id": "<original-base-revision>",
  "base_publication_id": "<original-base-publication>"
}
```

The declared settled output is:

```json
{
  "authoring_proposal": {
    "type": "file",
    "artifact_type": "timeline/authoring-proposal"
  }
}
```

For a script/object input, retain the ordinary execution-request carrier:
`inputs` is an ordered list of closed descriptors with keys
`name`, `object_id`, `filename`, `required`, and optional `digest`; when
present, `digest == object_id`. `input_object_ids` is its exact ordered mirror.
Do not add `script_pins`.

## Closed settled artifact and PIN

The authoritative CAS JSON has exactly these top-level keys:
`schema_version`, `producer`, `admitted_target`, `commands`, `rationale`, and
`proposal_digest`. `producer` has exactly `task_id`, `attempt_id`,
`executor_id`, `fence`, and `runtime_epoch`. The proposal digest hashes the
complete artifact object after removing only its own digest, using sorted keys,
compact separators, `ensure_ascii=False`, `allow_nan=False`, UTF-8, and
SHA-256 prefixed `sha256:`. Runtime hashes the authoritative CAS bytes and
separately checks the raw object digest, size, managed project association,
durability, lifecycle, and attempt-bound provenance.

Forwarded finite numeric values compare by value (`1 == 1.0`); booleans are
distinct. That value comparison never replaces the original artifact bytes
for digest authority.

The request starts with the existing `producer.guard` command. Its `args` is
exactly `{pin}`, and the pin has exactly:
`task_id`, `attempt_id`, `executor_id`, `fence`, `runtime_epoch`,
`admitted_target`, and `proposal_digest`. No proposal copy or inline authority
is forwarded. The provider uses the existing private `producer_attempt(pin)`
read and records the exact authority dependency.

The existing `timeline.producer.acceptance` checkpoint is checked unconsumed
before capture and persisted in the same acceptance transaction after the
accepted receipt/revision are established. No new envelope, coordinator,
journal, API, DTO, schema, scope, or action family is needed.

## Source references

- Runtime: `runtime_protocol/timeline_commit_producer.py:16-70,224-285`.
- Runtime: `runtime_protocol/timeline_commit_port.py:338-450`.
- Runtime: `runtime_protocol/timeline_commit_producer_checkpoint.py:14-92`.
- Runtime: `runtime_protocol/store.py:417-468,1518-1556`.
- Frozen M2 contract: `design/m2-render-producer-contract.md:63-225`.
- Frozen Agent SDK `origin/codex/handover-timeline-r4-20261019-candidate-sdk`:
  `astrid/sdk/execution_request.py:517-554,731-839` and
  `astrid/packs/video_editing/shared/draft_voiceover.py:382-414`.

The corrected detailed page is
`design/runtime-voiceover-native-admission.md`.
