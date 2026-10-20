> Manager correction 2026-10-20T17:02:02Z: generation.generate_speech below is the INNER action, not a verified outervoiceoveraction. Outertrace active. Proposed JSON examples must be checked against existing authoritative D13 codec; they are NOT a new agreed contract.

# Runtime voiceover native admission

Date: 2026-10-20 (UTC)

## Verdict

Runtime needs no product-code change for the currently agreed boundary. The
generic D13 producer admission and one-shot settlement guard already accept an
outer settled authoring proposal without a voiceover-specific codec whitelist.
There is no evidence that `rendering.assemble_timeline` is a voiceover
whitelist; its only Runtime special case is continuation-child validation.

The actual registered Agent action is `generation.generate_speech`. It is
invoked by the current Agent source as:

```python
sdk.invoke(
    "generation.generate_speech",
    kind="executor",
    project=project,
    inputs={"text": text, **settings},
    client=client,
    wait=True,
    idempotency_context=request_context,
)
```

This is the action name, not an inferred family or remapping. The held Agent
voiceover prototype is not an integrated/qualified workflow, so this report
does not claim that the normal Speech request is already an outer native
voiceover admission.

## Existing Runtime carrier and exact proposal shape

The existing private task-spec carrier is sufficient for the outer D13
boundary:

```json
{
  "runtime_dependencies": {
    "publication": {
      "admitted_target": {
        "project_id": "<project>",
        "timeline_id": "<timeline>",
        "base_revision_id": "<original-base-revision>",
        "base_publication_id": "<original-base-publication>"
      }
    }
  },
  "outputs": {
    "authoring_proposal": {
      "type": "file",
      "artifact_type": "timeline/authoring-proposal"
    }
  }
}
```

The four `admitted_target` keys are exact and must remain the original
requester target/base pair captured before POST. Runtime does not need a DTO,
endpoint, scope, coordinator, or scene field for this.

The settled output must be one durable JSON output named and ported as
`authoring_proposal`. Its closed top-level shape is:

```json
{
  "schema_version": 1,
  "producer": {
    "task_id": "<outer-task>",
    "attempt_id": "<attempt>",
    "executor_id": "<executor>",
    "fence": "<fence>",
    "runtime_epoch": "<epoch>"
  },
  "admitted_target": {
    "project_id": "<project>",
    "timeline_id": "<timeline>",
    "base_revision_id": "<original-base-revision>",
    "base_publication_id": "<original-base-publication>"
  },
  "commands": ["<outer-settled-edit-command>"],
  "rationale": "<reason>",
  "proposal_digest": "sha256:<64 lowercase hex characters>"
}
```

The producer identity in this object is the outer settled task/attempt. An
inner Speech result must not be used as a fabricated producer pin, and the
worker must not commit before the outer ledger settles.

The exact producer guard remains the existing one-shot port operation:

```json
{
  "schema_version": 1,
  "op": "producer.guard",
  "version": "1",
  "select": null,
  "args": {
    "pin": {
      "task_id": "<outer-task>",
      "attempt_id": "<attempt>",
      "executor_id": "<executor>",
      "fence": "<fence>",
      "runtime_epoch": "<epoch>",
      "admitted_target": {
        "project_id": "<project>",
        "timeline_id": "<timeline>",
        "base_revision_id": "<original-base-revision>",
        "base_publication_id": "<original-base-publication>"
      },
      "proposal_digest": "sha256:<64 lowercase hex characters>"
    }
  }
}
```

Runtime accepts this guard only after exact proposal capture and the
ledger-first producer-consumption check. Acceptance is persisted as the
one-shot producer checkpoint in the same outer commit transaction.

## Script-pin coordination boundary

The Agent source currently demonstrates the exact frozen script descriptor
that a voiceover command uses:

```json
{
  "object_id": "<registered-media-id>",
  "digest": "<content-hash>",
  "size": "<integer-byte-size>",
  "media_type": "text/plain; charset=utf-8"
}
```

The associated command binding is `kind: "voiceover_script"`, `slot: null`,
with the descriptor above as the text binding. The source-side admission also
requires the registered binding provenance `registered_pin`,
`media_id == content_hash`, an integer non-negative `byte_size`, and a digest
matching the UTF-8 script text.

However, Agent has not yet ACKed the exact private TaskSpec `inputs` key and
object shape that carries this pin before POST. Runtime must not invent a
`script_pins` field or add a new DTO. Agent owns freezing that existing input
carrier, the proposal builder, and the requester. Once ACKed, the outer task
must carry that exact script-pin object before POST and the settled commands
must preserve the same values. Runtime can preserve/compare the immutable
task-spec data; it does not need to interpret it as a new public API.

## Source seams

- `runtime_protocol/timeline_commit_producer.py:182` only checks
  `task["capability"] == "rendering.assemble_timeline"` while validating
  continuation child outputs. It is not a voiceover admission whitelist.
- `runtime_protocol/timeline_commit_producer.py:224` captures the settled
  `authoring_proposal`, checks the exact target, closed proposal keys, producer
  identity, digest, commands, and rationale, then returns detached authority.
- `runtime_protocol/timeline_commit_port.py:338` requires the exact producer
  pin before capture and records the detached authority dependency.
- `runtime_protocol/timeline_commit_port.py:356` enforces the guard-first,
  exact-command-suffix, no-write/no-read/no-undo producer attempt boundary.
- `runtime_protocol/timeline_commit_producer_checkpoint.py:22` performs the
  ledger-first one-shot consumption check; `:58` persists the checkpoint in
  the accepted commit transaction.
- `runtime_protocol/store.py:270` preserves arbitrary task-spec inputs while
  stripping only execution internals, so no Runtime schema expansion is
  required for the agreed private carrier.

## Evidence

Targeted Runtime D13 tests:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_timeline_producer_guards.py \
  tests/test_timeline_producer_checkpoint.py
```

Result: `54 passed in 18.59s`.

These tests prove the generic authority/settlement unit, including exact
proposal capture, guard ordering, refusal paths, and one-shot checkpointing.
They do not prove a registered outer `generation.generate_speech` workflow,
because the current normal Speech request carries only `text` and settings,
not the outer proposal intent or the frozen script-pin carrier.

## Blockers and next steps

Qualification is blocked on the Agent-side ACK of the exact existing private
TaskSpec input carrier for the script pin, plus an outer task/requester path
that submits the original target/base pair before POST and returns the settled
proposal through the existing D13 outbox. This is a coordination blocker, not
a Runtime seam defect.

After that ACK, add the smallest paired integration proof using the actual
`generation.generate_speech` entry and the same private input shape. Keep old
main paths, strict RIPPLE, and readable-audio requirements intact until that
proof qualifies. No Runtime codec whitelist, fake inner Speech producer pin,
worker commit, or new DTO/API/scope/coordinator/scene change is warranted now.
