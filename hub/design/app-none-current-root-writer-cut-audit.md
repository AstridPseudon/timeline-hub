# D01 App transition-None serialization: deletion-readiness audit

Status: **OPEN — source deletion ready, durable deletion unqualified.** Audited
candidate `0bc2d8ebbc724c54745276dffa3bd25e869e7d00`, tree
`81cee4ec952fede797417cbd52be1b006f7a7d99`, parent
`b22ab12b6babed85eb41396d5cc5eaa5becad70f`/tree
`61527d4e10e2ffe141de0c9ac2026357935bb9d4`. No product or ledger files were
changed here.

## BEFORE → AFTER durable writer graph

Before, `PropertiesPanel`/`PropertiesPanelBody` reached the single or bulk
inspector, then `ClipEffectsTab → ClipTransitionSection` or
`BulkClipPanel → BulkClipPanelBody`. Selecting `None`/`Remove` fell back to
the ordinary callbacks: `onChange({ transition: undefined })` or
`onChangeDeep(() => ({ transition: undefined }))`. Those snapshot/partial
writers fed the legacy publication path where `rowsToConfig` and the partial
publisher could restore the old raw transition.

After, the supported production routes pass the durable scalar ports:

* `PropertiesPanel.tsx:238-250,490-532` uses `useClipScalarControl(s)` and
  passes `onScalarEditStart`/`onScalarEditsStart`.
* `PropertiesPanelBody.tsx:244-250,493-546` passes the same ports through
  injected/default inspectors, with an explicit read-only refusal.
* `ClipTransitionSection.tsx:111-120` requires a captured scalar edit and
  submits `{ values: {}, clear: ['transition'] }` through
  `submitClipScalarEdit`; `BulkClipPanelBody.tsx:207-216` requires captured
  edits for every selected clip and submits one `submitClipTransitionClears`
  batch. The port validates raw ownership/basis before finish and the batch
  requires the same port plus `finishBatch`/`submitBatch`.
* The candidate diff deletes both old fallback expressions. A candidate-wide
  production search finds no `transition: undefined` fallback. This is an
  actual branch deletion, not fixture bypassing; `onChange`/`onChangeDeep`
  remain only for other supported fields.

Static deletion condition: all supported production inspector entrypoints
provide the required scalar capture port, and every in-repo portless direct
route refuses visibly. This condition passes in the candidate; durable row
deletion still waits for the real two-case gate below.

There is no non-test popup/preview instantiation of these controls:
`ShotTimelinePreview`/`shotTimelineDataProvider` use their separate canonical
draft/publication surface. In-repo direct standalone control tests omit the
port; they now show the existing alert and leave `onChange`/`onChangeDeep`,
patches, saves, and clip input untouched. This is a visible refusal, not a
legacy writer.

## Remaining writers (not part of this deletion)

Transition SET/type changes remain at `ClipTransitionSection.tsx:147-162` and
`BulkClipPanelBody.tsx:554-572`. Single duration, reset-defaults, and parameter
writes remain at `ClipTransitionSection.tsx:258-338`; bulk duration and
reset-defaults remain at `BulkClipPanelBody.tsx:648-701`. Other bulk effect
`onChangeDeep` SET/reset/parameter writers are likewise distinct. Do not call
these “None” writers or claim all transition writers are retired.

## Proposed ledger update (do not apply here)

`D01-app-transition-none-serialization | what: legacy rowsToConfig/partial
publisher transition-None removal path (the two fallback branches above) |
contradicts: explicit None must remove the canonical transition |
replaced by: native clip.set clear with original owner guards, single and
atomic bulk |
owner: app | ms: M2 | status: OPEN |
evidence: source cut 0bc2d8ebb/tree81cee4ec; removed paths
ClipTransitionSection.tsx and BulkClipPanelBody.tsx; replacement tests
ClipPanel.transition.test.tsx, ClipPanel.nativeNone.test.tsx,
TransitionPreservation.test.tsx,
tests/e2e/local/support/native-transition-clear.contract.test.mjs,
and the two-case `M2 native None` browser cases at
tests/e2e/local/three-products.spec.ts:1382,1458. Existing targeted evidence
is 9 files/165 passed plus the native contract test; no browser/integration
acceptance yet. Keep OPEN until both real cases prove raw absence, accepted
reload, inverse, lost-ACK/restart exact retry, real conflict draft retention,
and zero legacy traffic.`

The current-root cold-start fix is active and must be composed before that
real gate; this audit does not claim current-root readiness or gate evidence.
