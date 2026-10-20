# Runtime voiceover carrier shape audit

Date: 2026-10-20 (UTC)

This is a source audit of the existing D13 producer carrier. It does not add
an action family, codec, API, DTO, schema, scope, or voiceover qualification.

## Outer trace versus inner action

`generation.generate_speech` is the existing inner speech executor action. It
is not an outer voiceover action name and must not be used as one. The normal
Agent voiceover caller currently invokes it with `inputs={"text": text,
**settings}`; that path does not carry the outer proposal intent or the D13
admitted target, and this audit makes no claim that it is qualified as an
outer native voiceover workflow.

Runtime's only capability-specific producer check in this seam is the
existing continuation-child check for `task["capability"] ==
"rendering.assemble_timeline"`. That is not a generic producer/action
whitelist and does not justify adding a voiceover family.

## Existing private admission carrier

The original target is retained in the existing open task spec, not in a new
request DTO:

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

`admitted_target` has exactly these four keys:
`project_id`, `timeline_id`, `base_revision_id`, and
`base_publication_id`. Runtime requires that exact object to equal the commit
request's four target fields and the task spec's retained value. A producer
result cannot widen or rewrite it.

For a script or other managed object, the existing retained input carrier is
the ordinary execution-request input manifest; there is no `script_pins`
field. Each `execution_request.inputs` item has only:

```json
{
  "name": "script",
  "object_id": "sha256:<64 lowercase hex>",
  "filename": "script.txt",
  "required": true,
  "digest": "sha256:<same object id>"
}
```

`digest` is optional but, when present, must equal `object_id`. The ordered
top-level `input_object_ids` list mirrors the input items exactly. The normal
merge retains the descriptors under `spec.inputs[<name>]` and checks
`object_id`, `digest`, `filename`, and `required`; it does not invent a
voiceover-specific carrier. This is an input/object custody carrier, not
authority and not a proposal envelope.

## Settled `authoring_proposal` artifact

The normal task result contains one durable JSON output named
`authoring_proposal`. Its declared output is the exact file/artifact pair
above. Runtime requires the settled descriptor to have `name` and
`output_port` `authoring_proposal`, `media_type` `application/json`, object
kind, and a managed durable association in the same project/task/attempt with
matching size, object digest, and attempt-bound provenance. The lifecycle must
be `available` or `promoted`. Runtime reads the authoritative bytes from CAS,
verifies the CAS digest and size, and strictly parses those bytes; a caller's
re-serialized proposal is not authoritative.

The parsed JSON has exactly six top-level keys:

```json
{
  "schema_version": 1,
  "producer": {
    "task_id": "<task>",
    "attempt_id": "<attempt>",
    "executor_id": "<executor>",
    "fence": 7,
    "runtime_epoch": 3
  },
  "admitted_target": {
    "project_id": "<project>",
    "timeline_id": "<timeline>",
    "base_revision_id": "<original-base-revision>",
    "base_publication_id": "<original-base-publication>"
  },
  "commands": ["<nonempty ordinary EditCommand>"],
  "rationale": "<string>",
  "proposal_digest": "sha256:<64 lowercase hex>"
}
```

The `producer` object has exactly five keys: `task_id`, `attempt_id`,
`executor_id`, `fence`, and `runtime_epoch`. `schema_version` is integer 1;
fence and epoch are positive, non-boolean integers; commands are nonempty;
and rationale is a string. No `action_name`, inner Speech identity, forwarded
proposal, or inline authority field belongs in this artifact.

`proposal_digest` is SHA-256 over the entire proposal after removing only its
own top-level `proposal_digest`, serialized with the existing profile:
sorted object keys, compact separators, `ensure_ascii=false`,
`allow_nan=false`, UTF-8 bytes, prefixed with `sha256:`. Duplicate keys,
nonfinite numbers, and invalid Unicode are rejected. The original artifact
bytes are authoritative for this hash. Runtime separately verifies the raw
CAS object digest/size.

When comparing the forwarded request suffix and rationale, existing
`value_equal` compares finite numeric values by value (`1` and `1.0` compare
equal), keeps booleans distinct, and preserves object key/presence/null,
array order, and structure. That comparison does not replace or recompute
the artifact hash: a Node round-trip may spell an artifact `1.0` as `1`, while
the original settled artifact bytes still determine `proposal_digest`. The
raw CAS digest is a separate identity.

## Existing producer guard and checkpoint seam

The normal request begins with one existing registered command and then
forwards the artifact's ordinary commands:

```json
{
  "schema_version": 1,
  "op": "producer.guard",
  "version": "1",
  "select": null,
  "args": {
    "pin": {
      "task_id": "<task>",
      "attempt_id": "<attempt>",
      "executor_id": "<executor>",
      "fence": 7,
      "runtime_epoch": 3,
      "admitted_target": {
        "project_id": "<project>",
        "timeline_id": "<timeline>",
        "base_revision_id": "<original-base-revision>",
        "base_publication_id": "<original-base-publication>"
      },
      "proposal_digest": "sha256:<64 lowercase hex>"
    }
  }
}
```

The guard's `args` is exactly `{pin}`. The pin's exact keys are
`task_id`, `attempt_id`, `executor_id`, `fence`, `runtime_epoch`,
`admitted_target`, and `proposal_digest`. It is the first and only guard;
nested guard/inverse/restore or sibling authority claims are not part of this
carrier. `producer_attempt(pin)` performs the private Runtime read and
returns only the verified pin. The provider records the existing exact
authority dependency; the guard itself has no write or authority payload.

Before capture and acceptance, the checkpoint is required to be unconsumed.
After the accepted receipt and revision are established, the existing
`timeline.producer.acceptance` checkpoint is persisted in the same acceptance
transaction, using `timeline_render_publications`; rollback does not consume
it. This preserves exact accepted replay and one-shot consumption without a
new envelope, journal, or coordinator.

## Source references

- Runtime `runtime_protocol/timeline_commit_producer.py:16-70,224-285`:
  exact pin/target sets, strict proposal keys, CAS read, digest preimage,
  numeric/boolean comparison, and request suffix checks.
- Runtime `runtime_protocol/timeline_commit_port.py:338-385,387-450`:
  private `producer_attempt`, guard-record bijection, acceptance recheck, and
  checkpoint persistence call.
- Runtime `runtime_protocol/timeline_commit_producer_checkpoint.py:14-29,58-92`:
  one-shot consumption and same-transaction checkpoint persistence.
- Runtime `runtime_protocol/store.py:417-468,1518-1556`:
  ordinary execution-request object descriptors and ordered
  `input_object_ids` custody.
- Frozen M2 contract:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-render-producer-contract.md:63-225`.
- Frozen Agent SDK `origin/codex/handover-timeline-r4-20261019-candidate-sdk`:
  `astrid/sdk/execution_request.py:517-554,731-839` for the retained
  script/object carrier and `astrid/packs/video_editing/shared/draft_voiceover.py:382-414`
  for the current inner `generation.generate_speech` call.

No voiceover workflow is claimed qualified by this audit.
