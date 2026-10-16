# Project timeline retention

The request/result source is `schemas/timeline-retention.json`. Routes and
generated Python/TypeScript clients use the existing Runtime envelope and
command ledger. `planTimelinePurge` plans explicit identities; an authenticated
local owner uses `executeTimelinePurge` with the exact targets, digest and an
idempotency key. The plan grants no execution authority. The complete recheck,
payload compaction, deletion and terminal receipt share `BEGIN IMMEDIATE` via
the existing durable mutation wrapper. A changed reference or state rejects the
entire set. No partial deletion or automatic target expansion is permitted.

`createTimeline` optionally accepts `duplicate_source` with an exact active
source publication and revision. Runtime records authenticated creation lineage
in its hash-chained timeline events; ordinary metadata, names and test flags do
not establish eligibility. Runtime also records project-shot projection births
inside a duplicate's publication transaction. This distinguishes target ownership
from mere reachability. Existing project-shot projections without such birth
evidence are conservatively retained. Legacy duplicates without admitted creation
evidence remain ineligible; this change does not invent their provenance.

`archiveTimeline` optionally accepts `withdraw_publication` with an exact current
revision/publication pair. Only the authenticated local owner can withdraw an
admitted duplicate. Withdrawal removes the serving head, retains immutable history,
and records a withdrawal event. Ordinary archive preserves the head. Purge rejects
any current head; historical publications wholly owned by the exact set are
reclaimable after withdrawal. An external historical pin still blocks.

## Reference inventory and actual readers

`runtime_protocol/timeline_retention.py:REFERENCE_TABLES` is the finite inventory.
Each family is read as parsed values, including non-FK identity columns and JSON;
unknown extensions naming a target fail closed. Malformed reference data refuses
the plan. String substring search is not a reference proof.

| Stored family | Runtime readers and obligation |
| --- | --- |
| Parent heads, publications and revision payloads; occurrences and dependency manifests | `service.get_project_parent_composition_revision`, `list_project_parent_composition_revisions`, `restore_project_parent_composition_revision`; `timeline_commit.head`, `revisions`, `revision_closure`; `timeline_inspection.inspect`. Check previous/restored revisions and previous publications. Occurrence IDs are scoped by parent revision. |
| Shot heads/revisions, internal timeline revisions and project-shot projections/items | `service.get_project_shot_revision`, `_verify_shot_head_projection`, `timeline_inspection._child_timeline_id`; `store.verify` revision closure. Shared children survive. A retained internal revision that requires the target timeline's identity blocks deleting that timeline. |
| Legacy revisions, shots/references and state; project documents | `service._timeline_resource`, `_timeline_revision`, `list_timeline_history`, `get_document`; `store._bind_render_timeline_request` resolves exact timeline IDs and saved slugs. Target-owned `timeline:<id>` documents are removed; external document pins block. |
| Render publications, task/run specs, requests/results, continuation admissions, execution bindings and recovery receipts | `service` render preparation/publication recovery; `store` task materialization, continuation admission, effective execution/recovery readers. Frozen snapshots and resolving references remain blockers even when stored without FK constraints. |
| Managed output producer/provenance/regeneration/coverage; generations/variants; project/reference/media metadata and preferences | `store` managed-output reconstruction/provenance and public task-spec readers; `service` project media/generation/reference/document/preferences readers. Preserve shared media and object rows/files. |
| Text bindings/events | `service._validate_published_text_bindings`, `_text_binding_resource`, `_internal_revision_narration_state`; immutable child descriptors pin binding IDs/events/streams. A retained pin retains its owning shot, bindings and child history. Delete only exclusively owned projection history. |
| Command ledger and timeline/task event journals | `service._command_replay_state`, `_receipt_payload`; `timeline_commit.lookup_request`, `revisions`, `evidence`, `commit_timeline`; `store` history integrity. Compound COMMIT aggregate is the canonical `[project_id,timeline_id]` pair. Compact target-owned COMMIT records preserve wrapper shape and return a schema-valid terminal `base_not_found` error; ordinary target command records return terminal purge state. Keys/hashes and receipt identity remain, full reclaimed documents do not. |

Timeline/task event attribution and hash-chain mentions are audit data, not
resolving timeline references; their identifiers do not block unrelated deletion.
Target timeline event streams are removed in full. External publication attribution
is also audit-only, while its explicit previous/restored identity columns are checked.
Task event readers consume placement/provider/recovery facts rather than resolving
timeline identities. No event hash chain is rewritten. Permanent purge receipts
are compact audit data and remain replayable beyond the ordinary command window.
The existing CAS publication journal only manages object publication; retention
does not delete objects, staged object payloads, media, or journal files.

Counts include deleted rows and `command_idempotency_compacted` rows; UTF-8 JSON
payload estimates include removed payloads and replay payload bytes reclaimed by
compaction. They describe reusable SQLite storage, not file shrinkage, secure
erasure or media garbage collection. Plans are conservative: unknown data and
ambiguous references may refuse an otherwise reclaimable set.

All implementation proofs use disposable synthetic fixtures. Protected historical
film preservation, v8-specific evidence/admission/execution, product acceptance
and release remain outside this increment.
