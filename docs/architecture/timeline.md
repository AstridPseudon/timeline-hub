# Timeline architecture

**Status:** Agent-owned landing page for the approved canonical path and current
M4 groundwork. M4 is not complete. The historical R4 control documents remain
archived; this page does not delete or rewrite them.

Timeline has one accepted authored model and three surfaces. **Read** is a
revision-pinned projection: Agent owns timeline meaning and text/CLI views,
Runtime owns the accepted closure and history, and App owns presentation. A
view never relabels old content with a newer head. **See** is also a projection:
one Composition package/evaluator answers what is on screen; preview and export
stay outside save. **Edit** is the single write path.

Authors provide stable entity/anchor references and deterministic commands with
declared intent. SDK/CLI, App gestures and editable inputs become the same
command batch. The client persists the exact request, idempotency key, allocated
IDs and newer commands in a crash-safe outbox. Runtime's normal `/v1` door
loads the Agent provider before readiness. The provider works on a detached
candidate; Runtime permits only exact declared reads of the head/history,
revision closure, selected media and other pinned inputs. The recorder captures
writes (including unchanged writes), reads, selections/order, bindings and
created IDs; that record is accepted meaning, not merely a diff.

Acceptance is ledger-first: exact scope, key and request-hash replay is resolved
before provider work, then one transaction rechecks authority and ancestry and
atomically stores the immutable closure, accepted history/head, input links and
receipt. Undo is a new guarded inverse command; restore is a new sole-command
commit naming an immutable historical revision while guarding the current head.
Neither rewinds history nor invokes Composition.

Slow producers store immutable artifacts and task proposals. They do not publish
timeline edits: the requesting client supplies verified requester authority and
submits commands through the same commit path. A dry run is a semantic plan,
not a mutation receipt.

The current tuple is Runtime013's immutable `artifactproducer2c` client/artifact
producer (`2c4ac180c2220bdad966bc01e95ad230e99ce26a`) with compatible Runtime
server at `7f6dd89`; no second producer/client pin or delivery-completion claim
is made. Agent public Composition `0.0.12` is integrated. App adoption and the
final viewing/writer gates remain pending.

Open work is explicit: legacy/fallback writers and the cut-sheet migration are
not fully retired; native capture authority and `RenderRequest` propagation are
not fully qualified; frame/audio parity, final export and the owner-film viewing
gate remain open. These gaps do not justify a second writer, evaluator or
save-time renderer.

**Code anchors:** Runtime `runtime_protocol/daemon.py`,
`runtime_protocol/timeline_commit_port.py`,
`runtime_protocol/timeline_commit_store.py`,
`runtime_protocol/timeline_commit_producer.py`; Agent
`astrid/sdk/timeline/commit.py`, `astrid/sdk/timeline/outbox.py`,
`astrid/sdk/timeline/sync.py`; App
`src/integrations/runtime/dataProvider.ts`; Composition
`typescript/src/scene-evaluation.ts`.
