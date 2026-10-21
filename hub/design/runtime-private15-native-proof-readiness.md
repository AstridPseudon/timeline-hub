# Private 0.2.15 native outer voiceover proof readiness

Status: READY for one reviewed, normally generated private Agent pin after reciprocal review. This is a readiness handoff, not an execution or pin request.

## Fixed Runtime counterpart

Use the immutable Runtime checkout at `/home/user/work/wt/rt-pin-c3d26567`:

```text
commit  c3d26567ff6fe4e20a959476d40aff90ad23a0ca
tree    f3ae49d38454ce73a9c91a954bb530b3ce51c122
package private 0.2.15 (unpublished)
Agent source 4d4535882f1e028805c3da178bf9a7fa53696da8 / f18245ced9c231ddf8f6f2ee64405a84d3517921
raw schema 84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5 (59 definitions, 33 operations, 12 v2 clauses)
health/schema sha256:07c0668b2fb16226475429ec65637404c0b2e885e1b88e67f896e249089d6680
raw bundle sha256:bbbae375837456b267d9f0c7de89b962966da79a24abe7c4720301423b333bcb
artifact manifest version sha256:2df8ebf4fb17cae1b62e78a262b2b20b393770d045d0ef8748207ac7efacbfbb
```

Runtime’s private review approved this bundle. Its normal task admission accepts the existing generic carrier consisting of `runtime_dependencies.publication.admitted_target` with exactly these four keys: `project_id`, `timeline_id`, `base_revision_id`, and `base_publication_id`. The shortened names previously used in this handoff (`project`, `timeline`, `base_revision`, `base_publication`) were prose-only and are not accepted aliases.

## Exact admitted-target boundary

The accepted normal-admission body is the existing one in `tests/test_task_continuations.py:158-178`, exercised by `test_registered_outer_producer_with_ordered_input_is_not_an_assembly_continuation` at `:125-203`:

```python
{
    "project": project_id,
    "capability_id": "video_editing.sync_draft_voiceover",
    "capability_digest": capability_digest,
    "input_object_ids": [object_id],
    "execution_request": {"target": {"kind": "default"}, "inputs": [descriptor]},
    "spec": {
        "capability_id": "video_editing.sync_draft_voiceover",
        "kind": "executor",
        "inputs": {
            "project": project_id,
            "timeline_ref": "film",
            "timing_policy": "ripple",
            "occurrence_ids": ["o1"],
            "script": descriptor,
        },
        "runtime_dependencies": {
            "publication": {
                "admitted_target": {
                    "project_id": project_id,
                    "timeline_id": "film",
                    "base_revision_id": "bootstrap-revision",
                    "base_publication_id": "bootstrap-publication",
                },
            },
        },
        "outputs": {},
    },
    "idempotency_key": "outer-producer-admission",
}
```

This is three distinct boundaries, with no aliasing:

* Task-admission wire/body: top-level `project`; `execution_request.inputs` is an ordered descriptor list, and top-level `input_object_ids` mirrors its `object_id` values exactly. The publication target is nested under `spec.runtime_dependencies.publication.admitted_target` and uses the four `_id` keys above. Runtime stores and replays that exact object. See `runtime_protocol/remote_worker_deployment.py:688-728`, `runtime_protocol/store.py:2855-2874`, and the accepted fixture/test above.
* Producer proposal/pin: both `SettledProducerProposal.admitted_target` and `ProducerAttemptPin.admitted_target` use the same four-key `ProducerAdmittedTarget`. Runtime validates the closed set in `runtime_protocol/timeline_commit_producer.py:16-53`; the frozen Agent schema has the same closed definition at `astrid/core/timeline/schema/edit-command.schema.json:2720-2746` on Agent commit `4d4535882f1e028805c3da178bf9a7fa53696da8`.
* Commit wire/body: the existing Agent `build_producer_batch` (`astrid/sdk/timeline/producer.py:47-63`) flattens those exact values into `api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, `commands`, and `rationale`, with the first command carrying the same pin. This is a separate commit request shape; it does not change the task-admission body or proposal keys.

The accepted proposal artifact remains the existing six-key object: `schema_version`, `producer`, `admitted_target` (the four-key object), nonempty `commands`, `rationale`, and `proposal_digest`. Runtime checks the artifact and its pin/commit forwarding in `runtime_protocol/timeline_commit_producer.py:241-274`; no shortened target keys are accepted at any boundary.

## Remaining Agent carrier gap

The current Agent `f18245c` source has the needed existing primitives:

* `astrid/sdk/timeline/native_voiceover.py:capture_draft_voiceover` lowers the prepared voiceover into existing timing, track, occurrence media, and provenance commands without allocating IDs or mutating the candidate.
* `astrid/sdk/timeline/producer.py` already builds the existing first `producer.guard` and digest-bound producer batch.
* `astrid/sdk/timeline/sync.py:TimelineSession` already queues a settled proposal, persists the in-flight body/key, retries the same request after ambiguous loss, and sends guarded inverse/undo.

The actual missing source/port is in the outer action: `video_editing.sync_draft_voiceover` currently declares and returns only `report`/`receipt`, calls the legacy caller-bound `bound.publish`, and does not settle an existing `timeline/authoring-proposal` output. It therefore neither invokes `capture_draft_voiceover` with the verified five-field media selection nor hands that settled proposal to `TimelineSession.queue_proposal`. The pack declaration has the same output omission. This is the concrete item for the Agent owner; do not repair it by changing Runtime admission or by reusing `rendering.assemble_timeline`/`rendering.render`.

## Deferred single proof command

After both owners approve and Agent supplies the reviewed normal private pin, substitute the Agent owner’s exact private `commit`, `tree`, and checkout for the angle-bracket fields below. The service must fail closed if either source is not exact and clean:

```bash
test "$(git -C <AGENT_PRIVATE_WORKTREE> rev-parse HEAD)" = <AGENT_PRIVATE_COMMIT>
test "$(git -C <AGENT_PRIVATE_WORKTREE> rev-parse HEAD^{tree})" = <AGENT_PRIVATE_TREE>
test -z "$(git -C <AGENT_PRIVATE_WORKTREE> status --porcelain)"
test "$(git -C /home/user/work/wt/rt-pin-c3d26567 rev-parse HEAD)" = c3d26567ff6fe4e20a959476d40aff90ad23a0ca
test "$(git -C /home/user/work/wt/rt-pin-c3d26567 rev-parse HEAD^{tree})" = f3ae49d38454ce73a9c91a954bb530b3ce51c122

ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-c3d26567 \
ASTRID_NORMAL_RUNTIME_SOURCE=/home/user/work/wt/rt-pin-c3d26567 \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<AGENT_PRIVATE_WORKTREE> \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration \
  tests/packs/video_editing/test_outer_voiceover_native.py::test_outer_native_voiceover_proposal_outbox_retry_undo
```

Run that command only through one newly named central test-service entry owned by Agent (for example, the service’s `<future-worker-name> <future-suite-name>` pair); do not run it locally now. The test is exactly one normal requester flow:

The deferred service request, after that entry exists and the Agent pin is approved, is:

```bash
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
R=$($ORCH/bin/request-test <future-worker-name> <future-suite-name>)
$ORCH/bin/wait-test "$R"
```

The named service entry must run the exact source-asserting command above from the Agent private checkout; it must not silently substitute `/home/user/work/{agent,runtime}` or an ordinary/public pin.

The normal request metadata is the existing shape below (replace only the angle-bracket values with the admitted project/object values; do not add fields):

```text
kind: executor
executor_id: video_editing.sync_draft_voiceover
spec.runtime_dependencies.publication.admitted_target:
  project_id: <PROJECT_ID>
  timeline_id: <TIMELINE_ID>
  base_revision_id: <ORIGINAL_BASE_REVISION>
  base_publication_id: <ORIGINAL_BASE_PUBLICATION>
execution_request.inputs:
  - name: script
    object_id: <SCRIPT_SHA256>
    digest: <SCRIPT_SHA256>
    filename: script.txt
    required: true
execution_request.input_object_ids: [<SCRIPT_SHA256>]
outputs:
  authoring_proposal:
    type: file
    artifact_type: timeline/authoring-proposal
```

The settled output is the existing six-key object: `schema_version: 1`, `producer` containing `task_id`, `attempt_id`, `executor_id`, `fence`, and `runtime_epoch`, the same four-field `admitted_target`, a nonempty `commands` EditCommand list, nonempty `rationale`, and the SHA-256 `proposal_digest`. The requester forwards this unchanged through the existing producer batch; it does not derive outer producer identity from the inner Speech task.

1. Admit `video_editing.sync_draft_voiceover` as a normal executor using the four-field publication target and the UTF-8 script descriptor/object-id mirror above. The action must produce the existing six-key `authoring_proposal` (`schema_version`, `producer`, `admitted_target`, nonempty EditCommand list, `rationale`, `proposal_digest`).
2. Keep the inner `generation.generate_speech` admission/managed-WAV selection as a precondition only: the existing v1 intent/publication path must settle a real valid WAV, and the outer capture must use the exact five-field `MediaSelection` plus Runtime-verified intrinsic duration. Do not duplicate that inner proof in this case.
3. In the requester, open the existing `TimelineSession` against a private outbox, `queue_proposal`, flush once, simulate lost acknowledgement/restart, retry the identical persisted body and idempotency key, then call the existing guarded `undo` with the accepted publication id.
4. Assert the original voiceover22 positive coverage remains intact: ripple placement and hold changes, source window, draft-voiceover provenance and source identity, history/receipt, commit/retry/undo, and no producer-authority substitution. Assert `rendering.assemble_timeline` and `rendering.render` remain separate and that the inner Speech identity is never the outer producer identity.

No renderer/browser, generation-model, release, public/ordinary pin, old44 lifecycle, historical registered7012 renderer, or new schema is part of this proof.
