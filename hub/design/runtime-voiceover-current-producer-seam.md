# Runtime current producer seam: voiceover handoff

Date: 2026-10-20 (UTC)

Status: peer-ready design handoff. Runtime product source is unchanged. This
page answers the Agent question using the current generic producer carrier and
records the one remaining coordination boundary; it does not qualify a
voiceover/audio positive.

## Decision

The existing generic producer admission can carry the outer voiceover result.
It already carries the original target, the settled `authoring_proposal` CAS
artifact, its digest-bound producer pin, and the ordinary proposal commands.
No new DTO, endpoint, journal, coordinator, worker credential, producer pin,
or raw-output adoption is needed.

The exact registered outer action is:

```text
video_editing.sync_draft_voiceover
```

The exact inner speech action is:

```text
generation.generate_speech
```

The latter is a separate speech task and must not be remapped to
`rendering.render`, renamed as the outer action, or used as the outer producer
identity.

## The three identities are separate

| Boundary | Existing identity/carrier | Runtime consequence |
| --- | --- | --- |
| Requester admission | The normal task capability/spec and execution request. `runtime_dependencies.publication.admitted_target` retains exactly `project_id`, `timeline_id`, `base_revision_id`, and `base_publication_id`. The ordinary input manifest retains the script descriptor (`name`, `object_id`, `filename`, `required`, optional `digest`) and its exact ordered `input_object_ids` mirror. There is no `script_pins` field. | Runtime freezes the original head pair and managed input/object custody at admission. It does not reconstruct either from the later current head or from a producer result. |
| Outer producer settlement | The completed outer task declares `outputs.authoring_proposal` as `{type: "file", artifact_type: "timeline/authoring-proposal"}`. Runtime resolves the unique managed JSON output, verifies project/task/attempt provenance, lifecycle, size, CAS digest, and reads authoritative bytes. | The settled artifact is the producer result; its raw CAS bytes and canonical `proposal_digest` are authoritative. A caller digest or reserialized proposal is insufficient. |
| Inner speech completion | `generation.generate_speech` produces managed speech/WAV/manifest/word outputs. The normal Agent path currently admits it without `generation_intent`/`generation.publish_v1`, so its generic association has task/attempt/CAS identity but no generation/variant identity. The settled generation fixture and WAV intrinsic path separately prove the existing five-field media-selection/duration read when publication is explicitly present. | The inner task's generation/variant/media selection and duration remain a separate prerequisite for an audio EditCommand. They cannot authorize the outer proposal and cannot be substituted for the outer task's pin or proposal. |

The current `runtime_synthesizer` returns only text, settings,
`audio_media_id`, duration, run ID, and inner task ID. It drops the richer
managed association/attempt/provenance context. That is why normal inner
speech output is not evidence of a settled outer proposal.

## Existing outer proposal → one-shot guard path

The Agent requester must retain the original target/head pair and ordinary
script input in the existing task spec before slow work, then settle the outer
task with the declared `authoring_proposal`. The proposal JSON is the existing
closed shape:

```json
{
  "schema_version": 1,
  "producer": {
    "task_id": "...",
    "attempt_id": "...",
    "executor_id": "...",
    "fence": 7,
    "runtime_epoch": 3
  },
  "admitted_target": {
    "project_id": "...",
    "timeline_id": "...",
    "base_revision_id": "...",
    "base_publication_id": "..."
  },
  "commands": ["<nonempty ordinary EditCommand>"],
  "rationale": "...",
  "proposal_digest": "sha256:<64 lowercase hex>"
}
```

The requester sends the existing ordinary command batch with the existing
first guard:

```json
{
  "schema_version": 1,
  "op": "producer.guard",
  "version": "1",
  "select": null,
  "args": {
    "pin": {
      "task_id": "...",
      "attempt_id": "...",
      "executor_id": "...",
      "fence": 7,
      "runtime_epoch": 3,
      "admitted_target": {
        "project_id": "...",
        "timeline_id": "...",
        "base_revision_id": "...",
        "base_publication_id": "..."
      },
      "proposal_digest": "sha256:<64 lowercase hex>"
    }
  }
}
```

The existing Runtime path then:

1. requires the guard to be the first/only guard and rejects restore/inverse
   authority siblings;
2. checks the request target against the pin and the task's retained
   `runtime_dependencies.publication.admitted_target`;
3. checks the completed current task/attempt, settled status, executor,
   fence, epoch, project association, managed lifecycle, CAS bytes, size and
   raw digest;
4. strictly parses the six-key proposal, recomputes `proposal_digest` from the
   authoritative artifact bytes, derives the exact pin, and compares the
   entire forwarded command suffix/rationale; and
5. records the existing private `producer_attempt(pin)` authority dependency,
   rechecks it at acceptance, and consumes the existing one-shot
   `timeline.producer.acceptance` checkpoint in the same acceptance
   transaction.

Preview/capture do not consume. An exact accepted replay is resolved by the
existing acceptance receipt path; a new key cannot consume the settled
proposal twice. These guards remain unchanged.

## Action-name / allowlist boundary

There is no prepared Runtime codec/action-whitelist successor in the available
current worker history. Current Runtime has a capability-specific continuation
check for `rendering.assemble_timeline`, but `ProducerReads.capture` is not a
generic voiceover/action whitelist. It authenticates the settled task and
artifact through the existing pin/target/provenance path.

Therefore no allowlist wire change is made in this handoff. Before any such
change, Agent must ACK the exact existing carrier that identifies the outer
action. The only candidate already present without a new field is the task's
registered capability string; the required peer question is whether the
normal outer admission's capability is exactly
`video_editing.sync_draft_voiceover` and must be distinguished from the
generic assembler capability. If Agent confirms that existing identity, the
smallest follow-up is a Runtime-only check over that existing capability value,
with one normal positive and wrong-action/wrong-target negatives, while
preserving every current guard above. Until that ACK and an actual requester
submission exist, do not add the check, add an `action_name` field, or widen
the proposal/pin.

## Qualification still open

The next evidence is one actual normal outer requester proof: admission with
the original target/head pair and script input, one completed outer
`authoring_proposal`, and one normal requester commit through the existing
guard/outbox path. It must show the outer task/attempt and exact target/pin,
while separately showing the inner speech task's completed generation/media
selection and duration. Existing Agent voiceover/audio positives stay on their
original routes until that proof exists; no success is converted to
`proposal_open` and no old raw output is adopted.

## Source anchors

- Agent frozen registry/source:
  `astrid/packs/video_editing/pack.yaml:52-127` and
  `astrid/packs/video_editing/actions/sync_draft_voiceover/run.py:9-70`.
- Agent frozen inner caller:
  `astrid/packs/video_editing/shared/draft_voiceover.py:382-414`.
- Agent ordinary input carrier:
  `astrid/sdk/execution_request.py:42-47,517-554,731-839`.
- Runtime producer guard/artifact validation:
  `runtime_protocol/timeline_commit_producer.py:16-70,224-285`.
- Runtime private producer read and acceptance recheck:
  `runtime_protocol/timeline_commit_port.py:338-450`.
- Runtime one-shot checkpoint:
  `runtime_protocol/timeline_commit_producer_checkpoint.py:14-92`.
- Existing evidence:
  `runtime-voiceover-native-admission.md`,
  `runtime-voiceover-carrier-shape-audit.md`,
  `runtime-outer-voiceover-action-trace.md`,
  `runtime-speech-main-admission-trace.md`,
  `runtime-speech-settled-media-source.md`,
  `runtime-speech-wav-intrinsics.md`, and
  `agent-wc5-known-intent-preservation.md`.

## Peer-ready summary

Agent: use `video_editing.sync_draft_voiceover` as the outer registered
action. Keep `generation.generate_speech` inner-only. Put the original
project/timeline/base revision/base publication in the existing admitted
target and carry script custody through the ordinary input manifest; do not
invent `script_pins`. Settle the outer `authoring_proposal`, then forward its
exact digest-bound pin in the existing first `producer.guard`. Runtime keeps
the current guards and one-shot checkpoint. Inner generation/variant/five-field
audio selection and duration are separate and remain OPEN until the real
requester proof. Please ACK whether the existing task capability string is the
approved action discriminator before any Runtime allowlist check is proposed.
