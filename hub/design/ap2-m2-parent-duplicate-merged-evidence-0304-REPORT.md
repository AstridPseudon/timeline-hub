# Parent-media duplicate merge evidence

Status: complete. The remote merge is present and the owned parent-media
evidence was updated only in the App ledger, master ledger, and parent-media
handoff.

## Merge verified

Actual HOME merge SHA: `0cc7591f0364cfded00e4d582434753ef0c6085f`.

The merge has the required parents:

- approved resolved delivery: `facd9c65accd086b1a15804acaf073620356722e`;
- HOME integration: `1be92c689c77efc3fe1d82eced116e86459139cf`.

The merge tree is unchanged from the resolved delivery. The two parent
ancestry checks both passed. This is the actual two-parent merge result, not a
candidate SHA.

## Evidence update

Updated only:

- `deletion-ledger.app.md`, row `D01-app-parent-media`;
- `deletion-ledger.md`, row `D01-app-parent-media`;
- `handoff-app-to-app2-parent-media.md`.

The evidence records that the original Runtime `MediaSelection`, displayed
head/projection, and preparation epoch are retained. For this specific
`Duplicate generation` menu gesture, no legacy registration or publish writer
is reachable. The existing 26 focused source controls plus types/lint
evidence from reports 0243/0250/0257 remain referenced.

The broad parent-media row remains `open`. Main's catalog adapter and native
`afterClipId` remain visibly unsupported. No native acceptance, exact
placement, reload, lost-ack retry, guarded undo, or broad independent
duplicate-row closure is claimed.

## Live callers

The unchanged specific menu path is:

`ClipAction.tsx:241-251` -> `TimelineEditorCoreBody.tsx:807` ->
`TimelineEditorCore.tsx:839` -> `AstridTimelineEditor.tsx:544-625` ->
`generation-utils.ts` / `generationLookup.ts` ->
`useAssetManagement.prepareGenerationAsset` ->
`useTimelineCommandsService.addClip` -> the existing
`parentClipAddMedia` capture/verify/submit carrier.

Distinct registration callers, including pinned-shot-group synchronization and
`useAddVariantAsGeneration.ts`, remain unchanged and are outside this specific
menu gesture.

## Checks

Read-only merge checks run:

```text
git show --format=fuller --stat --summary 0cc7591f0364cfded00e4d582434753ef0c6085f
git rev-list --parents -n1 0cc7591f0364cfded00e4d582434753ef0c6085f
git diff --stat 0cc7591f0364cfded00e4d582434753ef0c6085f^1 0cc7591f0364cfded00e4d582434753ef0c6085f
git merge-base --is-ancestor facd9c65accd086b1a15804acaf073620356722e 0cc7591f0364cfded00e4d582434753ef0c6085f
git merge-base --is-ancestor 1be92c689c77efc3fe1d82eced116e86459139cf 0cc7591f0364cfded00e4d582434753ef0c6085f
```

Results: merge parents matched; merge diff was empty; both ancestry checks
passed. No product tests, source scan, browser/live run, central proof, or
actual acceptance run was performed, as instructed.

No blocker remains for this bounded ledger update. The broader parent-media
qualification remains open with the limitations above.
