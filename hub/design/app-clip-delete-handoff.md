# App ordinary clip-delete handoff

Status: **capture-ready; UI/session wiring not ready** (M2, docs plus standalone
offline parity only). This handoff is based on App `9c074972c`, Agent integration
`fc324e83`, Agent native worker `bbb60b5cd664f675df0de1679e8fc565ae73fd0c`,
frozen R4 SDK candidate `11caf1d9de291d76f491cf69f7942606b7471d7a`, Runtime
integration `9f9b25c000485e919f30f1411831fe2d5a3c1316`, and frozen Runtime
candidate `31c7ac3a00f7a205f507bf5bd4d4625628d429bd`.

## Native contract

Agent publishes one bounded operation:

```json
{
  "schema_version": 1,
  "op": "clip.delete",
  "version": "1",
  "select": "parent/clip:<raw-id>",
  "args": {},
  "intent": {}
}
```

`select` is exactly one parent-owned clip identity. The native capture records
the whole authored row as one root clear, the parent clip collection membership
and order, the parent occurrence collection, every declared relation it checks,
and the exact target-row guard. A mirrored `parent.config.clips` collection is
compiled as a derived write. The inverse restores the original row and order;
the accepted Agent record, not App state, authorizes undo.

This is not a general “remove” command. The native operation refuses occurrence-
owned targets, legacy shot-owned clips, nested clips, pinned groups, transitions,
and non-empty declared relations (`on`, `until`, `cut`, `formulas`, `sequence`,
`words`, `beats`, `replaces`, and the other listed semantic keys). It also refuses
missing/duplicate identities, divergent clip mirrors, changed membership/order,
changed target source or opaque data, and ABA/same-value intervening writes.
It does not inspect opaque strings as guessed dependencies and never deletes
media, registry entries, source pins, or unrelated rows.

The portable authored input and exact native output are copied from Agent's
`tests/editing_conformance/fixtures/recipe_clip_delete.json` into
`src/tools/video-editor/commands/fixtures/recipe_m2_app_clip_delete.json`.
The semantic input is `select: parent/clip:clip-b`; the command, after bundle,
reads, selections, guarded inverse record, and derived mirror write are fixture
data, not an App-invented wire shape.

## App parity seam

`src/tools/video-editor/commands/clipDeleteCapture.ts` is deliberately standalone.
It provides `captureClipDelete`, `finishClipDelete`, and
`executeClipDelete` over the existing `AuthoredBundle` and recording primitives.
It freezes the original bundle/claims, preserves null/absent/opaque values, and
rejects a refreshed basis rather than recapturing it. It does not register a UI
command, alter `useTimelineCommandSession`, call Runtime, or write a snapshot.
`clipDeleteCapture.test.ts` proves exact command/after-bundle/record parity and
the key ownership, dependency, identity, immutability, and closure refusals.

## Current remove ingress to replace later

The ordinary UI/service/public-patch paths are still legacy writers and remain
open until a real command-door journey exists:

* UI keyboard: `components/TimelineEditorShellCore.tsx` calls
  `lib/keyboard-delete.ts`, which expands pinned groups or builds a local
  `rows` mutation before falling through to `handleDeleteClips`.
* Editing hook: `hooks/clip-editing/useClipDeletion.ts` removes actions and
  calls `applyRowsEdit(..., metaDeletes)`.
* Public service: `hooks/useTimelineCommandsService.ts` exposes `deleteClip`
  and `PUBLIC_TIMELINE_COMMAND_NAMES`; its implementation builds a local rows
  mutation and calls `applyValidatedMutation`. This is not `clip.delete`.
* Public patch: `lib/timeline-patch.ts` still accepts and applies
  `clip.remove`; `lib/sequence-public.ts` projects `metaDeletes`, and
  `lib/shot-group-commands.ts` owns the separate pinned-group removal path.
  Prepared-media `removeClipId`/`removeClipIds` in `commands/media.ts` is a
  separate replacement flow and must not be silently mapped to ordinary delete.

No fallback `clip.remove` or whole-document save is a canonical writer for this
handoff. These paths should be deleted or converted only after the native
registry/capture artifact and Runtime commit artifact are named and frozen.

## Minimal next wiring and tests

1. Freeze the Agent registry entry and Runtime provider artifact/version used by
   App. App should pass the captured command through the existing command
   session/outbox/`commitTimeline` path; it must not add an App opcode or refresh
   the basis from display state.
2. Add a narrow ordinary-delete adapter for one parent clip. Keep group,
   occurrence, legacy-shot, nested, semantic-dependency, and multi-delete inputs
   visibly refused with the local draft/selection retained. No session or UI
   change belongs in this parity branch.
3. Add zero-traffic spies for `applyRowsEdit`/snapshot publication,
   `saveTimeline`, `saveTimelineAtHead`, `publishParentComposition`,
   `config-replaced`, and `clip.remove` on the migrated path. Add outbox lost-ACK,
   exact retry, reload, accepted undo, opaque closure, and intervening-write
   tests before removing any old ingress.

The portable fixture request for the next Agent/Runtime handoff is: provide an
existing authored bundle from the native capture fixture plus a semantic input
(target identity and any required selection/ownership context), and the exact
native command/record/after bundle. Do not request or invent a guessed App
`TimelinePatch`, `clip.remove`, or new wire opcode. Additional occurrence or
group cases need their own published Agent primitive and fixture first.

## Readiness

**Ready:** standalone App capture parity against the official Agent golden;
offline unit tests pass; the direct App typecheck has the two pre-existing
baseline diagnostics only (TS7053 at `RuntimeConnectionProvider.ts:90` and
TS2550 at `AgentChatNewChatButton.tsx:80`); no product writer or Runtime DTO
changes required. The prior claim that `npm exec tsc` passed was incorrect:
the direct `./node_modules/.bin/tsc --noEmit -p tsconfig.app.json` run before
this type-only correction also reported the new TS2345 at
`clipDeleteCapture.ts:92-103`, which this handoff fixes.

**Not ready:** UI/session integration, Runtime acceptance, multi-clip/group
delete, occurrence-owned deletion, or removal of the legacy ingress. M1 remains
merge-held per PLAN, and this branch does not claim Gate 6 closure.
