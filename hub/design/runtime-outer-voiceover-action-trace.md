# Runtime / Agent outer voiceover action trace

Date: 2026-10-20 UTC  
Scope: identify the actual registered outer voiceover action and its Runtime
task boundary. This is a source trace and handoff; it does not change the
Runtime contract or add an Agent action.

## Verdict

The exact registered outer action is `video_editing.sync_draft_voiceover`.
`generation.generate_speech` is the inner speech-generation action used by
that outer implementation and must not be renamed, remapped, or treated as
the outer voiceover family.

The outer action is declared and registered as an executor action. The frozen
video-editing documentation examples that invoke it with
`kind="orchestrator"`, and the prose describing child tasks, do not match the
action registry/source: there is no `local_orchestrator` marker and no
`child_delegation` declaration on this action.

There is no captured outer submission and no settled outer
`authoring_proposal` in the evidence available today. Therefore the existing
outer action is not yet qualified as a Runtime D13 producer flow. Runtime has
no product-code change to make for this trace.

## Source and registry chain

1. `astrid/packs/video_editing/pack.yaml:26-35,44-48` declares
   `sync_draft_voiceover` and exposes the entrypoint
   `video_editing.sync_draft_voiceover`.
2. `astrid/packs/video_editing/pack.yaml:52-127` declares the action,
   including its Python invocation at
   `actions/sync_draft_voiceover/run.py:function=run`, the project/timeline
   and script-adoption inputs, and report/receipt outputs.
3. `astrid/core/execution/executor/actions.py:91-152` turns that declaration
   into an executor definition. Since the declaration has no command and no
   `metadata.local_orchestrator`, its kind is the built-in/executor path.
4. `astrid/core/execution/executor/registry.py:155-182` registers the
   resulting executor action. The orchestrator registry only admits actions
   marked local orchestrators (`astrid/core/execution/orchestrator/registry.py:306-340`),
   so this action is not an orchestrator-registry entry.
5. `astrid/packs/video_editing/actions/sync_draft_voiceover/run.py:9-70`
   guards the exact symbol, opens the SDK client, invokes the shared
   `sync_draft_voiceover` helper, and returns only `report` and `receipt`.
6. `astrid/packs/video_editing/shared/draft_voiceover.py:382-411` is the
   inner call site. Its `runtime_synthesizer` invokes exactly
   `generation.generate_speech` and verifies the returned speech and manifest
   before returning audio metadata to the outer helper.
7. `draft_voiceover.py:414-477` performs the outer script comparison,
   preserve/RIPPLE planning, validation, and legacy authoring publication.
   The current source does not emit Runtime D13 `authoring_proposal` output.

## Task, attempt, and result boundaries

| Stage | Exact symbol | Identity relation | Settled result evidenced |
| --- | --- | --- | --- |
| Outer action | `video_editing.sync_draft_voiceover` | If admitted, its task and attempt are its own. No captured submit is available. | Caller-bound `report`/`receipt`; `output_result_exemptions.json:304-308` records no stable worker-owned artifact path. No D13 proposal is evidenced. |
| Inner speech task | `generation.generate_speech` | Separate executor task and attempt. No `delegated_parent`, `parent_task_id`, `parent_attempt_id`, or `child_key` is evidenced. | Managed `speech`, `speech_manifest`, and `speech_words` outputs, plus the SDK result IDs. `runtime_synthesizer` returns only selected text/settings/audio/duration/run/task fields and drops the richer association/attempt/provenance context. |
| Runtime D13 producer result | Existing generic `authoring_proposal` carrier | Not present in this outer flow today. | No settled producer result to capture or authorize. |

The outer action declaration has neither `child_delegation` nor
`delegated_recoverable_outputs`. The generic host installs a child bridge only
when such policy/custody is present (`astrid/core/execution/generic_host.py:10947-10959`;
`astrid/sdk/_child_bridge.py:476-515`). The inner source also supplies no
`child_key`. Consequently, the source does not establish a parent-child task
relationship; do not invent one from the call nesting.

The only SDK recorded-submit fixture currently available is the earlier
`generation.generate_speech` fixture in
`runtime-speech-main-admission-trace.md`. It proves inner admission only: it
contains the inner capability/spec and no outer action submission, outer task
identity, or settled outer proposal. No model, render, or full-flow run was
used.

## Runtime acceptance boundary

Runtime already has the generic D13 admitted-target and proposal guard:

- `runtime_protocol/timeline_commit_producer.py:16-39` defines the existing
  target and producer-pin fields.
- `timeline_commit_producer.py:224-265` captures a completed settled task only
  when its declared output is the existing `authoring_proposal` timeline
  artifact and the proposal is closed/valid.
- `runtime_protocol/timeline_commit_port.py:338-380` requires the producer
  guard first and consumes the one-shot producer capture.
- `runtime_protocol/store.py:270-285` preserves arbitrary public task-spec
  inputs after removing only internal execution fields.

There is no voiceover-specific Runtime whitelist or new Runtime DTO/API/schema
needed for this trace. The existing private script-pin input shape still
requires an Agent ACK before an outer POST is attempted. Preserve the exact
target/base pair and existing pin values; do not invent a new scope,
producer token, or carrier here.

## Agent handoff

Agent/orchestration must coordinate the choice of the existing native D13
wrapper around the already registered `video_editing.sync_draft_voiceover`
action. The qualification evidence should be one recorded outer submission
and its settled outer `authoring_proposal`, with the outer task/attempt
identity, exact admitted target/base pair, and the Agent-ACKed private script
pin. The inner `generation.generate_speech` task and its managed audio result
must remain a separate identity and cannot serve as the outer producer result.

Until that evidence exists, retain the original 22 successes and their paths;
do not rewrite those expectations or route the inner action as the outer
voiceover action.

