# Timeline cross-product architecture — DRAFT for owner review

**Scope:** M4 groundwork. This describes the current contract; it is not an M4 gate-complete claim.

Timeline has one accepted authored model with three surfaces. **Read** is a revision-pinned projection: Agent owns timeline meaning and text/CLI projections, Runtime owns the accepted closure and history, and App owns its read presentation. A view never relabels old content with a newer head. **See** is also a projection: one Composition package/evaluator answers what is on screen; Agent and App supply the admitted closure, assets, theme and rational frame rate. Composition, projectors, preview and export stay outside save. **Edit** is the single write path.

An author writes stable entity/anchor references and deterministic commands, with declared intent. App gestures, SDK/CLI and editable inputs become the same command batch. The client persists the exact request, idempotency key, allocated IDs and newer commands in a crash-safe outbox. Runtime’s normal `/v1` door loads the Agent provider before readiness. The provider executes against a detached candidate; Runtime’s port permits only exact declared reads (head/history, revision closure, selected media and other pinned inputs). The recorder captures writes—including unchanged writes—reads, selections/order, bindings and created IDs; it is part of accepted meaning, not a diff.

Acceptance is ledger-first: exact scope/key/request-hash replay is resolved before provider work, then one transaction rechecks authority and ancestry and atomically stores the immutable closure, accepted history/head, input links and receipt. Accepted history supplies the intervening-write facts. Undo is a new guarded inverse command; restore is a new sole-command commit naming an immutable historical revision while guarding the current head. Neither rewinds history or invokes Composition.

Slow producers store immutable artifacts and task proposals. They do not publish timeline edits: the requesting client supplies requester authority through a verified settled-attempt/proposal-digest guard, then submits commands through the same commit path. A dry run is a semantic plan, not a mutation receipt.

The current tuple is deliberately split: Runtime server `c1fb9ef` is a compatible patch; it does not replace the immutable generated-client artifact producer `2c4ac18` / contract `0.2.13` and requires no second client pin. Agent public Composition `0.0.12` is integrated; coordinated App adoption and current-pair qualification remain pending.

**Open gaps, stated plainly:** legacy/fallback writers are not yet all retired; capture/`RenderRequest` propagation and native capture authority are not fully qualified; audio and frame parity, final export qualification, and the owner-film viewing gate remain open. These gaps do not justify a second writer, evaluator or save-time renderer.

**Verified code anchors (repo-relative):** Runtime `runtime_protocol/daemon.py`, `runtime_protocol/timeline_commit_port.py`, `runtime_protocol/timeline_commit_store.py`, `runtime_protocol/timeline_commit_producer.py`; Agent `astrid/sdk/timeline/commit.py`, `astrid/sdk/timeline/outbox.py`, `astrid/sdk/timeline/inverse.py`; App `src/integrations/runtime/dataProvider.ts`; Composition `typescript/src/scene-evaluation.ts`.
