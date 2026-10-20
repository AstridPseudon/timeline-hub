# Runtime text-binding clear (10:31 approval)

Proposed representation, awaiting Agent ACK before coupled implementation:
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
Existing accepted media-input/history roots + project objects retain bytes through
GC; verify clear/restart/GC and old pinned head. No new retention store.

Qualification: existing real Runtime acceptance fixture (`bind`/`accept`) is
approved for projection proof; native Agent command+inverse pair only if its
source/schema is ready and ACKed. No fake provider/native end-to-end claim.
