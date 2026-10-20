# App M2 ordinary clip-parameter ingress map

## Result

The next App writer should route only authored, top-level `clip.params` edits through Agent `clip.set-params` v1. The raw authored source is the command-session/Agent basis , not `TimelineData.config`, `resolvedConfig`, `ClipMeta`, `rows`, or any compiled/display representation. If the verified session basis is unavailable, refuse visibly and retain the input; there is no config-based capture fallback. `resolvedConfig` is display data with derived `assetEntry`; `ClipMeta` is an editor mirror; `rowsToConfig` recomputes timing and serializes a broad clip. None is a safe params-only command basis.

Current native authority is Agent scalar implementation at `ceb2ab67bf97d342c5af7392bee1f24cabc2ea2e`. The App parity capture work is the standalone `5e7`-lineage capture/report from the M2 params-parity worker; it is not wired into this branch's UI/session/provider yet. M2 remains branch-only and must wait for the M1 record before integration.

## Exact conversion recipe

1. At the first authoring boundary of a gesture, resolve one stable Agent-owned target (`parent/clip:<id>` or `occurrence:<id>/clip:<id>`). The App display id may be used to ask the session port for the target, but App must not invent an occurrence owner or infer a raw ref from compiled rows. Capture the immutable Agent basis, identity, schema/binding claims, and the original values/absence of every key that will be set or cleared.

2. Convert the UI event to exactly:

   ```ts
   {
     values: { [literalTopLevelKey]: finiteJsonValue },
     clear: string[],
   }
   ```

   Keys remain literal strings, including dots, brackets, and `::`; never split them into paths. `null` is a value. `clear` removes presence. `values` and `clear` must be disjoint, `clear` must be unique, and the envelope must contain at least one change. Do not coerce raw stored units, add defaults, or send an entire params object. Agent owns element-schema validation.

3. Preview by applying only those leaf changes to a local raw `clip.params` projection: set `values`, delete `clear`, and preserve every unmentioned/opaque sibling and every non-params clip field. The existing visual update may remain immediate, but it must not call `rowsToConfig`, `useTimelineOps.apply`, `useTimelineCommandsService.updateClip`, or `setClipParams` as a save. Those paths currently compile/commit a full snapshot; `setClipParams` is only an alias for `updateClip({patch:{params}})`.

4. Finish the same captured basis with the latest gesture values and submit the native command once for the gesture/group. Never recapture from the display after preview, blur, or ACK. A later ACK reports acceptance only; it must not replace the original guard/basis. If the original guarded leaf changed, fail the whole command; do not partially save the remaining keys.

5. Keep batching boundaries explicit:

   - Text/string/textarea: begin on focus or the first keyboard/pointer change before preview; preview each valid change; finish on blur, Enter, or the existing commit callback.
   - Number input: begin before the first `onChange`; preview valid values; finish on `onValueCommitted`, blur, or Enter. Do not let the display's intermediate value become a new capture basis.
   - Slider: begin on pointer-down or keyboard focus before the first value event; preview continuously; finish on pointer-up/blur/keyboard commit.
   - JSON params: invalid drafts stay local; begin before the first valid parsed value; Clear is an explicit `clear` capture, not a default-valued set. The next writer needs a blur/commit boundary around the current `onCommit` callback.
   - Select/toggle/button: capture immediately before the change and submit one command.
   - If one UI event changes multiple params (for example an Astrid form merge), capture that exact set together. Do not reconstruct it from a later render.

6. Flush through the command session after enqueueing; `flush()` must await durable acknowledgement. A successful local `submit` is not a persistence result. Preserve the existing legacy-clean gate and do not allow a params command to share a mixed partial snapshot save.

## Actual ingress points and field classification

`PropertiesPanelBody.tsx:533-554` is the current ingress: multi-select sends `BulkInspector` patches to `handleUpdateClips`/`handleUpdateClipsDeep`; single selection sends `ClipInspector` patches to `handleSelectedClipChange`. `useClipEditing.ts` then builds `metaUpdates` and `applyRowsEdit`; `useTimelineCommit.ts` materializes rows into a broad config. The params writer must split only the top-level `params` case before this legacy path.

Already expressible by native `clip.set-params`:

- `SequenceParamEditor`'s `clip.params` fields (`SequenceParamEditor.tsx:44-57, 103-165, 212-291`), including finite scalar, array, and object JSON values, literal top-level keys, and explicit optional JSON clear.
- `AstridElementParams`/`CodePathParamEditor` values in the pinned element's top-level `clip.params` (`AstridElementParams.tsx:26-61`). Its current render-time `{...params, ...nextParams}` merge must be replaced or wrapped so capture records the exact changed keys and absence; it has no clear operation today.

Not params-only and therefore not expressible by this operation:

- `entrance.params`, `exit.params`, `continuous.params`, and `transition.params` from `ParameterControls`/`SchemaForm`/`ClipEffectsTab`: these are nested effect/transition data, not `clip.params`. They need a separate Agent operation/path and must not be tunneled through `clip.set-params`.
- `at`, `hold`, `speed`, `from`, `to`, duration, and keyframe timing: use the timing/move/keyframe operation when available. Do not use params merely because a sequence schema has a parameter named `keyframes` or `sourceSegments`.
- `asset`, source/variant/media identity, `source_uuid`, `generation`, `pool_id`, and registry/media fields: use the media/source operation.
- `label`, volume, position/crop, opacity, text, `effects`, `elementRef`, `app`, transition metadata, and other clip-top-level fields: use their dedicated operation. `clip.update` remains a broad snapshot path, not a params fallback.

Multi-select/bulk params are not automatically one native operation: the native scalar target is singular. Either emit one exact command per stable target in one command batch, with a basis per target, or leave the bulk params gesture refused until Agent publishes a multi-target operation. Never send the bulk patch as one `clip.update`.

## Smallest implementation split

1. **Session/port adapter.** Add a `ClipParamsCapturePort` alongside the existing `ClipMoveCapturePort`/`TrackLabelCapturePort`, with `capture({clipId,current})`, `finish(basis,args)`, `submit({command, preview, transactionId?})`, and session `flush`. Capture resolves the canonical raw ref and stores the original basis; finish accepts only the captured basis; submit queues the exact command plus a params-only local preview. Reuse the parity capture's `ClipParamsArgs`/native envelope. Tests: literal keys, absent/null/clear, opaque sibling preservation, disjoint replay, changed guarded leaf rejection, capture-before-preview, no ACK recapture, batch grouping, async flush, and no snapshot save.

2. **UI ingress adapter.** Split `params` from `PropertiesPanel`/`ClipInspector` callbacks and route `SequenceParamEditor` and `AstridElementParams` through the port. Add gesture lifecycle hooks at focus/pointer/keyboard/commit boundaries, preserving current immediate positive previews. Tests should cover ordinary sequence scalar/JSON edits, Astrid schema values, explicit clear, literal key spelling, invalid JSON staying local, and the three original M1 `it.fails` remaining unchanged.

3. **Boundary audit (optional but recommended).** Guard or narrow `useTimelineCommandsService.setClipParams` and the generic `updateClip`/`TimelineOps.clip.update` call sites so a params-only caller cannot silently re-enter the snapshot writer. Add a regression assertion that params ingress emits the native command and zero legacy `clip.update`/save traffic; leave timing/media/top-level fields on their separate paths.

## Blockers / decisions

- The current branch has no params session port/provider wiring. The standalone parity capture must not be treated as integrated evidence.
- Stable occurrence/raw clip identity and element-schema admission remain Agent responsibilities. App must wait for that projection/basis rather than deriving either from `resolvedConfig`.
- No code, tests, or repository documentation were changed in this worker. M1 integration remains blocked by the settled orchestration gate.

## Verification

No tests were run: this task produced a source-trace/handoff only and explicitly prohibited tsc, full/browser suites, installs, and network access. The next implementation workers should run their targeted Vitest lanes with one worker/thread and request central service suites only after their final edits.
