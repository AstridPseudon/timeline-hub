# Runtime text-binding clear (10:31 approval)

Representation ACKed by Agent at 2026-10-20 10:58 UTC (runtime-coordination.md, Agent ACK section); Runtime candidate bfec49af was independently rejected for legacy-MIME clear/inverse; the bounded custody correction is in rt-m2-text-clear-legacy-custody-fix. Native schema/pair remains open:
- Keep `shot_text_bindings` as the existing stream anchor: identity, non-null
  `media_digest` = last present media, monotonically increasing `head_seq`.
- Append existing kind `shot.text_binding.rebound` for clear and resurrection;
  first birth remains `shot.text_binding.created`. No migration/new event kind.
- Event payload is the existing `{binding_id,project_id,shot_id,kind,slot,
  media_id,content_hash,byte_size,mime_type,publication_id}` plus
  `state: "absent" | "present"`. Missing state in old events means present.
  A clear's media fields retain the last present descriptor as an anchor, NOT
  a live binding. The state is included in the existing event hash chain.
- A recorded present->absent clear compares the exact prior semantic descriptor,
  appends once in the acceptance transaction, then live GET returns not found
  and list omits it. Absent->present restores the recorded descriptor and advances
  the same stream. Present->same-present remains an event no-op; accepted history
  still records the write. Empty UTF-8 remains present even when size is zero.
- Canonical shot payload removes/restores its exact row and list position through
  Agent records/inverse; Runtime never sorts that list or derives film meaning
  from the anchor. Historical shot reuse without a recorded write changes no
  live binding. A pin to an absent event refuses; earlier present pins stay valid.

Reader census (all SQL references plus authored descriptor readers):
`timeline_commit_store._project_text_binding` (presence + exact before compare);
`service._text_binding_resource`, get/list (validated chain + live presence);
`service._validate_published_text_bindings` (selected event presence independently
of current state); `timeline_commit_baseline._text_bindings` (selected historical
head presence); shot GET/inspect/view consume immutable payload membership,
not anchor existence (`service.get_project_shot`, `timeline_inspection`,
`timeline_view`). `backup.export` exports anchor + every raw event including state;
backup/restore/doctor integrity must preserve these, not reinterpret as live rows.
Existing registered objects + project objects retain all text bytes. There is no
GC/delete-objects operation in this Runtime; PLAN defers purge. Qualify deep CAS
reachability, clear/rebind/restart/backup restore and old pinned head; no claim of
a destructive GC run or a new retention store.

Qualification: existing real Runtime acceptance fixture (`bind`/`accept`) is
approved for projection proof; native Agent command+inverse pair only if its
source/schema is ready and ACKed. No fake provider/native end-to-end claim.

Legacy custody correction (same representation):
- NEW first-use `text_selection` remains exactly `text/plain; charset=utf-8`.
  No inline text, caller flag or claimed inverse grants media authority.
- For retained `text/plain` only, projection checks the existing binding's
  complete hash-covered event chain for a PRESENT event with exact binding ID,
  media ID and content hash. It checks every scope/size/MIME field recorded in
  that event; compact main events derive omitted metadata from their binding
  identity and immutable objects row. An absent event alone is insufficient.
- This proof stays within the same project/shot/kind/slot stream. Both current
  before and desired after descriptors retain exact managed-project ownership,
  stored size/MIME, digest-verified CAS bytes, UTF-8 and 1 MiB checks. Missing or
  foreign objects, another binding's media, altered metadata or corrupt event
  history refuse in the existing acceptance transaction. No MIME or byte edits.
- Accepted history/closures supply the Agent's exact inverse descriptor and list
  position; the port's captured closure still supplies manifest media authority.
  Runtime binding-event custody permits projection of that retained descriptor,
  not new text selection. Direct coordination and Agent's actual failing pair
  are recorded in runtime-coordination.md and
  workers/agt-m2-text-clear-retained-pair/notes/report.md.

Qualification still requires independent correction review and the normal
full-schema native Agent pair; this Runtime acceptance fixture does not complete
those gates, publish an artifact, retire a writer or qualify destructive GC.
