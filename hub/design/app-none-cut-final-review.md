# App M2 transition-`None` legacy-cut final review

## Verdict

**APPROVE — source cut only.** The final committed tree removes the two
unauthorised transition-removal writers from the previously approved native
None implementation. Supported production inspector entrypoints already pass
the exact scalar capture ports. Missing authority now produces a visible
alert and leaves the draft unchanged. This is not browser qualification and
does not justify a ledger `DELETED` row.

## Frozen source

| Item | Value |
| --- | --- |
| Final commit | `0bc2d8ebbc724c54745276dffa3bd25e869e7d00` |
| Final tree | `81cee4ec952fede797417cbd52be1b006f7a7d99` |
| Parent / comparison base | `b22ab12b6babed85eb41396d5cc5eaa5becad70f` |
| Base tree | `61527d4e10e2ffe141de0c9ac2026357935bb9d4` |
| Final status | clean |
| Delta | 4 paths, 22 insertions, 19 deletions |

The earlier design note's uncommitted identity (`61527d4e` base plus working
delta SHA `43d8fd…`) is stale. Harnesses must key this review to the final
commit/tree above.

## Actual removed code and retained behavior

The final diff changes only these paths:

- `ClipTransitionSection.tsx`: removes the missing-port branch that called
  `onChange({ transition: undefined })`. The `None` selector and `Remove`
  button now require `onScalarEditStart`; otherwise the existing alert renders
  `Transition clear requires an active timeline command session.`
- `BulkClipPanelBody.tsx`: removes the missing-port branch that called
  `onChangeDeep(() => ({ transition: undefined }))`. The equivalent refusal is
  `Bulk transition clear requires an active timeline command session.`
- `ClipPanel.transition.test.tsx` and `TransitionPreservation.test.tsx` update
  the corresponding unauthorised cases one-to-one.

Native success remains unchanged: single clears call
`submitClipScalarEdit(..., { values: {}, clear: ['transition'] })`; bulk clears
call `submitClipTransitionClears`, which finishes every capture first and sends
one atomic batch through `submitBatch`.

## Production caller census

The supported callers are complete and supply the native ports:

- `PropertiesPanel.tsx:238-242` creates
  `useClipScalarControl(selectedClip?.id)` and
  `useClipScalarControls(selectedClipIdsList)`. It passes them at
  `:491` and `:532` to the bulk and single panels.
- `PropertiesPanelBody.tsx:244-250` creates the same ports. Its injected
  `BulkInspector` and `ClipInspector` callbacks at `:495-498` and `:543-546`
  enforce the read-only refusal before capture and otherwise return the exact
  native capture result.
- `ClipPanel` and `BulkClipPanel` are forwarding/resource wrappers. The chain
  is `ClipPanelBody -> ClipEffectsTab -> ClipTransitionSection` and
  `BulkClipPanel -> BulkClipPanelBody`; no other non-test source directly
  instantiates the transition controls.
- `PublicAstridEditorParts.tsx` loads `PropertiesPanelBody`, so it follows the
  guarded native path above.
- `ShotTimelinePreview.tsx` / `shotTimelineDataProvider.ts` use
  `TimelineEditorCore` and the canonical draft/publication surface. They do
  not import or instantiate these inspector controls and have no transition
  `None`/`Remove` callback. Their unrelated preview/projection behavior is not
  changed by this cut.

The only remaining production transition clear is the intended native command
path in `ClipTransitionSection.tsx` and `clipScalarGesture.ts`; the remaining
bulk `onChangeDeep` occurrences are duration/parameter SET writers. The
unrelated `transition: undefined` in `publicAstridNavigation.ts` is a browser
view-transition state field, not a timeline transition writer.

## Test mapping and review checks

Changed tests preserve the original inputs and now test refusal when no
authority is supplied:

| Old case | Final case | Native positive retained |
| --- | --- | --- |
| Single `ClipPanel` Remove with no capture port expected the legacy callback | Same Remove input shows the alert and `onChange` is untouched | `ClipPanel.nativeNone.test.tsx` covers single `None` and `Remove` through the native port, including original-basis guards and no snapshot saves |
| `TransitionPreservation.test.tsx` `None (bulk=false)` used the no-port editor and expected a patch/save | Same input has zero patches/saves and both raw transitions remain | Native single publication removes only the transition and preserves raw payload |
| `TransitionPreservation.test.tsx` `None (bulk=true)` used the no-port editor and expected bulk patches/saves | Same input visibly refuses with zero patches/saves and keeps both raw transitions | Native bulk `None`/`Remove` submits one atomic clear batch; retry/recovery, inverse, and conflict-retention cases remain |

No changed assertion was deleted, skipped, or marked `it.fails`/`xfail`.
SET/type-change and duration/parameter assertions remain on their original
callbacks.

The exact S2 scalar guards remain in `commitSession.ts`: parent targets bind
only `scalar.target`; occurrence targets validate the exact
`scalar.owner`/occurrence/raw-ID/project/document/source identity. The native
contract fixture and test still require the parent command's exact
`{ 'scalar.target': 'parent/clip:…' }` binding and reject invented owner
bindings.

## Evidence run in this review

All commands were local, targeted, and used worker-owned private12/cache/TMP
paths. Shared dependencies were not modified.

```text
TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-none-cut-final-review/private12/tmp \
NODE_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-none-cut-final-review/private12/node_modules \
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-none-cut-final-review/vitest-runner.cjs node_modules/vitest/vitest.mjs run \
  --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-none-cut-final-review/vitest.private12.config.ts --configLoader=runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  ClipPanel.transition.test.tsx TransitionPreservation.test.tsx \
  ClipPanel.nativeNone.test.tsx ClipEffectsTab.test.tsx \
  ClipPanelBody.test.tsx PropertiesPanel.test.tsx \
  clipScalarCapture.test.ts clipScalarGesture.test.ts commitSession.clipScalar.test.ts
```

Result: **9 files, 165 passed, 0 failed**.

```text
TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-none-cut-final-review/private12/tmp node --test \
  tests/e2e/local/support/native-transition-clear.contract.test.mjs
```

Result: **1 test passed, 0 failed, 0 skipped**.

```text
./node_modules/.bin/eslint --no-cache \
  src/tools/video-editor/components/PropertiesPanel/BulkClipPanelBody.tsx \
  src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/ClipTransitionSection.tsx \
  src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx
git diff --check b22ab12b6babed85eb41396d5cc5eaa5becad70f HEAD
```

Both passed. No browser, localhost/socket, build, TypeScript, install, full
suite, or central gate was run.

## Central two-case command (prepared, not executed)

Run only after the manager's root gate is green, from the central final-tree
snapshot. This is the existing two-test lane selected by `M2 native None` and
must use the exact current pair: Agent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`,
Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, Composition public12 archive
`sha256:0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`,
and the verified short TMP path `/tmp/tl13-core-b1`.

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock env \
  -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST \
  TIMELINE_CURRENT013_RUN=1 \
  TIMELINE_CURRENT013_APP_SHA=0bc2d8ebbc724c54745276dffa3bd25e869e7d00 \
  TIMELINE_CURRENT013_APP_TREE=81cee4ec952fede797417cbd52be1b006f7a7d99 \
  TIMELINE_CURRENT013_AGENT_SHA=d8749a9ce12a699672faf3ad96b4e4cbea9245c2 \
  TIMELINE_CURRENT013_RUNTIME_SHA=2c4ac180c2220bdad966bc01e95ad230e99ce26a \
  TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source \
  ASTRID_CHECKOUT=/home/user/work/wt/app-m3-agent013-current-pair-source \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/app-m3-runtime013-producer-source \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  TIMELINE_CURRENT013_SHORT_TMPDIR=/tmp/tl13-core-b1 \
  TMPDIR=/tmp/tl13-core-b1 \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  npm run test:e2e:three-products -- --grep 'M2 native None'
```

The final browser result must prove acceptance, reload/restart, exact retry,
inverse, conflict draft retention, and zero legacy traffic before any ledger
row is marked `DELETED`. This review makes no such claim.
