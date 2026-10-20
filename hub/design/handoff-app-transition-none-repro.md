# App M2 transition safety marker repair

## Source cleanup

Removed only the newly added `None publication` expected-failure declaration
from:

`src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx`

The removed declaration was:

```tsx
// Requirement: rowsToConfig must retain the explicit undefined transition
// until RuntimeDataProvider can remove it from the immutable raw basis.
it.fails.each([false, true])('None publication (bulk=%s) removes the raw transition', async (bulk) => {
  const { clips, assertPublished } = await editor(bulk);
  fireEvent.change(within(transitionSection()).getAllByRole('combobox')[0], { target: { value: '__none__' } });
  await assertPublished(clips.map((clip, index) => {
    if (!bulk && index) return clip;
    const { transition: _transition, ...rest } = clip;
    return rest;
  }));
});
```

This removed one source declaration representing exactly two cases (`bulk =
false` and `bulk = true`). The file therefore changed from 11 test
declarations / 23 expanded cases to 10 declarations / 21 expanded cases.
All product fixes, inputs, passing metadata/known-reset/None-callback/type
change cases, and the original ordinary `None (bulk=%s) explicitly clears
only the transition` cases remain in the repository unchanged.

The three named group-drag `it.fails` declarations remain the only expected
failures. `scripts/quality/check-known-failures.mjs` remains unchanged with
`MAX_SRC_ENTRIES = 0` and its exact three-name allowlist.

## RED requirement retained outside the repository

The new requirement remains open and RED: after a None callback, publication
must remove the raw transition for both single-clip and bulk edits. This is a
pre-existing legacy `rowsToConfig` / immutable raw-basis bug, not an M1
reopen. The current native `clip.transition.set` clear-None path already
exists in `028`; this small repair does not patch the legacy writer,
`rowsToConfig`, or refresh authority. Functional None publication sequencing
belongs to the manager/owner decision.

Exact input and expected result retained from the rejected test:

1. Build the same mounted editor fixture with `editor(false)` or
   `editor(true)`, using the existing `rawClip('a', 5)` and `rawClip('b', 9)`
   inputs (each has a raw `transition` plus opaque/nullable/prototype-looking
   JSON fields).
2. Select the transition combobox and dispatch
   `{ target: { value: '__none__' } }`.
3. Expected authored removal: for `bulk = true`, both selected clips have
   the `transition` own property removed; for `bulk = false`, only the first
   selected clip has it removed and the second remains unchanged.
4. Expected publication removal: the same transition-own-property removal
   must appear in `parent_composition.config.clips` and
   `parent_composition.clips`, with the predecessor clip still present.

The existing authored callback test already proves step 3. The missing RED
publication assertion is exactly step 4 and must not be converted into an
expected failure in the committed suite.

## Reproduction / run instructions

Run from the App worktree after temporarily placing the removed body back as
an ordinary `it.each([false, true])` test (or paste that exact body into a
local-only test file). Use the existing test's imports and helpers; no repo
helper export or framework change is needed:

```bash
npx vitest run --config config/testing/vitest.config.ts \
  src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx \
  --testNamePattern='None publication'
```

The repro is expected to be RED in both rows. It should show that the
published wire/config clips retain the old raw transition after the None
callback, so the exact failure is in legacy publication coverage rather than
in the callback's authored removal.

## File removal and test-count record

- Removed file declarations: 1 (`None publication (bulk=%s)`), expanding to
  2 removed test rows.
- Repository files otherwise changed: none.
- Expected-failure markers after cleanup: 3 authorized, 0 forbidden.
- The notes file is outside the repository and is not part of the App commit.

## Verification

- RED reproduction before cleanup: 2 failed rows (`bulk=false`, `bulk=true`),
  both showing the old raw transition retained in published config/wire clips.
- `npx vitest run --config config/testing/vitest.config.ts src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.test.tsx src/tools/video-editor/components/SchemaForm/SchemaForm.test.tsx src/tools/video-editor/transitions/catalog.test.ts src/tools/video-editor/transitions/validation.test.ts src/tools/video-editor/lib/timeline-domain.transition.test.ts` — 8 files, 268 tests passed.
- `node scripts/quality/check-known-failures.mjs` — 3 authorized, 0 forbidden,
  maximum 0.
- Targeted ESLint on the changed test — passed.
- `git diff --check` — passed; final source diff is 12 deletions in the one
  listed test file.
