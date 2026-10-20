# Render producer migration handoff

Worker `vw-m2-render-producer-handoff`, 2026-10-20. Source/design result:
[render-producer-migration.md](/home/user/work/wt/vw-m2-render-producer-handoff/docs/design/render-producer-migration.md).
The design is committed by the harness with the worker branch; this shared note
is its coordination pointer. Worker report:
[REPORT.md](/home/user/work/wt/vw-m2-render-producer-handoff/REPORT.md).

**Hold Runtime render-authority 410.** Installed commands cannot express asset
and clip insertion or explicit populated-target replacement. Agent owns ordinary
registry work and normal host command routing; worker credentials lack both
`projects:write` and `tasks:write`. Viewing made no producer changes.

Runtime follow-up: managed render freezes/checks current head before task replay
lookup (`runtime_protocol/store.py:2226` versus `:2295,2341`). Source indicates
lost render ACK + newer head + restart can refuse an exact admitted retry;
this was not executed. Prove the existing task/snapshot-ref handoff, retain
accepted pins/pending render across crash, and resolve cancellation/attempt-fence
semantics before the normal producer path is retired. No new endpoint/DTO/writer.

Inventory qualification: `publish_stitched_render` remains an exported writer
seam, but no production call was found in current Agent source (only its
definition/export and negative test caller). Assembly's host hook is active.
Both surfaces still need replacement or demonstrated retirement coverage.

No tests/CPU checks ran; required `QUIET.md` was absent from accessible supplied
trees. No full/socket/browser/install/build or shared App graph work occurred.
M2 remains held until the M1 record and original producer/retry/restart proof.
