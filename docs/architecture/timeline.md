# Timeline architecture

**Status:** Agent-owned landing page for the approved path and current M4
groundwork. M4 is not complete; the historical R4 control documents remain
archived. See the [editing guide](../timeline-editing-guide.md) and
[authoring capabilities](../timeline-authoring-capabilities.md) for usage.

Timeline has one accepted authored film model and three surfaces. **Read** is a
revision-pinned projection: Agent owns timeline meaning and text/CLI views,
Runtime owns the accepted closure and history, and App owns presentation. **See**
is a projection through the published Composition package/evaluator; preview and
export stay outside save. **Edit**, for migrated operations, is one path:
registered `EditCommand`s from SDK/CLI, App gestures, and supported editable
inputs are captured by the same session.

The command registry is Agent's `astrid/sdk/timeline/commands.py`; its provider
is `astrid/sdk/timeline/commit.py::RuntimeCommitService`. Runtime's ordinary
`/v1/projects/{project}/timelines/{timeline}/commit` route loads that provider
through `runtime_protocol/timeline_commit_provider.py` before readiness and
stores the accepted closure/history in `timeline_commit_store.py`. The client
outbox (`astrid/sdk/timeline/outbox.py`, App's `src/tools/video-editor/commands/commitOutbox.ts`) persists the
exact request, retry identity, and newer local commands. Acceptance validates
structure, timing, references, authority, and ancestry without importing a
renderer; undo and restore are new guarded commits.

Supported derived timing goes through `astrid/sdk/timeline/compiler.py::compile_timing`
and `astrid/sdk/timeline/_timing_evaluators.py`; D07's deprecated retime helpers
are deleted, while live reflow and other derived writers remain held below. See
has one evaluator in Composition (`typescript/src/evaluation.ts`
and `scene-evaluation.ts`). Managed Scene is an explicit diagnostic boundary:
`astrid/packs/rendering/actions/timeline_visualize/scene_only.py` asks the pinned
managed host for Scene answers and emits the filmstrip diagnostic artifact;
unknown or unavailable stays explicit. It is not save authority and does not
make save renderer-dependent.

Producers store immutable artifacts and submit a settled proposal. The requesting
client preserves its requester/attempt pin and queues the original proposal via
`astrid/sdk/timeline/producer.py` and the same outbox; producers do not publish
film edits directly. Runtime's catalog/reference operations remain catalog
metadata, while the film is the accepted canonical closure: its film pin may
authorize its own projection, never a newer catalog head
(`runtime_protocol/timeline_commit_store.py`).

The current tree includes published014/Main497 and the WC6 native document-script
cut/dead-leaf deletion. It consumes the normal published014 Runtime
source/producer lock `95bd3c5f` and Composition `0.0.13`; this is not a delivery or M2
completion claim.

Held legacy paths are visible: Agent's detached `Checkout.publish` /
`publish_authoring_candidate`, remaining cut-sheet three-way publication, and
whole-bundle mutations; timing `resolve`/`reflow` plus narration,
music, and sequence writers; App snapshot ingress
(`useTimelineOps.ts:277-321`), parent publication and `saveTimeline`/
`saveTimelineAtHead` (`dataProvider.ts:295,1000-1131`), popup add/swap, and
local checkpoint restore. Private track/group/transcript/rawOLD operations are
not public commands and are not claimed M2-complete.

**Code anchors:** Agent `astrid/sdk/timeline/{commands,commit,outbox,sync,compiler,producer}.py`;
Runtime `runtime_protocol/{daemon,timeline_commit_provider,timeline_commit_port,timeline_commit_store}.py`;
App `src/integrations/runtime/dataProvider.ts`; Composition
`typescript/src/{evaluation,scene-evaluation}.ts`.
