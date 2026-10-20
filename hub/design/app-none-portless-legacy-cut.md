# App M2 transition-`None` portless legacy cut

Status: source cut complete on the worker tree. The two real production inspector
entrypoints already supplied the existing scalar command-session ports, so this
cut removes only their now-unreachable legacy transition-removal writers. The
browser/Runtime gate remains unrun; no ledger row is marked `DELETED` and no
qualification or merge is claimed.

## Exact source

| Item | Value |
| --- | --- |
| Worktree | `/home/user/work/wt/app-m2-none-portless-legacy-cut` |
| Branch | `tl/app-m2-none-portless-legacy-cut` |
| Base commit | `b22ab12b6babed85eb41396d5cc5eaa5becad70f` |
| Base tree | `61527d4e10e2ffe141de0c9ac2026357935bb9d4` |
| Working delta | uncommitted; binary diff SHA256 `43d8fdffe497e807477f70caabaaa4e779b0f4607d8b3282cb493d6062918cb1` |
| Changed paths | 4; 22 additions, 19 deletions |

The harness must use the final committed tree after applying this working
delta. The base is exactly the reviewed `b22ab12` / tree `61527d4`; no older
Root, Main17, cold4, pin, or journey source was copied.

## Complete caller census

### Real production entrypoints (covered)

- `src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx`
  creates `useClipScalarControl(selectedClip?.id)` and
  `useClipScalarControls(selectedClipIdsList)`, then passes them to `ClipPanel`
  and `BulkClipPanel` respectively.
- `src/tools/video-editor/components/PropertiesPanel/PropertiesPanelBody.tsx`
  creates the same single and bulk capture ports and passes them through its
  `readOnly` guards to the injected/default `ClipPanelBody` and
  `BulkClipPanelBody` inspectors.
- `ClipPanel.tsx` and `BulkClipPanel.tsx` are forwarding/resource wrappers;
  they do not create another production callback or authority path.
- The internal chain is `ClipPanelBody -> ClipEffectsTab ->
  ClipTransitionSection` and `BulkClipPanel -> BulkClipPanelBody`. No other
  non-test source imports these controls.

### Standalone, popup, and preview census

- Direct standalone section/body uses are the nearest component tests only:
  `ClipPanel.transition.test.tsx` and `TransitionPreservation.test.tsx`.
  Omitting the port now visibly refuses a clear and leaves `onChange` /
  `onChangeDeep` untouched; it is not a writer.
- `ShotTimelinePreview.tsx` renders `TimelineEditorCore` and the
  `shotTimelineDataProvider` canonical draft/publication surface. It does not
  import or directly instantiate `ClipPanel`, `BulkClipPanel`,
  `ClipTransitionSection`, or `BulkClipPanelBody`, and has no transition-`None`
  callback. Its preview/projection and canonical draft publication behavior is
  unchanged.
- No `AstridBridgeDataProvider`, `SupabaseDataProvider`, popup transition
  callback, or other non-test transition-`None` writer was found in the source
  census.

## Deleted paths and retained paths

Deleted exactly:

1. `ClipTransitionSection.tsx`: the missing-port branch that called
   `onChange({ transition: undefined })`.
2. `BulkClipPanelBody.tsx`: the missing-port branch that called
   `onChangeDeep(() => ({ transition: undefined }))`.

When authority is absent, both controls now throw a local explanatory error
into their existing `role="alert"` UI and retain the draft. With authority,
they still use `submitClipScalarEdit` / `submitClipTransitionClears`, the
existing capture-before-finish and outbox path. No snapshot fallback, new
outbox, bridge, or ownership inference was added.

Retained intentionally:

- transition SET/type-change callbacks;
- duration and parameter/reset callbacks;
- all other unsupported bulk effect writers;
- the existing production read-only guards;
- all parent/Main17/cold4/pin and original seven-journey paths.

The remaining `onChangeDeep` transition occurrences are the existing duration
and parameter/reset SET writers, not `None`/removal writers.

## Old/new test case pairs

| Old named input | New no-authority expectation | Native positive retaining the original visible outcome |
| --- | --- | --- |
| `ClipPanel.transition.test.tsx`: single Remove click with no capture port, previously expected `onChange({ transition: undefined })` | Remove shows `Transition clear requires an active timeline command session.`; `onChange` is not called | `ClipPanel.nativeNone.test.tsx`: mounted single `None` and `Remove` capture and submit one guarded clear; opaque/revision/unknown/prototype/order/inverse assertions remain |
| `TransitionPreservation.test.tsx`: `None (bulk=false)` through the old single callback | Same input shows the refusal, produces zero patches/saves, and keeps each raw transition | `TransitionPreservation.test.tsx`: native single `None` publication removes only the transition and preserves raw payload; retry/recovery/inverse neighbors remain |
| `TransitionPreservation.test.tsx`: `None (bulk=true)` through the old bulk callback | Same input shows the bulk refusal, produces zero patches/saves, and keeps both raw transitions | `TransitionPreservation.test.tsx`: native bulk `None` and `Remove` submit one atomic clear batch; raw opaque/prototype/order, retry/recovery, inverse, and conflict-retention cases remain |

No old case was deleted, skipped, or marked xfail. SET/type-change and
duration/params cases retain their original callback assertions.

## Evidence

Commands run in this worktree:

```sh
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.test.tsx
# 4 files, 55 passed, 0 failed

./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx
# 2 files, 41 passed, 0 failed

./node_modules/.bin/eslint --no-cache \
  src/tools/video-editor/components/PropertiesPanel/ClipTransitionSection.tsx \
  src/tools/video-editor/components/PropertiesPanel/BulkClipPanelBody.tsx \
  src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx
# passed

git diff --check
# passed
```

The first attempted Vitest command used unsupported `--cacheDir` and ran no
tests; the subsequent commands used the installed Vitest `--no-cache` mode.
The `--configLoader=runner` form is incompatible with this repo config because
it relies on CommonJS `__dirname`; no test was claimed from that failed startup.
No browser, localhost/socket, build, install, TypeScript, full suite, or
central gate was run.

## Review boundary

The source cut is ready for the manager’s review. The actual two-case browser
gate must use the final harness tree only after the manager’s root gate is
green. Only after that gate passes should the manager update the ledger row to
`DELETED`; this worker does not make that claim.
