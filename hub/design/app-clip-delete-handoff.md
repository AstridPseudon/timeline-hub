# App ordinary clip-delete handoff

M2 branch only. Capture and durable-session seam are implemented; UI wiring and
actual server acceptance remain open. No M2 integration merge until PLAN records
M1. App base `9c074972c` retains the opaque recovery roots, all original journeys,
the exact three `it.fails`, Runtime 0.2.1/schema4e52 and Composition 0.0.8 pins.

## Sources and readiness

The original handoff at App `961197e84` names Agent native worker
`bbb60b5cd664f675df0de1679e8fc565ae73fd0c` (capture/delete/recording implementation
and golden), Agent integration `fc324e83`, Runtime integration `9f9b25c`, and
frozen R4 SDK `11caf1d9` / Runtime `31c7ac3a` for comparison. The R4 references
are historical source references, **not the current official Runtime artifact**.
The delete implementation/golden is native forward-port worker source, not a
claim that App's pinned official artifact accepts it. The old move source note
naming `sdk/timeline/capture.py::move` is recipe provenance, not a package pin.

Only the three capture/golden files were copied from `961197e84`; its mistakenly
repo-local design document was moved here. The original golden is byte-identical.
Two copied-capture parity gaps were corrected against that exact native source:
`Recording.compile_mirrors` records an empty final collection, and `State.set`
preserves colons within raw IDs. App now does both, with a regression test.

Actual server proof waits for the widened official Agent registry/provider and
Runtime generated artifact with an exact source tuple. App pins are unchanged:
client 0.2.1, schema
`4e52f7df017db99483ffcd0c593ce414b6443d5d0214ada943bb26fdfcc1714d`,
Composition 0.0.8. No schema guessing or compatibility writer is introduced.

## Native contract and guards

```json
{"schema_version":1,"op":"clip.delete","version":"1","select":"parent/clip:<raw-id>","args":{},"intent":{}}
```

The target is exactly one parent-owned raw clip. Native capture records its whole
authored row/root clear, parent clip membership/order, occurrence collection,
and every declared relation it checks. Mirror synchronization is a derived write.
The accepted Agent record authorizes inverse/restore; App never invents an inverse.
Original value-and-identity guards govern dependent commands: equal-state ABA is
NOT a dependent-edit conflict under PLAN. Accepted history/inverse write guards
remain server-owned; the old handoff's blanket ABA refusal statement was too broad.

Native delete refuses occurrence-owned/legacy-shot/nested targets, pinned groups,
transitions and nonempty declared semantic relations (`on`, `until`, `cut`,
`formulas`, `sequence`, `words`, `beats`, `replaces`, etc.). It rejects ambiguous
IDs, divergent clip mirrors, changed target source/opaque fields, and changed
collection membership/order. It never guesses dependencies from opaque strings,
removes media/registry/source pins, or replaces unrelated rows.

## Session seam

`commands/clipDeleteGesture.ts` publishes:

```ts
interface ClipDeleteCapturePort {
  capture(input: { clipId: string; current: TimelineData }): JsonObject;
  finish(basis: JsonObject): { command: EditCommand };
  submit(input: { command: EditCommand; preview: TimelinePatch }): void;
}
captureClipDeleteEdit(port, current, clipId);
submitClipDeleteEdit(captured);
```

Raw session and mounted hook expose `.clipDeletePort`. Capture fences raw scope,
exact display head pair and unique raw parent identity, then captures native
claims over the optimistic raw bundle. Finish verifies ORIGINAL claims against
the current bundle, preserving unrelated remote row updates. Submit accepts only
one `clip.remove` local preview for the SAME ID. Only the native `clip.delete`
command is persisted/submitted canonically; a preview is never a replacement save.
The existing prepared map, generation fence, dependent basis, outbox, retry,
undo and disposal drain are reused. The hook fences every phase while older
snapshot work remains dirty.

Track-label session work is on another branch. Compose its independent port
and hook deltas with this change; neither branch replaces the other's shared
files or adds another outbox/framework.

## Remaining writer integration

UI keyboard deletion (`keyboard-delete.ts`), `useClipDeletion.ts` via
`applyRowsEdit`, public `useTimelineCommandsService.deleteClip` via
`applyValidatedMutation`, and public `timeline-patch.ts`/`sequence-public.ts`
removal ingresses remain to migrate. Pinned-group removal and prepared-media
replacement (`removeClipId`/`removeClipIds`) are distinct operations; do not map
them silently to this bounded parent deletion. No UI/state/service/useTimelineOps
changes belong in this session branch.

Offline tests cover exact golden/record parity, whole-row guards, queued
move→delete, both lost-ACK/reload positions, identical retry keys/bodies, fresh
dependent identity, same-turn drain, unrelated-row preservation and native
refusals. Mounted tests cover local preview, visible refusal with retained
outbox, zero snapshot saves and every legacy-clean phase. Outgoing accepted
`timeline.inverse` intent is checked; actual server guarded undo is unverified.
Next: after official artifact publication and M1 record, compose the session
ports, wire ordinary single-parent ingress, then prove real success/reload/undo
and zero legacy traffic before deleting the old writer branches.
