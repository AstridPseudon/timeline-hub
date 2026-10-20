# App M2 prompt producer and current shot-name cut join

Status: **prepared; no source hunk applied**. The committed actual gate reached
the real product assertion and failed because the canonical embedded shot dialog
has no `#batchVideoPrompt` control. This is a product-surface omission, not a
selector/setup failure. The source tree is unchanged.

## Resolved source

The inspected App tree is commit `f5fa987f6298bf3d1cb02ecf4e812b84e4ce4ef8`
with tree `e30a482be493831f318a19aa3c911e68e5eb21b2`. It already contains the
prompt producer (`baffad17c`) on top of the current name cut (`0d8cb6a46`, with
the later native-join/type-narrowing ancestry `9d9eb4b18` and `3aef67c65`).

The resolved prompt path is:

1. `LocalTimelineShotBrowser` passes the mounted `shotSetPort` into
   `ShotEditorView`.
2. `ShotEditorView` mounts `VideoTravelSettingsProvider` with canonical
   persistence and `onPromptIntent={handlePromptIntent}`.
3. The existing prompt handler calls `captureShotPromptEdit` once at user
   intent, using the current occurrence and raw prompt (or `''` when absent).
4. `handleBatchVideoPromptChange` updates only the local settings projection;
   its save path recognizes the captured prompt and calls
   `submitShotPromptEdit`.
5. `shotSetGesture.ts` accepts only the native `shot.set` shape:
   `occurrence:<id>/shot`, `values.settings.prompt`, and `clear: []`, then
   submits the frozen command through the mounted port.

The current name path remains joined and must not be rewritten while repairing
prompt reachability. `captureShotNameEdit`/`submitShotNameEdit` uses the same
occurrence-owned port and exact `values.name`/`clear: []` shape. The embedded
canonical name fallback was removed; missing mounted name authority refuses with
`Mounted shot.set name authority is unavailable; draft kept.` The ordinary
unplaced/standalone path still uses the existing project name mutation.

## Why the actual selector is inapplicable

`ShotEditorView` sets `canonicalOnly` whenever both canonical composition and
occurrence are present. `ShotEditorLayout` always renders the header, but its
`!canonicalOnly` branch contains `TimelineSection`, `GenerationSection`, and
`ModalsSection`. `#batchVideoPrompt` is rendered by `BatchSettingsForm`, below
`GenerationSection`, so the canonical `Edit f2-shot` dialog correctly has no
such control on this tree. There is no truthful existing prompt selector to
substitute, and no test-only injection or browser rerun is warranted.

## Inherited semantic guards

- Prompt writes are occurrence-owned `shot.set` commands; they do not publish a
  whole canonical composition or post the legacy composition-revisions route.
- A prompt edit must be the only changed projected field. If normalization
  exposes another change, the save refuses and keeps the settings draft.
- A raw non-object/array settings root cannot be replaced by the form; the save
  refuses and keeps the draft.
- For represented object settings, changed nested authored values that are not
  represented by the form refuse rather than overwrite hidden data. Unchanged
  raw keys and opaque siblings are merged/preserved.
- An absent or `null` raw settings root can receive an explicit empty prompt;
  the command writes `settings: { prompt: '' }`, distinct from absence.
- Name refusal retains the exact untrimmed draft and leaves editing open; the
  accepted native completion closes the editor. These guards are inherited from
  the current name cut and its converted tests.
- Prompt acceptance, inverse/undo, lost-ack restart retry, relevant 409 draft
  retention, and zero legacy writes remain assertions of the untouched real
  journey. They are not qualified because the first real input control is
  absent.

## Focused source evidence

Command:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
  --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/shotSetCapture.test.ts \
  src/tools/video-editor/commands/shotSetSession.test.ts \
  src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.test.ts \
  src/tools/travel-between-images/pages/ShotEditorView.test.tsx \
  src/tools/travel-between-images/providers/VideoTravelSettingsProvider.test.tsx
```

Result: **5 files passed, 44 tests passed**.

The first attempted invocation added `--configLoader=runner` and stopped before
collection because this repository config uses `__dirname`; it was retried with
the repository invocation above. No browser, full suite, TypeScript, install,
private13 overlay, or shared-cache write was used.

## Next step

The App owner must expose the intended prompt editing control in the canonical
shot UI (or explicitly select an existing truthful route) while retaining this
native producer and the current name conversions. Then rerun the same strict
one-case actual gate against a fresh App SHA/tree. This note does not authorize
changing the active journey selector or weakening its assertions.
