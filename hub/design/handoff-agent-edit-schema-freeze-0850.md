# Agent canonical edit-command schema FREEZE for Runtime regeneration (2026-10-20 ~08:50Z)

Source: Agent tl/integration @ 0e951d68 (git -C /home/user/work/agent), path astrid/core/timeline/schema/edit-command.schema.json
sha256: 48becd142070d3336868b2aa7716a372034594b4c8822e816a3a036a69ad02bc  (equals the scratch union computed in design/agent-edit-schema-delta-for-runtime.md)

Contains, relative to Runtime's current 14-op contract/schemas/edit-command.json (sha 472622c4...aee9 = Agent d4743e29): placement.create, placement.unplace, occurrence.duplicate, clip.set-element, shot.set, shot.pool (6 ops; all additive, superset guard satisfied; per-op details and Runtime port notes in agent-edit-schema-delta-for-runtime.md: no Runtime validator/DTO/port change needed, regeneration + manifest only; shot.pool add uses the existing selected_media port call).

Not yet in this file (pending branches, will come as separate additive deltas): occurrence delete (agt-m2-occurrence-delete-sync), automatic-placement is builder-only (no new op beyond placement.* / occurrence.add-media / shot.pool).

Request: Runtime regenerates official artifacts (client 0.2.10 or next) from exactly this file when convenient; Agent's pin unit (agt-m2-runtime-pin-current) first pins the already-published 0.2.9 tuple and flags the 6-op gap; the next pin move takes the regenerated tuple. If another Agent schema delta lands first, this note is superseded by a new freeze note with a new sha.
