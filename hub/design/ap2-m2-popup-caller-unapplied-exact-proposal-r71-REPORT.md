# App2 popup occurrence ADD caller — exact proposal result

Status: **NO-CARRIER / blocked before an honest product patch**.

Source reviewed: App `92c30b570` (`tl/app-m2-popup-caller-unapplied-exact-proposal-r71`).
The r63 handoff and the rejected broad `6fcddfcb` review were read before the
current caller source and retained `15911` trace. No App2 row-local product
files or assertions were changed. No activation, SWAP/projection change,
browser run, or actual was performed.

## Exact blocking boundary

The existing occurrence port requires all of the following synchronously before
its verified-media await:

```ts
capture({ ownerRef, row, media, current })
```

(`src/tools/video-editor/commands/commitSession.ts:107-129`). The current
manual popup caller does not carry an explicit `ownerRef` plus approved raw
child birth row to any of the App2-owned files:

- `useAssetManagement.ts:67-94` accepts only editor state, parent `addClip`,
  and provisioned media. `TimelineProvisionedAsset` carries only the optional
  five-field `mediaSelection`; it carries no occurrence owner or raw child
  row (`commands/provisioning.ts:6-14`).
- `useExternalDrop.ts:62-134,453-474` forwards only the normal drop position,
  generation/file preparation, and `handleAssetDrop`; no occurrence carrier is
  present.
- `external-drop-utils.ts:43-67` receives ordinary `GenerationDropData` and
  prepares a registered asset. `GenerationDropData` itself has generation,
  variant, media-id, display URL, and metadata only
  (`src/shared/lib/dnd/dragDrop.ts:50-58`); it has neither `MediaSelection`
  nor an occurrence/raw-row birth result.
- `useTimelineState.ts:962-974` does not pass the already-mounted
  `save.commands.occurrenceAddMediaPort` into `useAssetManagement`, and
  `useTimelineState.ts:995-1015` does not pass it to `useExternalDrop`.
- The popup occurrence identity is available to `ShotTimelinePreview` as a
  component prop (`ShotTimelinePreview.tsx:388-417`), but the nested
  `VideoEditorProvider` receives no occurrence owner/birth carrier
  (`ShotTimelinePreview.tsx:638-648`). Deriving the owner by parsing the
  generated timeline ID or inspecting display projection would violate the
  settled ownership rule.

The parent path is not a carrier: `useTimelineCommandsService.ts:475-551`
builds a parent `addClip` row and calls `parentClipAddMedia`. Reusing it for an
occurrence would manufacture the missing owner/child-track binding and would
cross the App/App2 ownership boundary.

The five-field selection is also not available for every requested ingress:
Runtime file import can retain it through `PreparedMediaImport` and
`prepareGenerationAsset`, but gallery single/multi-generation and bare
`asset-key` drops enter through `GenerationDropData` without it. A late catalog
lookup would not be the original frozen selection and is explicitly refused by
the brief.

## Entry-point disposition

| Popup ingress | Current explicit carrier | Result |
| --- | --- | --- |
| Add Images chooser | `File` -> upload/prepared asset -> ordinary drop | **NO-CARRIER** for owner/raw row; file imports may retain media selection only |
| Desktop file drag/drop | same | **NO-CARRIER** for owner/raw row |
| Gallery single-generation drag | `GenerationDropData` | **NO-CARRIER** for selection and owner/raw row |
| Gallery multi-generation drag | `GenerationDropData[]` | **NO-CARRIER** per-item selection and owner/raw row |
| Gallery `asset-key` drag | asset key + kind | **NO-CARRIER**; no selection or owner/raw row |
| Gallery shot/group drag | shot/group payload; ordinary multi-row route | Not an occurrence ADD route; preserve existing route |

The existing parent-media route and current skeleton/drop cleanup remain
unchanged. No missing-port refusal or async success behavior was added because
there is no honest way to select the occurrence branch yet. In particular, the
rejected `6fcddfcb` pattern must not be revived: it late-looked up selection,
fabricated a popup row/owner, returned success before capture/finish/submit,
and changed parent behavior on an early `current` guard.

## Patch and regression result

No flat product patch is exported: the only possible hunk at this source state
would introduce a new owner/raw-row carrier or infer one, both prohibited by
the plan. Consequently no direct occurrence-branch regression can be written
honestly against a real carrier. The existing caller tests remain unchanged.

Required next input from the owner before App2 can produce the requested flat
patch:

1. An existing preparation/birth result containing the explicit
   `ownerRef`, raw child row (`id`, `track`, `clipType`, `asset`, `at`, `hold`,
   and video `from`/`to`/`speed` where applicable), and the original five-field
   `MediaSelection`.
2. A shared, typed handoff of that result into the App2 caller files without
   deriving it from display geometry, timeline IDs, latest media, or the
   parent row builder.

Once supplied, the App2 patch must await capture -> exact verified-media read ->
finish -> submit, return success only after submit, preserve draft/asset on
missing-port/refusal/throw, and remove only a still-transient upload skeleton
in `finally`. It must cover the chooser, file drop, and eligible gallery
callers while leaving unsupported bare/group routes distinct.

## Evidence

```text
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=2 \
  src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx \
  src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts \
  src/tools/video-editor/hooks/useExternalDrop.test.tsx
```

Result: **3 files passed, 44 tests passed** (5.59s).

Dependency resolution was read-only and points to the shared install:
`node_modules -> /home/user/work/app/node_modules`.

Not run: browser/full suite, localhost/live sockets, build, TypeScript,
install, graph, Runtime/Agent integration, or SWAP actual.
