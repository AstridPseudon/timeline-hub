# App D01 transition-`None`: current-root standalone writer audit

## Verdict

**No remaining transition-`None` callback fallback exists on the current root.**
The c57 ledger sentence saying that a callback fallback remains for portless
standalone callers is stale. The current source is the post-b14 cut, and its
portless standalone behavior is a visible refusal that leaves the draft alone.

Current source: commit `ddd9e7824c7c0c08b1293132484f5ac52d1de3c3`, tree
`83cf9199f2f858147d8ebbfc6648f01962bbe333`.

The narrow standalone/second inspector consumer was already migrated by the
existing `38b41fad9e` change: `PropertiesPanel.tsx:525` supplies
`captureScalarEdits` to the bulk control and `:566` supplies `captureScalar` to
the single control. No additional migration or new carrier is justified.

## Exact consumer → port → durable writer map

| Consumer | Existing carrier | `None`/`Remove` writer |
|---|---|---|
| `PropertiesPanel.tsx:524-525,560-566` | `useClipScalarControls(selectedClipIdsList)` / `useClipScalarControl(selectedClip?.id)` | `BulkClipPanelBody:207-212` → `submitClipTransitionClears`; `ClipTransitionSection:111-116` → `submitClipScalarEdit` |
| `PropertiesPanelBody.tsx:493-498,532-546` (the public `PublicAstridEditorParts.tsx:18-20,122` lazy consumer) | Existing scalar carriers, with read-only refusal before capture | Same native bulk/single writers; no snapshot callback |
| `ClipPanelBody.tsx:316-320` → `ClipEffectsTab.tsx:167` | `onScalarEditStart` forwarded unchanged | `ClipTransitionSection:111-116` |
| `BulkClipPanel.tsx:7-9` → `BulkClipPanelBody` | `onScalarEditsStart` forwarded unchanged | `BulkClipPanelBody:207-212` |

The native submitters validate the captured basis/session and emit the
durable `clip.set` command: `clipScalarGesture.ts:39-45` for one clip and
`:49-63` for one atomic bulk batch. The command is exactly
`{ values: {}, clear: ['transition'] }`.

## Source resolution of the conflicting reports

The b14 cut review correctly describes the source behavior: the two old
branches were removed from `ClipTransitionSection.tsx` and
`BulkClipPanelBody.tsx`; missing capture authority renders the existing alert.
The immutable c57 gate correctly qualifies bounded native single/bulk
behavior, but its note/ledger wording incorrectly says that the old callback
fallback remains. `git diff c57dcc26162642f503532f143ceb96bb185273aa..HEAD`
is empty for all six relevant inspector/forwarding files, and a current-root
production-only search finds no `transition: undefined` or equivalent
`None`/`Remove` callback writer.

The only remaining `onChangeDeep` transition writes are SET/type-change and
duration/reset/parameter writers (`BulkClipPanelBody.tsx:566,663,692`), which
are separate D01 work and are not `None` writers.

## Evidence

- Targeted Vitest, current root, private runner/cache: **8 files, 180 passed**.
  Files: `ClipPanel.transition.test.tsx`, `ClipPanel.nativeNone.test.tsx`,
  `TransitionPreservation.test.tsx`, `PropertiesPanel.test.tsx`,
  `clipScalarGesture.test.ts`, `clipScalarCapture.test.ts`,
  `commitSession.clipScalar.test.ts`, `useTimelineCommandSession.test.tsx`.
- Native contract: `node --test tests/e2e/local/support/native-transition-clear.contract.test.mjs` — **1 passed**.
- Scoped ESLint over the six consumer/forwarding files and the two scalar
  command files — **passed**.
- `git diff --check HEAD` — **passed**.
- The already-recorded immutable c57 central gate remains the bounded
  single+atomic-bulk qualification; it was not rerun per task instruction.

No full suite, TSC, install, local browser/socket run, or new browser claim
was made. Keep the ledger status **`QUALIFIED (bounded); D01 retirement OPEN`**:
the callback fallback is gone, but transition SET/reset/params and whole-D01
writer retirement remain separate.
