# App2 parent media native capture handoff

The source-only seam is `captureParentClipAddMedia(bundle, row, media,
verifiedMedia)` / `finishParentClipAddMedia(basis)` in the existing
`parentClipAddCapture.ts` module. The caller owns allocation of the raw clip
ID and authored asset alias before capture. It passes the original five-field
selection and the detached Runtime-verified media response; finish/retry uses
the frozen basis and never discovers a new selection, clock value, or ID.

The helper emits `clip.add-media` with `{row, media}` and records the Agent
claims. `row.asset` is the authored alias used for the exact registry binding;
it is not rewritten from the selected pin. The native bounded positive is a
literal image/video birth on an already explicit active visual output track.

Future App consumer wiring should therefore be one adapter at the existing
parent media producer boundary:

1. preserve the current manual recovery ADD/popup/automatic-placement paths;
2. after the existing exact selection and verified-media reads complete, capture
   one basis with the original row/selection/verified response;
3. submit the finished command through the existing commit session/outbox;
4. use the existing local preview path, preserving all row/registry opaque data;
5. keep the old producer until actual acceptance, reload, guarded undo/redo,
   exact retry after a lost acknowledgement/restart, and zero legacy traffic
   are proven.

No new session, door, outbox, DTO, allocator, or consumer pin is proposed.
The existing non-media `ParentClipAddCapturePort` remains unchanged until the
App owner chooses the consumer adapter shape.
